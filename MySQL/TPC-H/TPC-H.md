
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
# ./dbgen -s 1 产生 1G 的数据量
```
```sql
vi load.ddl 
LOAD DATA LOCAL INFILE 'customer.tbl' INTO TABLE CUSTOMER FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'region.tbl' INTO TABLE REGION FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'nation.tbl' INTO TABLE NATION FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'supplier.tbl' INTO TABLE SUPPLIER FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'part.tbl' INTO TABLE PART FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'partsupp.tbl' INTO TABLE PARTSUPP FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'orders.tbl' INTO TABLE ORDERS FIELDS TERMINATED BY '|';
LOAD DATA LOCAL INFILE 'lineitem.tbl' INTO TABLE LINEITEM FIELDS TERMINATED BY '|';
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

```sql
create index i_s_nationkey on supplier (s_nationkey);
create index i_ps_partkey on partsupp (ps_partkey);
create index i_ps_suppkey on partsupp (ps_suppkey);
create index i_c_nationkey on customer (c_nationkey);
create index i_o_custkey on orders (o_custkey);
create index i_o_orderdate on orders (o_orderdate);
create index i_l_orderkey on lineitem (l_orderkey);
create index i_l_partkey on lineitem (l_partkey);
create index i_l_suppkey on lineitem (l_suppkey);
create index i_l_partkey_suppkey on lineitem (l_partkey, l_suppkey);
create index i_l_shipdate on lineitem (l_shipdate);
create index i_l_commitdate on lineitem (l_commitdate);
create index i_l_receiptdate on lineitem (l_receiptdate);
create index i_n_regionkey on nation (n_regionkey);
analyze table supplier  ;
analyze table part      ;
analyze table partsupp  ;
analyze table customer  ;
analyze table orders    ;
analyze table lineitem  ;
analyze table nation    ;
analyze table region    ;
```

```sql
CREATE INDEX I_S_NATIONKEY ON SUPPLIER (S_NATIONKEY);
CREATE INDEX I_PS_PARTKEY ON PARTSUPP (PS_PARTKEY);
CREATE INDEX I_PS_SUPPKEY ON PARTSUPP (PS_SUPPKEY);
CREATE INDEX I_C_NATIONKEY ON CUSTOMER (C_NATIONKEY);
CREATE INDEX I_O_CUSTKEY ON ORDERS (O_CUSTKEY);
CREATE INDEX I_O_ORDERDATE ON ORDERS (O_ORDERDATE);
CREATE INDEX I_L_ORDERKEY ON LINEITEM (L_ORDERKEY);
CREATE INDEX I_L_PARTKEY ON LINEITEM (L_PARTKEY);
CREATE INDEX I_L_SUPPKEY ON LINEITEM (L_SUPPKEY);
CREATE INDEX I_L_PARTKEY_SUPPKEY ON LINEITEM (L_PARTKEY, L_SUPPKEY);
CREATE INDEX I_L_SHIPDATE ON LINEITEM (L_SHIPDATE);
CREATE INDEX I_L_COMMITDATE ON LINEITEM (L_COMMITDATE);
CREATE INDEX I_L_RECEIPTDATE ON LINEITEM (L_RECEIPTDATE);
CREATE INDEX I_N_REGIONKEY ON NATION (N_REGIONKEY);
ANALYZE TABLE SUPPLIER  ;
ANALYZE TABLE PART      ;
ANALYZE TABLE PARTSUPP  ;
ANALYZE TABLE CUSTOMER  ;
ANALYZE TABLE ORDERS    ;
ANALYZE TABLE LINEITEM  ;
ANALYZE TABLE NATION    ;
ANALYZE TABLE REGION    ;
```

```sql

USE TPCH;

ALTER TABLE TPCH.REGION DROP PRIMARY KEY;
ALTER TABLE TPCH.NATION DROP PRIMARY KEY;
ALTER TABLE TPCH.PART DROP PRIMARY KEY;
ALTER TABLE TPCH.SUPPLIER DROP PRIMARY KEY;
ALTER TABLE TPCH.PARTSUPP DROP PRIMARY KEY;
ALTER TABLE TPCH.ORDERS DROP PRIMARY KEY
ALTER TABLE TPCH.LINEITEM DROP PRIMARY KEY;
ALTER TABLE TPCH.CUSTOMER DROP PRIMARY KEY;

-- For table REGION˙
ALTER TABLE TPCH.REGION
ADD PRIMARY KEY (R_REGIONKEY);

-- For table NATION
ALTER TABLE TPCH.NATION
ADD PRIMARY KEY (N_NATIONKEY),
ADD CONSTRAINT NATION_FK1 FOREIGN KEY (N_REGIONKEY) REFERENCES TPCH.REGION(R_REGIONKEY);

-- For table PART
ALTER TABLE TPCH.PART
ADD PRIMARY KEY (P_PARTKEY);

-- For table SUPPLIER
ALTER TABLE TPCH.SUPPLIER
ADD PRIMARY KEY (S_SUPPKEY),
ADD CONSTRAINT SUPPLIER_FK1 FOREIGN KEY (S_NATIONKEY) REFERENCES TPCH.NATION(N_NATIONKEY);

-- For table PARTSUPP
ALTER TABLE TPCH.PARTSUPP
ADD PRIMARY KEY (PS_PARTKEY, PS_SUPPKEY),
ADD CONSTRAINT PARTSUPP_FK1 FOREIGN KEY (PS_SUPPKEY) REFERENCES TPCH.SUPPLIER(S_SUPPKEY),
ADD CONSTRAINT PARTSUPP_FK2 FOREIGN KEY (PS_PARTKEY) REFERENCES TPCH.PART(P_PARTKEY);

-- For table CUSTOMER
ALTER TABLE TPCH.CUSTOMER
ADD PRIMARY KEY (C_CUSTKEY),
ADD CONSTRAINT CUSTOMER_FK1 FOREIGN KEY (C_NATIONKEY) REFERENCES TPCH.NATION(N_NATIONKEY);

-- For table LINEITEM
ALTER TABLE TPCH.LINEITEM
ADD PRIMARY KEY (L_ORDERKEY, L_LINENUMBER),
ADD CONSTRAINT LINEITEM_FK1 FOREIGN KEY (L_ORDERKEY) REFERENCES TPCH.ORDERS(O_ORDERKEY),
ADD CONSTRAINT LINEITEM_FK2 FOREIGN KEY (L_PARTKEY, L_SUPPKEY) REFERENCES TPCH.PARTSUPP(PS_PARTKEY, PS_SUPPKEY);

-- For table ORDERS
ALTER TABLE TPCH.ORDERS
ADD PRIMARY KEY (O_ORDERKEY),
ADD CONSTRAINT ORDERS_FK1 FOREIGN KEY (O_CUSTKEY) REFERENCES TPCH.CUSTOMER(C_CUSTKEY);
```