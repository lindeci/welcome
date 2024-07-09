- [学习资料](#学习资料)
- [总体架构](#总体架构)
- [安装部署](#安装部署)
- [配置文件介绍](#配置文件介绍)
  - [pg\_hba.conf 介绍](#pg_hbaconf-介绍)
    - [文件位置](#文件位置)
    - [配置格式](#配置格式)
      - [字段说明](#字段说明)
      - [示例配置](#示例配置)
    - [加载配置](#加载配置)
  - [pg\_ident.conf](#pg_identconf)
    - [文件位置](#文件位置-1)
    - [配置格式](#配置格式-1)
      - [字段说明](#字段说明-1)
      - [示例配置](#示例配置-1)
    - [在 pg\_hba.conf 中使用 pg\_ident.conf](#在-pg_hbaconf-中使用-pg_identconf)
    - [加载配置](#加载配置-1)
  - [postgresql.conf 介绍](#postgresqlconf-介绍)
- [重要参数介绍](#重要参数介绍)
  - [synchronous\_commit](#synchronous_commit)
  - [wal\_level](#wal_level)
  - [max\_wal\_size](#max_wal_size)
  - [min\_wal\_size](#min_wal_size)
  - [shared\_buffers](#shared_buffers)
  - [work\_mem](#work_mem)
  - [maintenance\_work\_mem](#maintenance_work_mem)
  - [wal\_buffers](#wal_buffers)
  - [effective\_cache\_size](#effective_cache_size)
  - [autovacuum](#autovacuum)
  - [log\_destination](#log_destination)
  - [log\_min\_duration\_statement](#log_min_duration_statement)
  - [max\_prepared\_transactions](#max_prepared_transactions)
  - [log\_statement](#log_statement)
  - [logging\_collector](#logging_collector)
  - [log\_directory](#log_directory)
  - [log\_filename](#log_filename)
- [WAL归档](#wal归档)
    - [WAL归档的工作原理](#wal归档的工作原理)
    - [配置WAL归档](#配置wal归档)
    - [参数说明](#参数说明)
    - [示例配置](#示例配置-2)
    - [使用场景](#使用场景)
    - [注意事项](#注意事项)
    - [归档恢复](#归档恢复)
- [常用的运维操作](#常用的运维操作)
  - [检查进程是否正常](#检查进程是否正常)
  - [监控PG错误日志](#监控pg错误日志)
  - [备份工具参数](#备份工具参数)
    - [使用示例](#使用示例)
      - [导出整个数据库集群](#导出整个数据库集群)
      - [仅导出全局对象（角色和表空间）](#仅导出全局对象角色和表空间)
      - [仅导出角色](#仅导出角色)
      - [仅导出表空间](#仅导出表空间)
      - [仅导出数据库模式（不包括数据）](#仅导出数据库模式不包括数据)
      - [使用特定字符编码导出](#使用特定字符编码导出)
    - [恢复](#恢复)
- [常用SQL](#常用sql)
  - [监控数据库大小](#监控数据库大小)
  - [监控当前所有PG查询](#监控当前所有pg查询)
  - [查询库所有索引清单](#查询库所有索引清单)
  - [查找PG集群中最大的数据库](#查找pg集群中最大的数据库)
  - [查找PG性能阻塞SQL](#查找pg性能阻塞sql)
  - [查找PG库中臃肿表](#查找pg库中臃肿表)
- [查找PG中臃肿索引](#查找pg中臃肿索引)
- [查找PG中的阻塞](#查找pg中的阻塞)
- [监控 PG磁盘 I/O 性能](#监控-pg磁盘-io-性能)
- [数据类型](#数据类型)
- [基本操作\&数据类型](#基本操作数据类型)
  - [单引号和双引号](#单引号和双引号)
  - [数据类型转换](#数据类型转换)
  - [布尔类型](#布尔类型)
  - [数值类型](#数值类型)
  - [浮点型](#浮点型)
  - [序列](#序列)
  - [数值的常见操作](#数值的常见操作)
  - [字符串类型](#字符串类型)
  - [日期类型](#日期类型)
  - [枚举类型](#枚举类型)
  - [IP类型](#ip类型)
  - [JSON\&JSONB类型](#jsonjsonb类型)
  - [复合类型](#复合类型)
  - [数组类型](#数组类型)
- [表](#表)
  - [约束](#约束)
  - [触发器](#触发器)
  - [表空间](#表空间)
  - [视图](#视图)
  - [索引](#索引)
  - [物化视图](#物化视图)
- [事务](#事务)
  - [事务的基本使用](#事务的基本使用)
  - [savepoint](#savepoint)
- [并发问题](#并发问题)
  - [事务的隔离级别](#事务的隔离级别)
  - [MVCC](#mvcc)
- [锁](#锁)
  - [表锁](#表锁)
  - [行锁](#行锁)
- [备份\&恢复](#备份恢复)
- [归档备份 介绍](#归档备份-介绍)
  - [逻辑备份\&恢复](#逻辑备份恢复)
  - [物理备份（归档+物理）](#物理备份归档物理)
  - [物理恢复（归档+物理）](#物理恢复归档物理)
  - [物理备份\&恢复（PITR-Point in time Recovery）](#物理备份恢复pitr-point-in-time-recovery)
- [十四、数据迁移](#十四数据迁移)
- [十五、主从操作](#十五主从操作)
  - [主从切换（不这么玩）](#主从切换不这么玩)
  - [主从故障切换](#主从故障切换)
- [复制槽管理](#复制槽管理)
- [逻辑复制介绍](#逻辑复制介绍)
  - [一、PostgreSQL的wal\_level=logic的简介](#一postgresql的wal_levellogic的简介)
  - [、PostgreSQL开启wal\_level=logic的步骤](#postgresql开启wal_levellogic的步骤)
  - [三、开启wal\_level=logical模式的优点](#三开启wal_levellogical模式的优点)
  - [四、开启wal\_level=logical模式的缺点](#四开启wal_levellogical模式的缺点)
- [问答](#问答)
    - [1. 检查点频率和活动量](#1-检查点频率和活动量)
    - [2. WAL 保留](#2-wal-保留)
    - [3. 归档日志](#3-归档日志)
    - [4. 恢复和备份](#4-恢复和备份)
    - [5. 延迟检查点](#5-延迟检查点)
    - [解决方案和建议](#解决方案和建议)
    - [示例](#示例)

# 学习资料
PostgreSQL 14.1 手册  
http://www.postgres.cn/docs/14/


# 总体架构
![新版本总体架构](https://miro.medium.com/v2/resize:fit:720/format:webp/0*3cqz7aAk5S_JgT48)
https://medium.com/@ahosanhabib.974/postgresql-16-3-single-instance-architecture-deployment-redhat-linux-9-3ee3ec0905cd

PostgreSQL 多进程架构和内存模型流程示意图
![总体架构](https://static001.geekbang.org/infoq/f7/f7bf66d5ecad6ccc78f3ee66c8d0aef0.png)

在 PostgreSQL 多进程架构体系中，最重要的两个进程是`守护进程（Postmaster）`与`服务进程（Postgres）`

除了守护进程的和服务进程外，PG 在运行期间还需要一些辅助进程，包括：

- Background writer：负责将共享缓冲池中的脏页逐渐刷入持久化存储中。
- Checkpointer：在 PG9.2 及其后版本中，该进程负责处理检查点。
- Autovacuum launcher：周期性地启动自动清理工作进程。
- WAL writer：本进程周期性地将 WAL 缓冲区中的 WAL 数据刷入持久存储中。
- Statistics Collector：负责收集统计信息，用于诸如 pg_stat_activity, pg_stat_database 等系统视图。
- Logging collector (logger)：负责将错误消息写入日志文件。
- Archiver：负责将日志归档。

在内存模型方面，PostgreSQL 的内存体系结构可以分为两大类：`本地内存区域（Local memory area）`和`共享内存区域（Shared memory area）`。


本地内存由每个后端服务进程分配供自己使用，当后端服务进程被 fork 时，每个后端服务进程为查询分配一个本地内存区域，由以下三部分组成：

- work_mem：执行器在执行 ORDER BY 和 DISTINCT 时使用该区域对元组做排序，以及存储归并连接和散列连接中的连接表。
- maintenance_work_mem：某些类型的维护操作使用该区域（例如 VACUUM、REINDEX）。
- temp_buffers：临时表相关操作使用这部分内存。


共享内存区域由 PostgreSQL 服务器在启动时分配，由所有后端进程共同使用。这个区域也被划分为几个固定大小的子区域，如下所示：

- Shared buffer pool：PostgreSQL 将表和索引中的页面从持久存储加载至此，并直接操作。
- WAL buffer：WAL 数据是 PostgreSQL 中的事务日志；WAL 缓冲区是 WAL 数据在写入持久存储之前的缓冲区。
- Commit log buffer：提交日志为并发控制（CC）机制保存了所需的所有事务状态（例如进行中、已提交、已中止等）。

# 安装部署
```
源码下载
wget https://ftp.postgresql.org/pub/source/v16.3/postgresql-16.3.tar.gz
tar xvf postgresql-16.3.tar.gz
cd postgresql-16.3
安装介绍在 INSTALL 文件中

./configure --prefix=/data/ldc_docker/postgresql-16.3/build --without-icu
make
make install
su postgres
bin/initdb -D data


常用插件
PostGIS 是一个 PostgreSQL 扩展，用于存储、索引和查询地理空间数据。它基于 GEOS，并提供了更丰富的地理空间功能。

查看 PostGIS 支持哪儿PG版本：https://postgis.net/docs/postgis_installation.html
查找关键字：It can be built against PostgreSQL versions

安装 PostGIS
先安装GEO
wget https://download.osgeo.org/geos/geos-3.11.4.tar.bz2
tar xvfj geos-3.11.4.tar.bz2
cd geos-3.11.4
mkdir _build
cd _build
# Set up the build
cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local/geos \
    ..
# Run the build, test, install
make -j 32
ctest
make install

安装 sqlite
wget https://www.sqlite.org/2024/sqlite-autoconf-3460000.tar.gz
tar xvf sqlite-autoconf-3460000.tar.gz 
cd sqlite-autoconf-3460000/
./configure --prefix=/usr/local/sqlite
make 
make -j 32
make install
sqlite3 --version

安装 proj
yum install libtiff-devel
yum install libcurl-devel
wget https://download.osgeo.org/proj/proj-9.4.0.tar.gz
tar xvf proj-9.4.0.tar.gz 
cd proj-9.4.0
mkdir build
cd build
cmake3 -DCMAKE_PREFIX_PATH=/usr/local/sqlite ..  -DCMAKE_INSTALL_PREFIX=/usr/local/proj
cmake3 --build . -j 32
cmake3 --build . --target install

安装 gdal
wget https://github.com/OSGeo/gdal/releases/download/v3.9.1/gdal-3.9.1.tar.gz


wget https://download.osgeo.org/postgis/source/postgis-3.4.2.tar.gz
tar xvf postgis-3.4.2.tar.gz
cd postgis-3.4.2
yum install libxml2 libxml2-devel -y
export LD_LIBRARY_PATH=/usr/local/geos/lib64:/usr/local/proj/lib64:$LD_LIBRARY_PATH
export CFLAGS="-I/usr/local/geos/include -I/usr/local/proj/include"
export LDFLAGS="-L/usr/local/geos/lib64 -L/usr/local/proj/lib64"
./configure --with-pgconfig=/data/ldc_docker/postgresql-16.3/build/bin/pg_config --with-geosconfig=/usr/local/geos/bin/geos-config --with-projdir=/usr/local/proj/ --with-libgeos-c=/usr/local/geos/lib64/ --with-gdalconfig=/usr/local/gdal/bin/gdal-config


启动 
postgres -D /usr/local/pgsql/data >logfile 2>&1 &
pg_ctl start -D /usr/local/pgsql/data -l serverlog

关闭
pg_ctl -D /data/pg/pgsql/13 stop
```

# 配置文件介绍
## pg_hba.conf 介绍
`pg_hba.conf` 是 PostgreSQL 数据库的主机基于身份验证（Host-Based Authentication, HBA）配置文件。这个文件控制着谁可以连接到数据库以及如何进行身份验证。

以下是对 `pg_hba.conf` 文件的详细介绍：

### 文件位置

默认情况下，`pg_hba.conf` 文件位于 PostgreSQL 数据目录中。你可以通过查询 PostgreSQL 数据库获取数据目录的位置：

```sql
SHOW data_directory;
```

### 配置格式

`pg_hba.conf` 文件由多行配置组成，每行配置一条规则。每条规则由以下字段组成：

```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
```

#### 字段说明

1. **TYPE**:
   - `local`: 本地连接（Unix域套接字）。
   - `host`: TCP/IP连接。
   - `hostssl`: 需要SSL的TCP/IP连接。
   - `hostnossl`: 不允许SSL的TCP/IP连接。

2. **DATABASE**:
   - 指定允许访问的数据库名，可以是具体数据库名、`all`（所有数据库）、`sameuser`（用户名与数据库名相同）、`samerole`（用户具有数据库角色）、`replication`（仅限复制连接）。

3. **USER**:
   - 指定允许访问的用户名，可以是具体用户名或 `all`（所有用户）。

4. **ADDRESS**:
   - 对于`host`类型，指定允许连接的客户端地址，可以是IP地址、子网或`all`（所有地址）。对于`local`类型，这个字段留空。

5. **METHOD**:
   - 指定身份验证方法，包括：
     - `trust`: 不需要密码。
     - `reject`: 拒绝连接。
     - `md5`: MD5加密密码验证。
     - `password`: 明文密码验证。
     - `gss`: GSSAPI认证。
     - `sspi`: SSPI认证。
     - `ident`: 通过操作系统用户认证。
     - `peer`: 同一操作系统用户。
     - `ldap`: 通过LDAP认证。
     - `radius`: 通过RADIUS认证。
     - `cert`: 通过SSL证书认证。
     - `pam`: 通过PAM认证。

#### 示例配置

以下是一些常见的配置示例：

1. 允许本地连接（通过Unix域套接字）：

   ```
   local   all             all                                     trust
   ```

2. 允许从特定IP地址访问所有数据库：

   ```
   host    all             all             192.168.1.0/24          md5
   ```

3. 允许从特定IP地址访问特定数据库：

   ```
   host    mydatabase      myuser          192.168.1.100/32        md5
   ```

4. 允许通过SSL连接：

   ```
   hostssl all             all             0.0.0.0/0               md5
   ```

5. 拒绝特定IP地址的连接：

   ```
   host    all             all             192.168.1.200/32        reject
   ```

### 加载配置

修改`pg_hba.conf`文件后，需要重新加载配置以使更改生效。你可以使用以下命令重新加载配置：

```sh
pg_ctl reload
```

或者在PostgreSQL命令行中执行：

```sql
SELECT pg_reload_conf();
```

`pg_hba.conf` 文件是PostgreSQL安全性的重要组成部分，合理配置可以有效控制数据库的访问权限，确保系统的安全性。

## pg_ident.conf
`pg_ident.conf` 是 PostgreSQL 用于用户映射的配置文件。当你使用某些认证方法（如 `ident` 和 `peer`）时，这个文件允许你将操作系统用户映射到数据库用户。

### 文件位置

默认情况下，`pg_ident.conf` 文件位于 PostgreSQL 数据目录中。你可以通过查询 PostgreSQL 数据库获取数据目录的位置：

```sql
SHOW data_directory;
```

### 配置格式

`pg_ident.conf` 文件由多行配置组成，每行配置一条规则。每条规则由以下字段组成：

```
# MAPNAME       SYSTEM-USERNAME        PG-USERNAME
```

#### 字段说明

1. **MAPNAME**:
   - 映射名称，用于在 `pg_hba.conf` 文件中引用。

2. **SYSTEM-USERNAME**:
   - 操作系统用户名（或远程用户的用户名）。也可以使用正则表达式。

3. **PG-USERNAME**:
   - PostgreSQL 数据库用户名。

#### 示例配置

以下是一些常见的配置示例：

1. 将操作系统用户 `os_user` 映射到 PostgreSQL 用户 `db_user`：

   ```
   mymap        os_user                 db_user
   ```

2. 将多个操作系统用户映射到不同的 PostgreSQL 用户：

   ```
   mymap        os_user1                db_user1
   mymap        os_user2                db_user2
   ```

3. 使用正则表达式将一组操作系统用户映射到相应的 PostgreSQL 用户：

   ```
   mymap        /^os_(.*)$/             db_\1
   ```

   这条规则会将操作系统用户 `os_john` 映射到 PostgreSQL 用户 `db_john`，将 `os_jane` 映射到 `db_jane`。

### 在 pg_hba.conf 中使用 pg_ident.conf

在 `pg_hba.conf` 文件中配置使用 `pg_ident.conf` 文件进行用户映射时，需要引用映射名称。例如：

```ini
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             127.0.0.1/32            ident map=mymap
local   all             all                                     peer map=mymap
```

在上面的例子中：

- 第一行配置表示，允许所有数据库的所有用户从 `127.0.0.1` 地址连接，使用 `ident` 认证方法，并通过映射名称 `mymap` 查找映射规则。
- 第二行配置表示，允许所有数据库的所有用户通过本地连接（Unix域套接字），使用 `peer` 认证方法，并通过映射名称 `mymap` 查找映射规则。

### 加载配置

修改 `pg_ident.conf` 文件后，需要重新加载配置以使更改生效。你可以使用以下命令重新加载配置：

```sh
pg_ctl reload
```

或者在 PostgreSQL 命令行中执行：

```sql
SELECT pg_reload_conf();
```

通过合理配置 `pg_ident.conf` 和 `pg_hba.conf`，你可以精细控制 PostgreSQL 数据库的访问权限，确保系统的安全性和灵活性。


## postgresql.conf 介绍
```sh
checkpoint_timeout = '30min'                    # 检查点完成前的最长等待时间为 30 分钟（修改需要重启数据库）
cluster_name = 'yace_pgsql'                     # 集群名称
datestyle = 'iso, ymd'                          # 日期样式设置为 "ISO, 年月日" 格式
default_text_search_config = 'pg_catalog.simple' # 全文搜索默认配置为 pg_catalog.simple
dynamic_shared_memory_type = 'posix'            # 动态共享内存类型，默认为 POSIX 共享内存
hot_standby = 'on'                              # 启用热备用
lc_messages = 'zh_CN.UTF8'                      # 系统错误消息的本地化设置为中文 UTF-8
lc_monetary = 'zh_CN.UTF8'                      # 货币格式化本地化设置为中文 UTF-8
lc_numeric = 'zh_CN.UTF8'                       # 数字格式化本地化设置为中文 UTF-8
lc_time = 'zh_CN.UTF8'                          # 时间格式化本地化设置为中文 UTF-8
listen_addresses = '0.0.0.0'                    # 监听所有IP地址
log_destination = 'csvlog'                      # 日志输出格式为 CSV 文件（修改需要重启数据库）
log_timezone = 'PRC'                            # 日志时区设置为中国标准时间（Asia/Shanghai）
logging_collector = 'on'                        # 启用日志收集器（修改需要重启数据库）
max_connections = '3000'                        # 允许的最大客户端连接数（修改需要重启数据库）
max_locks_per_transaction = '64'                # 每个事务的最大锁数
max_prepared_transactions = '0'                 # 最大预准备事务数
max_replication_slots = '8'                     # 最大复制槽数
max_wal_senders = '8'                           # 最大WAL发送者数
max_worker_processes = '16'                     # 最大工作进程数

pg_stat_log.max = '1024'                        # pg_stat_log 中保留的最大日志条目数量
pg_stat_log.track = 'all'                       # 跟踪所有查询的日志记录
pg_stat_log.track_utility = 'true'              # 跟踪系统命令的日志记录
pg_stat_statements.max = '1000'                 # pg_stat_statements 中保留的最大 SQL 语句数量
pg_stat_statements.track = 'all'                # 对所有语句进行跟踪统计

port = '5432'                                   # 监听端口号（修改需要重启数据库）
synchronous_commit = 'on'                       # 启用同步提交
synchronous_standby_names = 'pg03'              # 同步备用名称
timezone = 'PRC'                                # 时区设置为中国标准时间（Asia/Shanghai）
track_commit_timestamp = 'off'                  # 是否追踪提交时间戳
wal_compression = 'on'                          # 启用 WAL 日志压缩
wal_keep_size = '128MB'                         # 保留用于流复制的 WAL 日志大小为 128MB
wal_level = 'logical'                           # WAL级别，设置为逻辑复制
wal_log_hints = 'on'                            # 启用 WAL 日志提示
hba_file = '/data/pgsql/13/data/pg_hba.conf'    # HBA 配置文件的位置
ident_file = '/data/pgsql/13/data/pg_ident.conf'# ident 配置文件的位置

# recovery.conf
recovery_target = ''                            # 设置恢复的目标
recovery_target_lsn = ''                        # 设置恢复的目标 LSN
recovery_target_name = ''                       # 设置恢复的目标名称
recovery_target_time = ''                       # 设置恢复的目标时间点
recovery_target_timeline = 'latest'             # 恢复时使用最新的时间线
recovery_target_xid = ''                        # 设置恢复的目标 XID

```

# 重要参数介绍

## synchronous_commit

`synchronous_commit` 参数控制着事务提交时的同步行为。它影响的是在事务提交后，PostgreSQL 会等待多长时间来确认事务的持久性，即数据已成功写入磁盘。

- **取值**：
  - `on`：默认值。事务在提交时，会等待将WAL记录同步到磁盘和所有的同步复制节点确认收到这些记录后，才返回成功。
  - `remote_apply`：事务在提交时，会等待将WAL记录同步到磁盘并且至少一个同步复制节点将这些记录应用到数据库中，才返回成功。
  - `remote_write`：事务在提交时，会等待将WAL记录同步到磁盘和至少一个同步复制节点将这些记录写入WAL日志后，才返回成功。
  - `local`：事务在提交时，只会等待将WAL记录同步到本地磁盘后，才返回成功，而不等待同步复制节点确认。
  - `off`：事务在提交时，不等待WAL记录同步到磁盘，立即返回成功。这种情况下，虽然性能提高，但可能在系统崩溃时导致数据丢失。

- **示例**：

  ```ini
  synchronous_commit = 'on'     # 默认值，事务在提交时会等待WAL记录同步到磁盘和同步复制节点确认
  ```

- **应用场景**：
  - **高一致性需求**：如果系统对数据一致性要求很高，应该使用 `on` 或 `remote_apply`。
  - **性能优先**：如果系统对性能要求高而能容忍少量数据丢失，可以使用 `local` 或 `off`。

## wal_level

`wal_level` 参数决定了WAL（Write-Ahead Logging）记录的详细程度以及是否启用某些功能（如归档、复制）。

- **取值**：
  - `minimal`：最小日志级别，只记录必要的WAL信息。这种模式下不支持流复制和归档。
  - `replica`：默认值，记录足够的WAL信息以支持流复制和基础备份，但不支持逻辑复制。
  - `logical`：记录所有必要的WAL信息以支持逻辑复制和流复制。这种模式下，可以实现更高级的复制功能，如逻辑解码和逻辑复制。

- **示例**：

  ```ini
  wal_level = 'logical'     # 设置WAL级别为逻辑复制，支持流复制和逻辑复制
  ```

- **应用场景**：
  - **归档和备份**：如果需要归档和备份日志，至少需要设置为 `replica`。
  - **流复制**：如果需要实现流复制功能，也至少需要设置为 `replica`。
  - **逻辑复制**：如果需要实现逻辑复制和更复杂的复制功能，则需要设置为 `logical`。

## max_wal_size

含义：max_wal_size 指定了WAL文件的最大大小。当WAL文件的总大小达到这个阈值时，PostgreSQL 将触发一个检查点，以减少WAL文件的数量。

作用：

    增大 max_wal_size 可以减少检查点的频率，适用于有大量写操作的系统，有助于提高写操作的性能，但会增加恢复时间。
    减小 max_wal_size 会增加检查点的频率，有助于减少恢复时间，但可能会影响写操作的性能。

## min_wal_size

含义：min_wal_size 指定了WAL文件的最小大小。当WAL文件的总大小减少到这个阈值以下时，PostgreSQL 将不会删除旧的WAL文件，以确保在高峰写操作期间有足够的WAL文件可用。

作用：

    增大 min_wal_size 可以减少频繁删除和创建WAL文件的开销，有助于提高系统性能。
    减小 min_wal_size 可以减少WAL文件占用的磁盘空间，但可能会增加频繁删除和创建WAL文件的开销，影响性能。

## shared_buffers
控制PostgreSQL使用的共享内存缓冲区大小。

## work_mem
每个排序操作和哈希表使用的内存量

## maintenance_work_mem
用于维护操作（如VACUUM、CREATE INDEX）的内存量

## wal_buffers
为WAL数据分配的共享内存

## effective_cache_size
数据库可以使用的操作系统缓存大小

## autovacuum
控制自动垃圾回收的行为

## log_destination
日志文件的输出目的地

## log_min_duration_statement
记录超过指定时间的SQL语句
```
log_min_duration_statement = 500ms
```

## max_prepared_transactions
允许的最大预准备事务数

## log_statement
含义：记录哪些SQL语句。  
默认值：none  
示例：log_statement = 'all'

## logging_collector

    含义：启用日志收集器进程，将日志写入文件。
    默认值：off
    示例：logging_collector = on

## log_directory

    含义：日志文件存放的目录。
    默认值：pg_log
    示例：log_directory = 'pg_log'

## log_filename

    含义：日志文件的命名模式。
    默认值：postgresql-%Y-%m-%d_%H%M%S.log
    示例：log_filename = 'postgresql-%Y-%m-%d.log'

性能优化相关参数

    shared_buffers
        含义：PostgreSQL 使用的共享内存缓冲区的大小。
        默认值：128MB
        示例：shared_buffers = 1GB

    work_mem
        含义：每个排序和哈希操作使用的内存大小。
        默认值：4MB
        示例：work_mem = 64MB

    maintenance_work_mem
        含义：维护操作（如VACUUM、CREATE INDEX等）使用的内存大小。
        默认值：64MB
        示例：maintenance_work_mem = 512MB

    effective_cache_size
        含义：用于估计操作系统文件系统缓存的大小，影响查询规划器的选择。
        默认值：4GB
        示例：effective_cache_size = 4GB

WAL配置相关参数

    wal_level
        含义：设置写前日志（WAL）的级别。
        默认值：replica
        示例：wal_level = logical

    checkpoint_completion_target
        含义：检查点过程的完成目标，范围为0到1，表示检查点周期的百分比。
        默认值：0.5
        示例：checkpoint_completion_target = 0.9

    checkpoint_timeout
        含义：两次检查点之间的时间间隔。
        默认值：5min
        示例：checkpoint_timeout = 15min

连接和会话管理参数

    max_connections
        含义：允许的最大客户端连接数。
        默认值：100
        示例：max_connections = 300

    superuser_reserved_connections
        含义：保留给超级用户的连接数量。
        默认值：3
        示例：superuser_reserved_connections = 3

日志和监控相关参数

    logging_collector
        含义：启用日志收集器进程，将日志写入文件。
        默认值：off
        示例：logging_collector = on

    log_directory
        含义：日志文件存放的目录。
        默认值：pg_log
        示例：log_directory = 'pg_log'

    log_filename
        含义：日志文件的命名模式。
        默认值：postgresql-%Y-%m-%d_%H%M%S.log
        示例：log_filename = 'postgresql-%Y-%m-%d.log'

    log_statement
        含义：记录哪些SQL语句。
        默认值：none
        示例：log_statement = 'all'

安全相关参数

    password_encryption
        含义：启用密码加密。
        默认值：md5
        示例：password_encryption = scram-sha-256

    ssl
        含义：启用SSL连接。
        默认值：off
        示例：ssl = on

其他重要参数

    datestyle
        含义：日期和时间的显示格式。
        默认值：ISO, MDY
        示例：datestyle = 'ISO, DMY'

    timezone
        含义：设置时区。
        默认值：系统时区
        示例：timezone = 'UTC'

    lc_messages
        含义：设置系统错误消息的本地化。
        默认值：C
        示例：lc_messages = 'en_US.UTF-8'

    autovacuum
        含义：启用自动VACUUM。
        默认值：on
        示例：autovacuum = on

# WAL归档
在 PostgreSQL 中，WAL（Write-Ahead Logging）归档是一种数据保护机制，通过它可以将写前日志（WAL）文件复制到安全存储位置，以便在发生数据损坏或其他故障时进行数据恢复。WAL归档可以用于构建备份和灾难恢复系统，确保数据库的高可用性和数据完整性。

### WAL归档的工作原理

WAL归档的基本思想是将生成的WAL文件保存到一个安全的地方。每当一个WAL文件被填满或达到一定的时间间隔时，PostgreSQL 会调用一个用户定义的命令，将这个WAL文件复制到一个归档位置。

### 配置WAL归档

要启用WAL归档，需要在 `postgresql.conf` 中设置以下参数：

1. **archive_mode**：启用WAL归档。
2. **archive_command**：指定用于复制WAL文件的命令。

### 参数说明

- **archive_mode**
  - 含义：启用或禁用WAL归档。
  - 可能的值：`on`, `off`
  - 示例：`archive_mode = on`

- **archive_command**
  - 含义：指定归档命令。这个命令将在每个WAL文件准备好归档时执行。`%p` 是源文件路径，`%f` 是文件名。
  - 示例：`archive_command = 'cp %p /path/to/archive/%f'`

### 示例配置

```ini
# 启用WAL归档
archive_mode = on

# 归档命令，将WAL文件复制到 /mnt/server/archivedir 目录
archive_command = 'test ! -f /mnt/server/archivedir/%f && cp %p /mnt/server/archivedir/%f'
```

### 使用场景

1. **备份和恢复**：
   - 在设置了WAL归档后，你可以使用这些归档的WAL文件来恢复数据库到特定的时间点（时间点恢复，PITR）。

2. **灾难恢复**：
   - 如果数据库崩溃或数据文件损坏，可以使用备份的基础数据文件和归档的WAL文件进行恢复。

3. **高可用性**：
   - 可以通过归档WAL文件并将它们传输到备用服务器上，以实现数据库的热备份或冷备份，提高系统的高可用性。

### 注意事项

1. **存储空间**：
   - 确保归档位置有足够的存储空间来保存所有归档的WAL文件，否则可能会导致数据库写入操作被阻塞。

2. **归档命令的可靠性**：
   - `archive_command` 必须是一个可靠的命令，如果命令失败，WAL文件将无法归档，可能会影响数据库的正常运行。

3. **性能影响**：
   - 启用归档会对数据库性能有一定的影响，特别是在归档命令较慢或归档频率较高的情况下。

### 归档恢复

要使用归档的WAL文件进行恢复，你需要将这些文件复制回 `pg_wal` 目录，并在恢复配置中指定 `restore_command`。例如：

```ini
restore_command = 'cp /path/to/archive/%f %p'
```

然后启动数据库恢复过程，PostgreSQL 会按顺序应用这些WAL文件，以恢复数据库到最近的状态。

通过正确配置和使用WAL归档，您可以显著提高PostgreSQL数据库的可靠性和数据安全性。

# 常用的运维操作

## 检查进程是否正常
```
-- 单实例
pgrep -u postgres -fa -- -D
返回
8947 /data/ldc_docker/postgresql-16.3/build/bin/postgres -D ../data

-- 多实例
pgrep -fa -- -D |grep postgres
```
## 监控PG错误日志
```
-- 首先配置postgresql.conf文件，在文件ERROR REPORTING AND LOGGING 部分添加如下参数
log_destination = 'stderr' 
logging_collector = on 
log_directory = 'pg_log' 
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log' 
log_truncate_on_rotation = off 
log_rotation_age = 1d 
log_min_duration_statement = 0 
log_connections = on 
log_duration = on 
log_hostname = on 
log_timezone = 'UTC'

-- 然后生效保存 postgresql.conf，并重启PG服务
```
## 备份工具参数
`pg_dumpall` 是 PostgreSQL 提供的一个工具，用于导出整个数据库集群，包括所有的数据库和相关的元数据。它生成一个SQL脚本文件，该文件可以用 `psql` 命令重新导入，从而恢复整个数据库集群。
```
### 重要参数

以下是一些 `pg_dumpall` 常用和重要的参数及其说明：

1. **-f, --file=FILENAME**
   - **说明**：将输出写入指定文件。如果不指定文件，输出将写到标准输出。
   - **示例**：`pg_dumpall -f all_databases.sql`

2. **-h, --host=HOSTNAME**
   - **说明**：连接到指定主机上的数据库服务器。如果不指定，默认为本地主机。
   - **示例**：`pg_dumpall -h dbserver.example.com`

3. **-p, --port=PORT**
   - **说明**：连接到指定端口上的数据库服务器。如果不指定，默认为 5432。
   - **示例**：`pg_dumpall -p 5432`

4. **-U, --username=USERNAME**
   - **说明**：以指定的用户名连接数据库服务器。
   - **示例**：`pg_dumpall -U postgres`

5. **-w, --no-password**
   - **说明**：不提示输入密码。如果服务器要求密码且未提供密码，则连接将失败。
   - **示例**：`pg_dumpall -w`

6. **-W, --password**
   - **说明**：强制提示输入密码。
   - **示例**：`pg_dumpall -W`

7. **-g, --globals-only**
   - **说明**：仅转储全局对象（例如，角色和表空间），不包括任何数据库。
   - **示例**：`pg_dumpall -g`

8. **-r, --roles-only**
   - **说明**：仅转储角色（用户和组）。
   - **示例**：`pg_dumpall -r`

9. **-t, --tablespaces-only**
   - **说明**：仅转储表空间。
   - **示例**：`pg_dumpall -t`

10. **-s, --schema-only**
    - **说明**：仅转储数据库模式（不包括数据）。
    - **示例**：`pg_dumpall -s`

11. **-v, --verbose**
    - **说明**：生成详细输出，显示进度消息。
    - **示例**：`pg_dumpall -v`

12. **-E, --encoding=ENCODING**
    - **说明**：以指定的字符编码进行转储。
    - **示例**：`pg_dumpall -E UTF8`

13. **-l, --no-privileges**
    - **说明**：不要转储授予/撤销权限。
    - **示例**：`pg_dumpall -l`

14. **--column-inserts**
    - **说明**：生成列名显式指定的INSERT命令，这对依赖列顺序的重排非常有用。
    - **示例**：`pg_dumpall --column-inserts`

15. **--if-exists**
    - **说明**：在删除命令中使用 IF EXISTS，这样删除不存在的对象时不会出错。
    - **示例**：`pg_dumpall --if-exists`
```
### 使用示例

以下是一些 `pg_dumpall` 的使用示例：

#### 导出整个数据库集群

```sh
pg_dumpall -U postgres -f all_databases.sql
```

#### 仅导出全局对象（角色和表空间）

```sh
pg_dumpall -U postgres -g -f globals.sql
```

#### 仅导出角色

```sh
pg_dumpall -U postgres -r -f roles.sql
```

#### 仅导出表空间

```sh
pg_dumpall -U postgres -t -f tablespaces.sql
```

#### 仅导出数据库模式（不包括数据）

```sh
pg_dumpall -U postgres -s -f schema.sql
```

#### 使用特定字符编码导出

```sh
pg_dumpall -U postgres -E UTF8 -f all_databases_utf8.sql
```

### 恢复

使用 `psql` 工具可以恢复由 `pg_dumpall` 生成的转储文件：

```sh
psql -U postgres -f all_databases.sql
```

通过正确使用 `pg_dumpall` 的这些参数，可以灵活地导出和备份整个PostgreSQL数据库集群或其特定部分。

# 常用SQL
## 监控数据库大小
```sql
SELECT datname,
         pg_size_pretty(pg_database_size(datname))
FROM pg_database
ORDER BY  pg_database_size(datname);

  datname  | pg_size_pretty 
-----------+----------------
 template0 | 7305 kB
 postgres  | 7460 kB
 template1 | 7532 kB
```
## 监控当前所有PG查询
```sql
SELECT pid,
         age(clock_timestamp(),
         query_start),
         usename,
         query
FROM pg_stat_activity
WHERE query != '<IDLE>'
        AND query NOT ILIKE '%pg_stat_activity%'
ORDER BY  query_start desc;

 pid  | age | usename  | query 
------+-----+----------+-------
 8952 |     |          | 
 8953 |     | postgres | 
 8949 |     |          | 
 8948 |     |          | 
 8951 |     |          | 
```
## 查询库所有索引清单
```sql
SELECT t.relname AS table_name,
         i.relname AS index_name,
         string_agg(a.attname,
         ',') AS column_name
FROM pg_class t, pg_class i, pg_index ix, pg_attribute a
WHERE t.oid = ix.indrelid
        AND i.oid = ix.indexrelid
        AND a.attrelid = t.oid
        AND a.attnum = ANY(ix.indkey)
        AND t.relkind = 'r'
        AND t.relname NOT LIKE 'pg_%'
GROUP BY  t.relname, i.relname
ORDER BY  t.relname, i.relname;

 table_name | index_name | column_name 
------------+------------+-------------
```

## 查找PG集群中最大的数据库
```sql
SELECT d.datname AS Name,
         pg_catalog.pg_get_userbyid(d.datdba) AS Owner,     
    CASE
    WHEN pg_catalog.has_database_privilege(d.datname, 'CONNECT') THEN
    pg_catalog.pg_size_pretty(pg_catalog.pg_database_size(d.datname))
    ELSE 'No Access'
    END AS Size
FROM pg_catalog.pg_database d
ORDER BY 
    CASE
    WHEN pg_catalog.has_database_privilege(d.datname, 'CONNECT') THEN
    pg_catalog.pg_database_size(d.datname)
    ELSE NULL
    END DESC -- nulls first LIMIT 20
;

   name    |  owner   |  size   
-----------+----------+---------
 template1 | postgres | 7532 kB
 postgres  | postgres | 7460 kB
 template0 | postgres | 7305 kB
```

## 查找PG性能阻塞SQL
这段 SQL 语句通过递归公用表表达式（CTE）来构建锁等待图，并结合 pg_stat_activity 来显示锁等待链的详细信息，包括事务持续时间、状态、用户、客户端地址和阻塞的查询。
```sql
WITH RECURSIVE l AS (
    SELECT 
        pid,
        locktype,
        mode,
        granted,
        ROW(locktype, database, relation, page, tuple, virtualxid, transactionid, classid, objid, objsubid) obj
    FROM 
        pg_locks
),
pairs AS (
    SELECT 
        w.pid waiter,
        l.pid locker,
        l.obj,
        l.mode
    FROM 
        l w
    JOIN 
        l
        ON l.obj IS NOT DISTINCT
        FROM w.obj
        AND l.locktype = w.locktype
        AND NOT l.pid = w.pid
        AND l.granted
    WHERE 
        NOT w.granted
),
tree AS (
    SELECT 
        l.locker pid,
        l.locker root,
        NULL::record obj,
        NULL AS mode,
        0 lvl,
        locker::text path,
        array_agg(l.locker) OVER () all_pids
    FROM 
        (SELECT DISTINCT locker
        FROM pairs l
        WHERE NOT EXISTS 
            (SELECT 1
            FROM pairs
            WHERE waiter = l.locker)
        ) l
    UNION ALL
    SELECT 
        w.waiter pid,
        tree.root,
        w.obj,
        w.mode,
        tree.lvl + 1,
        tree.path || '.' || w.waiter, 
        all_pids || array_agg(w.waiter) OVER ()
    FROM 
        tree
    JOIN 
        pairs w
        ON tree.pid = w.locker
        AND NOT w.waiter = ANY (all_pids)
)
SELECT 
    (clock_timestamp() - a.xact_start)::interval(3) AS ts_age,
    replace(a.state, 'idle in transaction', 'idletx') state, 
    (clock_timestamp() - state_change)::interval(3) AS change_age, 
    a.datname, 
    tree.pid,
    a.usename,
    a.client_addr,
    lvl, 
    (SELECT count(*)
    FROM tree p
    WHERE p.path ~ ('^' || tree.path)
    AND NOT p.path = tree.path) blocked, 
    repeat(' .', lvl) || ' ' || left(regexp_replace(query, '\s+', ' ', 'g'), 100) query
FROM 
    tree
JOIN 
    pg_stat_activity a
USING (pid)
ORDER BY path;

 ts_age | state | change_age | datname | pid | usename | client_addr | lvl | blocked | query 
--------+-------+------------+---------+-----+---------+-------------+-----+---------+-------
```

## 查找PG库中臃肿表
```sql
WITH constants AS (
    -- Define some constants for sizes of things for reference down the query
    SELECT current_setting('block_size')::numeric AS bs,
           23 AS hdr,
           8 AS ma
),
no_stats AS (
    -- Screen out tables which have attributes without stats, such as JSON
    SELECT table_schema,
           table_name,
           n_live_tup::numeric AS est_rows,
           pg_table_size(relid)::numeric AS table_size
    FROM information_schema.columns
    JOIN pg_stat_user_tables AS psut
    ON table_schema = psut.schemaname
    AND table_name = psut.relname
    LEFT OUTER JOIN pg_stats
    ON table_schema = pg_stats.schemaname
    AND table_name = pg_stats.tablename
    AND column_name = attname
    WHERE attname IS NULL
    AND table_schema NOT IN ('pg_catalog', 'information_schema')
    GROUP BY table_schema, table_name, relid, n_live_tup
),
null_headers AS (
    -- Calculate NULL header sizes, omitting tables which don't have complete stats
    -- and attributes which aren't visible
    SELECT hdr + 1 + (sum(case when null_frac <> 0 THEN 1 else 0 END)/8) as nullhdr,
           SUM((1 - null_frac) * avg_width) as datawidth,
           MAX(null_frac) as maxfracsum,
           schemaname,
           tablename,
           hdr,
           ma,
           bs
    FROM pg_stats
    CROSS JOIN constants
    LEFT OUTER JOIN no_stats
    ON schemaname = no_stats.table_schema
    AND tablename = no_stats.table_name
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    AND no_stats.table_name IS NULL
    AND EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE schemaname = columns.table_schema
        AND tablename = columns.table_name
    )
    GROUP BY schemaname, tablename, hdr, ma, bs
),
data_headers AS (
    -- Estimate header and row size
    SELECT ma,
           bs,
           hdr,
           schemaname,
           tablename,
           (datawidth + (hdr + ma - (case when hdr % ma = 0 THEN ma ELSE hdr % ma END)))::numeric AS datahdr,
           (maxfracsum * (nullhdr + ma - (case when nullhdr % ma = 0 THEN ma ELSE nullhdr % ma END))) AS nullhdr2
    FROM null_headers
),
table_estimates AS (
    -- Make estimates of how large the table should be based on row and page size
    SELECT schemaname,
           tablename,
           bs,
           reltuples::numeric as est_rows,
           relpages * bs as table_bytes,
           CEIL((reltuples * (datahdr + nullhdr2 + 4 + ma - (CASE WHEN datahdr % ma = 0 THEN ma ELSE datahdr % ma END)) / (bs - 20))) * bs AS expected_bytes,
           reltoastrelid
    FROM data_headers
    JOIN pg_class
    ON tablename = relname
    JOIN pg_namespace
    ON relnamespace = pg_namespace.oid
    AND schemaname = nspname
    WHERE pg_class.relkind = 'r'
),
estimates_with_toast AS (
    -- Add in estimated TOAST table sizes, estimate based on 4 toast tuples per page because we don't have anything better.
    SELECT schemaname,
           tablename,
           TRUE as can_estimate,
           est_rows,
           table_bytes + (coalesce(toast.relpages, 0) * bs) as table_bytes,
           expected_bytes + (ceil(coalesce(toast.reltuples, 0) / 4) * bs) as expected_bytes
    FROM table_estimates
    LEFT OUTER JOIN pg_class as toast
    ON table_estimates.reltoastrelid = toast.oid
    AND toast.relkind = 't'
),
table_estimates_plus AS (
    -- Add some extra metadata to the table data and calculations to be reused, including whether we can estimate it or whether we think it might be compressed
    SELECT current_database() as databasename,
           schemaname,
           tablename,
           can_estimate,
           est_rows,
           CASE WHEN table_bytes > 0 THEN table_bytes::NUMERIC ELSE NULL::NUMERIC END AS table_bytes,
           CASE WHEN expected_bytes > 0 THEN expected_bytes::NUMERIC ELSE NULL::NUMERIC END AS expected_bytes,
           CASE WHEN expected_bytes > 0 AND table_bytes > 0 AND expected_bytes <= table_bytes THEN (table_bytes - expected_bytes)::NUMERIC ELSE 0::NUMERIC END AS bloat_bytes
    FROM estimates_with_toast
    UNION ALL
    SELECT current_database() as databasename,
           table_schema,
           table_name,
           FALSE,
           est_rows,
           table_size,
           NULL::NUMERIC,
           NULL::NUMERIC
    FROM no_stats
),
bloat_data AS (
    -- Do final math calculations and formatting
    SELECT current_database() as databasename,
           schemaname,
           tablename,
           can_estimate,
           table_bytes,
           round(table_bytes / (1024^2)::NUMERIC, 3) as table_mb,
           expected_bytes,
           round(expected_bytes / (1024^2)::NUMERIC, 3) as expected_mb,
           round(bloat_bytes * 100 / table_bytes) as pct_bloat,
           round(bloat_bytes / (1024::NUMERIC^2), 2) as mb_bloat,
           table_bytes,
           expected_bytes,
           est_rows
    FROM table_estimates_plus
)
-- Filter output for bloated tables
SELECT databasename,
       schemaname,
       tablename,
       can_estimate,
       est_rows,
       pct_bloat,
       mb_bloat,
       table_mb
FROM bloat_data
-- This where clause defines which tables actually appear in the bloat chart
-- Example below filters for tables which are either 50% bloated and more than 20MB in size, or more than 25% bloated and more than 4GB in size
WHERE (pct_bloat >= 50 AND mb_bloat >= 20) OR (pct_bloat >= 25 AND mb_bloat >= 1024)
ORDER BY pct_bloat DESC;


 databasename | schemaname | tablename | can_estimate | est_rows | pct_bloat | mb_bloat | table_mb 
--------------+------------+-----------+--------------+----------+-----------+----------+----------
```
# 查找PG中臃肿索引
```sql
WITH btree_index_atts AS (
    SELECT 
        nspname,
        indexclass.relname AS index_name,
        indexclass.reltuples,
        indexclass.relpages,
        indrelid,
        indexrelid,
        indexclass.relam,
        tableclass.relname AS tablename,
        regexp_split_to_table(indkey::text, ' ')::smallint AS attnum,
        indexrelid AS index_oid
    FROM pg_index
    JOIN pg_class AS indexclass ON pg_index.indexrelid = indexclass.oid
    JOIN pg_class AS tableclass ON pg_index.indrelid = tableclass.oid
    JOIN pg_namespace ON pg_namespace.oid = indexclass.relnamespace
    JOIN pg_am ON indexclass.relam = pg_am.oid
    WHERE pg_am.amname = 'btree'
        AND indexclass.relpages > 0
        AND nspname NOT IN ('pg_catalog','information_schema')
),
index_item_sizes AS (
    SELECT 
        ind_atts.nspname,
        ind_atts.index_name,
        ind_atts.reltuples,
        ind_atts.relpages,
        ind_atts.relam,
        indrelid AS table_oid,
        index_oid,
        current_setting('block_size')::numeric AS bs,
        8 AS maxalign,
        24 AS pagehdr,
        CASE
            WHEN max(coalesce(pg_stats.null_frac, 0)) = 0 THEN 2
            ELSE 6
        END AS index_tuple_hdr,
        sum((1 - coalesce(pg_stats.null_frac, 0)) * coalesce(pg_stats.avg_width, 1024)) AS nulldatawidth
    FROM pg_attribute
    JOIN btree_index_atts AS ind_atts ON pg_attribute.attrelid = ind_atts.indexrelid AND pg_attribute.attnum = ind_atts.attnum
    JOIN pg_stats ON pg_stats.schemaname = ind_atts.nspname
        AND ((pg_stats.tablename = ind_atts.tablename AND pg_stats.attname = pg_catalog.pg_get_indexdef(pg_attribute.attrelid, pg_attribute.attnum, TRUE))
        OR (pg_stats.tablename = ind_atts.index_name AND pg_stats.attname = pg_attribute.attname))
    WHERE pg_attribute.attnum > 0
    GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9
),
index_aligned_est AS (
    SELECT 
        maxalign,
        bs,
        nspname,
        index_name,
        reltuples,
        relpages,
        relam,
        table_oid,
        index_oid,
        coalesce(
            ceil(
                reltuples * (
                    6 + maxalign - CASE
                        WHEN index_tuple_hdr % maxalign = 0 THEN maxalign
                        ELSE index_tuple_hdr % maxalign
                    END + nulldatawidth + maxalign - CASE
                        WHEN nulldatawidth::integer % maxalign = 0 THEN maxalign
                        ELSE nulldatawidth::integer % maxalign
                    END
                )::numeric / (bs - pagehdr::NUMERIC) + 1
            ),
            0
        ) AS expected
    FROM index_item_sizes
),
raw_bloat AS (
    SELECT 
        current_database() AS dbname,
        nspname,
        pg_class.relname AS table_name,
        index_name,
        bs * index_aligned_est.relpages::bigint AS totalbytes,
        expected,
        CASE
            WHEN index_aligned_est.relpages <= expected THEN 0
            ELSE bs * (index_aligned_est.relpages - expected)::bigint
        END AS wastedbytes,
        CASE
            WHEN index_aligned_est.relpages <= expected THEN 0
            ELSE bs * (index_aligned_est.relpages - expected)::bigint * 100 / (bs * index_aligned_est.relpages::bigint)
        END AS realbloat,
        pg_relation_size(index_aligned_est.table_oid) AS table_bytes,
        stat.idx_scan AS index_scans
    FROM index_aligned_est
    JOIN pg_class ON pg_class.oid = index_aligned_est.table_oid
    JOIN pg_stat_user_indexes AS stat ON index_aligned_est.index_oid = stat.indexrelid
),
format_bloat AS (
    SELECT 
        dbname AS database_name,
        nspname AS schema_name,
        table_name,
        index_name,
        round(realbloat) AS bloat_pct,
        round(wastedbytes / (1024^2)::NUMERIC) AS bloat_mb,
        round(totalbytes / (1024^2)::NUMERIC, 3) AS index_mb,
        round(table_bytes / (1024^2)::NUMERIC, 3) AS table_mb,
        index_scans
    FROM raw_bloat
)
-- Final query outputting the bloated indexes
SELECT 
    *
FROM format_bloat
WHERE (bloat_pct > 50 AND bloat_mb > 10)
ORDER BY bloat_mb DESC;

 database_name | schema_name | table_name | index_name | bloat_pct | bloat_mb | index_mb | table_mb | index_scans 
---------------+-------------+------------+------------+-----------+----------+----------+----------+-------------
```

# 查找PG中的阻塞
```sql
SELECT blocked_locks.pid AS blocked_pid,
         blocked_activity.usename AS blocked_user,
         blocking_locks.pid AS blocking_pid,
         blocking_activity.usename AS blocking_user,
         blocked_activity.query AS blocked_statement,
         blocking_activity.query AS current_statement_in_blocking_process
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity
    ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
        AND blocking_locks.database IS NOT DISTINCT
FROM blocked_locks.database
        AND blocking_locks.relation IS NOT DISTINCT
FROM blocked_locks.relation
        AND blocking_locks.page IS NOT DISTINCT
FROM blocked_locks.page
        AND blocking_locks.tuple IS NOT DISTINCT
FROM blocked_locks.tuple
        AND blocking_locks.virtualxid IS NOT DISTINCT
FROM blocked_locks.virtualxid
        AND blocking_locks.transactionid IS NOT DISTINCT
FROM blocked_locks.transactionid
        AND blocking_locks.classid IS NOT DISTINCT
FROM blocked_locks.classid
        AND blocking_locks.objid IS NOT DISTINCT
FROM blocked_locks.objid
        AND blocking_locks.objsubid IS NOT DISTINCT
FROM blocked_locks.objsubid
        AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity
    ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

 blocked_pid | blocked_user | blocking_pid | blocking_user | blocked_statement | current_statement_in_blocking_process 
-------------+--------------+--------------+---------------+-------------------+---------------------------------------
```

# 监控 PG磁盘 I/O 性能
```sql
-- Perform a "SELECT pg_stat_reset();" when you want to reset counter statistics
WITH all_tables AS (
    SELECT
        'all'::text AS table_name,
        sum((
            coalesce(heap_blks_read, 0) +
            coalesce(idx_blks_read, 0) +
            coalesce(toast_blks_read, 0) +
            coalesce(tidx_blks_read, 0)
        )) AS from_disk,
        sum((
            coalesce(heap_blks_hit, 0) +
            coalesce(idx_blks_hit, 0) +
            coalesce(toast_blks_hit, 0) +
            coalesce(tidx_blks_hit, 0)
        )) AS from_cache
    FROM pg_statio_all_tables
    -- Change to pg_statio_user_tables if you want to check only user tables (excluding PostgreSQL's own tables)
), 
tables AS (
    SELECT
        relname AS table_name,
        (
            coalesce(heap_blks_read, 0) +
            coalesce(idx_blks_read, 0) +
            coalesce(toast_blks_read, 0) +
            coalesce(tidx_blks_read, 0)
        ) AS from_disk,
        (
            coalesce(heap_blks_hit, 0) +
            coalesce(idx_blks_hit, 0) +
            coalesce(toast_blks_hit, 0) +
            coalesce(tidx_blks_hit, 0)
        ) AS from_cache
    FROM pg_statio_all_tables
    -- Change to pg_statio_user_tables if you want to check only user tables (excluding PostgreSQL's own tables)
    WHERE (coalesce(heap_blks_read, 0) +
           coalesce(idx_blks_read, 0) +
           coalesce(toast_blks_read, 0) +
           coalesce(tidx_blks_read, 0) +
           coalesce(heap_blks_hit, 0) +
           coalesce(idx_blks_hit, 0) +
           coalesce(toast_blks_hit, 0) +
           coalesce(tidx_blks_hit, 0)) > 0 -- Discard tables without hits
)
SELECT
    a.table_name AS "table name",
    a.from_disk AS "disk hits",
    round((a.from_disk::numeric / (a.from_disk + a.from_cache)::numeric) * 100.0, 2) AS "% disk hits",
    round((a.from_cache::numeric / (a.from_disk + a.from_cache)::numeric) * 100.0, 2) AS "% cache hits",
    (a.from_disk + a.from_cache) AS "total hits"
FROM (
    SELECT * FROM all_tables
    UNION ALL
    SELECT * FROM tables
) AS a
ORDER BY (CASE WHEN a.table_name = 'all' THEN 0 ELSE 1 END), a.from_disk DESC;


      table name       | disk hits | % disk hits | % cache hits | total hits 
-----------------------+-----------+-------------+--------------+------------
 all                   |       417 |        2.11 |        97.89 |      19777
 pg_proc               |        78 |       12.81 |        87.19 |        609
 pg_attribute          |        70 |        0.65 |        99.35 |      10817
 pg_statistic          |        26 |       11.35 |        88.65 |        229
 pg_class              |        24 |        0.78 |        99.22 |       3064
 pg_operator           |        23 |        2.89 |        97.11 |        796
 pg_rewrite            |        22 |       44.90 |        55.10 |         49
 pg_toast_2618         |        15 |       60.00 |        40.00 |         25
 pg_amop               |        15 |        3.60 |        96.40 |        417
 pg_type               |        14 |        4.38 |        95.63 |        320
 pg_authid             |        11 |       16.42 |        83.58 |         67
 pg_database           |        10 |        1.79 |        98.21 |        558
 pg_index              |         9 |        2.16 |        97.84 |        416
 pg_amproc             |         8 |        4.10 |        95.90 |        195
 pg_tablespace         |         8 |       23.53 |        76.47 |         34
 pg_opclass            |         6 |        0.85 |        99.15 |        706
 pg_namespace          |         6 |        6.82 |        93.18 |         88
 pg_am                 |         5 |       17.86 |        82.14 |         28
 pg_constraint         |         5 |      100.00 |         0.00 |          5
 pg_collation          |         5 |       35.71 |        64.29 |         14
 pg_aggregate          |         4 |       25.00 |        75.00 |         16
 pg_shdescription      |         4 |       17.39 |        82.61 |         23
 pg_range              |         4 |      100.00 |         0.00 |          4
 pg_cast               |         4 |        0.73 |        99.27 |        547
 pg_auth_members       |         4 |        9.09 |        90.91 |         44
 pg_parameter_acl      |         3 |      100.00 |         0.00 |          3
 pg_toast_2619         |         3 |       50.00 |        50.00 |          6
 pg_db_role_setting    |         3 |        0.66 |        99.34 |        458
 pg_toast_1255         |         3 |      100.00 |         0.00 |          3
 pg_subscription       |         3 |      100.00 |         0.00 |          3
 pg_replication_origin |         3 |      100.00 |         0.00 |          3
 pg_shdepend           |         2 |        1.15 |        98.85 |        174
 pg_attrdef            |         2 |       50.00 |        50.00 |          4
 pg_depend             |         2 |      100.00 |         0.00 |          2
 pg_shseclabel         |         2 |      100.00 |         0.00 |          2
 pg_toast_1213         |         1 |      100.00 |         0.00 |          1
 pg_toast_2396         |         1 |      100.00 |         0.00 |          1
 pg_toast_6000         |         1 |      100.00 |         0.00 |          1
 pg_toast_3592         |         1 |      100.00 |         0.00 |          1
 pg_toast_6243         |         1 |      100.00 |         0.00 |          1
 pg_toast_6100         |         1 |      100.00 |         0.00 |          1
 pg_toast_2964         |         1 |      100.00 |         0.00 |          1
 pg_toast_1262         |         1 |       50.00 |        50.00 |          2
 pg_sequence           |         1 |       50.00 |        50.00 |          2
 pg_statistic_ext      |         1 |        2.78 |        97.22 |         36
 pg_toast_1260         |         1 |      100.00 |         0.00 |          1
```

# 数据类型

| 名称       | 说明                                           | 对比MySQL                                                                                       |
|------------|------------------------------------------------|-------------------------------------------------------------------------------------------------|
| 布尔类型   | boolean，标准的布尔类型，只能存储true，false     | MySQL中虽然没有对应的boolean，但是有替换的类型，数值的tinyint类型，和PGSQL的boolean都是占1个字节。  |
| 整型       | smallint（2字节），integer（4字节），bigint（8字节） | 跟MySQL没啥区别。                                                                                |
| 浮点型     | decimal，numeric（和decimal一样一样的，精准浮点型），real（float），double precision（double），money（货币类型） | 和MySQL基本也没区别，MySQL支持float，double，decimal。MySQL没有这个货币类型。                    |
| 字符串类型 | varchar(n)（character varying），char(n)（character），text | 这里和MySQL基本没区别。PGSQL存储的varchar类型，可以存储一个G。MySQL好像存储64kb（应该是）。        |
| 日期类型   | date（年月日），time（时分秒），timestamp（年月日时分秒）（time和timestamp可以设置时区） | 没啥说的，和MySQL基本没区别。MySQL有个datetime。                                                  |
| 二进制类型 | bytea-存储二进制类型                             | MySQL也支持，MySQL中是blob。                                                                      |
| 位图类型   | bit(n)（定长位图），bit varying(n)（可变长度位图） | 就是存储0，1。MySQL也有，只是这个类型用的不多。                                                    |
| 枚举类型   | enum，跟Java的enum一样                          | MySQL也支持。                                                                                   |
| 几何类型   | 点，直线，线段，圆……                             | MySQL没有，但是一般开发也用不到。                                                                 |
| 数组类型   | 在类型后，追加[]，代表存储数组                   | MySQL没有。                                                                                      |
| JSON类型   | json（存储JSON数据的文本），jsonb（存储JSON二进制） | 可以存储JSON，MySQL 8.x 也支持。                                                                 |
| ip类型     | cidr（存储ip地址）                              | MySQL也不支持。                                                                                  |

# 基本操作&数据类型
## 单引号和双引号
在PGSQL中，写SQL语句时，单引号用来标识实际的值。双引号用来标识一个关键字，比如表名，字段名。

## 数据类型转换
第一种方式：只需要在值的前面，添加上具体的数据类型即可
```sql
-- 将字符串转成位图类型
select bit '010101010101001';
```
第二种方式：也可以在具体值的后面，添加上 ::类型 ，来指定
```sql
-- 数据类型
select '2011-11-11'::date;
select '101010101001'::bit(20);
select '13'::int;
```
第三种方式：使用CAST函数
```sql
-- 类型转换的完整写法
select CAST(varchar '100' as int);
```
## 布尔类型
可以存储三个值，true，false，null
boolean类型在做and和or的逻辑操作时，结果
```
字段A	字段B	a and b	a or b
true	true	true	true
true	false	false	true
true	NULL	NULL	true
false	false	false	false
false	NULL	false	NULL
NULL	NULL	NULL	NULL
```
## 数值类型
如果要存主键，比如雪花算法，那就bigint。空间要节约，根据情况smallint

## 浮点型
浮点类型就关注2个（其实是一个）

    decimal(n,m)：本质就是numeric，PGSQL会帮你转换
    numeric(n,m)：PGSQL本质的浮点类型

针对浮点类型的数据，就使用 

numeric 数据类型  用于存储任意精度的数字，非常适合金融和其他需要精确计算的应用场景
```sql
CREATE TABLE transactions (
    id serial PRIMARY KEY,
    amount numeric(15, 2)
);
```

money 数据类型 专门用于存储货币值，带有本地化格式的显示
```sql
CREATE TABLE transactions (
    id serial PRIMARY KEY,
    amount money
);
```
推荐

在大多数情况下，推荐使用 numeric 数据类型，因为它提供了更高的精度和灵活性。money 类型虽然提供了一些便捷的格式化功能，但其灵活性和精度不如 numeric。

使用 money 类型存储金钱数据：
```sql
CREATE TABLE transactions (
    id serial PRIMARY KEY,
    amount money,
    description text
);

INSERT INTO transactions (amount, description)
VALUES ('$1234.56', 'Payment for services'), ('$7890.12', 'Refund for overcharge');

SELECT * FROM transactions;
```

## 序列
MySQL中的主键自增，是基于auto_increment去实现。MySQL里没有序列的对象。

PGSQL和Oracle十分相似，支持序列：sequence。

PGSQL可没有auto_increment。

序列的正常构建方式：
```sql
create sequence laozheng.table_id_seq;
-- 查询下一个值
select nextval('laozheng.table_id_seq');
-- 查询当前值
select currval('laozheng.table_id_seq');
```
默认情况下，seqeunce的起始值是0，每次nextval递增1，最大值9223372036854775807

告诉缓存，插入的数据比较多，可以指定告诉缓存，一次性计算出20个后续的值，nextval时，就不可以不去计算，直接去高速缓存拿值，效率会有一内内的提升。

序列大多数的应用，是用作表的主键自增效果。
```sql
-- 表自增
create table laozheng.xxx(
    id int8 default nextval('laozheng.table_id_seq'),
    name varchar(16)
);
insert into laozheng.xxx (name) values ('xxx');
select * from laozheng.xxx;
```
上面这种写法没有问题，但是很不爽~很麻烦。

PGSQL提供了序列的数据类型，可以在声明表结构时，直接指定序列的类型即可。

bigserial相当于给bigint类型设置了序列实现自增。

    smallserial
    serial
    bigserial
```sql
-- 表自增（爽）
create table laozheng.yyy(
    id bigserial,   
    name varchar(16)
);
insert into laozheng.yyy (name) values ('yyy');
```
在drop表之后，序列不会被删除，但是序列会变为不可用的状态。
因为序列在使用serial去构建时，会绑定到指定表的指定列上。

如果是单独构建序列，再构建表，使用传统方式实现，序列和表就是相对独立的。

## 数值的常见操作
针对数值咱们可以实现加减乘除取余这5个操作

还有其他的操作方式
| 操作符 | 描述   | 示例    | 结果 |
|--------|--------|---------|------|
| ^      | 幂     | 2 ^ 3   | 8    |
| \|/    | 平方根 | \|/ 36  | 6    |
| @      | 绝对值 | @ -5    | 5    |
| &      | 与     | 31 & 16 | 16   |
| \|     | 或     | 31 \| 32| 63   |
| <<     | 左移   | 1 << 1  | 2    |
| >>     | 右移   | 16 >> 1 | 8    |

数值操作也提供了一些函数，比如pi()，round(数值，位数)，floor()，ceil()

## 字符串类型

字符串类型用的是最多的一种，在PGSQL里，主要支持三种：

    character（就是MySQL的char类型），定长字符串。（最大可以存储1G）
    character varying（varchar），可变长度的字符串。（最大可以存储1G）
    text（跟MySQL异常）长度特别长的字符串。

操作没什么说的，但是字符串常见的函数特别多。

字符串的拼接一要要使用||来拼接。

其他的函数，可以查看 http://www.postgres.cn/docs/13/functions-string.html

## 日期类型

在PGSQL中，核心的时间类型，就三个。

    timestamp（时间戳，覆盖 年月日时分秒）
    date（年月日）
    time（时分秒）

在PGSQL中，声明时间的方式。

只需要使用字符串正常的编写 yyyy-MM-dd HH:mm:ss 就可以转换为时间类型。

直接在字符串位置使用之前讲到的数据类型转换就可以了。

当前系统时间 ：
- 可以使用now作为当前系统时间（没有时区的概念）
```sql
select timestamp 'now';
-- 直接查询now，没有时区的概念
select time with time zone 'now' at time zone '08:00:00'
```
- 也可以使用current_timestamp的方式获取（推荐，默认东八区）

日期类型的运算
- 正常对date类型做+，-操作，默认单位就是天~
- date + time = timestamp~~~
```sql
    select date '2011-11-11' + time '12:12:12' ;
```

- 可以针对timestamp使用interval的方式进行 +，-操作，在查询以时间范围为条件的内容时，可以使用
```sql
    select timestamp '2011-11-11 12:12:12' + interval '1day' + interval '1minute' + interval '1month';
```

## 枚举类型
枚举类型MySQL也支持，只是没怎么用，PGSQL同样支持这种数据类型

可以声明枚举类型作为表中的字段类型，这样可以无形的给表字段追加诡异的规范。
```sql
-- 声明一个星期的枚举，值自然只有周一~周日。
create type week as enum ('Mon','Tues','Sun');
-- 声明一张表，表中的某个字段的类型是上面声明的枚举。
drop table test;
create table test(
    id bigserial ,
    weekday week
);
insert into test (weekday) values ('Mon');
insert into test (weekday) values ('Fri');
```

## IP类型

PGSQL支持IP类型的存储，支持IPv4，IPv6这种，甚至Mac内种诡异类型也支持

这种IP类型，可以在存储IP时，帮助做校验，其次也可以针对IP做范围查找。

## JSON&JSONB类型
JSON在MySQL8.x中也做了支持，但是MySQL支持的不好，因为JSON类型做查询时，基本无法给JSON字段做索引。

PGSQL支持JSON类型以及JSONB类型。

JSON和JSONB的使用基本没区别。

撇去JSON类型，本质上JSON格式就是一个字符串，比如MySQL5.7不支持JSON的情况的下，使用text也可以，但是字符串类型无法校验JSON的格式，其次单独的字符串没有办法只获取JSON中某个key对应的value。

JSON和JSONB的区别：

    JSON类型无法构建索引，JSONB类型可以创建索引。
    JSON类型的数据中多余的空格会被存储下来。JSONB会自动取消多余的空格。
    JSON类型甚至可以存储重复的key，以最后一个为准。JSONB不会保留多余的重复key（保留最后一个）。
    JSON会保留存储时key的顺序，JSONB不会保留原有顺序。

JSON中key对应的value的数据类型
| JSON   | PGSQL   |
|--------|---------|
|String	 |text     |
|number	 |numeric  |
|boolean |	boolean|
|null	 |(none)   |

JSON还支持很多函数。可以直接查看 http://www.postgres.cn/docs/14/functions-json.html 

## 复合类型

复合类型就好像Java中的一个对象，Java中有一个User，User和表做了一个映射，User中有个人信息对象。可以基于符合类型对映射上个人信息。
```java
public class User{
   private Integer id;
   private Info info;
}

class Info{
   private String name;
   private Integer age;
}
```

按照上面的情况，将Info构建成一个复合类型
```sql
-- 构建复合类型，映射上Info
create type info_type as (name varchar(32),age int);
-- 构建表，映射User
create table tb_user(
    id serial,
    info info_type
);
-- 添加数据
insert into tb_user (info) values (('张三',23));
insert into tb_user (info) values (('露丝',233));
insert into tb_user (info) values (('jack',33));
insert into tb_user (info) values (('李四',24));
select * from tb_user;
```

## 数组类型

数组还是要依赖其他类型，比如在设置住址，住址可能有多个住址，可以采用数组类型去修饰字符串。

PGSQL中，指定数组的方式就是[]，可以指定一维数组，也支持二维甚至更多维数组。

构建数组的方式：
```sql
drop table test;
create table test(
    id serial,
    col1 int[],
    col2 int[2],
    col3 int[][]
);
-- 构建表指定数组长度后，并不是说数组内容只有2的长度，可以插入更多数据
-- 甚至在你插入数据，如果将二维数组结构的数组扔到一维数组上，也可以存储。
-- 数组编写方式
select '{{how,are},{are,you}}'::varchar[];
select array[[1,2],[3,4]];
insert into test (col1,col2,col3) values ('{1,2,3}','{4,5,6}','{7,8,9}');
insert into test (col1,col2,col3) values ('{1,2,3}','{4,5,6}',array[[1,2],[3,4]]);
insert into test (col1,col2,col3) values ('{1,2,3}','{4,5,6}','{{1,2},{3,4}}');
select * from test;
```
如果现在要存储字符串数组，如果存储的数组中有双引号怎么办，有大括号怎么办。
```sql
-- 如果存储的数组中的值，有单引号怎么办？
-- 使用两个单引号，作为一个单引号使用
select '{''how''}'::varchar[];
-- 如果存储的数组中的值，有逗号怎么办？(PGSQL中的数组索引从1开始算，写0也是从1开始算。)
-- 用双引号将数组的数据包起来~
select ('{"how,are"}'::varchar[])[2];
-- 如果存储的数组中的值，有双引号怎么办？
-- 如果要添加双引号，记得转义。
select ('{"\"how\",are"}'::varchar[])[1];
```
数组的比较方式
```sql
-- 包含
select array[1,2] @> array[1];
-- 被包含
select array[1,2] <@ array[1,2,4];
-- 是否有相同元素
select array[2,4,4,45,1] && array[1];
```
# 表
表的构建语句，基本都会。

核心在于构建表时，要指定上一些约束。
## 约束
`主键、非空、唯一、检查、外键（不玩）、默认值`

一般公司内，要求表中除了主键和业务字段之外，必须要有5个字段

created，create_id，updated，update_id，is_delete

检查的例子
```sql
-- 检查约束
-- 价格的表，price，discount_price
drop table test;
create table test(
    id bigserial primary key,
    name varchar(32) not null,
    price numeric check(price > 0),
    discount_price numeric check(discount_price > 0),
    check(price >= discount_price)
);
insert into test (name,price,discount_price) values ('粽子',122,12);
```

## 触发器
PGSQL的plsql语法
```sql
[ <<label>> ]
[ DECLARE
    declarations ]
BEGIN
    statements
END [ label ];
```

构建一个存储函数，测试一下plsql
```sql
-- 优先玩一下plsql
-- $$可以理解为是一种特殊的单引号，避免你在declare，begin，end中使用单引号时，出现问题，
-- 需要在编写后，在$$之后添加上当前内容的语言。
create function test() returns int as $$
declare
    money int := 10;
begin
    return money;
end;
$$ language plpgsql;

select test();
```

触发器语法：
```sql
CREATE [ OR REPLACE ] [ CONSTRAINT ] TRIGGER name { BEFORE | AFTER | INSTEAD OF } { event [ OR ... ] }
    ON table_name
    [ FROM referenced_table_name ]
    [ NOT DEFERRABLE | [ DEFERRABLE ] [ INITIALLY IMMEDIATE | INITIALLY DEFERRED ] ]
    [ REFERENCING { { OLD | NEW } TABLE [ AS ] transition_relation_name } [ ... ] ]
    [ FOR [ EACH ] { ROW | STATEMENT } ]
    [ WHEN ( condition ) ]
    EXECUTE { FUNCTION | PROCEDURE } function_name ( arguments )

where event can be one of:

    INSERT
    UPDATE [ OF column_name [, ... ] ]
    DELETE
    TRUNCATE
```
当 CONSTRAINT选项被指定，这个命令会创建一个 约束触发器 。这和一个常规触发器相同，不过触发该触发器的时机可以使用SET CONSTRAINTS调整。约束触发器必须是表上的 AFTER ROW触发器。它们可以在导致触发器事件的语句末尾被引发或者在包含该语句的事务末尾被引发。在后一种情况中，它们被称作是被 延迟 。一个待处理的延迟触发器的引发也可以使用 SET CONSTRAINTS立即强制发生。当约束触发器实现的约束被违背时，约束触发器应该抛出一个异常。

## 表空间
在存储数据时，数据肯定要落到磁盘上，基于构建的tablespace，指定数据存放在磁盘上的物理地址。

如果没有自己设计tablespace，PGSQL会自动指定一个位置作为默认的存储点。

可以通过一个函数，查看表的物理数据存放在了哪个磁盘路径下。
```sql
-- 查询表存储的物理地址
select pg_relation_filepath('student');
```
结果是 在$PG_DATA后的存放地址

```sql
-- 构建表空间,构建表空间需要用户权限是超级管理员，其次需要指定的目录已经存在
create tablespace tp_test location '/var/lib/pgsql/12/tp_test';
```

## 视图
在PGSQL中，简单（单表）的视图是允许写操作的
但是强烈不推荐对视图进行写操作，虽然PGSQL默认允许（简单的视图）。

写入的时候，其实修改的是表本身

## 索引
索引的分类
- B-Tree索引：最常用的索引。
- Hash索引：跟MySQL类似，做等值判断，范围凉凉~
- GIN索引：针对字段的多个值的类型，比如数组类型。
```sql
postgres=# \help create index
Command:     CREATE INDEX
Description: define a new index
Syntax:
CREATE [ UNIQUE ] INDEX [ CONCURRENTLY ] [ [ IF NOT EXISTS ] name ] ON [ ONLY ] table_name [ USING method ]
    ( { column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] )
    [ INCLUDE ( column_name [, ...] ) ]
    [ WITH ( storage_parameter [= value] [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    [ WHERE predicate ]

URL: https://www.postgresql.org/docs/13/sql-createindex.html
```

测试GIN索引效果

在没有索引的情况下，基于phone字段做包含查询
```sql
-- 测试索引效果
create table tb_index(
    id bigserial primary key,
    name varchar(64),
    phone varchar(64)[]
);

-- 添加300W条数据测试效果
do $$
declare
    i int := 0;
begin
    while i < 3000000 loop
        i = i + 1;
        insert into
            tb_index
        (name,phone) 
            values
        (md5(random()::text || current_timestamp::text)::uuid,array[random()::varchar(64),random()::varchar(64)]);
    end loop;
end;
$$ language plpgsql;

-- 在没有索引的情况下，基于phone字段做包含查询
-- phone：{0.6925242730781953,0.8569644964711074}
select * from tb_index where phone @> array['0.6925242730781953'::varchar(64)];
explain select * from tb_index where phone @> array['0.6925242730781953'::varchar(64)];
-- Seq Scan 全表扫描
-- 0.5s左右


-- 给phone字段构建GIN索引，在查询
-- 给phone字符串数组类型字段构建一个GIN索引
create index index_tb_index_phone_gin on tb_index using gin(phone);
-- 查询
select * from tb_index where phone @> array['0.6925242730781953'::varchar(64)];
explain select * from tb_index where phone @> array['0.6925242730781953'::varchar(64)];
-- Bitmap Index 位图扫描
-- 0.1s以内完成
```

## 物化视图
前面说过普通视图，本质就是一个SQL语句，普通的视图并不会本地磁盘存储任何物理。

每次查询视图都是执行这个SQL。效率有点问题。

物化视图从名字上就可以看出来，必然是要持久化一份数据的。使用套路和视图基本一致。这样一来查询物化视图，就相当于查询一张单独的表。相比之前的普通视图，物化视图就不需要每次都查询复杂SQL，每次查询的都是真实的物理存储地址中的一份数据（表）。

物化视图因为会持久化到本地，完全脱离原来的表结构。

而且物化视图是可以单独设置索引等信息来提升物化视图的查询效率。

But，有好处就有坏处，更新时间不太好把控。 如果更新频繁，对数据库压力也不小。 如果更新不频繁，会造成数据存在延迟问题，实时性就不好了。

如果要更新物化视图，可以采用触发器的形式，当原表中的数据被写后，可以通过触发器执行同步物化视图的操作。或者就基于定时任务去完成物化视图的数据同步。

物化视图语法
```sql
postgres=# \help create materialized view
Command:     CREATE MATERIALIZED VIEW
Description: define a new materialized view
Syntax:
CREATE MATERIALIZED VIEW [ IF NOT EXISTS ] table_name
    [ (column_name [, ...] ) ]
    [ USING method ]
    [ WITH ( storage_parameter [= value] [, ... ] ) ]
    [ TABLESPACE tablespace_name ]
    AS query
    [ WITH [ NO ] DATA ]

URL: https://www.postgresql.org/docs/13/sql-creatematerializedview.html
```

演示
```sql
-- 构建物化视图
create materialized view mv_test as (select id,name,price from test);
-- 操作物化视图和操作表的方式没啥区别。
select * from mv_test;
-- 操作原表时，对物化视图没任何影响
insert into test values (4,'月饼',50,10);
-- 物化视图的添加操作(不允许写物化视图)，会报错
insert into mv_test values (5,'大阅兵',66);
```
物化视图如何从原表中进行同步操作。

PostgreSQL中，对物化视图的同步，提供了两种方式，一种是全量更新，另一种是增量更新。

全量更新语法，没什么限制，直接执行，全量更新
```sql
-- 查询原来物化视图的数据
select * from mv_test;
-- 全量更新物化视图
refresh materialized view mv_test;
-- 再次查询物化视图的数据
select * from mv_test;
```

增量更新，增量更新需要一个唯一标识，来判断哪些是增量，同时也会有行数据的版本号约束。
```sql
-- 查询原来物化视图的数据
select * from mv_test;
-- 增量更新物化视图，因为物化视图没有唯一索引，无法判断出哪些是增量数据
refresh materialized view concurrently mv_test;
-- 给物化视图添加唯一索引。
create unique index index_mv_test on mv_test(id);
-- 增量更新物化视图
refresh materialized view concurrently mv_test;
-- 再次查询物化视图的数据
select * from mv_test;
-- 增量更新时，即便是修改数据，物化视图的同步，也会根据一个xmin和xmax的字段做正常的数据同步

update test set name = '汤圆' where id = 5;
insert into test values (5,'猪头肉',99,40);
select * from test;
```

# 事务
PostgreSQL中，在事务的并发问题里，也是基于MVCC，多版本并发控制去维护数据的一致性。相比于传统的锁操作，MVCC最大的有点就是可以让 读写互相不冲突 。

当然，PostgreSQL也支持表锁和行锁，可以解决写写的冲突问题。

PostgreSQL相比于其他数据，有一个比较大的优化，DDL也可以包含在一个事务中。比如集群中的操作，一个事务可以保证多个节点都构建出一个表，才算成功。

## 事务的基本使用
可以基于关闭PostgreSQL的自动提交事务来进行操作。
```sql
postgres=# \echo :AUTOCOMMIT
on
postgres=# \set AUTOCOMMIT off
postgres=# \echo :AUTOCOMMIT  
off
```
```sql
-- 开启事务
begin;
-- 操作
insert into test values (7,'bbb',12,5);
-- 提交事务 
commit;
```

## savepoint
比如项目中有一个大事务操作，不好控制，超时有影响，回滚会造成一切重来，成本太高。

我针对大事务，拆分成几个部分，第一部分完成后，构建一个保存点。如果后面操作失败了，需要回滚，不需要全盘回滚，回滚到之前的保存点，继续重试。

有人会发现，破坏了整体事务的原子性。

But，只要操作合理，可以在保存点的举出上，做重试，只要重试不成功，依然可以全盘回滚。

比如一个电商项目，下订单，扣库存，创建订单，删除购物车，增加用户积分，通知商家…………。这个其实就是一个大事务。可以将扣库存和下订单这种核心功能完成后，增加一个保存点，如果说后续操作有失败的，可以从创建订单成功后的阶段，再做重试。

不过其实上述的业务，基于最终一致性有更好的处理方式，可以保证可用性。

简单操作一下。
```sql
-- savepoint操作
-- 开启事务
begin;
-- 插入一条数据
insert into test values (8,'铃铛',55,11);
-- 添加一个保存点
savepoint ok1;
-- 再插入数据,比如出了一场
insert into test values (9,'大唐官府',66,22);
-- 回滚到之前的提交点
rollback to savepoint ok1;
-- 就可以开始重试操作，重试成功，commit，失败可以rollback;
commit;
```

# 并发问题
## 事务的隔离级别
在不考虑隔离性的前提下，事务的并发可能会出现的问题：

    脏读：读到了其他事务未提交的数据。（必须避免这种情况）
    不可重复读：同一事务中，多次查询同一数据，结果不一致，因为其他事务修改造成的。（一些业务中这种不可重复读不是问题）
    幻读：同一事务中，多次查询同一数据，因为其他事务对数据进行了增删吗，导致出现了一些问题。（一些业务中这种幻读不是问题）

针对这些并发问题，关系型数据库有一些事务的隔离级别，一般用4种。

    READ UNCOMMITTED：读未提交（啥用没用，并且PGSQL没有，提供了只是为了完整性）
    READ COMMITTED：读已提交，可以解决脏读（PGSQL默认隔离级别）
    REPEATABLE READ：可重复读，可以解决脏读和不可重复读（MySQL默认是这个隔离级别，PGSQL也提供了，但是设置为可重复读，效果还是串行化）
    SERIALIZABLE：串行化，啥都能解决（锁，效率慢）

## MVCC

首先要清楚，为啥要有MVCC。

如果一个数据库，频繁的进行读写操作，为了保证安全，采用锁的机制。但是如果采用锁机制，如果一些事务在写数据，另外一个事务就无法读数据。会造成读写之间相互阻塞。 大多数的数据库都会采用一个机制 多版本并发控制 MVCC 来解决这个问题。

比如你要查询一行数据，但是这行数据正在被修改，事务还没提交，如果此时对这行数据加锁，会导致其他的读操作阻塞，需要等待。如果采用PostgreSQL，他的内部会针对这一行数据保存多个版本，如果数据正在被写入，包就保存之前的数据版本。让读操作去查询之前的版本，不需要阻塞。等写操作的事务提交了，读操作才能查看到最新的数据。 这几个及时可以确保 `读写操作没有冲突` ，这个就是MVCC的主要特点。

`写写操作，和MVCC没关系，那个就是加锁的方式！`

`这里的MVCC是基于 读已提交 去聊的，如果是串行化，那就读不到了。`

在操作之前，先了解一下PGSQL中，每张表都会自带两个字段

    xmin：给当前事务分配的数据版本。如果有其他事务做了写操作，并且提交事务了，就给xmin分配新的版本。
    xmax：当前事务没有存在新版本，xmax就是0。如果有其他事务做了写操作，未提交事务，将写操作的版本放到xmax中。提交事务后，xmax会分配到xmin中，然后xmax归0。

演示

事务A
```sql
-- 左，事务A
--1、开启事务
begin;
--2、查询某一行数据,  xmin = 630,xmax = 0
select xmin,xmax,* from test where id = 8;
--3、每次开启事务后，会分配一个事务ID 事务id=631
select txid_current();
--7、修改id为8的数据，然后在本事务中查询   xmin = 631, xmax = 0
update test set name = '铃铛' where id = 8;
select xmin,xmax,* from test where id = 8;
--9、提交事务
commit;
```
事务B
```sql
-- 右，事务B
--4、开启事务
begin;
--5、查询某一行数据,  xmin = 630,xmax = 0
select xmin,xmax,* from test where id = 8;
--6、每次开启事务后，会分配一个事务ID 事务id=632
select txid_current();
--8、事务A修改完，事务B再查询  xmin = 630  xmax = 631
select xmin,xmax,* from test where id = 8;
--10、事务A提交后，事务B再查询  xmin = 631  xmax = 0
select xmin,xmax,* from test where id = 8;
```

# 锁
PostgreSQL中主要有两种锁，一个表锁一个行锁

PostgreSQL中也提供了页锁，咨询锁，But，这个不需要关注，他是为了锁的完整性

## 表锁
表锁的模式很多，其中最核心的两个：

    ACCESS SHARE：共享锁（读锁），读读操作不阻塞，但是不允许出现写操作并行
    ACCESS EXCLUSIVE：互斥锁（写锁），无论什么操作进来，都阻塞。
语法
```sql
postgres=# \help lock
Command:     LOCK
Description: lock a table
Syntax:
LOCK [ TABLE ] [ ONLY ] name [ * ] [, ...] [ IN lockmode MODE ] [ NOWAIT ]

where lockmode is one of:

    ACCESS SHARE | ROW SHARE | ROW EXCLUSIVE | SHARE UPDATE EXCLUSIVE
    | SHARE | SHARE ROW EXCLUSIVE | EXCLUSIVE | ACCESS EXCLUSIVE
```
就是基于LOCK开启表锁，指定表的名字name，其次在MODE中指定锁的模式，NOWAIT可以指定是否在没有拿到锁时，一致等待

例子
```sql
-- 111号连接
-- 基于互斥锁，锁住test表
-- 先开启事务
begin;
-- 基于默认的ACCESS EXCLUSIVE锁住test表
lock test in ACCESS SHARE mode;
-- 操作
select * from test;
-- 提交事务，锁释放
commit;
```

## 行锁

PostgreSQL的行锁和MySQL的基本是一模一样的，基于select for update就可以指定行锁。

MySQL中有一个概念，for update时，如果select的查询没有命中索引，可能会锁表。

PostgerSQL有个特点，一般情况，在select的查询没有命中索引时，他不一定会锁表，依然会实现行锁。

PostgreSQL的行锁，就玩俩，一个for update，一个for share。
在开启事务之后，直接执行select * from table where 条件 for update;
```sql
-- 先开启事务
begin;
-- 基于for update 锁住id为3的数据
select * from test where id = 3 for update;
update test set name = 'v1' where id = 3;
-- 提交事务，锁释放
commit;
```
其他的连接要锁住当前行，会阻塞住。

# 备份&恢复
在PostgreSQL中，有三种备份方式：
- SQL备份（逻辑备份）
- 文件系统备份（物理备份
- 归档备份：（也属于物理备份  

# 归档备份 介绍
在PostgreSQL有多个子进程来辅助一些操作

- BgWriter进程：BgWriter是将内存中的数据写到磁盘中的一个辅助进程。当向数据库中执行写操作后，数据不会马上持久化到磁盘里。这个主要是为了提升性能。BgWriter会周期性的将内存中的数据写入到磁盘。但是这个周期时间，长了不行，短了也不行。

    如果快了，IO操作频繁，效率慢。

    如果慢了，有查询操作需要内存中的数据时，需要BgWriter现把数据从内存写到磁盘中，再提供给查询操作作为返回结果。会导致查询操作效率变低。
    考虑一个问题： 事务提交了，数据没落到磁盘，这时，服务器宕机了怎么办？

- WalWriter进程：WAL就是write ahead log的缩写，说人话就是预写日志（redo log）。其实数据还在内存中时，其实已经写入到WAL日志中一份，这样一来，即便BgWriter进程没写入到磁盘中时，数据也不会存在丢失的问题。

    WAL能单独做备份么？单独不行！

    但是WAL日志有个问题，这个日志会循环使用，WAL日志有大小的线程，只能保存指定时间的日志信息，如果超过了，会覆盖之前的日志。

- PgArch进程：WAL日志会循环使用，数据会丢失。没关系，还有一个归档的进程，会在切换wal日志前，将WAL日志备份出来。PostgreSQL也提供了一个全量备份的操作。可以根据WAL日志，选择一个事件点，进行恢复。

查看WAL日志
```
cd pg_wal
# ll
total 2457632
-rw------- 1 postgres postgres 16777216 May  7 13:54 000000010000000000000001
-rw------- 1 postgres postgres 16777216 May  7 13:54 000000010000000000000002.partial
-rw------- 1 postgres postgres 16777216 May  7 13:55 000000020000000000000002
-rw------- 1 postgres postgres 16777216 May  7 13:55 000000020000000000000003
-rw------- 1 postgres postgres       41 May  7 13:54 00000002.history
-rw------- 1 postgres postgres 16777216 May  7 14:01 0000000B00000002000000C9.partial
-rw------- 1 postgres postgres      422 May  7 14:01 0000000B.history
-rw------- 1 postgres postgres 16777216 May  7 14:29 0000000C00000002000000C9
-rw------- 1 postgres postgres 16777216 May  7 14:29 0000000C00000002000000CA
-rw------- 1 postgres postgres      342 May  7 14:29 0000000C00000002000000CA.00000028.backup
-rw------- 1 postgres postgres      342 May  7 14:29 0000000C00000002000000CA.00001798.backup
-rw------- 1 postgres postgres 16777216 May  7 14:29 0000000C00000002000000CB
-rw------- 1 postgres postgres 16777216 May  7 22:55 0000000C00000002000000CC
```
    wal日志的名称，是三块内容组成，
    没8个字符分成一组，用16进制标识的
    00000001 00000000 0000000A
    时间线 逻辑id 物理id

查询当前库用的是哪个wal日志
```sql
-- 查看当前使用的wal日志  查询到的lsn：0/47233270
select pg_current_wal_lsn();

 pg_current_wal_lsn 
--------------------
 0/1517478

-- 基于lsn查询具体的wal日志名称  000000010000000000000047
select pg_walfile_name('0/47233270');

     pg_walfile_name      
--------------------------
 000000010000000000000001
```
归档默认不是开启的，需要手动开启归档操作，才能保证wal日志的完整性

修改postgresql.conf文件
```
# 开启wal日志的内容，注释去掉即可
wal_level = replica
fsync = on

# 开启归档操作
archive_mode = on
# 修改一小下命令，修改存放归档日志的路径
archive_command = 'test ! -f /archive/%f && cp %p /archive/%f'
```
修改完上述配置文件后，记得重启postgreSQL进程，才会生效！！！！

归档操作执行时，需要保证/archive存在，并且postgres用户有权限进行w操作

构建/archive路径
```
# postgres没有权限在/目录下构建目录
# 切换到root，构建目录，将目录的拥有者更改为postgres
mkdir /archive
chown -R postgres. archive
```

在当前库中做大量写操作，接入到wal日志，重置切换wal日志，再查看归档情况

发现，将当前的正在使用的wal日志和最新的上一个wal日志归档过来了，但是之前的没归档，不要慌，后期备份时，会执行命令，这个命令会直接要求wal日志立即归档，然后做全量备份。

## 逻辑备份&恢复
PostgreSQL提供了pg_dump以及pg_dumpall的命令来实现逻辑备份

pg_dump这种备份，不会造成用户对数据的操作出现阻塞。

## 物理备份（归档+物理）
这里需要基于前面的文件系统的备份和归档备份实现最终的操作

单独使用文件系统的方式，不推荐毕竟数据会丢失。

这里直接上PostgreSQL提供的pg_basebackup命令来实现。

pg_basebackup会做两个事情、

    会将内存中的脏数据落到磁盘中，然后将数据全部备份
    会将wal日志直接做归档，然后将归档也备走。

pg_basebackup命令

```sh
pg_basebackup takes a base backup of a running PostgreSQL server.  pg_basebackup 用于对运行中的 PostgreSQL 服务器进行基础备份。

Usage:  使用方法：
  pg_basebackup [OPTION]...  pg_basebackup [选项]...

Options controlling the output:  控制输出的选项：
  -D, --pgdata=DIRECTORY receive base backup into directory  将基础备份接收到目录中
  -F, --format=p|t       output format (plain (default), tar)  输出格式（普通（默认），tar）
  -r, --max-rate=RATE    maximum transfer rate to transfer data directory  最大传输速率传输数据目录
                         (in kB/s, or use suffix "k" or "M")  （以 kB/s 为单位，或使用后缀 "k" 或 "M"）
  -R, --write-recovery-conf  write configuration for replication  写入恢复配置
  -T, --tablespace-mapping=OLDDIR=NEWDIR  relocate tablespace in OLDDIR to NEWDIR  将表空间从 OLDDIR 重新定位到 NEWDIR
      --waldir=WALDIR    location for the write-ahead log directory  预写日志目录的位置
  -X, --wal-method=none|fetch|stream  include required WAL files with specified method  包含指定方法的所需 WAL 文件
  -z, --gzip             compress tar output  压缩 tar 输出
  -Z, --compress=0-9     compress tar output with given compression level  使用指定压缩级别压缩 tar 输出

General options:  常规选项：
  -c, --checkpoint=fast|spread  set fast or spread checkpointing  设置快速或扩展检查点
  -C, --create-slot      create replication slot  创建复制槽
  -l, --label=LABEL      set backup label  设置备份标签
  -n, --no-clean         do not clean up after errors  出现错误后不清理
  -N, --no-sync          do not wait for changes to be written safely to disk  不等待更改安全写入磁盘
  -P, --progress         show progress information  显示进度信息
  -S, --slot=SLOTNAME    replication slot to use  使用的复制槽
  -v, --verbose          output verbose messages  输出详细信息
  -V, --version          output version information, then exit  输出版本信息，然后退出
      --manifest-checksums=SHA{224,256,384,512}|CRC32C|NONE  use algorithm for manifest checksums  使用算法进行清单校验
      --manifest-force-encode  hex encode all file names in manifest  清单中的所有文件名强制进行十六进制编码
      --no-estimate-size do not estimate backup size in server side  不估算服务器端的备份大小
      --no-manifest      suppress generation of backup manifest  禁止生成备份清单
      --no-slot          prevent creation of temporary replication slot  防止创建临时复制槽
      --no-verify-checksums  do not verify checksums  不验证校验和
  -?, --help             show this help, then exit  显示此帮助，然后退出

Connection options:  连接选项：
  -d, --dbname=CONNSTR   connection string  连接字符串
  -h, --host=HOSTNAME    database server host or socket directory  数据库服务器主机或套接字目录
  -p, --port=PORT        database server port number  数据库服务器端口号
  -s, --status-interval=INTERVAL  time between status packets sent to server (in seconds)  发送到服务器的状态包之间的时间间隔（以秒为单位）
  -U, --username=NAME    connect as specified database user  以指定的数据库用户连接
  -w, --no-password      never prompt for password  从不提示输入密码
  -W, --password         force password prompt (should happen automatically)  强制密码提示（应自动发生）
```
准备一个pg_basebackup的备份命令
```
# -D 指定备份文件的存储位置
# -Ft 备份文件打个包
# -Pv 输出备份的详细信息
# -U 用户名（要拥有备份的权限）
# -h ip地址  -p 端口号
# -R 复制写配置文件
pg_basebackup -D /pg_basebackup -Ft -Pv -Upostgres -h 192.168.11.32 -p 5432 -R
```
提前准备出/pg_basebackup目录。记得将拥有者赋予postgres用户
```
mkdir /pg_basebackup
chown -R postgres. /pg_basebackup/
```
给postgres用户提供replication的权限，修改pg_hba.conf，记得重启生效
```
host replication postgres 0.0.0.0/0 md5
```
执行备份
```
pg_basebackup -D /pg_basebackup -Ft -Pv -Upostgres -h 192.168.11.32 -p 5432 -R

结果会生成 base.tar 和 pg_wal.tar 两个文件。
```
## 物理恢复（归档+物理）
模拟数据库崩盘，先停止postgresql服务，然后直接删掉data目录下的全部内容

将之前备份的两个文件准备好，一个base.tar，一个pg_wal.tar

第一步：将base.tar中的内容，全部解压到 12/data 目录下

第二步：将pg_wal.tar中的内容，全部解压到 /archive 目录下

第三步：在postgresql.auto.conf文件中，指定归档文件的存储位置，以及恢复数据的方式
```
restor_comman = 'cp %p /archive/%f %p'
recovery_target = 'immediate'
```
第四步：启动postgresql服务

第五步：启动后，发现查询没问题，但是执行写操作时，出错，不让写。需要执行一个函数，取消这种恢复数据后的状态，才允许正常的执行写操作。
```sql
select pg_wal_replay_resume();
```
## 物理备份&恢复（PITR-Point in time Recovery）
模拟场景

    场景：每天凌晨02:00，开始做全备（PBK），到了第二天，如果有人14:00分将数据做了误删，希望将数据恢复到14:00分误删之前的状态？

1、恢复全备数据，使用PBK的全备数据恢复到凌晨02:00的数据。（数据会丢失很多）

2、归档恢复：备份中的归档，有02:00~14:00之间的额数据信息，可以基于归档日志将数据恢复到指定的事务id或者是指定时间点，从而实现数据的完整恢复。

准备场景和具体操作

1、构建一张t3表查询一些数据
```sql
-- 构建一张表
create table t3 (id int);
insert into t3 values (1);
insert into t3 values (11);
```
2、模拟凌晨2点开始做全备操作
```sql
pg_basebackup -D /pg_basebackup -Ft -Pv -Upostgres -h 192.168.11.32 -p 5432 -R
```
3、再次做一些写操作，然后误删数据
```sql
-- 凌晨2点已经全备完毕
-- 模拟第二天操作
insert into t3 values (111);
insert into t3 values (1111);
-- 误删操作  2023年3月20日20:13:26
delete from t3;
```
4、恢复数据（确认有归档日志）

将当前服务的数据全部干掉，按照之前的全备恢复的套路先走着

然后将全备的内容中的base.tar扔data目录下，归档日志也扔到/archive位置。

5、查看归档日志，找到指定的事务id

查看归档日志，需要基于postgresql提供的一个命令
```sql
# 如果命令未找到，说明两种情况，要么没有这个可执行文件，要么是文件在，没设置环境变量
# 咱们这是后者
pg_waldump
# 也可以采用全路径的方式
/usr/pgsql-12/bin/pg_waldump
```
```sql
./pg_waldump ../data/pg_wal/000000010000000000000001

```
6、修改data目录下的恢复数据的方式

修改postgresql.auto.conf文件

将之前的最大恢复，更换为指定的事务id恢复

基于提供的配置例子，如何指定事务id

7、启动postgreSQL服务，查看是否恢复到指定事务ID

8、记得执行会后的函数，避免无法执行写操作
```sql
select pg_wal_replay_resume();
```

# 十四、数据迁移
```
# 用root用户下载
yum -y install pgloader
```
官方文档： https://pgloader.readthedocs.io/en/latest/

# 十五、主从操作
PostgreSQL自身只支持简单的主从，没有主从自动切换

主节点查看从节点信息
```sql
select * from pg_stat_replication
```

从节点查看主节点信息
```sql
select * from pg_stat_wal_receiver
```

## 主从切换（不这么玩）

其实主从的本质就是从节点去主节点不停的备份新的数据。

配置文件的系统其实就是两个：

    standby.signal文件，这个是从节点开启备份
    postgresql.auto.conf文件，这个从节点指定主节点的地址信息

切换就是原主追加上述配置，原从删除上述配追

1、主从节点全部stop停止：………………

2、原从删除上述配置：…………

3、原从新主启动服务：………

4、原主新从去原从新主备份一次数据：pg_basebackup操作，同时做解压，然后修改postgresql.conf文件以及standby.signal配置文件

5、启动原主新从查看信息

## 主从故障切换

默认情况下，这里的主从备份是异步的，导致一个问题，如果主节点写入的数据还没有备份到从节点，主节点忽然宕机了，导致后面如果基于上述方式实现主从切换，数据可能丢失。

PGSQL在9.5版本后提供了一个pg_rewind的操作，基于归档日志帮咱们做一个比对，比对归档日志，是否有时间差冲突。

实现操作：

1、rewind需要开启一项配置才可以使用

修改postgresql.conf中的 wal_log_hints = ‘on’

2、为了可以更方便的使用rewind，需要设置一下 /usr/pgsql-12/bin/ 的环境变量
```
vi /etc/profile
  追加信息
  export PATH=/usr/pgsql-12/bin/:$PATH
source /etc/profile
```
3、模拟主库宕机，直接对主库关机

4、从节点切换为主节点

3、模拟主库宕机，直接对主库关机

4、从节点切换为主节点
```
# 因为他会去找$PGDATA，我没配置，就基于-D指定一下PGSQL的data目录
pg_ctl promote -D ~/12/data/
```
5、将原主节点开机，执行命令，搞定归档日志的同步
- 启动虚拟机
- 停止PGSQL服务
```
pg_ctl stop -D ~/12/data
```
- 基于pg_rewind加入到集群
```
pg_rewind -D ~/12/data/ --source-server='host=192.168.11.66 user=postgres password=postgres'
```
- 如果上述命令失败，需要启动再关闭PGSQL，并且在执行，完成归档日志的同步
```
pg_ctl start -D ~/12/data
pg_ctl stop -D ~/12/data
pg_rewind -D ~/12/data/ --source-server='host=192.168.11.66 user=postgres password=postgres'
```
6、修改新从节点的配置，然后启动
- 构建standby.signal
```
standby_mode = 'on'
```
- 修改postgresql.auto.conf文件
```
# 注意ip地址
primary_conninfo = 'user=postgres password=postgres host=192.168.11.66 port=5432 sslmode=prefer sslcompression=0 gssencmode=prefer krbsrvname=postgres target_session_attrs=any'
restore_command = 'cp /archive/%f %p'
```
- 启动新的从节点
```
pg_ctl start -D ~/12/data/
```

# 复制槽管理
增加复制槽
```sql
alter system set max_replication_slots=20;
```
查询复制槽
```sql
select * from pg_replication_slots;
```
删除复制槽
```sql
SELECT * FROM pg_drop_replication_slot('查询复制槽的名称');

---Publication（发布）

---查询发布

    psql
    \c testdb
    \dRp   或者：select * from  pg_publication;


--删除发布

DROP PUBLICATION 发布名;
```

# 逻辑复制介绍
## 一、PostgreSQL的wal_level=logic的简介

`wal_level=logic` 是 PostgreSQL 中的一个配置选项，用于启用逻辑复制（logical replication）功能。逻辑复制是一种高级的数据复制技术，它允许您将变更（例如插入、更新和删除）从一个 PostgreSQL 数据库复制到另一个数据库，而不仅仅是将整个数据文件复制到另一个服务器。

启用逻辑复制后，PostgreSQL 将在事务日志（WAL）中记录更改，并将更改发送给订阅者，让其按照相同的顺序应用更改。这种方式可以更灵活地复制部分数据或特定类型的更改，并且可以在不同版本的 PostgreSQL 之间进行复制。

`wal_level=logic` 的配置选项告诉 PostgreSQL 使用逻辑复制模式。在此模式下，PostgreSQL 将在事务日志中记录完整的 SQL 语句，并将其发送给订阅者，从而使其能够准确地重现修改操作。

启用逻辑复制需要在主服务器和目标服务器上创建复制槽，并使用适当的命令来启动逻辑复制进程。一旦启用了逻辑复制，主服务器上的任何更改都将通过复制进程传输到目标服务器上。

逻辑复制在许多场景下很有用，例如实时数据备份、分布式系统和数据分析。它提供了更高级的复制和数据同步功能，使您能够更好地管理和利用 PostgreSQL 数据库的复制能力。
## 、PostgreSQL开启wal_level=logic的步骤

要在 PostgreSQL 中启用逻辑复制（logical replication），您需要执行以下步骤：

1. 编辑 PostgreSQL 的配置文件 postgresql.conf。您可以使用命令 `sudo vim $PGDATA/postgresql.conf` 来打开文件。

2. 在配置文件中查找 `wal_level` 参数，并将其设置为 `logical`。如果找不到该参数，您可以在文件的末尾添加以下行：

wal_level = logical

或者直接在psql中执行

alter system set wal_level='logical';

 3. 保存并关闭配置文件。

4. 重新启动 PostgreSQL 服务器以应用更改。您可以使用以下命令重启 PostgreSQL 服务：

sudo systemctl restart postgresql

5. 确保您在主服务器和要进行逻辑复制的目标服务器上都启用了逻辑复制功能。您可以在 PostgreSQL 的配置文件中找到以下配置项，确保两个服务器上都已启用：

    max_replication_slots = <desired_number_of_replication_slots>
    max_wal_senders = <desired_number_of_wal_senders>

   `<desired_number_of_replication_slots>` 是您希望为逻辑复制使用的复制槽数量，`<desired_number_of_wal_senders>` 是您希望为逻辑复制使用的 WAL 发送进程数量。

6. 在主服务器上创建逻辑复制槽。您可以使用以下命令在主服务器上创建复制槽：

CREATE_REPLICATION_SLOT <slot_name> LOGICAL pgoutput;

   `<slot_name>` 是您为复制槽指定的名称。

7. 在目标服务器上创建逻辑复制槽。您可以使用以下命令在目标服务器上创建复制槽：

CREATE_REPLICATION_SLOT <slot_name> LOGICAL pgoutput;

   `<slot_name>` 是与主服务器上创建的复制槽名称相同的名称。

8. 启动逻辑复制进程。在目标服务器上，您可以使用以下命令启动逻辑复制进程：

START_REPLICATION SLOT <slot_name> LOGICAL <starting_position>;

   `<slot_name>` 是您在目标服务器上创建的复制槽名称，`<starting_position>` 是您希望从主服务器复制的起始位置。

现在，您已经成功地在 PostgreSQL 中启用了逻辑复制。主服务器上的更改将通过逻辑复制传输到目标服务器上。请注意，逻辑复制可能会对系统性能产生一定影响，因此在进行大规模的逻辑复制操作时，需谨慎评估系统的负载和性能。
## 三、开启wal_level=logical模式的优点

1. 灵活性：逻辑复制允许选择哪些表和数据进行复制。与物理复制相比，它提供了更大的灵活性，可以根据需求选择性地复制数据。

2. 多版本并发控制 (MVCC)：逻辑复制可以在源数据库和目标数据库之间实现MVCC。这意味着源数据库在复制操作期间可以继续正常运行，不会阻塞其他事务的执行。

3. 跨版本兼容性：逻辑复制可以在不同版本的PostgreSQL之间进行复制。这对于升级或迁移数据库非常有用，可以在不同版本之间进行平滑的数据迁移。

4. 多节点复制：逻辑复制支持多节点复制，即一个源数据库可以同时复制到多个目标数据库。这可以实现数据的分发和同步，从而提供更高的可用性和数据复制的冗余。

5. 逻辑补充：逻辑复制可以补充物理复制的功能。它允许在源数据库和目标数据库之间执行更复杂的数据转换和处理，例如数据清理、数据过滤和数据转换等。
## 四、开启wal_level=logical模式的缺点

1. 性能开销：逻辑复制相对于物理复制来说，通常会有更大的性能开销。逻辑复制需要对数据进行解析、转换和重新构建，这会增加系统的负载和延迟。

2. 数据一致性：由于逻辑复制是基于逻辑解析和转换的，可能存在数据一致性的问题。在复制过程中，如果有复杂的数据转换或处理操作，可能会导致数据的不一致性。

3. 配置复杂性：逻辑复制的配置相对较复杂，需要进行更多的设置和参数调整。这可能需要更多的时间和努力来进行配置和管理。

4. 兼容性限制：逻辑复制可能对所使用的PostgreSQL版本和插件有一定的兼容性限制。不同版本之间的差异或插件的不兼容可能导致复制操作无法正常进行。

5. 数据库结构变更限制：逻辑复制对数据库结构变更有一定的限制。某些结构变更可能无法正确地复制，需要额外的手动操作或配置来实现。


# 问答

在 PostgreSQL 中，即使你设置了 `max_wal_size = 1GB`，`pg_wal` 目录的实际占用空间可能会超过这个值。下面是一些可能的原因和解释：

### 1. 检查点频率和活动量

`max_wal_size` 控制的是在触发检查点之前WAL文件的最大累积大小。然而，多个因素可能导致WAL目录的实际大小超过这个限制：

- **高活动量**：如果数据库的写操作非常频繁，在检查点之间会产生大量的WAL文件。
- **检查点完成时间**：虽然达到 `max_wal_size` 后会触发检查点，但检查点的完成需要时间。在此期间，新的WAL文件继续生成。

### 2. WAL 保留

- **wal_keep_size**：此参数用于保留WAL文件以供流复制使用。如果设置得过大，会导致更多的WAL文件保留在磁盘上。
- **replication slots**：如果有复制槽（replication slots）未被清理，它们会继续保留WAL文件，直到这些槽被显式删除或清理。

### 3. 归档日志

- **archive_mode 和 archive_command**：如果启用了WAL归档，并且归档进程无法跟上生成WAL文件的速度，未归档的WAL文件会继续累积，增加 `pg_wal` 目录的大小。

### 4. 恢复和备份

- **恢复操作**：在恢复或重放日志过程中，PostgreSQL 可能需要保留额外的WAL文件。
- **未清理的备份**：如果你有基于WAL的备份策略，确保备份进程正常运行并且定期清理过期的WAL文件。

### 5. 延迟检查点

- **checkpoint_completion_target**：该参数控制检查点的完成时间。一个较高的值（接近1）意味着检查点过程更加平滑，但也可能导致更多的WAL文件在检查点之间累积。

### 解决方案和建议

1. **监控WAL活动**：使用 `pg_stat_bgwriter` 和 `pg_stat_archiver` 视图监控检查点活动和WAL归档情况。
   ```sql
   SELECT * FROM pg_stat_bgwriter;
   SELECT * FROM pg_stat_archiver;
   ```

2. **调整配置参数**：
   - 确保 `wal_keep_size` 和 `max_wal_size` 的设置符合你的工作负载需求。
   - 确保 `checkpoint_completion_target` 设置合理，通常在 0.7 到 0.9 之间。

3. **检查复制槽**：确保没有未清理的复制槽。
   ```sql
   SELECT * FROM pg_replication_slots;
   ```

4. **归档配置**：确保 `archive_command` 正常工作，并且归档进程能及时处理WAL文件。
   ```ini
   archive_mode = on
   archive_command = 'cp %p /path/to/archive/%f'
   ```

5. **调试工具**：使用 `pg_waldump` 工具检查WAL文件内容，以了解WAL文件的生成和使用情况。
   ```bash
   pg_waldump -p /path/to/pg_wal
   ```

### 示例

以下是一些配置示例：

```ini
max_wal_size = 1GB
min_wal_size = 512MB
checkpoint_timeout = 10min
checkpoint_completion_target = 0.7
wal_keep_size = 128MB
archive_mode = on
archive_command = 'cp %p /path/to/archive/%f'
```

通过监控和调整这些参数，你可以更好地控制 `pg_wal` 目录的大小，确保数据库的高效运行。

