
# 官方下载地址
需要注册
[TPC-H](http://tpc.org/TPC_Documents_Current_Versions/download_programs/tools-download-request5.asp?bm_type=TPC-H&bm_vers=2.18.0&mode=CURRENT-ONLY)

http://tpc.org/TPC_Documents_Current_Versions/download_programs/tools-download-request5.asp?bm_type=TPC-H&bm_vers=2.18.0&mode=CURRENT-ONLY

# 参考

https://help.aliyun.com/zh/polardb/polardb-for-mysql/olap-performance-test?spm=a2c4g.11186623.0.i2

# 脚本
```sh
unzip dbgen.zip
cd dbgen
cp makefile.suite makefile
vim makefile # 修改CC、DATABASE、MACHINE、WORKLOAD参数的值

  ################
  ## CHANGE NAME OF ANSI COMPILER HERE
  ################
  CC= gcc
  # Current values for DATABASE are: INFORMIX, DB2, ORACLE,
  #                                  SQLSERVER, SYBASE, TDAT (Teradata)
  # Current values for MACHINE are:  ATT, DOS, HP, IBM, ICL, MVS,
  #                                  SGI, SUN, U2200, VMS, LINUX, WIN32
  # Current values for WORKLOAD are:  TPCH
  DATABASE= MYSQL
  MACHINE = LINUX
  WORKLOAD = TPCH
```

```sh
vim tpcd.h # 添加新的宏定义


#ifdef MYSQL
#define GEN_QUERY_PLAN "EXPLAIN PLAN"
#define START_TRAN "START TRANSACTION"
#define END_TRAN "COMMIT"
#define SET_OUTPUT ""
#define SET_ROWCOUNT "limit %d;\n"
#define SET_DBASE "use %s;\n"
#endif
```

```sh
make
./dbgen -s 100 # 参数-s的作用是指定生成测试数据的仓库数
```
```sql
vi load.ddl 
load data local INFILE 'customer.tbl' INTO TABLE customer FIELDS TERMINATED BY '|';
load data local INFILE 'region.tbl' INTO TABLE region FIELDS TERMINATED BY '|';
load data local INFILE 'nation.tbl' INTO TABLE nation FIELDS TERMINATED BY '|';
load data local INFILE 'supplier.tbl' INTO TABLE supplier FIELDS TERMINATED BY '|';
load data local INFILE 'part.tbl' INTO TABLE part FIELDS TERMINATED BY '|';
load data local INFILE 'partsupp.tbl' INTO TABLE partsupp FIELDS TERMINATED BY '|';
load data local INFILE 'orders.tbl' INTO TABLE orders FIELDS TERMINATED BY '|';
load data local INFILE 'lineitem.tbl' INTO TABLE lineitem FIELDS TERMINATED BY '|';
```
```sql
SET GLOBAL local_infile = true;


如果你想知道你当前的工作目录，你可以在 MySQL 命令行中使用 SELECT @@global.secure_file_priv;

create database tpch100g;
source ./dss.ddl

/data/mysql-server-8.2.0/build/runtime_output_directory/mysql -uroot -p'root' --socket=/data/mysql-server-8.2.0/data/mysql.sock.lock  --local-infile=1

source ./load.ddl

source ./dss.ri
```

创建索引
```sh
#!/usr/bin/bash
host=$1
port=$2
user=$3
password=$4
db=$5
sqls=("create index i_s_nationkey on supplier (s_nationkey);"
"create index i_ps_partkey on partsupp (ps_partkey);"
"create index i_ps_suppkey on partsupp (ps_suppkey);"
"create index i_c_nationkey on customer (c_nationkey);"
"create index i_o_custkey on orders (o_custkey);"
"create index i_o_orderdate on orders (o_orderdate);"
"create index i_l_orderkey on lineitem (l_orderkey);"
"create index i_l_partkey on lineitem (l_partkey);"
"create index i_l_suppkey on lineitem (l_suppkey);"
"create index i_l_partkey_suppkey on lineitem (l_partkey, l_suppkey);"
"create index i_l_shipdate on lineitem (l_shipdate);"
"create index i_l_commitdate on lineitem (l_commitdate);"
"create index i_l_receiptdate on lineitem (l_receiptdate);"
"create index i_n_regionkey on nation (n_regionkey);"
"analyze table supplier"
"analyze table part"
"analyze table partsupp"
"analyze table customer"
"analyze table orders"
"analyze table lineitem"
"analyze table nation"
"analyze table region")
for sql in "${sqls[@]}"
do
    mysql -h$host -P$port -u$user -p$password -D$db  -e "$sql"
done
```