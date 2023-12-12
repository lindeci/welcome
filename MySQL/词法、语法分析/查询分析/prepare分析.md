- [调用堆栈](#调用堆栈)
- [optimize 调用堆栈](#optimize-调用堆栈)
- [execute 调用堆栈](#execute-调用堆栈)

# 调用堆栈
```cpp
Query_block::prepare(Query_block * const this, THD * thd, mem_root_deque<Item*> * insert_field_list) (\data\mysql-server-8.2.0\sql\sql_resolver.cc:178)
Sql_cmd_select::prepare_inner(Sql_cmd_select * const this, THD * thd) (\data\mysql-server-8.2.0\sql\sql_select.cc:650)
Sql_cmd_dml::prepare(Sql_cmd_dml * const this, THD * thd) (\data\mysql-server-8.2.0\sql\sql_select.cc:564)
Sql_cmd_dml::execute(Sql_cmd_dml * const this, THD * thd) (\data\mysql-server-8.2.0\sql\sql_select.cc:718)
mysql_execute_command(THD * thd, bool first_level) (\data\mysql-server-8.2.0\sql\sql_parse.cc:4869)
dispatch_sql_command(THD * thd, Parser_state * parser_state) (\data\mysql-server-8.2.0\sql\sql_parse.cc:5524)
dispatch_command(THD * thd, const COM_DATA * com_data, enum_server_command command) (\data\mysql-server-8.2.0\sql\sql_parse.cc:2137)
do_command(THD * thd) (\data\mysql-server-8.2.0\sql\sql_parse.cc:1466)
handle_connection(void * arg) (\data\mysql-server-8.2.0\sql\conn_handler\connection_handler_per_thread.cc:303)
pfs_spawn_thread(void * arg) (\data\mysql-server-8.2.0\storage\perfschema\pfs.cc:3049)
libc.so.6!start_thread(void * arg) (pthread_create.c:442)
libc.so.6!clone() (clone.S:100)
```
# optimize 调用堆栈
```cpp
JOIN::optimize(JOIN * const this, bool finalize_access_paths) (\data\mysql-server-8.2.0\sql\sql_optimizer.cc:1110)
Query_block::optimize(Query_block * const this, THD * thd, bool finalize_access_paths) (\data\mysql-server-8.2.0\sql\sql_select.cc:2043)
Query_expression::optimize(Query_expression * const this, THD * thd, TABLE * materialize_destination, bool create_iterators, bool finalize_access_paths) (\data\mysql-server-8.2.0\sql\sql_union.cc:1017)
Sql_cmd_dml::execute_inner(Sql_cmd_dml * const this, THD * thd) (\data\mysql-server-8.2.0\sql\sql_select.cc:1026)
Sql_cmd_dml::execute(Sql_cmd_dml * const this, THD * thd) (\data\mysql-server-8.2.0\sql\sql_select.cc:792)
mysql_execute_command(THD * thd, bool first_level) (\data\mysql-server-8.2.0\sql\sql_parse.cc:4869)
dispatch_sql_command(THD * thd, Parser_state * parser_state) (\data\mysql-server-8.2.0\sql\sql_parse.cc:5524)
dispatch_command(THD * thd, const COM_DATA * com_data, enum_server_command command) (\data\mysql-server-8.2.0\sql\sql_parse.cc:2137)
do_command(THD * thd) (\data\mysql-server-8.2.0\sql\sql_parse.cc:1466)
handle_connection(void * arg) (\data\mysql-server-8.2.0\sql\conn_handler\connection_handler_per_thread.cc:303)
pfs_spawn_thread(void * arg) (\data\mysql-server-8.2.0\storage\perfschema\pfs.cc:3049)
libc.so.6!start_thread(void * arg) (pthread_create.c:442)
libc.so.6!clone() (clone.S:100)
```

# execute 调用堆栈
```cpp
Query_expression::ExecuteIteratorQuery(Query_expression * const this, THD * thd) (\data\mysql-server-8.2.0\sql\sql_union.cc:1676)
Query_expression::execute(Query_expression * const this, THD * thd) (\data\mysql-server-8.2.0\sql\sql_union.cc:1840)
Sql_cmd_dml::execute_inner(Sql_cmd_dml * const this, THD * thd) (\data\mysql-server-8.2.0\sql\sql_select.cc:1041)
Sql_cmd_dml::execute(Sql_cmd_dml * const this, THD * thd) (\data\mysql-server-8.2.0\sql\sql_select.cc:792)
mysql_execute_command(THD * thd, bool first_level) (\data\mysql-server-8.2.0\sql\sql_parse.cc:4869)
dispatch_sql_command(THD * thd, Parser_state * parser_state) (\data\mysql-server-8.2.0\sql\sql_parse.cc:5524)
dispatch_command(THD * thd, const COM_DATA * com_data, enum_server_command command) (\data\mysql-server-8.2.0\sql\sql_parse.cc:2137)
do_command(THD * thd) (\data\mysql-server-8.2.0\sql\sql_parse.cc:1466)
handle_connection(void * arg) (\data\mysql-server-8.2.0\sql\conn_handler\connection_handler_per_thread.cc:303)
pfs_spawn_thread(void * arg) (\data\mysql-server-8.2.0\storage\perfschema\pfs.cc:3049)
libc.so.6!start_thread(void * arg) (pthread_create.c:442)
libc.so.6!clone() (clone.S:100)
```


```sql
CREATE TABLE `orders` (
  `O_ORDERKEY` int NOT NULL,
  `O_CUSTKEY` int NOT NULL,
  `O_ORDERSTATUS` char(1) NOT NULL,
  `O_TOTALPRICE` decimal(15,2) NOT NULL,
  `O_ORDERDATE` date NOT NULL,
  `O_ORDERPRIORITY` char(15) NOT NULL,
  `O_CLERK` char(15) NOT NULL,
  `O_SHIPPRIORITY` int NOT NULL,
  `O_COMMENT` varchar(79) NOT NULL,
  PRIMARY KEY (`O_ORDERKEY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `lineitem` (
  `L_ORDERKEY` int NOT NULL,
  `L_PARTKEY` int NOT NULL,
  `L_SUPPKEY` int NOT NULL,
  `L_LINENUMBER` int NOT NULL,
  `L_QUANTITY` decimal(15,2) NOT NULL,
  `L_EXTENDEDPRICE` decimal(15,2) NOT NULL,
  `L_DISCOUNT` decimal(15,2) NOT NULL,
  `L_TAX` decimal(15,2) NOT NULL,
  `L_RETURNFLAG` char(1) NOT NULL,
  `L_LINESTATUS` char(1) NOT NULL,
  `L_SHIPDATE` date NOT NULL,
  `L_COMMITDATE` date NOT NULL,
  `L_RECEIPTDATE` date NOT NULL,
  `L_SHIPINSTRUCT` char(25) NOT NULL,
  `L_SHIPMODE` char(10) NOT NULL,
  `L_COMMENT` varchar(44) NOT NULL,
  PRIMARY KEY (`L_ORDERKEY`,`L_LINENUMBER`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

select o_orderpriority, count(*) as order_count 
from orders 
where 
	o_orderdate >=  '1996-08-01' and o_orderdate < date_add( '1996-08-01', interval '3' month) and 
	exists ( select *  from  lineitem  where  l_orderkey = o_orderkey and l_commitdate < l_receiptdate ) 
group by o_orderpriority order by o_orderpriority;
```