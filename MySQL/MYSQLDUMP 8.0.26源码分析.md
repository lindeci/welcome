# 版本
mysql 8.0.26  
mysqldump路径：mysql-8.0.27\client\mysqldump.cc
# 阅读源码动力
生产环境TDSQL大规模使用二级分区，且按天分区，产生大量表文件，mysqldump导出表结构时一直卡住，show processlist时，发现DB一直在查询INFORMATION_SCHEMA.FILES，最后导致query timeout。于是决定通过源码定位问题。
# mysqldump query timeout原因
```sh
mysqldump --default-character-set=utf8mb4 --single-transaction --extended-insert=1  --no-data --complete-insert --skip-add-locks --skip-comments --skip-disable-keys --add-drop-database -B ldc -h10.10.10.1 -P3306 -uldc -pldc > struct.sql
```
上面的脚本默认会设置--all-tablespaces，然后DB一直在执行下面慢SQL(视图不会走索引)，导致无法正常备份出表结构。
```sql
SELECT
    LOGFILE_GROUP_NAME, FILE_NAME, TOTAL_EXTENTS, INITIAL_SIZE, ENGINE, EXTRA 
FROM INFORMATION_SCHEMA.FILES 
WHERE 
    FILE_TYPE = 'UNDO LOG' AND FILE_NAME IS NOT NULL AND LOGFILE_GROUP_NAME IS NOT NULL 
    AND LOGFILE_GROUP_NAME IN (SELECT 
                                    DISTINCT LOGFILE_GROUP_NAME 
                                FROM INFORMATION_SCHEMA.FILES 
                                WHERE 
                                    FILE_TYPE = 'DATAFILE' 
                                    AND TABLESPACE_NAME IN (SELECT 
                                                                DISTINCT TABLESPACE_NAME 
                                                            FROM INFORMATION_SCHEMA.PARTITIONS 
                                                            WHERE 
                                                                TABLE_SCHEMA='test' AND TABLE_NAME IN ('l')
                                                            )
                                ) 
GROUP BY LOGFILE_GROUP_NAME, FILE_NAME, ENGINE, TOTAL_EXTENTS, INITIAL_SIZE 
ORDER BY LOGFILE_GROUP_NAME
```
```sql
SELECT 
    DISTINCT TABLESPACE_NAME, FILE_NAME, LOGFILE_GROUP_NAME, EXTENT_SIZE, INITIAL_SIZE, ENGINE 
FROM INFORMATION_SCHEMA.FILES 
WHERE 
    FILE_TYPE = 'DATAFILE' 
    AND TABLESPACE_NAME IN (SELECT 
                                DISTINCT TABLESPACE_NAME 
                            FROM INFORMATION_SCHEMA.PARTITIONS 
                            WHERE 
                                TABLE_SCHEMA='test' AND TABLE_NAME IN ('l')
                            )
ORDER BY TABLESPACE_NAME, LOGFILE_GROUP_NAME
```
关于all-tablespaces的官网解释，发现该参数只影响到NDB引擎。
```
--all-tablespaces, -Y

Adds to a table dump all SQL statements needed to create any tablespaces used by an NDB table. This information is not otherwise included in the output from mysqldump. This option is currently relevant only to NDB Cluster tables.
```
# 源码分析
## main函数
会调用dump_selected_tables函数
```cpp
int main(int argc, char **argv) {
  ……
 
  exit_code = get_options(&argc, &argv);   //读取配置文件、命令行参数，设置全局控制参数，过滤日志表mysql.apply_status、mysql.schema、mysql.general_log、mysql.slow_log
  ……
 
  if (connect_to_db(current_host, current_user)) {//连接数据库
    free_resources();
    exit(EX_MYSQLERR);
  }
 
  stats_tables_included = is_innodb_stats_tables_included(argc, argv);//判断是否导出mysql.innodb_table_stats、mysql.innodb_index_stats这两张表
 
  if (!path) write_header(md_result_file, *argv); //打印头文件
 
  if (opt_slave_data && do_stop_slave_sql(mysql)) goto err;//如果设置--dump-replica并且SQL_THREAD不为NO，则执行STOP SLAVE SQL_THREAD
 
  if ((opt_lock_all_tables || opt_master_data ||   //如果--lock_all_tables或者--source-data或者--master_data或者(--single_transaction and --flush_logs)
       (opt_single_transaction && flush_logs)) &&
      do_flush_tables_read_lock(mysql))           //执行FLUSH TABLES; FLUSH TABLES WITH READ LOCK; 之间如果有DML，则第二个FLUSH会被STALL
    goto err;
 
  /*
    Flush logs before starting transaction since
    this causes implicit commit starting mysql-5.5.
  */
  if (opt_lock_all_tables || opt_master_data ||
      (opt_single_transaction && flush_logs) || opt_delete_master_logs) {   //如果5.5+版本设置--delete-master-logs则需要Flush logs,因为会隐式执行COMMIT
    ……
  }
 
  if (opt_delete_master_logs) {
    if (get_bin_log_name(mysql, bin_log_name, sizeof(bin_log_name))) goto err; //通过SHOW MASTER STATUS或者当前bin_log_name
  }
 
  if (opt_single_transaction && start_transaction(mysql)) goto err; //如果设置--single_transaction，则执行SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ; 
                                                                    //START TRANSACTION /*!40100 WITH CONSISTENT SNAPSHOT */;
 
  /* Add 'STOP SLAVE to beginning of dump */
  if (opt_slave_apply && add_stop_slave()) goto err;  //如果设置--apply-replica-statements则“打印”STOP SLAVE
 
  /* Process opt_set_gtid_purged and add SET @@GLOBAL.GTID_PURGED if required.
   */
  if (process_set_gtid_purged(mysql)) goto err; //根据set-gtid-purged的设置，打印SET @@SESSION.SQL_LOG_BIN= 0;SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ GTID列表
 
  if (opt_master_data && do_show_master_status(mysql)) goto err;//打印CHANGE MASTER TO MASTER_LOG_FILE='%s', MASTER_LOG_POS=%s;
  if (opt_slave_data && do_show_slave_status(mysql)) goto err;//5837行STOP SLAVE SQL_THREAD，根据SHOW SLAVE STATUS的结果，打印CHANGE MASTER TO MASTER_LOG_FILE='%s', MASTER_LOG_POS=%s;
  if (opt_single_transaction &&                                //UNLOCK TABLES
      do_unlock_tables(mysql)) /* unlock but no commit! */
    goto err;
 
  if (opt_alltspcs) dump_all_tablespaces();  //如果设置--all-tablespaces，则dump all logfile groups and tablespaces，只对NDB引擎有效
 
  if (opt_alldbs) {
    if (!opt_alltspcs && !opt_notspcs) dump_all_tablespaces();
    dump_all_databases();        //如果设置all-databases,则SHOW DATABASES,导出表、视图，过滤information_schema、performance_schema、sys
  } else {
    ……
    }
 
    if (argc > 1 && !opt_databases) {         //没有--databases，只导出指定表
      /* Only one database and selected table(s) */
      if (!opt_alltspcs && !opt_notspcs)
        dump_tablespaces_for_tables(*argv, (argv + 1), (argc - 1));
      dump_selected_tables(*argv, (argv + 1), (argc - 1));  //遍历导出表
    } else {
      /* One or more databases, all tables */
      if (!opt_alltspcs && !opt_notspcs) dump_tablespaces_for_databases(argv);
      dump_databases(argv);
    }
  }
 
  /* if --dump-replica , start the slave sql thread */
  if (opt_slave_data && do_start_slave_sql(mysql)) goto err; //如果设置--dump-replica则执行START SLAVE
 
  /*
    if --set-gtid-purged, restore binlog at the end of the session
    if required.
  */
  set_session_binlog(true); //打印SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
 
  /* add 'START SLAVE' to end of dump */
  if (opt_slave_apply && add_slave_statements()) goto err; //打印START SLAVE;
 
  if (md_result_file) md_result_fd = my_fileno(md_result_file);
 
  /*
     Ensure dumped data flushed.
     First we will flush the file stream data to kernel buffers with fflush().
     Second we will flush the kernel buffers data to physical disk file with
     my_sync(), this will make sure the data successfully dumped to disk file.
     fsync() fails with EINVAL if stdout is not redirected to any file, hence
     MY_IGNORE_BADFD is passed to ignore that error.
  */
  if (md_result_file &&
      (fflush(md_result_file) || my_sync(md_result_fd, MYF(MY_IGNORE_BADFD)))) {//调用fflush刷到内核buffers，然后调用my_sync刷到磁盘
    if (!first_error) first_error = EX_MYSQLERR;
    goto err;
  }
  /* everything successful, purge the old logs files */
  if (opt_delete_master_logs && purge_bin_logs_to(mysql, bin_log_name)) //如果设置--delete-master-logs则执行PURGE BINARY LOGS TO xx
    goto err;
  ……
} /* main */
```
## dump_selected_tables函数
里面调用dump_table函数
```cpp
static int dump_selected_tables(char *db, char **table_names, int tables) {
  ……
  //设置SAVEPOINT sp
  if (opt_single_transaction && mysql_get_server_version(mysql) >= 50500) {
    verbose_msg("-- Setting savepoint...\n");
    if (mysql_query_with_error_report(mysql, nullptr, "SAVEPOINT sp")) return 1;
  }
 
  /* Dump each selected table */
  for (pos = dump_tables; pos < end; pos++) {
    DBUG_PRINT("info", ("Dumping table %s", *pos));
    dump_table(*pos, db);
    ……
    if (opt_single_transaction && mysql_get_server_version(mysql) >= 50500) {
      verbose_msg("-- Rolling back to savepoint sp...\n");
      if (mysql_query_with_error_report(mysql, nullptr,
                                        "ROLLBACK TO SAVEPOINT sp"))
        maybe_exit(EX_MYSQLERR);
    }
  }
  //RELEASE SAVEPOINT sp
  if (opt_single_transaction && mysql_get_server_version(mysql) >= 50500) {
    verbose_msg("-- Releasing savepoint...\n");
    if (mysql_query_with_error_report(mysql, nullptr, "RELEASE SAVEPOINT sp"))
      return 1;
  }
 
  /* Dump each selected view */
  //备份视图
  ……
  /* obtain dump of routines (procs/functions) */
  //备份存储过程
  ……
  ……
} /* dump_selected_tables */
```
## dump_table函数分析
从代码中可以了解到，如果导出文件中SQL长度超过--net-buffer-length则使用COMMMIT；分割。这个对我们导入数据时，规避大事务很有帮助。

如果字段是blob类型，则申请length * 2 + 2的BUFFER。其中length为结果集中字段数值具体长度。因为
- In HEX mode we need exactly 2 bytes per character plus 2 bytes for '0x' prefix.
- In non-HEX mode we need up to 2 bytes per character
```cpp
static void dump_table(char *table, char *db) {
  ……
  num_fields = get_table_structure(table, db, table_type, &ignore_flag,//获取表结构 
                                   real_columns, &column_list);
 
  /*
    The "table" could be a view.  If so, we don't do anything here.
  */
  if (strcmp(table_type, "VIEW") == 0) return;//遇到视图则返回
 
  /*
    We don't dump data for replication metadata tables.
  */
  if (replication_metadata_tables(db, table)) return;//遇到replication metadata tables则返回
 
  /* Check --no-data flag */
  ……
  /* Check that there are any fields in the table */
  if (num_fields == 0) {                         //遇到没字段的表则返回
    verbose_msg("-- Skipping dump data for table '%s', it has no fields\n",
                table);
    return;
  }
 
  ……
 
  if (opt_order_by_primary) order_by = primary_key_fields(result_table);
  if (path) {                                     //如果设置-T，则使用SELECT INTO OUTFILE导出，否则使用SELECT * FROM导出
   ……
    //通过SELECT /*!40001 SQL_NO_CACHE */……/*!50138 CHARACTER SET xx*/ FROM WHERE ORDER BY查询出记录集
    dynstr_append_checked(&query_string, "SELECT /*!40001 SQL_NO_CACHE */ ");
    if (column_list.empty())
      dynstr_append_checked(&query_string, "*");
    else
      dynstr_append_checked(&query_string, column_list.c_str());
    dynstr_append_checked(&query_string, " INTO OUTFILE '");
    dynstr_append_checked(&query_string, filename);
    dynstr_append_checked(&query_string, "'");
 
    dynstr_append_checked(&query_string, " /*!50138 CHARACTER SET ");
    dynstr_append_checked(&query_string,
                          default_charset == mysql_universal_client_charset
                              ? my_charset_bin.name
                              : /* backward compatibility */
                              default_charset);
    dynstr_append_checked(&query_string, " */");
 
    if (fields_terminated || enclosed || opt_enclosed || escaped)
      dynstr_append_checked(&query_string, " FIELDS");
 
    add_load_option(&query_string, " TERMINATED BY ", fields_terminated);
    add_load_option(&query_string, " ENCLOSED BY ", enclosed);
    add_load_option(&query_string, " OPTIONALLY ENCLOSED BY ", opt_enclosed);
    add_load_option(&query_string, " ESCAPED BY ", escaped);
    add_load_option(&query_string, " LINES TERMINATED BY ", lines_terminated);
 
    dynstr_append_checked(&query_string, " FROM ");
    dynstr_append_checked(&query_string, result_table);
 
    if (where) {
      dynstr_append_checked(&query_string, " WHERE ");
      dynstr_append_checked(&query_string, where);
    }
 
    if (order_by) {
      dynstr_append_checked(&query_string, " ORDER BY ");
      ……
  } else {
    ……
    }
    if (quick)                           //如果设置--quick，则使用mysql_use_result(mysql)，否则使用mysql_store_result(mysql)
      res = mysql_use_result(mysql);
    else
      res = mysql_store_result(mysql);
    ……
 
    verbose_msg("-- Retrieving rows...\n");
    //检索返回的结果集
    if (mysql_num_fields(res) != num_fields) {
      ……
    }
 
    if (opt_lock && !(innodb_stats_tables(db, table))) { //如果设置--add-locks则打印LOCK TABLES xxx WRITE;
      fprintf(md_result_file, "LOCK TABLES %s WRITE;\n", opt_quoted_table);
      check_io(md_result_file);
    }
    /* Moved disable keys to after lock per bug 15977 */
    if (opt_disable_keys) {                     //如果设置disable-keys则打印/*!40000 ALTER TABLE xxx DISABLE KEYS */;
      fprintf(md_result_file, "/*!40000 ALTER TABLE %s DISABLE KEYS */;\n",
              opt_quoted_table);
      check_io(md_result_file);
    }
 
    total_length = opt_net_buffer_length; /* Force row break */  //如果SQL长度超过--net-buffer-length则使用COMMMIT；分割
    ……
 
    while ((row = mysql_fetch_row(res))) {
        ……
        //blob字段特殊处理
        /*
           63 is my_charset_bin. If charsetnr is not 63,
           we have not a BLOB but a TEXT column.
        */
        is_blob =
            (field->charsetnr == 63 && (field->type == MYSQL_TYPE_BIT ||
                                        field->type == MYSQL_TYPE_STRING ||
                                        field->type == MYSQL_TYPE_VAR_STRING ||
                                        field->type == MYSQL_TYPE_VARCHAR ||
                                        field->type == MYSQL_TYPE_BLOB ||
                                        field->type == MYSQL_TYPE_LONG_BLOB ||
                                        field->type == MYSQL_TYPE_MEDIUM_BLOB ||
                                        field->type == MYSQL_TYPE_TINY_BLOB ||
                                        field->type == MYSQL_TYPE_GEOMETRY))
                ? 1
                : 0;
        ……
 
          if (row[i]) {
            if (length) {
              if (!(field->flags & NUM_FLAG)) { //如果是blob类型，则申请length * 2 + 2的BUFFER
                /*
                  "length * 2 + 2" is OK for HEX mode:
                  - In HEX mode we need exactly 2 bytes per character
                  plus 2 bytes for '0x' prefix.
                  - In non-HEX mode we need up to 2 bytes per character,
                  plus 2 bytes for leading and trailing '\'' characters
                  and reserve 1 byte for terminating '\0'.
                  In addition to this, for the blob type, we need to
                  reserve for the "_binary " string that gets added in
                  front of the string in the dump.
                */
                ……
      //支持xml格式
      if (opt_xml) {
        fputs("\t</row>\n", md_result_file);
        check_io(md_result_file);
      }
      //如果命令行参数设置extended_insert
      if (extended_insert) {
        ……
      } else if (!opt_xml) {
        fputs(");\n", md_result_file);
        check_io(md_result_file);
      }
    }
 
    ……
 
    /* Moved enable keys to before unlock per bug 15977 */
    //打印/*!40000 ALTER TABLE %s ENABLE KEYS */;
    if (opt_disable_keys) {
      fprintf(md_result_file, "/*!40000 ALTER TABLE %s ENABLE KEYS */;\n",
              opt_quoted_table);
      check_io(md_result_file);
    }
    //UNLOCK TABLES;
    if (opt_lock && !(innodb_stats_tables(db, table))) {
      fputs("UNLOCK TABLES;\n", md_result_file);
      check_io(md_result_file);
    }
    ……
} /* dump_table */
```