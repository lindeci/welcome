- [官网](#官网)
- [yum包安装](#yum包安装)
- [常用操作](#常用操作)
  - [登录](#登录)
  - [命令行中执行SQL](#命令行中执行sql)
  - [显示列名](#显示列名)
  - [记录执行的SQL](#记录执行的sql)
  - [显示SQL的执行耗时](#显示sql的执行耗时)
  - [查看当前的数据库](#查看当前的数据库)
  - [查看当前的 Schema](#查看当前的-schema)
  - [查看当前的用户](#查看当前的用户)
  - [查看当前的用户所属的角色](#查看当前的用户所属的角色)
  - [查看有哪些数据库](#查看有哪些数据库)
  - [查看当前数据库有哪些 Schema](#查看当前数据库有哪些-schema)
  - [查看角色有哪些权限](#查看角色有哪些权限)
    - [角色级别的权限](#角色级别的权限)
    - [表级别权限](#表级别权限)
    - [SCHEMA 级别权限](#schema-级别权限)
    - [列级别权限](#列级别权限)
    - [database 级别权限](#database-级别权限)
  - [删除操作](#删除操作)
  - [切换数据库](#切换数据库)
  - [切换schema](#切换schema)
  - [查看从库列表](#查看从库列表)
  - [查看参数](#查看参数)
  - [查看表结构](#查看表结构)
  - [查看 SCHEMA 的所有表数据量](#查看-schema-的所有表数据量)
  - [查看 SCHEMA 的所有表的空间大小](#查看-schema-的所有表的空间大小)
  - [查看安装了哪些插件](#查看安装了哪些插件)
- [备份恢复](#备份恢复)
  - [库级别](#库级别)
  - [表级别](#表级别)
- [查看连接和 kill 连接](#查看连接和-kill-连接)
- [SEQUENCE](#sequence)
- [创建指定权限用户](#创建指定权限用户)
- [创建只读账号](#创建只读账号)
- [授权监控权限](#授权监控权限)
- [修改库的OWNER](#修改库的owner)
- [修改用户密码](#修改用户密码)
- [添加建表权限](#添加建表权限)
- [授权序列](#授权序列)
- [给 kong 的所有权限](#给-kong-的所有权限)
- [pgbench 压测](#pgbench-压测)
- [帮助命令](#帮助命令)
  - [General](#general)
  - [Help](#help)
  - [Query Buffer](#query-buffer)
  - [Input/Output](#inputoutput)
  - [Conditional](#conditional)
  - [Informational](#informational)
  - [Large Objects](#large-objects)
  - [Formatting](#formatting)
  - [Connection](#connection)
  - [Operating System](#operating-system)
  - [Variables](#variables)
- [启动关闭](#启动关闭)
- [物理备份恢复](#物理备份恢复)

# 官网

https://www.postgresql.org/

# yum包安装

环境：Centos 7.8

```sh
#postgresql-client 	libraries and client binaries
#postgresql-server 	core database server
#postgresql-contrib 	additional supplied modules
#postgresql-devel 	libraries and headers for C language development

# Download the repository RPM:
wget https://yum.postgresql.org/15/redhat/rhel-7-x86_64/postgresql15-15.1-1PGDG.rhel7.x86_64.rpm
wget https://yum.postgresql.org/15/redhat/rhel-7-x86_64/postgresql15-contrib-15.1-1PGDG.rhel7.x86_64.rpm
wget https://yum.postgresql.org/15/redhat/rhel-7-x86_64/postgresql15-libs-15.1-1PGDG.rhel7.x86_64.rpm
wget https://yum.postgresql.org/15/redhat/rhel-7-x86_64/postgresql15-server-15.1-1PGDG.rhel7.x86_64.rpm

# Install PostgreSQL
yum install postgresql15-15.1-1PGDG.rhel7.x86_64.rpm postgresql15-contrib-15.1-1PGDG.rhel7.x86_64.rpm postgresql15-libs-15.1-1PGDG.rhel7.x86_64.rpm postgresql15-server-15.1-1PGDG.rhel7.x86_64.rpm

# 此时/var/lib/pgsql/15/data/目录为空， /usr/pgsql-15/bin/ 有常用的工具


mkdir /data/pgsql
chown postgres /data/pgsql
chmod 700 /data/pgsql
sudo -u postgres /usr/pgsql-15/bin/initdb -D /data/pgsql

vi /usr/lib/systemd/system/postgresql-15.service
# 修改下面的变量为
Environment=PGDATA=/data/pgsql/

# Optionally initialize the database and enable automatic start:
# sudo /usr/pgsql-15/bin/postgresql-15-setup initdb
sudo systemctl enable postgresql-15
sudo systemctl start postgresql-15
sudo systemctl stop postgresql-15

# 卸载
rpm -aq |grep postgresq
yum remove postgresql15-contrib-15.1-1PGDG.rhel7.x86_64
yum remove postgresql15-libs-15.1-1PGDG.rhel7.x86_64
yum remove postgresql15-server-15.1-1PGDG.rhel7.x86_64
yum remove postgresql15-15.1-1PGDG.rhel7.x86_64
```

# 常用操作
## 登录
```sql
psql -U postgres
```
```sql
PGPASSWORD=123456 psql -h172.1.1.1 -Upostgres -p5432
```
## 命令行中执行SQL
PGPASSWORD=123456 psql -h172.1.1.1 -Upostgres -p5432 -c "select id from test;"

## 显示列名
```sql
\pset tuples_only off
```

## 记录执行的SQL
```sql
SET log_duration = on;
```

## 显示SQL的执行耗时
```sql
\timing
```

## 查看当前的数据库
```sql
SELECT current_database();
```

## 查看当前的 Schema
```sql
SELECT current_schema;
```

## 查看当前的用户
```sql
SELECT current_user;
```

## 查看当前的用户所属的角色
```sql
SELECT rolname
FROM pg_roles
WHERE pg_roles.oid IN (SELECT usesysid FROM pg_user WHERE usename = current_user);
```

## 查看有哪些数据库
```sql
postgres=# SELECT datname FROM pg_database;
  datname  
-----------
 postgres
 template1
 template0
(3 rows)
```

## 查看当前数据库有哪些 Schema
```sql
SELECT schema_name
FROM information_schema.schemata;
```

## 查看角色有哪些权限
### 角色级别的权限
```sql
postgres=# \du+ postgres;
                                          List of roles
 Role name |                         Attributes                         | Member of | Description 
-----------+------------------------------------------------------------+-----------+-------------
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}        | 


postgres=# SELECT * FROM pg_roles;
          rolname          | rolsuper | rolinherit | rolcreaterole | rolcreatedb | rolcanlogin | rolreplication | rolconnlimit | rolpassword | rolvaliduntil | rolbypassrls | rolconfig |  oid  
---------------------------+----------+------------+---------------+-------------+-------------+----------------+--------------+-------------+---------------+--------------+-----------+-------
 postgres                  | t        | t          | t             | t           | t           | t              |           -1 | ********    |               | t            |           |    10
 pg_database_owner         | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  6171
 pg_read_all_data          | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  6181
 pg_write_all_data         | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  6182
 pg_monitor                | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  3373
 pg_read_all_settings      | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  3374
 pg_read_all_stats         | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  3375
 pg_stat_scan_tables       | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  3377
 pg_read_server_files      | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  4569
 pg_write_server_files     | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  4570
 pg_execute_server_program | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  4571
 pg_signal_backend         | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  4200
 pg_checkpoint             | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           |  4544
 ldc                       | f        | t          | f             | f           | t           | f              |           -1 | ********    |               | f            |           | 16390
(14 rows)

postgres=# SELECT * FROM pg_user;
 usename  | usesysid | usecreatedb | usesuper | userepl | usebypassrls |  passwd  | valuntil | useconfig 
----------+----------+-------------+----------+---------+--------------+----------+----------+-----------
 postgres |       10 | t           | t        | t       | t            | ******** |          | 
 ldc      |    16390 | f           | f        | f       | f            | ******** |          | 
(2 rows)
```
### 表级别权限
```sql
postgres=# SELECT *
FROM information_schema.role_table_grants
WHERE grantee = 'postgres' limit 5;
 grantor  | grantee  | table_catalog | table_schema |  table_name  | privilege_type | is_grantable | with_hierarchy 
----------+----------+---------------+--------------+--------------+----------------+--------------+----------------
 postgres | postgres | postgres      | pg_catalog   | pg_statistic | INSERT         | YES          | NO
 postgres | postgres | postgres      | pg_catalog   | pg_statistic | SELECT         | YES          | YES
 postgres | postgres | postgres      | pg_catalog   | pg_statistic | UPDATE         | YES          | NO
 postgres | postgres | postgres      | pg_catalog   | pg_statistic | DELETE         | YES          | NO
 postgres | postgres | postgres      | pg_catalog   | pg_statistic | TRUNCATE       | YES          | NO
```
### SCHEMA 级别权限
```sql
SELECT 
  nspname AS schema_name,
  has_schema_privilege('postgres', nspname, 'USAGE') AS has_usage_permission,
  has_schema_privilege('postgres', nspname, 'CREATE') AS has_create_permission
FROM pg_namespace;

    schema_name     | has_usage_permission | has_create_permission 
--------------------+----------------------+-----------------------
 pg_toast           | t                    | t
 pg_catalog         | t                    | t
 public             | t                    | t
 information_schema | t                    | t
 pg_temp_4          | t                    | t
 pg_toast_temp_4    | t                    | t
```
### 列级别权限
```sql
postgres=# SELECT table_schema, table_name, column_name, privilege_type
FROM information_schema.role_column_grants
WHERE grantee = 'postgres' limit 5;
    table_schema    |       table_name        |        column_name         | privilege_type 
--------------------+-------------------------+----------------------------+----------------
 pg_catalog         | pg_stat_progress_vacuum | datid                      | SELECT
 information_schema | table_privileges        | table_schema               | UPDATE
 pg_catalog         | pg_namespace            | nspname                    | SELECT
 pg_catalog         | pg_type                 | typelem                    | INSERT
 information_schema | routines                | result_cast_collation_name | SELECT
```
### database 级别权限
```sql
SELECT 
  datname AS database_name,
  has_database_privilege('postgres', datname, 'CONNECT') AS has_connect_permission,
  has_database_privilege('postgres', datname, 'CREATE') AS has_create_permission,
  has_database_privilege('postgres', datname, 'TEMPORARY') AS has_temporary_permission,
  has_database_privilege('postgres', datname, 'TEMP') AS has_temp_permission
FROM pg_database;

 database_name | has_connect_permission | has_create_permission | has_temporary_permission | has_temp_permission 
---------------+------------------------+-----------------------+--------------------------+---------------------
 postgres      | t                      | t                     | t                        | t
 template1     | t                      | t                     | t                        | t
 template0     | t                      | t                     | t                        | t
(3 rows)
```
在PostgreSQL中，没有单独的删除数据库的权限。但是，如果角色拥有对数据库的CREATE权限，它可以使用`DROP DATABASE`命令删除数据库。您可以使用以下命令来检查角色是否拥有对数据库的CREATE权限：`SELECT has_database_privilege('role_name', 'database_name', 'CREATE');`。如果返回值为true，则表示该角色拥有删除数据库的权限。

## 删除操作
```sql
-- To delete a user or role
DROP ROLE your_user_or_role_name;

-- To delete a schema
DROP SCHEMA your_schema_name;

-- To delete a database
DROP DATABASE your_database_name;
```

## 切换数据库
```sql
postgres=# \c lindc   
You are now connected to database "lindc" as user "postgres".
lindc=# \c postgres
You are now connected to database "postgres" as user "postgres".
postgres=#
```

## 切换schema
```sql
lindc=# create schema lindeci;
CREATE SCHEMA
lindc=# SET search_path TO lindeci;
SET
lindc=# 
```
## 查看从库列表
```sql
SELECT * FROM pg_stat_replication;


以下是 pg_stat_replication 视图的一些常用字段：

    pid: 从库复制进程的进程 ID。
    application_name: 从库连接时指定的应用程序名称。
    client_addr: 从库的 IP 地址。
    state: 从库的连接状态，例如 streaming、backup、catchup 等。
    sync_state: 同步状态，通常显示为 async。
    sent_lsn: 主库发送到该从库的最后一个 WAL 位置。
    write_lsn: 从库已经写入磁盘的最后一个 WAL 位置。
    flush_lsn: 从库已经将其写入磁盘并且已通知主库的最后一个 WAL 位置。
    replay_lsn: 从库已经重放的最后一个 WAL 位置。
```

## 查看参数
```sql
SHOW archive_mode;
```

## 查看表结构
```sql
\dS+ 表名
```

## 查看 SCHEMA 的所有表数据量
```sql
SELECT schemaname, relname, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```
## 查看 SCHEMA 的所有表的空间大小
```sql
SELECT table_name, pg_total_relation_size('"' || table_schema || '"."' || table_name || '"') AS size_bytes
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY size_bytes DESC;
```

## 查看安装了哪些插件
```sql
-- 返回所有可用的扩展插件列表，无论是否已经安装
SELECT * FROM pg_available_extensions;
-- 这条查询将返回已安装的扩展插件列表
SELECT * FROM pg_extension;
```

# 备份恢复
## 库级别
```
pg_dump -h 172.1.1.2 -U postgres -d kong -n public -f /tmp/backup.sql
psql -h 172.1.1.2 -U postgres -d pgbench < backup.sql
```
## 表级别
```
pg_dump -h 172.1.1.2 -U postgres -d pgbench -t pgbench_accounts > backup.sql
psql -h 172.1.1.2 -U postgres -d pgbench < backup.sql
```
# 查看连接和 kill 连接
```sql
SELECT datid,datname,pid,usename,backend_start,xact_start,query_start,query FROM pg_stat_activity;
```
kill 连接
```sql
SELECT pg_terminate_backend(pid);
```

# SEQUENCE
查看序列
```sql
SELECT * FROM information_schema.sequences WHERE sequence_name = 'undo_log_id_seq';

 sequence_catalog | sequence_schema |  sequence_name  | data_type | numeric_precision | numeric_precision_radix | numeric_scale | start_value | minimum_value | maximum_value | increment | cycle_option 
------------------+-----------------+-----------------+-----------+-------------------+-------------------------+---------------+-------------+---------------+---------------+-----------+--------------
 kong             | public          | undo_log_id_seq | integer   |                32 |                       2 |             0 | 1           | 1             | 2147483647    | 1         | NO
```
删除序列
```sql
DROP SEQUENCE IF EXISTS undo_log_id_seq;
```
创建序列
```sql
-- 默认
CREATE TABLE IF NOT EXISTS public.undo_log
(
    id            SERIAL       NOT NULL,
    name text,
    CONSTRAINT pk_undo_log PRIMARY KEY (id)
);
insert into undo_log (name) values ('a'),('b');

select * from undo_log;
 id | name 
----+------
  1 | a
  2 | b
(2 rows)

drop table undo_log;

-- 与预期不符的测试
-- 原因：虽然你在创建序列时设置了 INCREMENT BY 2，但在 SERIAL 数据类型中，序列的递增值是由数据类型本身确定的。SERIAL 数据类型的默认值是 1，这意味着它会自动递增生成主键值，而不受序列的 INCREMENT BY 影响。
CREATE SEQUENCE IF NOT EXISTS undo_log_id_seq INCREMENT BY 2 MINVALUE 1 ;
CREATE TABLE IF NOT EXISTS public.undo_log
(
    id            SERIAL       NOT NULL,
    name text,
    CONSTRAINT pk_undo_log PRIMARY KEY (id)
);
insert into undo_log (name) values ('a'),('b');
select * from undo_log;
 id | name 
----+------
  1 | a
  2 | b
(2 rows)
-- 与预期相符的测试
insert into undo_log (id,name) values (NEXTVAL('undo_log_id_seq'),'a'),(NEXTVAL('undo_log_id_seq'),'b');
select * from undo_log;
 id | name 
----+------
  1 | a
  3 | b
(2 rows)

-- 与预期相符的测试
CREATE SEQUENCE IF NOT EXISTS undo_log_id_seq INCREMENT BY 2 MINVALUE 1;
CREATE TABLE undo_log (
    id integer DEFAULT nextval('undo_log_id_seq') NOT NULL,
    name text,
    CONSTRAINT pk_undo_log PRIMARY KEY (id)
);
insert into undo_log (name) values ('a'),('b');
INSERT 0 2
select * from undo_log;
 id | name 
----+------
  1 | a
  3 | b
(2 rows)
```
修改序列
```sql
alter sequence undo_log_id_seq start with 1;
ALTER SEQUENCE undo_log_id_seq RESTART WITH 100 INCREMENT BY 2;
```

# 创建指定权限用户
```sql
CREATE USER kong_dev WITH PASSWORD 'kong@123';
# 需要进入
\c kong
GRANT CONNECT ON DATABASE kong TO kong_dev;
GRANT USAGE ON SCHEMA public TO kong_dev;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO kong_dev;
```
# 创建只读账号
```sql
/c mydb
CREATE USER readonly_user WITH ENCRYPTED PASSWORD '123';
ALTER USER readonly_user SET default_transaction_read_only = ON;
ALTER USER readonly_user WITH login;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

# 授权序列
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO readonly_user;
```

# 授权监控权限
```sql
CREATE USER postgres_exporter WITH PASSWORD '123';
GRANT pg_read_all_settings, pg_read_all_stats TO postgres_exporter;
ALTER USER postgres_exporter SET SEARCH_PATH TO postgres_exporter,pg_catalog;
```
# 修改库的OWNER
```sql
ALTER DATABASE db_test OWNER TO my_user;
```

# 修改用户密码
```sql
ALTER USER postgres WITH PASSWORD 'new_password';
ALTER USER repl WITH PASSWORD 'repl123';
```

# 添加建表权限
```sql
GRANT CREATE ON SCHEMA public TO kong_dev;
```
# 授权序列
```sql
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO kong_dev;
```
# 给 kong 的所有权限
```sql
ALTER DATABASE kong OWNER TO kong_dev;
```
# pgbench 压测



# 帮助命令
## General

| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \copyright             | show PostgreSQL usage and distribution terms         | 显示PostgreSQL使用和分发条款                             |
| \crosstabview          | execute query and display result in crosstab         | 执行查询并以交叉表方式显示结果                           |
| \errverbose            | show most recent error message at maximum verbosity  | 以最大详细程度显示最近的错误消息                         |
| \g [(OPTIONS)] [FILE]  | execute query (and send result to file or pipe); \g with no arguments is equivalent to a semicolon  | 执行查询（并将结果发送到文件或管道）；\g 没有参数的g相当于分号 |
| \gdesc                 | describe result of query, without executing it       | 描述查询的结果，而不执行它                               |
| \gexec                 | execute query, then execute each value in its result | 执行查询，然后执行结果中的每个值                         |
| \gset [PREFIX]         | execute query and store result in psql variables     | 执行查询并将结果存储在psql变量中                         |
| \gx [(OPTIONS)] [FILE] | as \g, but forces expanded output mode               | 与\g相同，但强制使用扩展输出模式                         |
| \q                     | quit psql                                            | 退出psql                                                 |
| \watch [SEC]           | execute query every SEC seconds                      | 每隔SEC秒执行查询                                        |

## Help
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| ? [commands]          | show help on backslash commands                      | 显示反斜杠命令的帮助                   |
| ? options             | show help on psql command-line options               | 显示psql命令行选项的帮助               |
| ? variables           | show help on special variables                       | 显示特殊变量的帮助                     |
| \h [NAME]             | help on syntax of SQL commands, * for all commands   | SQL命令语法的帮助，*表示所有命令       |

## Query Buffer
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \e [FILE] [LINE]      | edit the query buffer (or file) with external editor | 使用外部编辑器编辑查询缓冲区（或文件） |
| \ef [FUNCNAME [LINE]] | edit function definition with external editor        | 使用外部编辑器编辑函数定义             |
| \ev [VIEWNAME [LINE]] | edit view definition with external editor            | 使用外部编辑器编辑视图定义             |
| \p                    | show the contents of the query buffer                | 显示查询缓冲区的内容                   |
| \r                    | reset (clear) the query buffer                       | 重置（清除）查询缓冲区                 |
| \s [FILE]             | display history or save it to file                   | 显示历史记录或将其保存到文件           |
| \w FILE               | write query buffer to file                           | 将查询缓冲区写入文件                   |

## Input/Output
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \copy ...            | perform SQL COPY with data stream to the client host | 执行SQL COPY，并将数据流复制到客户端主机   |
| \echo [-n] [STRING]  | write string to standard output (-n for no newline)  | 将字符串写入标准输出（-n表示无换行符）     |
| \i FILE              | execute commands from file                           | 从文件执行命令                             |
| \ir FILE             | as \i, but relative to location of current script    | 与\i相同，但相对于当前脚本的位置           |
| \o [FILE]            | send all query results to file or                    | pipe                                       |
| \qecho [-n] [STRING] | write string to \o output stream (-n for no newline) | 将字符串写入\o输出流（-n表示无换行符）     |
| \warn [-n] [STRING]  | write string to standard error (-n for no newline)   | 将字符串写入标准错误输出（-n表示无换行符） |


## Conditional
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \if EXPR             | begin conditional block                              | 开始条件块                                 |
| \elif EXPR           | alternative within current conditional block         | 当前条件块中的替代选项                     |
| \else                | final alternative within current conditional block   | 当前条件块中的最后一个替代选项             |
| \endif               | end conditional block                                | 结束条件块                                 |


## Informational
(options: S = show system objects, + = additional detail)
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \d[S+]                                   | list tables, views, and sequences                         | 列出表、视图和序列                             |
| \d[S+] NAME                              | describe table, view, sequence, or index                  | 描述表、视图、序列或索引                       |
| \da[S] [PATTERN]                         | list aggregates                                           | 列出聚合函数                                   |
| \dA[+] [PATTERN]                         | list access methods                                       | 列出访问方法                                   |
| \dAc[+] [AMPTRN [TYPEPTRN]]              | list operator classes                                     | 列出操作符类                                   |
| \dAf[+] [AMPTRN [TYPEPTRN]]              | list operator families                                    | 列出操作符族                                   |
| \dAo[+] [AMPTRN [OPFPTRN]]               | list operators of operator families                       | 列出操作符族的操作符                           |
| \dAp[+] [AMPTRN [OPFPTRN]]               | list support functions of operator families               | 列出操作符族的支持函数                         |
| \db[+] [PATTERN]                         | list tablespaces                                          | 列出表空间                                     |
| \dc[S+] [PATTERN]                        | list conversions                                          | 列出转换函数                                   |
| \dconfig[+] [PATTERN]                    | list configuration parameters                             | 列出配置参数                                   |
| \dC[+] [PATTERN]                         | list casts                                                | 列出类型转换函数                               |
| \dd[S] [PATTERN]                         | show object descriptions not displayed elsewhere          | 显示未在其他地方显示的对象描述                 |
| \dD[S+] [PATTERN]                        | list domains                                              | 列出域                                         |
| \ddp [PATTERN]                           | list default privileges                                   | 列出默认权限                                   |
| \dE[S+] [PATTERN]                        | list foreign tables                                       | 列出外部表                                     |
| \des[+] [PATTERN]                        | list foreign servers                                      | 列出外部服务器                                 |
| \det[+] [PATTERN]                        | list foreign tables                                       | 列出外部表                                     |
| \deu[+] [PATTERN]                        | list user mappings                                        | 列出用户映射                                   |
| \dew[+] [PATTERN]                        | list foreign-data wrappers                                | 列出外部数据封装                               |
| \df[anptw][S+] [FUNCPTRN [TYPEPTRN ...]] | list [only agg/normal/procedure/trigger/window] functions | 列出[仅聚合函数/普通函数/过程/触发器/窗口函数] |
| \dF[+] [PATTERN]                         | list text search configurations                           | 列出文本搜索配置                               |
| \dFd[+] [PATTERN]                        | list text search dictionaries                             | 列出文本搜索字典                               |
| \dFp[+] [PATTERN]                        | list text search parsers                                  | 列出文本搜索解析器                             |
| \dFt[+] [PATTERN]                        | list text search templates                                | 列出文本搜索模板                               |
| \dg[S+] [PATTERN]                        | list roles                                                | 列出角色                                       |
| \di[S+] [PATTERN]                        | list indexes                                              | 列出索引                                       |
| \dl[+]                                   | list large objects, same as \lo_list                      | 列出大型对象，与\lo_list相同                   |
| \dL[S+] [PATTERN]                        | list procedural languages                                 | 列出过程化语言                                 |
| \dm[S+] [PATTERN]                        | list materialized views                                   | 列出物化视图                                   |
| \dn[S+] [PATTERN]                        | list schemas                                              | 列出模式                                       |
| \do[S+] [OPPTRN [TYPEPTRN [TYPEPTRN]]]   | list operators                                            | 列出操作符                                     |
| \dO[S+] [PATTERN]                        | list collations                                           | 列出排序规则                                   |
| \dp [PATTERN]                            | list table, view, and sequence access privileges          | 列出表、视图和序列的访问权限                   |
| \dP[itn+] [PATTERN]                      | list [only index/table] partitioned relations [n=nested]  | 列出[仅索引/表]的分区关系[n=嵌套]              |
| \drds [ROLEPTRN [DBPTRN]]                | list per-database role settings                           | 列出每个数据库的角色设置                       |
| \dRp[+] [PATTERN]                        | list replication publications                             | 列出复制发布                                   |
| \dRs[+] [PATTERN]                        | list replication subscriptions                            | 列出复制订阅                                   |
| \ds[S+] [PATTERN]                        | list sequences                                            | 列出序列                                       |
| \dt[S+] [PATTERN]                        | list tables                                               | 列出表                                         |
| \dT[S+] [PATTERN]                        | list data types                                           | 列出数据类型                                   |
| \du[S+] [PATTERN]                        | list roles                                                | 列出角色                                       |
| \dv[S+] [PATTERN]                        | list views                                                | 列出视图                                       |
| \dx[+] [PATTERN]                         | list extensions                                           | 列出扩展                                       |
| \dX [PATTERN]                            | list extended statistics                                  | 列出扩展统计信息                               |
| \dy[+] [PATTERN]                         | list event triggers                                       | 列出事件触发器                                 |
| \l[+] [PATTERN]                          | list databases                                            | 列出数据库                                     |
| \sf[+] FUNCNAME                          | show a function's definition                              | 显示函数的定义                                 |
| \sv[+] VIEWNAME                          | show a view's definition                                  | 显示视图的定义                                 |
| \z [PATTERN]                             | same as \dp                                               | 与\dp相同                                      |

## Large Objects
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \lo_export LOBOID FILE    | write large object to file  | 将大型对象写入文件 |
| \lo_import FILE [COMMENT] | read large object from file | 从文件读取大型对象 |
| \lo_list[+]               | list large objects          | 列出大型对象       |
| \lo_unlink LOBOID         | delete a large object       | 删除大型对象       |

## Formatting
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \a                   | toggle between unaligned and aligned output mode       | 在未对齐和对齐输出模式之间切换                  |
| \C [STRING]          | set table title, or unset if none                      | 设置表标题，如果没有则取消设置                  |
| \f [STRING]          | show or set field separator for unaligned query output | 显示或设置未对齐查询输出的字段分隔符            |
| \H                   | toggle HTML output mode (currently off)                | 切换HTML输出模式（当前关闭）                    |
| \pset [NAME [VALUE]] | set table output option                                | 设置表输出选项                                  |
| \t [on               | off]                                                   | show only rows (currently off)                  |
| \T [STRING]          | set HTML`<table>` tag attributes, or unset if none   | 设置HTML`<table>`标签属性，如果没有则取消设置 |
| \x [on               | off                                                    | auto]                                           |

## Connection
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \c[onnect] {[DBNAME    | - USER                                              | - HOST                                    |
| \conninfo              | display information about current connection        | 显示有关当前连接的信息                    |
| \encoding [ENCODING]   | show or set client encoding                         | 显示或设置客户端编码                      |
| \password [USERNAME]   | securely change the password for a user             | 安全地更改用户的密码                      |

## Operating System
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \cd [DIR]              | change the current working directory                | 更改当前工作目录                          |
| \getenv PSQLVAR ENVVAR | fetch environment variable                          | 获取环境变量                              |
| \setenv NAME [VALUE]   | set or unset environment variable                   | 设置或取消设置环境变量                    |
| \timing [on            | off]                                                | toggle timing of commands (currently off) |
| ! [COMMAND]            | execute command in shell or start interactive shell | 在Shell中执行命令或启动交互式Shell        |


## Variables
| 命令                   | 原英文描述                                           | 中文描述                                                 |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------------------- |
| \prompt [TEXT] NAME | prompt user to set internal variable                | 提示用户设置内部变量                       |
| \set [NAME [VALUE]] | set internal variable, or list all if no parameters | 设置内部变量，如果没有参数，则列出所有变量 |
| \unset NAME         | unset (delete) internal variable                    | 取消设置（删除）内部变量                   |

# 启动关闭
```sql
/data/pgsql/13/bin/pg_ctl  -D /data/pgsql/13/data start
/data/pgsql/13/bin/pg_ctl -D /data/pgsql/13/data stop
```

# 物理备份恢复
注意点：  
1、文件权限、属主
2、注释 postgresql.conf 中的这段：
```sh
recovery_target = ''
recovery_target_lsn = ''
recovery_target_name = ''
recovery_target_time = ''
recovery_target_timeline = 'latest'
recovery_target_xid = ''
```
3、 postgresql.base.conf 中的 shared_buffers 调整
