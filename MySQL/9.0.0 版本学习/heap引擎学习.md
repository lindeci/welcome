- [官方文档](#官方文档)
- [调用栈跟踪](#调用栈跟踪)

# 官方文档
https://dev.mysql.com/doc/refman/8.4/en/memory-storage-engine.html

# 调用栈跟踪
```sql
create table mt_vector(id int) ENGINE = MEMORY;
```

```cpp
heap_create(const char * name, HP_CREATE_INFO * create_info, HP_SHARE ** res, bool * created_new_share) (\data\ldc_docker\mysql-server_9.0.0\storage\heap\hp_create.cc:46)
ha_heap::create(ha_heap * const this, const char * name, TABLE * table_arg, HA_CREATE_INFO * create_info) (\data\ldc_docker\mysql-server_9.0.0\storage\heap\ha_heap.cc:648)
handler::ha_create(handler * const this, const char * name, TABLE * form, HA_CREATE_INFO * info, dd::Table * table_def) (\data\ldc_docker\mysql-server_9.0.0\sql\handler.cc:5123)
ha_create_table(THD * thd, const char * path, const char * db, const char * table_name, HA_CREATE_INFO * create_info, bool update_create_info, bool is_temp_table, dd::Table * table_def) (\data\ldc_docker\mysql-server_9.0.0\sql\handler.cc:5295)
rea_create_base_table(THD * thd, const char * path, const dd::Schema & sch_obj, const char * db, const char * table_name, HA_CREATE_INFO * create_info, List<Create_field> & create_fields, uint keys, KEY * key_info, Alter_info::enum_enable_or_disable keys_onoff, uint fk_keys, FOREIGN_KEY * fk_key_info, const Sql_check_constraint_spec_list * check_cons_spec, handler * file, bool no_ha_table, bool do_not_store_in_dd, partition_info * part_info, bool * binlog_to_trx_cache, std::unique_ptr<dd::Table, std::default_delete<dd::Table> > * table_def_ptr, handlerton ** post_ddl_ht) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_table.cc:1197)
create_table_impl(THD * thd, const dd::Schema & schema, const char * db, const char * table_name, const char * error_table_name, const char * path, HA_CREATE_INFO * create_info, Alter_info * alter_info, bool internal_tmp_table, uint select_field_count, bool find_parent_keys, bool no_ha_table, bool do_not_store_in_dd, bool * is_trans, KEY ** key_info, uint * key_count, Alter_info::enum_enable_or_disable keys_onoff, FOREIGN_KEY ** fk_key_info, uint * fk_key_count, FOREIGN_KEY * existing_fk_info, uint existing_fk_count, const dd::Table * existing_fk_table, uint fk_max_generated_name_number, std::unique_ptr<dd::Table, std::default_delete<dd::Table> > * table_def, handlerton ** post_ddl_ht) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_table.cc:9207)
mysql_create_table_no_lock(THD * thd, const char * db, const char * table_name, HA_CREATE_INFO * create_info, Alter_info * alter_info, uint select_field_count, bool find_parent_keys, bool * is_trans, handlerton ** post_ddl_ht) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_table.cc:9432)
mysql_create_table(THD * thd, Table_ref * create_table, HA_CREATE_INFO * create_info, Alter_info * alter_info) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_table.cc:10350)
Sql_cmd_create_table::execute(Sql_cmd_create_table * const this, THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_cmd_ddl_table.cc:456)
mysql_execute_command(THD * thd, bool first_level) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:3656)
dispatch_sql_command(THD * thd, Parser_state * parser_state, bool is_retry) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:5331)
dispatch_command(THD * thd, const COM_DATA * com_data, enum_server_command command) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:2122)
do_command(THD * thd) (\data\ldc_docker\mysql-server_9.0.0\sql\sql_parse.cc:1466)
handle_connection(void * arg) (\data\ldc_docker\mysql-server_9.0.0\sql\conn_handler\connection_handler_per_thread.cc:304)
pfs_spawn_thread(void * arg) (\data\ldc_docker\mysql-server_9.0.0\storage\perfschema\pfs.cc:3061)
libpthread.so.0!start_thread (Unknown Source:0)
libc.so.6!clone (Unknown Source:0)
```

存储引擎的接口定义在 `sql\handler.h` 

接口概览
```cpp
/**
  The handler class is the interface for dynamically loadable
  storage engines. Do not add ifdefs and take care when adding or
  changing virtual functions to avoid vtable confusion

  Functions in this class accept and return table columns data. Two data
  representation formats are used:
  1. TableRecordFormat - Used to pass [partial] table records to/from
     storage engine

  2. KeyTupleFormat - used to pass index search tuples (aka "keys") to
     storage engine. See opt_range.cc for description of this format.

  TableRecordFormat
  =================
  [Warning: this description is work in progress and may be incomplete]
  The table record is stored in a fixed-size buffer:

    record: null_bytes, column1_data, column2_data, ...

  The offsets of the parts of the buffer are also fixed: every column has
  an offset to its column{i}_data, and if it is nullable it also has its own
  bit in null_bytes.

  The record buffer only includes data about columns that are marked in the
  relevant column set (table->read_set and/or table->write_set, depending on
  the situation).
  <not-sure>It could be that it is required that null bits of non-present
  columns are set to 1</not-sure>

  VARIOUS EXCEPTIONS AND SPECIAL CASES

  If the table has no nullable columns, then null_bytes is still
  present, its length is one byte <not-sure> which must be set to 0xFF
  at all times. </not-sure>

  If the table has columns of type BIT, then certain bits from those columns
  may be stored in null_bytes as well. Grep around for Field_bit for
  details.

  For blob columns (see Field_blob), the record buffer stores length of the
  data, following by memory pointer to the blob data. The pointer is owned
  by the storage engine and is valid until the next operation.

  If a blob column has NULL value, then its length and blob data pointer
  must be set to 0.


  Overview of main modules of the handler API
  ===========================================
  The overview below was copied from the storage/partition/ha_partition.h when
  support for non-native partitioning was removed.

  -------------------------------------------------------------------------
  MODULE create/delete handler object
  -------------------------------------------------------------------------
  Object create/delete method. Normally called when a table object
  exists.

  -------------------------------------------------------------------------
  MODULE meta data changes
  -------------------------------------------------------------------------
  Meta data routines to CREATE, DROP, RENAME table are often used at
  ALTER TABLE (update_create_info used from ALTER TABLE and SHOW ..).

  Methods:
    delete_table()
    rename_table()
    create()
    update_create_info()

  -------------------------------------------------------------------------
  MODULE open/close object
  -------------------------------------------------------------------------
  Open and close handler object to ensure all underlying files and
  objects allocated and deallocated for query handling is handled
  properly.

  A handler object is opened as part of its initialisation and before
  being used for normal queries (not before meta-data changes always.
  If the object was opened it will also be closed before being deleted.

  Methods:
    open()
    close()

  -------------------------------------------------------------------------
  MODULE start/end statement
  -------------------------------------------------------------------------
  This module contains methods that are used to understand start/end of
  statements, transaction boundaries, and aid for proper concurrency
  control.

  Methods:
    store_lock()
    external_lock()
    start_stmt()
    lock_count()
    unlock_row()
    was_semi_consistent_read()
    try_semi_consistent_read()

  -------------------------------------------------------------------------
  MODULE change record
  -------------------------------------------------------------------------
  This part of the handler interface is used to change the records
  after INSERT, DELETE, UPDATE, REPLACE method calls but also other
  special meta-data operations as ALTER TABLE, LOAD DATA, TRUNCATE.

  These methods are used for insert (write_row), update (update_row)
  and delete (delete_row). All methods to change data always work on
  one row at a time. update_row and delete_row also contains the old
  row.
  delete_all_rows will delete all rows in the table in one call as a
  special optimization for DELETE from table;

  Bulk inserts are supported if all underlying handlers support it.
  start_bulk_insert and end_bulk_insert is called before and after a
  number of calls to write_row.

  Methods:
    write_row()
    update_row()
    delete_row()
    delete_all_rows()
    start_bulk_insert()
    end_bulk_insert()

  -------------------------------------------------------------------------
  MODULE full table scan
  -------------------------------------------------------------------------
  This module is used for the most basic access method for any table
  handler. This is to fetch all data through a full table scan. No
  indexes are needed to implement this part.
  It contains one method to start the scan (rnd_init) that can also be
  called multiple times (typical in a nested loop join). Then proceeding
  to the next record (rnd_next) and closing the scan (rnd_end).
  To remember a record for later access there is a method (position)
  and there is a method used to retrieve the record based on the stored
  position.
  The position can be a file position, a primary key, a ROWID dependent
  on the handler below.

  All functions that retrieve records and are callable through the
  handler interface must indicate whether a record is present after the call
  or not. Record found is indicated by returning 0 and setting table status
  to "has row". Record not found is indicated by returning a non-zero value
  and setting table status to "no row".
  @see TABLE::set_found_row() and TABLE::set_no_row().
  By enforcing these rules in the handler interface, storage handler functions
  need not set any status in struct TABLE. These notes also apply to module
  index scan, documented below.

  Methods:

    rnd_init()
    rnd_end()
    rnd_next()
    rnd_pos()
    rnd_pos_by_record()
    position()

  -------------------------------------------------------------------------
  MODULE index scan
  -------------------------------------------------------------------------
  This part of the handler interface is used to perform access through
  indexes. The interface is defined as a scan interface but the handler
  can also use key lookup if the index is a unique index or a primary
  key index.
  Index scans are mostly useful for SELECT queries but are an important
  part also of UPDATE, DELETE, REPLACE and CREATE TABLE table AS SELECT
  and so forth.
  Naturally an index is needed for an index scan and indexes can either
  be ordered, hash based. Some ordered indexes can return data in order
  but not necessarily all of them.
  There are many flags that define the behavior of indexes in the
  various handlers. These methods are found in the optimizer module.

  index_read is called to start a scan of an index. The find_flag defines
  the semantics of the scan. These flags are defined in
  include/my_base.h
  index_read_idx is the same but also initializes index before calling doing
  the same thing as index_read. Thus it is similar to index_init followed
  by index_read. This is also how we implement it.

  index_read/index_read_idx does also return the first row. Thus for
  key lookups, the index_read will be the only call to the handler in
  the index scan.

  index_init initializes an index before using it and index_end does
  any end processing needed.

  Methods:
    index_read_map()
    index_init()
    index_end()
    index_read_idx_map()
    index_next()
    index_prev()
    index_first()
    index_last()
    index_next_same()
    index_read_last_map()
    read_range_first()
    read_range_next()

  -------------------------------------------------------------------------
  MODULE information calls
  -------------------------------------------------------------------------
  This calls are used to inform the handler of specifics of the ongoing
  scans and other actions. Most of these are used for optimisation
  purposes.

  Methods:
    info()
    get_dynamic_partition_info
    extra()
    extra_opt()
    reset()

  -------------------------------------------------------------------------
  MODULE optimizer support
  -------------------------------------------------------------------------
  NOTE:
  One important part of the public handler interface that is not depicted in
  the methods is the attribute records which is defined in the base class.
  This is looked upon directly and is set by calling info(HA_STATUS_INFO) ?

  Methods:
    min_rows_for_estimate()
    get_biggest_used_partition()
    scan_time()
    read_time()
    records_in_range()
    estimate_rows_upper_bound()
    records()

  -------------------------------------------------------------------------
  MODULE print messages
  -------------------------------------------------------------------------
  This module contains various methods that returns text messages for
  table types, index type and error messages.

  Methods:
    table_type()
    get_row_type()
    print_error()
    get_error_message()

  -------------------------------------------------------------------------
  MODULE handler characteristics
  -------------------------------------------------------------------------
  This module contains a number of methods defining limitations and
  characteristics of the handler (see also documentation regarding the
  individual flags).

  Methods:
    table_flags()
    index_flags()
    min_of_the_max_uint()
    max_supported_record_length()
    max_supported_keys()
    max_supported_key_parts()
    max_supported_key_length()
    max_supported_key_part_length()
    low_byte_first()
    extra_rec_buf_length()
    min_record_length(uint options)
    primary_key_is_clustered()
    ha_key_alg get_default_index_algorithm()
    is_index_algorithm_supported()

  -------------------------------------------------------------------------
  MODULE compare records
  -------------------------------------------------------------------------
  cmp_ref checks if two references are the same. For most handlers this is
  a simple memcmp of the reference. However some handlers use primary key
  as reference and this can be the same even if memcmp says they are
  different. This is due to character sets and end spaces and so forth.

  Methods:
    cmp_ref()

  -------------------------------------------------------------------------
  MODULE auto increment
  -------------------------------------------------------------------------
  This module is used to handle the support of auto increments.

  This variable in the handler is used as part of the handler interface
  It is maintained by the parent handler object and should not be
  touched by child handler objects (see handler.cc for its use).

  Methods:
    get_auto_increment()
    release_auto_increment()

  -------------------------------------------------------------------------
  MODULE initialize handler for HANDLER call
  -------------------------------------------------------------------------
  This method is a special InnoDB method called before a HANDLER query.

  Methods:
    init_table_handle_for_HANDLER()

  -------------------------------------------------------------------------
  MODULE fulltext index
  -------------------------------------------------------------------------
  Fulltext index support.

  Methods:
    ft_init_ext_with_hints()
    ft_init()
    ft_init_ext()
    ft_read()

  -------------------------------------------------------------------------
  MODULE in-place ALTER TABLE
  -------------------------------------------------------------------------
  Methods for in-place ALTER TABLE support (implemented by InnoDB and NDB).

  Methods:
    check_if_supported_inplace_alter()
    prepare_inplace_alter_table()
    inplace_alter_table()
    commit_inplace_alter_table()
    notify_table_changed()

  -------------------------------------------------------------------------
  MODULE tablespace support
  -------------------------------------------------------------------------
  Methods:
    discard_or_import_tablespace()

  -------------------------------------------------------------------------
  MODULE administrative DDL
  -------------------------------------------------------------------------
  Methods:
    optimize()
    analyze()
    check()
    repair()
    check_and_repair()
    auto_repair()
    is_crashed()
    check_for_upgrade()
    checksum()
    assign_to_keycache()

  -------------------------------------------------------------------------
  MODULE enable/disable indexes
  -------------------------------------------------------------------------
  Enable/Disable Indexes are only supported by HEAP and MyISAM.

  Methods:
    disable_indexes()
    enable_indexes()
    indexes_are_disabled()

  -------------------------------------------------------------------------
  MODULE append_create_info
  -------------------------------------------------------------------------
  Only used by MyISAM MERGE tables.

  Methods:
    append_create_info()

  -------------------------------------------------------------------------
  MODULE partitioning specific handler API
  -------------------------------------------------------------------------
  Methods:
    get_partition_handler()
*/
```