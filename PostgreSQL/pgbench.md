
- [压测工具 pgbench](#压测工具-pgbench)
  - [部分参数中文含义：](#部分参数中文含义)
- [初始化测试数据](#初始化测试数据)
  - [查看表数据](#查看表数据)
  - [查看表结构](#查看表结构)
- [测试](#测试)
  - [1个session](#1个session)
  - [50个session](#50个session)
- [参考](#参考)
- [脚本封装pgbench添加重连机制](#脚本封装pgbench添加重连机制)

# 压测工具 pgbench
```sh
pgbench  --help
pgbench is a benchmarking tool for PostgreSQL.

Usage:
  pgbench [OPTION]... [DBNAME]

Initialization options:
  -i, --initialize         invokes initialization mode
  -I, --init-steps=[dtgGvpf]+ (default "dtgvp")
                           run selected initialization steps
  -F, --fillfactor=NUM     set fill factor
  -n, --no-vacuum          do not run VACUUM during initialization
  -q, --quiet              quiet logging (one message each 5 seconds)
  -s, --scale=NUM          scaling factor
  --foreign-keys           create foreign key constraints between tables
  --index-tablespace=TABLESPACE
                           create indexes in the specified tablespace
  --partition-method=(range|hash)
                           partition pgbench_accounts with this method (default: range)
  --partitions=NUM         partition pgbench_accounts into NUM parts (default: 0)
  --tablespace=TABLESPACE  create tables in the specified tablespace
  --unlogged-tables        create tables as unlogged tables

Options to select what to run:
  -b, --builtin=NAME[@W]   add builtin script NAME weighted at W (default: 1)
                           (use "-b list" to list available scripts)
  -f, --file=FILENAME[@W]  add script FILENAME weighted at W (default: 1)
  -N, --skip-some-updates  skip updates of pgbench_tellers and pgbench_branches
                           (same as "-b simple-update")
  -S, --select-only        perform SELECT-only transactions
                           (same as "-b select-only")

Benchmarking options:
  -c, --client=NUM         number of concurrent database clients (default: 1)
  -C, --connect            establish new connection for each transaction
  -D, --define=VARNAME=VALUE
                           define variable for use by custom script
  -j, --jobs=NUM           number of threads (default: 1)
  -l, --log                write transaction times to log file
  -L, --latency-limit=NUM  count transactions lasting more than NUM ms as late
  -M, --protocol=simple|extended|prepared
                           protocol for submitting queries (default: simple)
  -n, --no-vacuum          do not run VACUUM before tests
  -P, --progress=NUM       show thread progress report every NUM seconds
  -r, --report-per-command report latencies, failures, and retries per command
  -R, --rate=NUM           target rate in transactions per second
  -s, --scale=NUM          report this scale factor in output
  -t, --transactions=NUM   number of transactions each client runs (default: 10)
  -T, --time=NUM           duration of benchmark test in seconds
  -v, --vacuum-all         vacuum all four standard tables before tests
  --aggregate-interval=NUM aggregate data over NUM seconds
  --failures-detailed      report the failures grouped by basic types
  --log-prefix=PREFIX      prefix for transaction time log file
                           (default: "pgbench_log")
  --max-tries=NUM          max number of tries to run transaction (default: 1)
  --progress-timestamp     use Unix epoch timestamps for progress
  --random-seed=SEED       set random seed ("time", "rand", integer)
  --sampling-rate=NUM      fraction of transactions to log (e.g., 0.01 for 1%)
  --show-script=NAME       show builtin script code, then exit
  --verbose-errors         print messages of all errors

Common options:
  -d, --debug              print debugging output
  -h, --host=HOSTNAME      database server host or socket directory
  -p, --port=PORT          database server port number
  -U, --username=USERNAME  connect as specified database user
  -V, --version            output version information, then exit
  -?, --help               show this help, then exit
```

## 部分参数中文含义：
```sh
-c, --client=NUM
数据库客户端数量, 可以理解为数据库会话数量(postgres进程数), 默认为1

-C, --connect
每个事务创建一个连接,由于PG使用进程模型, 可以测试频繁Kill/Create进程的性能表现

-j, --jobs=NUM
pgbench的工作线程数

-T, --time=NUM
以秒为单位的压测时长

-v, --vacuum-all
每次测试前执行vacuum命令, 避免"垃圾"空间的影响

-M, --protocol=simple|extended|prepared
提交查询命令到服务器使用的协议, simple是默认选项, prepared是类似绑定

-r, --report-latencies
报告每条命令(SQL语句)的平均延时

-S, --select-only
只执行查询语句
```
# 初始化测试数据
```
# pgbench -i pgbench
./pgbench -i pgbench -U postgres
```
## 查看表数据
```
[postgres@localhost  ~]$ psql -d pgbench
psql (9.1.2)
Type "help" for help.

pgbench=# select count(1) from pgbench_accounts;
 count
--------
 100000
(1 row)

pgbench=# select count(1) from pgbench_branches;
 count
-------
     1
(1 row)

pgbench=# select count(1) from pgbench_history;
 count
-------
     0
(1 row)

pgbench=# select count(1) from pgbench_tellers;
 count
-------
    10
(1 row)
```

## 查看表结构
```sql
pgbench=# \d+ pgbench_accounts
                Table "public.pgbench_accounts"
  Column  |     Type      | Modifiers | Storage  | Description
----------+---------------+-----------+----------+-------------
 aid      | integer       | not null  | plain    |
 bid      | integer       |           | plain    |
 abalance | integer       |           | plain    |
 filler   | character(84) |           | extended |
Indexes:
    "pgbench_accounts_pkey" PRIMARY KEY, btree (aid)
Has OIDs: no
Options: fillfactor=100

pgbench=# \d+ pgbench_branches
                Table "public.pgbench_branches"
  Column  |     Type      | Modifiers | Storage  | Description
----------+---------------+-----------+----------+-------------
 bid      | integer       | not null  | plain    |
 bbalance | integer       |           | plain    |
 filler   | character(88) |           | extended |
Indexes:
    "pgbench_branches_pkey" PRIMARY KEY, btree (bid)
Has OIDs: no
Options: fillfactor=100

pgbench=# \d+ pgbench_history
                      Table "public.pgbench_history"
 Column |            Type             | Modifiers | Storage  | Description
--------+-----------------------------+-----------+----------+-------------
 tid    | integer                     |           | plain    |
 bid    | integer                     |           | plain    |
 aid    | integer                     |           | plain    |
 delta  | integer                     |           | plain    |
 mtime  | timestamp without time zone |           | plain    |
 filler | character(22)               |           | extended |
Has OIDs: no

pgbench=# \d+ pgbench_tellers
                Table "public.pgbench_tellers"
  Column  |     Type      | Modifiers | Storage  | Description
----------+---------------+-----------+----------+-------------
 tid      | integer       | not null  | plain    |
 bid      | integer       |           | plain    |
 tbalance | integer       |           | plain    |
 filler   | character(84) |           | extended |
Indexes:
    "pgbench_tellers_pkey" PRIMARY KEY, btree (tid)
Has OIDs: no
Options: fillfactor=100
```

说明：

1. 这里使用的是默认的参数值，-s参数时可指定测试数据的数据量，-f可以指定测试的脚本，这里用的是默认脚本。

2. 不要在生产的库上做，新建一个测试库（当生产上有同名的测试表时将被重置）。

# 测试
## 1个session
```sql

# [postgres@localhost  ~]$ nohup pgbench -c 1 -T 20 -r pgbench > file.out  2>&1
[postgres@localhost  ~]$ ./pgbench -c 1 -T 20 -r pgbench -U postgres
[postgres@localhost  ~]$ more file.out
nohup: ignoring input
starting vacuum...end.
transaction type: TPC-B (sort of)
scaling factor: 1
query mode: simple
number of clients: 1
number of threads: 1
duration: 20 s
number of transactions actually processed: 12496                                                                                     tps = 624.747958 (including connections establishing)                                                                                tps = 625.375564 (excluding connections establishing)
statement latencies in milliseconds:
        0.005299        \set nbranches 1 * :scale
        0.000619        \set ntellers 10 * :scale
        0.000492        \set naccounts 100000 * :scale
        0.000700        \setrandom aid 1 :naccounts
        0.000400        \setrandom bid 1 :nbranches
        0.000453        \setrandom tid 1 :ntellers
        0.000430        \setrandom delta -5000 5000
        0.050707        BEGIN;
        0.200909        UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
        0.098718        SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
        0.111621        UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;
        0.107297        UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;
        0.095156        INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
        0.919101        END;
```

## 50个session
```sql
[postgres@localhost  ~]$nohup pgbench -c 50 -T 20 -r pgbench > file.out  2>&1
[postgres@localhost  ~]$ more file.out
nohup: ignoring input
starting vacuum...end.
transaction type: TPC-B (sort of)
scaling factor: 1
query mode: simple
number of clients: 50
number of threads: 1
duration: 20 s
number of transactions actually processed: 7504                                                                                      tps = 370.510431 (including connections establishing)                                                                               tps = 377.964565 (excluding connections establishing)
statement latencies in milliseconds:
        0.004291        \set nbranches 1 * :scale
        0.000769        \set ntellers 10 * :scale
        0.000955        \set naccounts 100000 * :scale
        0.000865        \setrandom aid 1 :naccounts
        0.000513        \setrandom bid 1 :nbranches
        0.000580        \setrandom tid 1 :ntellers
        0.000522        \setrandom delta -5000 5000
        0.604671        BEGIN;
        1.480723        UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
        0.401148        SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
        104.713566      UPDATE pgbench_tellers SET tbalance = tbalance + :delta WHERE tid = :tid;
        21.562787       UPDATE pgbench_branches SET bbalance = bbalance + :delta WHERE bid = :bid;
        0.412209        INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (:tid, :bid, :aid, :delta, CURRENT_TIMESTAMP);
        2.243497        END;
```

# 参考
https://www.postgresql.org/docs/15/pgbench.html


# 脚本封装pgbench添加重连机制
```sh
cat pgbench_test.sh 
#!/bin/bash
export PGPASSWORD=123456
while true; do
    pgbench -c 10 -j 2 -T 30 -P 1 -U postgres -h xx.xx.xx.xx -p 5432 ldc_test
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 1
done
```
参数说明：

-c:并发客户端数

-j:每个客户端的线程数

-T:运行时间

-P:表示每N秒显示一次进度报告
