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
- [关闭数据库所有会话](#关闭数据库所有会话)
- [查询注释](#查询注释)
- [to\_timestamp() 字符串转时间](#to_timestamp-字符串转时间)
- [to\_char 时间转字符串](#to_char-时间转字符串)
- [根据已有表结构创建表](#根据已有表结构创建表)
- [时间加减](#时间加减)
- [substring字符串截取](#substring字符串截取)
- [执行sql脚本](#执行sql脚本)
- [导出数据到SQL文件](#导出数据到sql文件)
- [单机 PostgreSQL 连接串](#单机-postgresql-连接串)
- [集群PostgreSQL 连接串](#集群postgresql-连接串)
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
- [参数讲解](#参数讲解)
- [数据同步点位日志](#数据同步点位日志)
- [PG 编译脚本](#pg-编译脚本)

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

在 PostgreSQL 中，如果你执行 `SET log_duration = on;`，它会记录每个已完成的 SQL 语句的持续时间。但是需要注意的是，默认情况下，这个选项是关闭的。如果你想要记录所有 SQL 语句，你还需要在 `postgresql.conf` 文件中设置以下参数：
- 将 `log_statement` 设置为 `'all'`，以记录所有 SQL 语句。
- 将 `log_min_duration_statement` 设置为 `0`，以记录所有语句的执行时间²。
此外，确保你已经启用了 `logging_collector`，并且 `log_directory` 目录已经存在且可写入。


postgresql 开启审计日志  
1、审计清单说明
```sh
logging_collector     --是否开启日志收集开关，默认off，推荐on
log_destination       --日志记录类型，默认是stderr，只记录错误输出，推荐csvlog，总共包含：stderr, csvlog, syslog, and eventlog,
log_directory          --日志路径，默认是$PGDATA/pg_log, 
log_filename            --日志名称，默认是postgresql-%Y-%m-%d_%H%M%S.log
log_file_mode           --日志文件类型，默认为0600
log_truncate_on_rotation  --默认为off，设置为on的话，文件内容覆盖方式：off后面附加，on：清空再加
log_rotation_age      --保留单个文件的最大时长,默认是1d,也有1h,1min,1s
log_rotation_size       --保留单个文件的最大尺寸，默认是10MB
log_error_verbosity    --默认为default，verbose表示冗长的
log_connections    --用户session登陆时是否写入日志，默认off，推荐为on
log_disconnections --用户session退出时是否写入日志，默认off，推荐为on
log_statement    --记录用户登陆数据库后的各种操作 none，即不记录ddl(记录create,drop和alter) mod(记录ddl+insert,delete,update和truncate) all(mod+select)
log_min_duration_statement = 2s   --记录超过2秒的SQL
log_checkpoints = on
log_lock_waits ＝ on
deadlock_timeout ＝ 1s
```
2、推荐的设置参数
```
logging_collector = on
log_destination = 'csvlog'
log_truncate_on_rotation = on
log_connections = on
log_disconnections = on
log_error_verbosity = verbose
log_statement = ddl
log_min_duration_statement = 60s
log_checkpoints = on
log_lock_waits ＝ on
deadlock_timeout ＝ 1s
```
log_min_duration_statement、log_checkpoints、log_lock_waits是postgresql.conf文件中没有的

查看日志目录和日志文件名：
``
show log_directory;
show log_filename;
``
3、参数修改方法

直接修改配置文件

postgresql.conf默认位于$PGDATA目录下。
```
vi /usr/data/pgsql/data/postgresql.conf

用超级用户运行：postgres=# SELECT pg_reload_conf();
```
show命令可以查询当前状态

 审计日志例子
```sh
2024-07-20 03:50:20.371 UTC,"postgres","postgres",28023,"[local]",669b320b.6d77,8,"idle",2024-07-20 03:42:03 UTC,0/11,0,LOG,00000,"statement: select name,enumvals,extra_desc from pg_settings where name like 'log%';",,,,,,,,,"psql","client backend",,0
```
这个 PostgreSQL 的审计日志中的字段含义如下：
1. **时间戳**：2024-07-20 03:50:20.371 UTC，表示日志记录的时间。
2. **用户名**：`"postgres"`，表示执行 SQL 语句的数据库用户。
3. **数据库名**：`"postgres"`，表示连接到的数据库名称。
4. **进程 ID**：`28023`，表示执行 SQL 语句的后台进程的 ID。
5. **客户端地址**：`"[local]"`，表示客户端连接的地址。
6. **会话 ID**：`669b320b.6d77`，表示会话的唯一标识符。
7. **会话状态**：`"idle"`，表示会话当前的状态。
8. **开始时间**：`2024-07-20 03:42:03 UTC`，表示会话开始的时间。
9. **事务 ID**：`0/11`，表示当前事务的 ID。
10. **日志级别**：`LOG`，表示日志的级别。
11. **消息代码**：`00000`，表示消息的代码。
12. **SQL 语句**：`"statement: select name,enumvals,extra_desc from pg_settings where name like 'log%';"`，表示执行的 SQL 查询语句。
13. **客户端应用程序名称**：`"psql"`，表示连接的客户端应用程序。
14. **客户端类型**：`"client backend"`，表示客户端的类型。
15. **错误位置**：空白，表示错误的位置（如果有）。
16. **错误详情**：空白，表示错误的详细信息（如果有）。

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
查看 Schema 下有哪些表
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'information_schema';
```


当你查询 `information_schema` schema 下的表时，你会看到以下表，它们的用途如下：

1. **`column_column_usage`**：存储关于列之间的关系的信息，例如外键关系。

2. **`information_schema_catalog_name`**：存储关于数据库目录的信息。

3. **`check_constraints`**：存储关于检查约束的信息。

4. **`applicable_roles`**：存储适用于当前会话的角色信息。

5. **`administrable_role_authorizations`**：存储角色授权信息。

6. **`attributes`**：存储关于用户定义类型的属性信息。

7. **`collations`**：存储关于排序规则的信息。

8. **`character_sets`**：存储关于字符集的信息。

9. **`check_constraint_routine_usage`**：存储关于检查约束的例程使用信息。

10. **`column_privileges`**：存储关于列级权限的信息。

11. **`collation_character_set_applicability`**：存储关于排序规则和字符集的适用性信息。

12. **`column_domain_usage`**：存储关于列和域之间的关系的信息。

13. **`column_udt_usage`**：存储关于列和用户定义类型之间的关系的信息。

14. **`columns`**：存储关于表的列的信息。

15. **`constraint_column_usage`**：存储关于约束和列之间的关系的信息。

16. **`constraint_table_usage`**：存储关于约束和表之间的关系的信息。

17. **`domain_constraints`**：存储关于域约束的信息。

18. **`routine_table_usage`**：存储关于例程和表之间的关系的信息。

19. **`domain_udt_usage`**：存储关于域和用户定义类型之间的关系的信息。

20. **`domains`**：存储关于域的信息。

21. **`enabled_roles`**：存储启用的角色信息。

22. **`routines`**：存储关于例程（函数和过程）的信息。

23. **`key_column_usage`**：存储关于主键和外键列之间的关系的信息。

24. **`parameters`**：存储关于例程参数的信息。

25. **`referential_constraints`**：存储关于引用约束的信息。

26. **`schemata`**：存储关于模式（schema）的信息。

27. **`role_column_grants`**：存储关于角色和列权限之间的关系的信息。

28. **`routine_column_usage`**：存储关于例程和列之间的关系的信息。

29. **`sql_parts`**：存储关于 SQL 语句部分的信息。

30. **`routine_privileges`**：存储关于例程权限的信息。

31. **`sequences`**：存储关于序列的信息。

32. **`role_routine_grants`**：存储关于角色和例程权限之间的关系的信息。

33. **`routine_routine_usage`**：存储关于例程之间的关系的信息。

34. **`routine_sequence_usage`**：存储关于例程和序列之间的关系的信息。

35. **`sql_features`**：存储关于 SQL 功能的信息。

36. **`sql_implementation_info`**：存储关于 SQL 实现的信息。

37. **`role_table_grants`**：存储关于角色和表权限之间的关系的信息。

38. **`sql_sizing`**：存储关于 SQL 大小的信息。

39. **`table_privileges`**：存储关于表级权限的信息。

40. **`table_constraints`**：存储关于表约束的信息。

41. **`transforms`**：存储关于转换的信息。

42. **`tables`**：存储关于数据库中所有表的信息，包括表名、所属模式、表类型等。

43. **`triggered_update_columns`**：存储关于触发器更新的列的信息。

44. **`triggers`**：存储关于触发器的信息，包括触发器名称、所属表、触发事件等。

45. **`udt_privileges`**：存储关于用户定义类型（UDT）的权限信息。

46. **`_pg_foreign_data_wrappers`**：存储外部数据包装器的信息，用于访问外部数据源。

47. **`role_udt_grants`**：存储关于角色和用户定义类型权限之间的关系的信息。

48. **`usage_privileges`**：存储关于对象使用权限的信息，例如表、视图等。

49. **`foreign_tables`**：存储关于外部表的信息，这些表连接到外部数据源。

50. **`role_usage_grants`**：存储关于角色和对象使用权限之间的关系的信息。

51. **`foreign_data_wrapper_options`**：存储外部数据包装器的选项信息。

52. **`user_defined_types`**：存储关于用户定义类型（UDT）的信息。

53. **`view_column_usage`**：存储关于视图列的使用信息。

54. **`view_routine_usage`**：存储关于视图和例程之间的关系的信息。

55. **`foreign_data_wrappers`**：存储外部数据包装器的信息。

56. **`view_table_usage`**：存储关于视图和表之间的关系的信息。

57. **`views`**：存储关于数据库中所有视图的信息。

58. **`_pg_foreign_servers`**：存储外部服务器的信息，用于连接到外部数据源。

59. **`data_type_privileges`**：存储关于数据类型权限的信息。

60. **`element_types`**：存储关于数组元素类型的信息。

61. **`_pg_foreign_table_columns`**：存储外部表的列信息。

62. **`_pg_user_mappings`**：存储用户映射的信息，用于连接到外部数据源。

63. **`column_options`**：存储关于列选项的信息。

64. **`foreign_server_options`**：存储外部服务器的选项信息。

65. **`foreign_servers`**：存储外部服务器的信息。

66. **`_pg_foreign_tables`**：存储外部表的信息。

67. **`foreign_table_options`**：存储外部表的选项信息。

68. **`user_mapping_options`**：存储用户映射的选项信息。

69. **`user_mappings`**：存储用户映射的信息。



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

# 关闭数据库所有会话
```sql
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE datname='mydb' AND pid<>pg_backend_pid();
```
# 查询注释
```sql
SELECT
a.attname as "字段名",
col_description(a.attrelid,a.attnum) as "注释",
concat_ws('',t.typname,SUBSTRING(format_type(a.atttypid,a.atttypmod) from '(.*)')) as "字段类型"
FROM
pg_class as c,
pg_attribute as a,
pg_type as t
WHERE
c.relname = 't_batch_task'
and a.atttypid = t.oid
and a.attrelid = c.oid
and a.attnum>0;
```
# to_timestamp() 字符串转时间
```sql
select * from t_user
where create_time >= to_timestamp('2023-01-01 00:00:00', 'yyyy-mm-dd hh24:MI:SS');
```
# to_char 时间转字符串
```sql
select to_char(create_time, 'yyyy-mm-dd hh24:MI:SS') from t_user;
```

# 根据已有表结构创建表
```sql
create table if not exists 新表 (like 旧表 including indexes including comments including defaults);
```
# 时间加减
```sql
-- 当前时间加一天
SELECT NOW()::TIMESTAMP + '1 day';
SELECT NOW() + INTERVAL '1 DAY';
SELECT now()::timestamp + ('1' || ' day')::interval
-- 当前时间减一天
SELECT NOW()::TIMESTAMP + '-1 day';
SELECT NOW() - INTERVAL '1 DAY';
SELECT now()::timestamp - ('1' || ' day')::interval
-- 加1年1月1天1时1分1秒
select NOW()::timestamp + '1 year 1 month 1 day 1 hour 1 min 1 sec';
```
# substring字符串截取
```sql
--从第一个位置开始截取，截取4个字符,返回结果:Post
SELECT SUBSTRING ('PostgreSQL', 1, 4);
-- 从第8个位置开始截取，截取到最后一个字符，返回结果:SQL
SELECT SUBSTRING ('PostgreSQL', 8);
--正则表达式截取，截取'gre'字符串
SELECT SUBSTRING ('PostgreSQL', 'gre');
```
# 执行sql脚本
方式一：先登录再执行
```sql
\i testdb.sql
```

方式二：通过psql执行
```sql
psql -d testdb -U postgres -f /pathA/xxx.sql
```
# 导出数据到SQL文件
```sql
pg_dump -h localhost -p 5432 -U postgres --column-inserts -t table_name -f save_sql.sql database_name

--column-inserts #以带有列名的 `INSERT` 命令形式转储数据。
-t #只转储指定名称的表。
-f #指定输出文件或目录名。
```

# 单机 PostgreSQL 连接串
```java
url: jdbc:postgresql://10.20.1.231:5432/postgres?
binaryTransfer=false&forceBinary=false&reWriteBatchedInserts=true

binaryTransfer=false：控制是否使用二进制协议传输数据，false 表示不适用，默认为 true
forceBinary=false：控制是否将非 ASCII 字符串强制转换为二进制格式，false 表示不强制转换，默认为 true
reWriteBatchedInserts=true：控制是否将批量插入语句转换成更高效的形式，true 表示转换，默认为 false
```
# 集群PostgreSQL 连接串
```java
url: jdbc:postgresql://10.20.1.231:5432/postgres?
binaryTransfer=false&forceBinary=false&reWriteBatchedInserts=true&targetServerType=master&loadBalanceHosts=true

单机 PostgreSQL 连接串的所有参数。
targetServerType=master：只允许连接到具有所需状态的服务器，可选值有：
any：默认，表示连接到任何一个可用的数据库服务器，不区分主从数据库；
master：表示连接到主数据库，可读写；
slave：表示连接到从数据库，可读，不可写；
其他不常用值：primary, master, slave, secondary, preferSlave, preferSecondary and preferPrimary。
loadBalanceHosts=true：控制是否启用主从模式下的负载均衡，true 表示启用，开启后依序选择一个 ip1:port 进行连接，默认为 false。
```

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

# 参数讲解
```
在 PostgreSQL 中，参数配置对于数据库性能和稳定性至关重要。最优参数配置方案将根据你的具体硬件、工作负载和应用程序需求而变化。以下是一些通用的建议，但在实际配置之前，请先在测试环境中进行评估和测试，并根据测试结果进行调整。

内存配置：
    shared_buffers：设置为物理内存的 25% - 50%。这是最重要的参数，用于设置 PostgreSQL 缓冲区的大小。
    work_mem：设置每个连接的内存排序和哈希操作的内存量。根据并发连接数和工作负载进行调整。
    maintenance_work_mem：设置维护操作（如 VACUUM、索引创建等）的内存量。根据数据库大小进行调整。

并发连接：
    max_connections：设置数据库允许的最大并发连接数。根据应用程序的并发需求进行调整，避免过多的连接数导致资源耗尽。

并发控制：
    deadlock_timeout：设置检测死锁的超时时间。
    max_locks_per_transaction：限制每个事务可以获取的锁的数量，避免死锁。

日志和统计：
    log_destination：配置日志输出的目标（例如日志文件或控制台）。
    logging_collector：启用日志收集器，用于管理日志文件。
    log_rotation_age 和 log_rotation_size：配置日志文件的自动轮换策略。
    log_statement：根据需求设置记录哪些 SQL 语句到日志中（例如 'all' 记录所有语句）。
    track_counts：启用或禁用表行计数。

查询优化：
    effective_cache_size：设置查询规划器预估的系统缓存大小。
    random_page_cost 和 seq_page_cost：根据存储设备类型调整随机 IO 和顺序 IO 的成本估算。
    autovacuum：启用自动 VACUUM 进程，定期回收过时数据，避免表膨胀。
	
自动保存配置：
    autovacuum：启用自动 VACUUM 进程，它有助于维护数据库表的性能。
    autovacuum_vacuum_scale_factor 和 autovacuum_analyze_scale_factor：根据表的大小，调整自动 VACUUM 和自动分析操作的阈值。默认值为 0.2 和 0.1。

其他：
    timezone：设置数据库的时区。
    synchronous_commit：设置事务的同步提交方式，可以根据对数据安全性和性能的需求调整。
    max_wal_size 和 min_wal_size：配置 WAL 日志大小，以确保足够的日志保留和切换频率。

以上仅是一些常见的 PostgreSQL 参数配置建议，实际配置应根据你的具体情况进行调整。注意，在更改配置后，需要重新启动 PostgreSQL 服务才能使配置生效。始终建议在进行参数调整前备份数据库，并进行充分的性能测试，以确保改动不会导致意外的影响。
```

# 数据同步点位日志
```
Starting stream read, table list: [pgbench_branches, pgbench_accounts, pgbench_tellers, pgbench_history], offset: {"sortString":null,"offsetValue":null,"sourceOffset":"{\"lsn_proc\":1854861168,\"lsn_commit\":1854861168,\"lsn\":1854861168,\"ts_usec\":1718957298702780}"}
```

# PG 编译脚本
```sh
cat install.sh 
#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
postgres='postgresql-12.3'
geos='geos-3.6.1'
proj='proj-4.9.1'
gdal='gdal-2.2.1'
postgis='postgis-3.0.1'
ipsegment=`ifconfig -a|grep inet | grep -v 127.0.0.1 | grep -v inet6 | awk '{print $2}' | awk -F . '{print $1,$2,$3}' OFS="."`
neiwangIP=`ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`

mkdir -p /tmp/xlwlogs/

zlibpack=`rpm -qa |grep zlib|grep i686`
if [ "$zlibpack" != "" ]; then
   yum remove $zlibpack -y
fi

rpm -ivh ${basepath}/json-c-devel-0.11-4.el7_0.x86_64.rpm --nodeps >>/dev/null
tar -xzvf ${basepath}/${postgres}.tar.gz -C /tmp/ >>/dev/null
tar -xzvf ${basepath}/${geos}-make.tar.gz  -C /tmp/ >> /dev/null
tar -xzvf ${basepath}/${proj}-make.tar.gz -C /tmp/ >> /dev/null
tar -xzvf ${basepath}/${gdal}.tar.gz -C /tmp/ >> /dev/null
tar -xvf ${basepath}/${postgis}.tar.gz -C /tmp/ >> /dev/null

mkdir -p /usr/local/postgresql

cd /tmp/$postgres
echo -e "\033[1;34m安装postgresql，请稍候......（时间较久，请勿强制停止脚本） \033[0m"
echo -e "\033[1;34m开始编译安装postgresql,0为成功，其它数字为失败 \033[0m" >>/tmp/xlwlogs/install.log
./configure --prefix=/usr/local/postgresql >> /dev/null
make  >> /dev/null
make install >> /dev/null && echo $? >>/tmp/xlwlogs/install.log

cd /tmp/$proj
echo -e "\033[1;34m安装proj，请稍候...... \033[0m"
echo -e "\033[1;34m开始编译安装proj,0为成功，其它数字为失败 \033[0m" >>/tmp/xlwlogs/install.log
./configure --prefix=/usr/local/proj >> /dev/null && make >> /dev/null && make install >> /dev/null && echo $? >>/tmp/xlwlogs/install.log

cd /tmp/$geos
echo -e "\033[1;34m安装geos，请稍候...... \033[0m"
echo -e "\033[1;34m开始编译安装geos,0为成功，其它数字为失败 \033[0m" >>/tmp/xlwlogs/install.log
./configure --prefix=/usr/local/geos >> /dev/null
make >> /dev/null
make install >> /dev/null && echo $? >>/tmp/xlwlogs/install.log

cd /tmp/$gdal/gdal/
echo -e "\033[1;34m安装gdal，请稍候...... \033[0m"
echo -e "\033[1;34m开始编译安装gdal,0为成功，其它数字为失败 \033[0m" >>/tmp/xlwlogs/install.log
./configure --prefix=/usr/local/gdal --with-pg=/usr/local/postgresql/bin/pg_config >> /dev/null
make >> /dev/null
make install >> /dev/null && echo $? >>/tmp/xlwlogs/install.log

cd /tmp/$postgis
echo -e "\033[1;34m安装postgis，请稍候...... \033[0m"
echo -e "\033[1;34m开始编译安装postgis,0为成功，其它数字为失败 \033[0m" >>/tmp/xlwlogs/install.log
echo '/usr/local/postgresql/lib' >>/etc/ld.so.conf
echo '/usr/local/proj/lib' >>/etc/ld.so.conf
echo '/usr/local/gdal/lib' >>/etc/ld.so.conf
echo '/usr/local/geos/lib' >>/etc/ld.so.conf
ldconfig
./configure --prefix=/usr/local/postgresql/ --with-pgconfig=/usr/local/postgresql/bin/pg_config --with-geosconfig=/usr/local/geos/bin/geos-config --with-projdir=/usr/local/proj/ --with-gdalconfig=/usr/local/gdal/bin/gdal-config >> /dev/null
make >> /dev/null && make install >> /dev/null && echo $? >>/tmp/xlwlogs/install.log

echo "signalway        hard    nofile          65535" >> /etc/security/limits.conf
echo "signalway        soft    nofile          65535" >> /etc/security/limits.conf

g=`egrep "^signalway" /etc/group |wc -l`
if [ $g == 0 ]
then
    groupadd signalway
fi

u=`egrep "^signalway" /etc/passwd |wc -l `
if [ $u == 0 ]
then
    useradd -d /home/signalway -g signalway signalway
fi

echo -e "\033[1;33m请设置postgresql的存储路径，默认为/data目录，如果使用默认，请输入1并回车；如果需要自定义，请输入路径： \033[0m"
read PG_DATA
if [ $PG_DATA = 1 ]
  then PG_DATA_HOME=/data/postgresql/data
  else PG_DATA_HOME=$PG_DATA/postgresql/data
fi

rm -rf $PG_DATA_HOME/*
mkdir -p $PG_DATA_HOME
chown -R signalway:signalway $PG_DATA_HOME
su - signalway -c "/usr/local/postgresql/bin/initdb -D $PG_DATA_HOME" >> /dev/null

echo "PATH=/usr/local/postgresql/bin:\$PATH" >> /home/signalway/.bashrc
echo "port = 5432" >> $PG_DATA_HOME/postgresql.conf
echo "listen_addresses = '*'" >> $PG_DATA_HOME/postgresql.conf

echo -e "\033[1;34m你的内网IP地址为: \033[0m \n\033[1;31m$neiwangIP \033[0m"
echo -e "\033[1;34m请确认是否正确，正确则输入1并回车；如果错误，请手动输入你的内网IP地址： \033[0m"
read ifconfig
if [ $ifconfig = 1 ]
  then ip=$ipsegment
  else ip=`echo $ifconfig >>/tmp/ip | awk '{print $2}' /tmp/ip | awk -F . '{print $1,$2,$3}' OFS="." /tmp/ip`
fi

rm -rf /tmp/ip

echo "host    all             all             $ip.0/0            md5" >> $PG_DATA_HOME/pg_hba.conf
chown -R signalway:signalway $PG_DATA_HOME

sed -i "s#PGDATA=/usr/local/postgresql/data#PGDATA="$PG_DATA_HOME"#" ${basepath}/postgresql
/bin/cp -f ${basepath}/postgresql /etc/init.d/postgresql
chmod +x /etc/init.d/postgresql
chkconfig postgresql on
echo -e "\033[1;34m启动postgresql \033[0m" >>/tmp/xlwlogs/install.log
/etc/init.d/postgresql start >>/tmp/xlwlogs/install.log

sleep 3
ps -ef |grep postgresql |grep -v grep >>/dev/null
if [ $? = 0 ]
  then
    echo -e "\033[1;33mpostgresql正常运行 \033[0m"
  else
    echo -e "\033[1;31mpostgresql启动失败 \033[0m"
fi

echo -e "\033[1;34mpostgresql安装完成 \033[0m"
echo -e "\033[1;34mpostgresql安装目录为：/usr/local/postgresql \033[0m" && echo -e "\033[1;34mpostgresql安装目录为：/usr/local/postgresql \033[0m" >>/tmp/xlwlogs/install.log
echo -e "\033[1;34mpostgresql存储目录为：$PG_DATA_HOME \033[0m" && echo -e "\033[1;34mpostgresql存储目录为：$PG_DATA_HOME \033[0m" >>/tmp/xlwlogs/install.log
echo -e "\033[1;34mpostgresql配置文件目录为：$PG_DATA_HOME \033[0m" && echo -e "\033[1;34mpostgresql存储目录为：$PG_DATA_HOME \033[0m" >>/tmp/xlwlogs/install.log

/etc/init.d/postgresql start
/usr/local/postgresql/bin/psql -U signalway -d postgres -c "ALTER USER signalway WITH PASSWORD '1234zxcv';"
```

