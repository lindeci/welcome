- [安装etcd](#安装etcd)
- [安装PG](#安装pg)
- [patroni 流程讲解](#patroni-流程讲解)
- [安装Patroni](#安装patroni)
- [etcd 中键值对讲解](#etcd-中键值对讲解)
	- [查看租约信息](#查看租约信息)
	- [查看日志](#查看日志)
- [patroni 修改配置](#patroni-修改配置)
	- [不用进入编辑器](#不用进入编辑器)
- [Patroni是如何工作的](#patroni是如何工作的)
- [Pending restart 列的介绍](#pending-restart-列的介绍)
	- [添加空密码用户](#添加空密码用户)
- [高可用切换](#高可用切换)
	- [手工切换](#手工切换)

# 安装etcd

```sh
yum install -y etcd
cat /etc/etcd/etcd.conf | grep -v '#'
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_CLIENT_URLS="http://172.1.1.197:2379"
ETCD_NAME="default"
ETCD_ADVERTISE_CLIENT_URLS="http://172.1.1.197:2379"

systemctl restart etcd
```

# 安装PG

```
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
sudo yum install -y postgresql12-server

# sudo /usr/pgsql-12/bin/postgresql-12-setup initdb

# sudo systemctl enable postgresql-12

# sudo systemctl start postgresql-12

/var/lib/pgsql/12/data/
/usr/pgsql-12/bin/postmaster
```

# patroni 流程讲解
https://github.com/zalando/patroni/blob/master/docs/ha_loop_diagram.png

# 安装Patroni

yum install -y gcc epel-release
yum install -y python-pip python-psycopg2 python-devel

pip3 install --upgrade pip
pip3 install --upgrade setuptools
pip3 install psycopg
pip3 install patroni[etcd]

/usr/local/python3/bin/patroni
ExecStart=/usr/local/bin/patroni /etc/patroni.yml

cat /etc/systemd/system/patroni.service
[Unit]
Description=Runners to orchestrate a high-availability PostgreSQL
After=syslog.target network.target

[Service]
Type=simple
User=postgres
Group=postgres
#StandardOutput=syslog
ExecStart=/usr/local/python3/bin/patroni /etc/patroni.yml
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=process
TimeoutSec=30
Restart=no

[Install]
WantedBy=multi-user.targe

创建Patroni配置文件/etc/patroni.yml，以下是node1的配置示例

```yml
scope: pgsql                           # 指定集群的范围
namespace: /service/                   # ETCD中的命名空间
name: pg01                             # 集群的名称

restapi:
	listen: 0.0.0.0:8008                  # REST API监听地址
	connect_address: 172.1.1.197:8008   # REST API连接地址

etcd3:
	host: 172.1.1.197:2379              # ETCD的主机和端口

bootstrap:
	dcs:
	ttl: 30                            # 租约有效期，单位为秒
	loop_wait: 10                      # 轮询间隔，单位为秒
	retry_timeout: 10                  # 重试超时，单位为秒
	maximum_lag_on_failover: 1048576    # 故障转移时允许的最大延迟，单位为字节
	master_start_timeout: 300          # 启动主节点的超时，单位为秒
	synchronous_mode: false            # 同步模式是否启用
	synchronous_mode_strict: false
	postgresql:
		use_pg_rewind: true               # 是否使用pg_rewind工具
		use_slots: true                   # 是否使用复制槽
		parameters:
		listen_addresses: "0.0.0.0"     # 监听地址
		port: 5432                      # 监听端口
		wal_level: logical              # WAL日志级别
		hot_standby: "on"               # 热备用是否开启
		wal_keep_segments: 100          # 保留的WAL日志段数量
		max_wal_senders: 10             # 最大的WAL发送者数量
		max_replication_slots: 10       # 最大的复制槽数量
		wal_log_hints: "on"             # 是否开启WAL日志提示
		listen_addresses: "0.0.0.0"             # 哪些 IP 地址监听连接请求；使用 "*" 表示监听所有地址
        port: 5432                              # 监听端口号（修改需要重启数据库）
        max_connections: 200                    # 允许的最大客户端连接数（修改需要重启数据库）
        shared_buffers: 128MB                   # 共享内存缓冲区大小，最小�� 128kB（修改需要重启数据库）
        dynamic_shared_memory_type: posix       # 动态共享内存类型，默认为第一个选项
        max_wal_size: 1GB                       # WAL 日志最大大小（修改需要重启数据库）
        min_wal_size: 80MB                      # WAL 日志最小大小（修改需要重启数据库）
        log_timezone: "PRC"                     # 日志时区设置为中国标准时间（Asia/Shanghai）
        datestyle: "iso, ymd"                   # 日期样式设置为 "ISO, 年月日" 格式
        timezone: "PRC"                         # 时区设置为中国标准时间（Asia/Shanghai）
        lc_messages: "zh_CN.UTF8"               # 系统错误消息的本地化设置为中文 UTF-8
        lc_monetary: "zh_CN.UTF8"               # 货币格式化本地化设置为中文 UTF-8
        lc_numeric: "zh_CN.UTF8"                # 数字格式化本地化设置为中文 UTF-8
        lc_time: "zh_CN.UTF8"                   # 时间格式化本地化设置为中文 UTF-8
        default_text_search_config: "pg_catalog.simple"  # 全文搜索默认配置为 pg_catalog.simple
        wal_compression: "on"                          # 启用 WAL 日志压缩
        log_min_duration_statement: "10ms"            # 记录执行时间超过 10 毫秒的 SQL 语句
        checkpoint_timeout: "30min"                   # 检查点完成前的最长等待时间为 30 分钟（修改需要重启数据库）
        pg_stat_statements.max: "1000"                # pg_stat_statements 中保留的最大 SQL 语句数量
        pg_stat_statements.track: "all"               # 对所有语句进行跟踪统计
        pg_stat_log.max: "1024"                       # pg_stat_log 中保留的最大日志条目数量
        pg_stat_log.track: "all"                      # 跟踪所有查询的日志记录
        pg_stat_log.track_utility: "true"             # 跟踪系统命令的日志记录
        wal_keep_size: "1600MB"                       # 保留用于流复制的 WAL 日志大小为 1600MB
        logging_collector: "on"                       # 启用日志收集器（修改需要重启数据库）
        log_destination: "csvlog"                     # 日志输出格式为 CSV 文件（修改需要重启数据库）
        archive_mode: "on"                            # 启用归档模式
        recovery_target_time: "2023-08-08 00:00:00"   # 设置恢复的目标时间点
        recovery_target_timeline: "latest"            # 恢复时使用最新的时间线
        archive_command: 'DATE=`date +%Y%m%d`;DIR="/back/$DATE";(test -d $DIR || mkdir -p $DIR)&&cp %p $DIR/%f'  # 设置归档命令用于归档日志      
        restore_command: 'DATE=`date +%Y%m%d`;DIR="/back/$DATE";cp $DIR/%f %p'  # 设置还原命令用于恢复归档日志

	initdb:
	- encoding: UTF8                     # 数据库编码
	- locale: C                          # 默认区域设置
	- lc-ctype: zh_CN.UTF-8              # LC_CTYPE设置
	- data-checksums                     # 开启数据校验和

	pg_hba:
	- host replication repl 0.0.0.0/0 md5  # 访问复制的客户端认证方式
	- host all all 0.0.0.0/0 md5           # 其他客户端认证方式

postgresql:
	listen: 0.0.0.0:5432                 # PostgreSQL监听地址
	connect_address: 172.1.1.197:5432  # PostgreSQL连接地址
	data_dir: /var/lib/pgsql/12/data     # 数据库数据目录
	bin_dir: /usr/pgsql-12/bin           # PostgreSQL二进制文件目录

	authentication:
		replication:
			username: repl                  # 复制用户的用户名
			password: "123456"              # 复制用户的密码
		superuser:
			username: postgres              # 超级用户的用户名
			password: "123456"              # 超级用户的密码

	callbacks:
		on_start: /data/pgsql/loadvip.sh
		on_restart: /data/pgsql/loadvip.sh
		on_role_change: /data/pgsql/loadvip.sh

	basebackup:
		max-rate: 100M                    # 备份的最大速率
		checkpoint: fast                  # 备份时是否使用快速检查点

tags:
	nofailover: false                  # 是否允许故障转移
	noloadbalance: false               # 是否允许负载均衡
	clonefrom: false                   # 是否是一个从节点的克隆
	nosync: false                      # 是否禁用同步
```

完整的参数含有可参考Patroni手册中的 YAML Configuration Settings，其中PostgreSQL参数可根据需要自行补充。

其他PG节点的patroni.yml需要相应修改下面3个参数

```
name
    node1~node4分别设置pg1~pg4
restapi.connect_address
    根据各自节点IP设置
postgresql.connect_address
    根据各自节点IP设置
```

systemctl start patroni

patronictl -c /etc/patroni.yml list

patronictl -c /etc/patroni.yml switchover pgsql

| 故障位置 | 场景                           | Patroni的动作                                                    |
| -------- | ------------------------------ | ---------------------------------------------------------------- |
| 备库     | 备库PG停止                     | 停止备库PG                                                       |
| 备库     | 停止备库Patroni                | 停止备库PG                                                       |
| 备库     | 强杀备库Patroni（或Patroni     |                                                                  |
| crash）  | 无操作                         |                                                                  |
| 备库     | 备库无法连接etcd               | 无操作                                                           |
| 备库     | 非Leader角色但是PG处于生产模式 | 重启PG并切换到恢复模式作为备库运行                               |
| 主库     | 主库PG停止                     | 重启PG，重启超过master_start_timeout设定时间，进行主备切换       |
| 主库     | 停止主库Patroni                | 停止主库PG，并触发failover                                       |
| 主库     | 强杀主库Patroni（或Patroni     |                                                                  |
| crash）  | 触发failover，此时出现”双主” |                                                                  |
| 主库     | 主库无法连接etcd               | 将主库降级为备库，并触发failover                                 |
| -        | etcd集群故障                   | 将主库降级为备库，此时集群中全部都是备库。                       |
| -        | 同步模式下无可用同步备库       | 临时切换主库为异步复制，在恢复为同步复制之前自动failover暂不生效 |

/usr/local/bin/patronictl -c /etc/patroni.yml edit-config -s 'synchronous_mode_strict=true'

/usr/local/bin/patronictl -c /etc/patroni.yml edit-config -s 'synchronous_mode=true'

# etcd 中键值对讲解

在 Patroni 中，当您将 ETCD 作为外部协调服务时，它将使用 ETCD 来存储和管理有关 PostgreSQL 集群状态的信息。ETCD 是一个分布式键值存储系统，它允许多个节点共享和访问键值对数据，因此可以用于协调和同步分布式系统的状态。

在 ETCD 中，Patroni 存储了几个关键的键值对，用于跟踪 PostgreSQL 集群的状态和故障转移。以下是一些重要的键值对和它们的含义：

1. **/service/{cluster_name}/{scope}/leader**：
   这个键值对用于记录当前的主节点（Leader）的信息。`{cluster_name}` 是您在 Patroni 配置文件中定义的 PostgreSQL 集群的名称。`{scope}` 是 Patroni 的范围，通常是 "leader"。
2. **/service/{cluster_name}/{scope}/{member_name}**：
   这个键值对用于记录每个 Patroni 成员（PostgreSQL 节点）的信息。其中，`{member_name}` 是 Patroni 成员的名称，通常与 PostgreSQL 节点的名称相同。包含在这个键下的信息包括成员的连接信息、角色（主节点或从节点）、状态（运行、故障等）等。
3. **/service/{cluster_name}/{scope}/optime**：
   这个键值对用于记录 Patroni 集群的复制进度信息。包含了复制进度的相关数据，如复制的 WAL 位置（WAL position）和复制进度的时间戳等。
4. **/service/{cluster_name}/{scope}/initialize**：
   如果正在进行初始化或还原操作，Patroni 将使用这个键值对来记录相关信息。

以上只是一些常见的键值对，实际上 Patroni 还可能使用其他键值对来存储更多的信息，以支持其高可用性和自动故障转移功能。当 Patroni 运行时，它将使用 ETCD 中的这些键值对来跟踪 PostgreSQL 集群的状态，并根据需要进行故障转移和自动主节点的选举。

请注意，ETCD 的配置和操作都应该根据您的环境和需求进行适当的调整和管理。在配置和使用 ETCD 时，务必确保安全性和可靠性，以确保 PostgreSQL 集群的稳定运行。

```sh
patronictl -c /etc/patroni.yml list
+ Cluster: pgsql --------+--------------+-----------+----+-----------+---------------------+
| Member | Host          | Role         | State     | TL | Lag in MB | Tags                |
+--------+---------------+--------------+-----------+----+-----------+---------------------+
| pg01   | 172.1.1.197 | Leader       | running   | 10 |           |                     |
+--------+---------------+--------------+-----------+----+-----------+---------------------+
| pg02   | 172.1.1.198 | Replica      | streaming | 10 |         0 | nofailover: true    |
|        |               |              |           |    |           | noloadbalance: true |
|        |               |              |           |    |           | nosync: true        |
+--------+---------------+--------------+-----------+----+-----------+---------------------+
| pg03   | 172.1.1.196 | Sync Standby | streaming | 10 |         0 |                     |
+--------+---------------+--------------+-----------+----+-----------+---------------------+


export ETCDCTL_API=3

./etcdctl get --prefix /service/
/service/pgsql/config
{"ttl": 30, "loop_wait": 10, "retry_timeout": 10, "maximum_lag_on_failover": 1048576, "master_start_timeout": 300, "synchronous_mode": true, "postgresql": {"use_pg_rewind": true, "use_slots": true, "parameters": {"listen_addresses": "0.0.0.0", "port": 5432, "wal_level": "logical", "hot_standby": "on", "wal_keep_segments": 100, "max_wal_senders": 10, "max_replication_slots": 10, "wal_log_hints": "on"}}, "synchronous_mode_strict": true}
/service/pgsql/failover
{}
/service/pgsql/history
[[1,50332624,"no recovery target specified","2023-07-27T14:24:04.400493+08:00","pg01"],[2,50332960,"no recovery target specified","2023-07-27T14:52:40.300396+08:00","pg03"],[3,50457392,"no recovery target specified","2023-07-27T15:02:40.784982+08:00","pg01"],[4,66811336,"no recovery target specified","2023-07-27T15:15:04.609427+08:00","pg03"],[5,74046416,"no recovery target specified","2023-07-27T15:15:41.959271+08:00","pg01"],[6,117441136,"no recovery target specified","2023-07-27T19:34:16.137562+08:00","pg03"],[7,117441536,"no recovery target specified","2023-07-27T19:38:26.929193+08:00","pg01"],[8,207467488,"no recovery target specified","2023-07-28T20:23:56.619380+08:00","pg03"],[9,207468328,"no recovery target specified","2023-07-28T21:13:34.802744+08:00","pg01"]]
/service/pgsql/initialize
7260332825476436099
/service/pgsql/leader
pg01
/service/pgsql/members/pg01
{"conn_url":"postgres://172.1.1.197:5432/postgres","api_url":"http://172.1.1.197:8008/patroni","state":"running","role":"master","version":"3.0.4","xlog_location":207469224,"timeline":10}
/service/pgsql/members/pg02
{"conn_url":"postgres://172.1.1.198:5432/postgres","api_url":"http://172.1.1.198:8008/patroni","state":"running","role":"replica","version":"3.0.4","tags":{"nofailover":true,"noloadbalance":true,"nosync":true},"xlog_location":207469224,"replication_state":"streaming","timeline":10}
/service/pgsql/members/pg03
{"conn_url":"postgres://172.1.1.196:5432/postgres","api_url":"http://172.1.1.196:8008/patroni","state":"running","role":"replica","version":"3.0.4","xlog_location":207469224,"replication_state":"streaming","timeline":10}
/service/pgsql/status
{"optime":207469224}
/service/pgsql/sync
{"leader":"pg01","sync_standby":"pg03"}



```

## 查看租约信息

```sh
# 查看所有租约
etcdctl lease list
found 2 leases
24fd89f8b3853f04
24fd89f8b3853f0f

# 查看租约跟KYES的绑定信息
etcdctl lease timetolive 24fd89f8b3853f04 --keys
lease 24fd89f8b3853f04 granted with TTL(30s), remaining(28s), attached keys([/service/ysc_pgsql/members/pg01 /service/ysc_pgsql/leader])

# 查看租约跟KYES的绑定信息
etcdctl lease timetolive 24fd89f8b3853f0f --keys
lease 24fd89f8b3853f0f granted with TTL(30s), remaining(15s), attached keys([/service/ysc_pgsql/members/pg02])
```

## 查看日志

主节点上日志

```
journalctl -f -u patroni
-- Logs begin at Tue 2023-08-15 16:45:21 CST. --
Aug 16 11:09:11 host-172-1-1-28 patroni[78584]: 2023-08-16 11:09:11,784 INFO: no action. I am (pg01), the leader with the lock
Aug 16 11:09:21 host-172-1-1-28 patroni[78584]: INFO:patroni.ha:Lock owner: pg01; I am pg01
Aug 16 11:09:21 host-172-1-1-28 patroni[78584]: INFO:patroni.__main__:no action. I am (pg01), the leader with the lock
Aug 16 11:09:21 host-172-1-1-28 patroni[78584]: 2023-08-16 11:09:21,783 INFO: no action. I am (pg01), the leader with the lock
Aug 16 11:09:31 host-172-1-1-28 patroni[78584]: INFO:patroni.ha:Lock owner: pg01; I am pg01
Aug 16 11:09:31 host-172-1-1-28 patroni[78584]: INFO:patroni.__main__:no action. I am (pg01), the leader with the lock
Aug 16 11:09:31 host-172-1-1-28 patroni[78584]: 2023-08-16 11:09:31,802 INFO: no action. I am (pg01), the leader with the lock
Aug 16 11:09:41 host-172-1-1-28 patroni[78584]: INFO:patroni.ha:Lock owner: pg01; I am pg01
Aug 16 11:09:41 host-172-1-1-28 patroni[78584]: INFO:patroni.__main__:no action. I am (pg01), the leader with the lock
Aug 16 11:09:41 host-172-1-1-28 patroni[78584]: 2023-08-16 11:09:41,787 INFO: no action. I am (pg01), the leader with the lock
```

从节点上日志

```
journalctl -f -u patroni  
-- Logs begin at Tue 2023-08-15 16:54:44 CST. --
Aug 16 10:56:16 host-172-1-1-29 patroni[23174]: INFO:patroni.ha:Lock owner: pg01; I am pg02
Aug 16 10:56:16 host-172-1-1-29 patroni[23174]: INFO:patroni.postgresql.connection:establishing a new patroni connection to the postgres cluster
Aug 16 10:56:16 host-172-1-1-29 patroni[23174]: 2023-08-16 10:56:16,693 INFO: Lock owner: pg01; I am pg02
Aug 16 10:56:16 host-172-1-1-29 patroni[23174]: 2023-08-16 10:56:16,694 INFO: establishing a new patroni connection to the postgres cluster
Aug 16 10:56:16 host-172-1-1-29 patroni[23174]: /data/pgsql/script/loadvip.sh: line 49: /data/pgsql/script/loadvip.log: Permission denied
Aug 16 10:56:16 host-172-1-1-29 patroni[23174]: INFO:patroni.__main__:no action. I am (pg02), a secondary, and following a leader (pg01)
Aug 16 10:56:16 host-172-1-1-29 patroni[23174]: 2023-08-16 10:56:16,733 INFO: no action. I am (pg02), a secondary, and following a leader (pg01)
Aug 16 10:56:21 host-172-1-1-29 patroni[23174]: INFO:patroni.ha:Lock owner: pg01; I am pg02
Aug 16 10:56:21 host-172-1-1-29 patroni[23174]: INFO:patroni.__main__:no action. I am (pg02), a secondary, and following a leader (pg01)
Aug 16 10:56:21 host-172-1-1-29 patroni[23174]: 2023-08-16 10:56:21,800 INFO: no action. I am (pg02), a secondary, and following a leader (pg01)
```

# patroni 修改配置

使用 `patronictl edit-config` 命令来修改 Patroni 集群的配置。例如，您可以使用以下命令来修改 `postgresql` 部分的 `max_connections` 参数：

```bash
patronictl -c /etc/patroni.yml edit-config
```

在执行上述命令后，您将进入一个文本编辑器，您可以在其中修改配置文件。例如，您可以在 `postgresql.parameters` 部分添加一行 `max_connections: 500` 来将 `max_connections` 参数的值设置为 500。

```yaml
postgresql:
  parameters:
    max_connections: 500
```

完成修改后，保存并退出文本编辑器。然后，您将被提示是否应用更改。输入 `y` 并按回车键确认应用更改。

## 不用进入编辑器

`patronictl -c /etc/patroni.yml edit-config -s 'postgresql.parameters.max_connections=500' `

或者

`patronictl -c /etc/patroni.yml edit-config -p 'max_connections=500' `

上面的修改不会同步到 `/etc/patroni.yml`
# Patroni是如何工作的

https://www.modb.pro/db/67114

# Pending restart 列的介绍
```
patronictl -c /etc/patroni.yml list

+ Cluster: yace_pgsql ---+---------+-----------+----+-----------+-----------------+
  | Member | Host          | Role    | State     | TL | Lag in MB | Pending restart |
  +--------+---------------+---------+-----------+----+-----------+-----------------+
  | pg01   | 172.1.1.95 | Replica | streaming |  2 |         0 |                 |
  | pg02   | 172.1.1.96 | Leader  | running   |  2 |           | *               |
  +--------+---------------+---------+-----------+----+-----------+-----------------+
```
在 Patroni 中，如果某些需要重启才能生效的选项被更改，那么对应节点的 `pending_restart` 标记将被设置。这意味着该节点需要重启才能使更改生效。您可以使用 `patronictl list` 命令来查看集群中每个节点的状态，包括 `pending_restart` 标记。当您重启对应节点后，`pending_restart` 标记将被重置。

## 添加空密码用户
groupadd postgres
useradd -d /home/postgres postgres -g postgres
echo "postgres ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers.d/postgres

# 高可用切换
## 手工切换
```sh
# 要求主库存活
patronictl -c /etc/patroni.yml switchover pgsql

# 不要求主库存活，强制切换
patronictl -c /etc/patroni.yml failover  pgsql
```

# 清理 etcd 中集群信息
```sh
patronictl -c /etc/patroni.yml remove 集群名称
```
