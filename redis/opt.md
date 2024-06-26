- [Redis Cluster 安装部署](#redis-cluster-安装部署)
  - [提前准备好各实例的配置文件，以6401为例](#提前准备好各实例的配置文件以6401为例)
  - [启动各Redis实例](#启动各redis实例)
  - [搭建Redis Cluster](#搭建redis-cluster)
  - [检查集群是否搭建完成、槽完全被分配](#检查集群是否搭建完成槽完全被分配)
  - [添加新节点到集群](#添加新节点到集群)
  - [给新节点分配槽](#给新节点分配槽)
  - [新节点置为从库](#新节点置为从库)
  - [收缩集群](#收缩集群)
  - [集群全局命令](#集群全局命令)
  - [集群节点命令](#集群节点命令)
  - [其它操作](#其它操作)
- [redis主从哨兵和集群的区别](#redis主从哨兵和集群的区别)
- [常用操作](#常用操作)
  - [关闭、启动](#关闭启动)
  - [基本命令](#基本命令)
- [主从复制命令](#主从复制命令)
- [查找大KEY](#查找大key)
- [Redis数据类型](#redis数据类型)
  - [字符串](#字符串)
  - [散列/哈希  每个散列/哈希可以存储多达2^32 - 1个健-值对(超过40亿个)](#散列哈希--每个散列哈希可以存储多达232---1个健-值对超过40亿个)
  - [列表](#列表)
  - [集合](#集合)
  - [可排序集合](#可排序集合)
- [REDIS跟MYSQL数据同步](#redis跟mysql数据同步)
- [击穿、穿透、雪崩](#击穿穿透雪崩)
  - [击穿](#击穿)
  - [穿透](#穿透)
  - [雪崩](#雪崩)
- [常用命令的函数调用链](#常用命令的函数调用链)
  - [set](#set)
  - [meet](#meet)
  - [forget](#forget)
  - [hmset](#hmset)
  - [lpush](#lpush)
  - [sadd](#sadd)
  - [zadd](#zadd)
  - [hash表查找](#hash表查找)
  - [gossip](#gossip)
  - [accept接受连接](#accept接受连接)
- [VSCODE调试redis的配置](#vscode调试redis的配置)
- [进程的文件句柄、端口查看](#进程的文件句柄端口查看)
- [客户端连接服务端时，为什么服务端触发两次EPOLLOUT](#客户端连接服务端时为什么服务端触发两次epollout)
  - [原因](#原因)
  - [服务端限制返回包最大64k](#服务端限制返回包最大64k)
  - [为什么客户端连接服务端后，服务端会返回那么大的包](#为什么客户端连接服务端后服务端会返回那么大的包)
- [查看RDB文件](#查看rdb文件)
- [rax结构](#rax结构)
- [源码阅读网站](#源码阅读网站)
- [源码文件描述](#源码文件描述)
- [redis跨机房部署方案](#redis跨机房部署方案)

# Redis Cluster 安装部署

参考 https://blog.csdn.net/zimu312500/article/details/123466423

OS 8.0
Redis  7.0
Redis node1 Master 127.0.0.1 6401 /data/redis/data/6401
Redis node1 Slave 127.0.0.1 6402 /data/redis/data/6402
Redis node2 Master 127.0.0.1 6403 /data/redis/data/6403
Redis node2 Slave 127.0.0.1 6404 /data/redis/data/6404
Redis node3 Master 127.0.0.1 6405 /data/redis/data/6405
Redis node3 Slave 127.0.0.1 6406 /data/redis/data/6406

```sh
wget https://download.redis.io/redis-stable.tar.gz  
tar -xzvf redis-stable.tar.gz  
cd redis-stable  
make  

mkdir -p /data/redis/{bin,data,conf,log}  
mkdir -p /data/redis/data/{6401..6406}  
make PREFIX=/data/redis/bin install  

./redis-server --version  
Redis server v=7.0.2 sha=00000000:0 malloc=jemalloc-5.2.1 bits=64 build=317a0dc33f11edb5
```

## 提前准备好各实例的配置文件，以6401为例

```sh
bind 0.0.0.0  
port 6401  
pidfile /var/run/redis_6401.pid  
logfile ""/data/redis/log/redis_6401.log""  
dir /data/redis/data/6401  
cluster-enabled yes  
cluster-node-timeout 15000  
cluster-config-file ""nodes-6401.conf""  
daemonize yes  
protected-mode yes
tcp-backlog 511  
timeout 0  
tcp-keepalive 300  
supervised no  
loglevel notice  
databases 16  
always-show-logo yes  
save 900 1  
save 300 10  
save 60 10000  
stop-writes-on-bgsave-error yes  
rdbcompression yes  
rdbchecksum yes  
dbfilename dump.rdb  
replica-serve-stale-data yes  
replica-read-only yes  
repl-diskless-sync no  
repl-diskless-sync-delay 5  
repl-disable-tcp-nodelay no  
replica-priority 100  
lazyfree-lazy-eviction no  
lazyfree-lazy-expire no  
lazyfree-lazy-server-del no  
replica-lazy-flush no  
appendonly no  
appendfilename ""appendonly.aof""  
appendfsync everysec  
no-appendfsync-on-rewrite no  
auto-aof-rewrite-percentage 100  
auto-aof-rewrite-min-size 64mb  
aof-load-truncated yes  
aof-use-rdb-preamble yes  
lua-time-limit 5000  
slowlog-log-slower-than 10000  
slowlog-max-len 128  
latency-monitor-threshold 0  
notify-keyspace-events """"  
hash-max-ziplist-entries 512  
hash-max-ziplist-value 64  
list-max-ziplist-size -2  
list-compress-depth 0  
set-max-intset-entries 512  
zset-max-ziplist-entries 128  
zset-max-ziplist-value 64  
hll-sparse-max-bytes 3000  
stream-node-max-bytes 4096  
stream-node-max-entries 100  
activerehashing yes  
client-output-buffer-limit normal 0 0 0  
client-output-buffer-limit replica 256mb 64mb 60  
client-output-buffer-limit pubsub 32mb 8mb 60  
hz 10  
dynamic-hz yes  
aof-rewrite-incremental-fsync yes  
rdb-save-incremental-fsync yes
```

## 启动各Redis实例

```sh
redis-server /data/redis/conf/redis_6401.conf
redis-server /data/redis/conf/redis_6402.conf
redis-server /data/redis/conf/redis_6403.conf
redis-server /data/redis/conf/redis_6404.conf
redis-server /data/redis/conf/redis_6405.conf
redis-server /data/redis/conf/redis_6406.conf
```

## 搭建Redis Cluster

cluster-replicas 设置为1表示分配1个Slave节点

```sh
./redis-cli --cluster-replicas 1 --cluster create 127.0.0.1:6401 127.0.0.1:6402 127.0.0.1:6403 127.0.0.1:6404 127.0.0.1:6405 127.0.0.1:6406
>>> Performing hash slots allocation on 6 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
Adding replica 127.0.0.1:6405 to 127.0.0.1:6401
Adding replica 127.0.0.1:6406 to 127.0.0.1:6402
Adding replica 127.0.0.1:6404 to 127.0.0.1:6403
>>> Trying to optimize slaves allocation for anti-affinity
[WARNING] Some slaves are in the same host as their master
M: 059779536a3fcbdd3e326f84dacc9bc5db52fa5b 127.0.0.1:6401
   slots:[0-5460] (5461 slots) master
M: b9aef8906f61806de8f84cfa6f90cde007c0bc9f 127.0.0.1:6402
   slots:[5461-10922] (5462 slots) master
M: 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 127.0.0.1:6403
   slots:[10923-16383] (5461 slots) master
S: c63b93805c90125453773de1458fd00ee3f26ae4 127.0.0.1:6404
   replicates 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c
S: a6fb5f4722d526a1a96d434ea2d66b700c3a7ed2 127.0.0.1:6405
   replicates 059779536a3fcbdd3e326f84dacc9bc5db52fa5b
S: 23b3d4319ab60bafb545bbfbaa963b2b56fad120 127.0.0.1:6406
   replicates b9aef8906f61806de8f84cfa6f90cde007c0bc9f
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join
.
>>> Performing Cluster Check (using node 127.0.0.1:6401)
M: 059779536a3fcbdd3e326f84dacc9bc5db52fa5b 127.0.0.1:6401
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
S: c63b93805c90125453773de1458fd00ee3f26ae4 127.0.0.1:6404
   slots: (0 slots) slave
   replicates 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c
S: 23b3d4319ab60bafb545bbfbaa963b2b56fad120 127.0.0.1:6406
   slots: (0 slots) slave
   replicates b9aef8906f61806de8f84cfa6f90cde007c0bc9f
M: 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 127.0.0.1:6403
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
M: b9aef8906f61806de8f84cfa6f90cde007c0bc9f 127.0.0.1:6402
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
S: a6fb5f4722d526a1a96d434ea2d66b700c3a7ed2 127.0.0.1:6405
   slots: (0 slots) slave
   replicates 059779536a3fcbdd3e326f84dacc9bc5db52fa5b
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
[root@VM-32-26-centos bin]#
```

## 检查集群是否搭建完成、槽完全被分配

```sh
./redis-cli --cluster check 127.0.0.1:6401
127.0.0.1:6401 (05977953...) -> 0 keys | 5461 slots | 1 slaves.
127.0.0.1:6403 (75fea4cb...) -> 0 keys | 5461 slots | 1 slaves.
127.0.0.1:6402 (b9aef890...) -> 0 keys | 5462 slots | 1 slaves.
[OK] 0 keys in 3 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 127.0.0.1:6401)
M: 059779536a3fcbdd3e326f84dacc9bc5db52fa5b 127.0.0.1:6401
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
S: c63b93805c90125453773de1458fd00ee3f26ae4 127.0.0.1:6404
   slots: (0 slots) slave
   replicates 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c
S: 23b3d4319ab60bafb545bbfbaa963b2b56fad120 127.0.0.1:6406
   slots: (0 slots) slave
   replicates b9aef8906f61806de8f84cfa6f90cde007c0bc9f
M: 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 127.0.0.1:6403
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
M: b9aef8906f61806de8f84cfa6f90cde007c0bc9f 127.0.0.1:6402
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
S: a6fb5f4722d526a1a96d434ea2d66b700c3a7ed2 127.0.0.1:6405
   slots: (0 slots) slave
   replicates 059779536a3fcbdd3e326f84dacc9bc5db52fa5b
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
[root@VM-32-26-centos bin]#
```

## 添加新节点到集群

添加新节点到集群，第一个地址为新节点IP和端口，第二个地址为集群中任意存在的节点即可

```sh
./redis-cli -p 6401 --cluster add-node 127.0.0.1:7401 127.0.0.1:6401
>>> Adding node 127.0.0.1:7401 to cluster 127.0.0.1:6401
>>> Performing Cluster Check (using node 127.0.0.1:6401)
M: 059779536a3fcbdd3e326f84dacc9bc5db52fa5b 127.0.0.1:6401
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
S: c63b93805c90125453773de1458fd00ee3f26ae4 127.0.0.1:6404
   slots: (0 slots) slave
   replicates 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c
S: 23b3d4319ab60bafb545bbfbaa963b2b56fad120 127.0.0.1:6406
   slots: (0 slots) slave
   replicates b9aef8906f61806de8f84cfa6f90cde007c0bc9f
M: 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 127.0.0.1:6403
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
M: b9aef8906f61806de8f84cfa6f90cde007c0bc9f 127.0.0.1:6402
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
S: a6fb5f4722d526a1a96d434ea2d66b700c3a7ed2 127.0.0.1:6405
   slots: (0 slots) slave
   replicates 059779536a3fcbdd3e326f84dacc9bc5db52fa5b
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
>>> Getting functions from cluster
>>> Send FUNCTION LIST to 127.0.0.1:7401 to verify there is no functions in it
>>> Send FUNCTION RESTORE to 127.0.0.1:7401
>>> Send CLUSTER MEET to node 127.0.0.1:7401 to make it join the cluster.
[OK] New node added correctly.
[root@VM-32-26-centos bin]#
```

新节点添加成功后，可以使用 cluster nodes命令查看集群节点列表信息

```sh
./redis-cli -p 6401 cluster nodes
c63b93805c90125453773de1458fd00ee3f26ae4 127.0.0.1:6404@16404 slave 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 0 1655552360248 3 connected
23b3d4319ab60bafb545bbfbaa963b2b56fad120 127.0.0.1:6406@16406 slave b9aef8906f61806de8f84cfa6f90cde007c0bc9f 0 1655552360000 2 connected
18d36784879469a0c26d867193b6098360b473e6 127.0.0.1:7401@17401 master - 0 1655552361000 0 connected
75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 127.0.0.1:6403@16403 master - 0 1655552361251 3 connected 10923-16383
059779536a3fcbdd3e326f84dacc9bc5db52fa5b 127.0.0.1:6401@16401 myself,master - 0 1655552358000 1 connected 0-5460
b9aef8906f61806de8f84cfa6f90cde007c0bc9f 127.0.0.1:6402@16402 master - 0 1655552360000 2 connected 5461-10922
a6fb5f4722d526a1a96d434ea2d66b700c3a7ed2 127.0.0.1:6405@16405 slave 059779536a3fcbdd3e326f84dacc9bc5db52fa5b 0 1655552359000 1 connected
[root@VM-32-26-centos bin]#
```

## 给新节点分配槽

Redis Cluster集群如果16384个槽全部被分配，那么分配槽给新加节点则需要使用reshard命令

```sh
./redis-cli -p 6401 --cluster  reshard 127.0.0.1:6401
>>> Performing Cluster Check (using node 127.0.0.1:6401)
M: 059779536a3fcbdd3e326f84dacc9bc5db52fa5b 127.0.0.1:6401
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
S: c63b93805c90125453773de1458fd00ee3f26ae4 127.0.0.1:6404
   slots: (0 slots) slave
   replicates 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c
S: 23b3d4319ab60bafb545bbfbaa963b2b56fad120 127.0.0.1:6406
   slots: (0 slots) slave
   replicates b9aef8906f61806de8f84cfa6f90cde007c0bc9f
M: 18d36784879469a0c26d867193b6098360b473e6 127.0.0.1:7401
   slots: (0 slots) master
M: 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 127.0.0.1:6403
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
M: b9aef8906f61806de8f84cfa6f90cde007c0bc9f 127.0.0.1:6402
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
S: a6fb5f4722d526a1a96d434ea2d66b700c3a7ed2 127.0.0.1:6405
   slots: (0 slots) slave
   replicates 059779536a3fcbdd3e326f84dacc9bc5db52fa5b
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
How many slots do you want to move (from 1 to 16384)? 2500
What is the receiving node ID? 18d36784879469a0c26d867193b6098360b473e6
Please enter all the source node IDs.
  Type 'all' to use all the nodes as source nodes for the hash slots.
  Type 'done' once you entered all the source nodes IDs.
Source node #1: all

Ready to move 2500 slots.
  Source nodes:
    M: 059779536a3fcbdd3e326f84dacc9bc5db52fa5b 127.0.0.1:6401
       slots:[0-5460] (5461 slots) master
       1 additional replica(s)
    M: 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 127.0.0.1:6403
       slots:[10923-16383] (5461 slots) master
       1 additional replica(s)
    M: b9aef8906f61806de8f84cfa6f90cde007c0bc9f 127.0.0.1:6402
       slots:[5461-10922] (5462 slots) master
       1 additional replica(s)
  Destination node:
    M: 18d36784879469a0c26d867193b6098360b473e6 127.0.0.1:7401
       slots: (0 slots) master
  Resharding plan:
    Moving slot 5461 from b9aef8906f61806de8f84cfa6f90cde007c0bc9f
    Moving slot 5462 from b9aef8906f61806de8f84cfa6f90cde007c0bc9f
 ……
    Moving slot 11755 from 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c
Do you want to proceed with the proposed reshard plan (yes/no)? yes
Moving slot 5461 from 127.0.0.1:6402 to 127.0.0.1:7401: 
Moving slot 5462 from 127.0.0.1:6402 to 127.0.0.1:7401: 
……
Moving slot 11755 from 127.0.0.1:6403 to 127.0.0.1:7401: 
[root@VM-32-26-centos bin]#
```

分配完毕后，通过cluster nodes查看槽位分配情况

```sh
./redis-cli -p 6401 cluster nodes
c63b93805c90125453773de1458fd00ee3f26ae4 127.0.0.1:6404@16404 slave 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 0 1655552726282 3 connected
23b3d4319ab60bafb545bbfbaa963b2b56fad120 127.0.0.1:6406@16406 slave b9aef8906f61806de8f84cfa6f90cde007c0bc9f 0 1655552726000 2 connected
18d36784879469a0c26d867193b6098360b473e6 127.0.0.1:7401@17401 master - 0 1655552727000 7 connected 0-832 5461-6294 10923-11755
75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 127.0.0.1:6403@16403 master - 0 1655552727284 3 connected 11756-16383
059779536a3fcbdd3e326f84dacc9bc5db52fa5b 127.0.0.1:6401@16401 myself,master - 0 1655552724000 1 connected 833-5460
b9aef8906f61806de8f84cfa6f90cde007c0bc9f 127.0.0.1:6402@16402 master - 0 1655552728287 2 connected 6295-10922
a6fb5f4722d526a1a96d434ea2d66b700c3a7ed2 127.0.0.1:6405@16405 slave 059779536a3fcbdd3e326f84dacc9bc5db52fa5b 0 1655552726000 1 connected
[root@VM-32-26-centos bin]#
```

## 新节点置为从库

第一种是随机被分配到从库较少的主节点（--cluster-slave）

```sh
./redis-cli -p 6401 --cluster add-node 127.0.0.1:7402 127.0.0.1:6401 --cluster-slave
>>> Adding node 127.0.0.1:7402 to cluster 127.0.0.1:6401
>>> Performing Cluster Check (using node 127.0.0.1:6401)
M: 059779536a3fcbdd3e326f84dacc9bc5db52fa5b 127.0.0.1:6401
   slots:[833-5460] (4628 slots) master
   1 additional replica(s)
S: c63b93805c90125453773de1458fd00ee3f26ae4 127.0.0.1:6404
   slots: (0 slots) slave
   replicates 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c
S: 23b3d4319ab60bafb545bbfbaa963b2b56fad120 127.0.0.1:6406
   slots: (0 slots) slave
   replicates b9aef8906f61806de8f84cfa6f90cde007c0bc9f
M: 18d36784879469a0c26d867193b6098360b473e6 127.0.0.1:7401
   slots:[0-832],[5461-6294],[10923-11755] (2500 slots) master
M: 75fea4cb3b2622fcd2b983ecd65ef7d3091b8c2c 127.0.0.1:6403
   slots:[11756-16383] (4628 slots) master
   1 additional replica(s)
M: b9aef8906f61806de8f84cfa6f90cde007c0bc9f 127.0.0.1:6402
   slots:[6295-10922] (4628 slots) master
   1 additional replica(s)
S: a6fb5f4722d526a1a96d434ea2d66b700c3a7ed2 127.0.0.1:6405
   slots: (0 slots) slave
   replicates 059779536a3fcbdd3e326f84dacc9bc5db52fa5b
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
Automatically selected master 127.0.0.1:7401
>>> Send CLUSTER MEET to node 127.0.0.1:7402 to make it join the cluster.
Waiting for the cluster to join

>>> Configure node as replica of 127.0.0.1:7401.
[OK] New node added correctly.
[root@VM-32-26-centos bin]#
```

第二种指定主节点建立复制关系，灾备场景、跨机房场景非常适用（--cluster-slave --cluster-master-id node_id）
除--cluster-slave外，还需使用--cluster-master-id指定需要复制的主节点node_id，该示例选择7401该主节点作为新节点的主库

```sh
redis-cli -p 6401 --cluster add-node 127.0.0.1:7402 127.0.0.1:6401 --cluster-slave --cluster-master-id 18d36784879469a0c26d867193b6098360b473e6
```

## 收缩集群

下线从节点

```sh
redis-cli --cluster del-node 127.0.0.1:7001 nodeID_7001
#del-node 后面跟着slave节点的 ip:port 和node ID
```

下线主节点

```sh
#先清空master的slot
redis-cli --cluster reshard 127.0.0.1:7000 --cluster-from nodeID_7000 --cluster-to nodeID_target --cluster-slots 1024 --cluster-yes
#下线（删除）节点
redis-cli --cluster del-node 127.0.0.1:7000 nodeID_7000
```

```sh
./redis-cli --cluster reshard 127.0.0.1:6379 --cluster-from e3d110e6bda857031747f21b60e00d8bd3071c4d --cluster-to 8dac64ca81f99d90d49dc790acf91841991d8963 --cluster-slots 10923-16383 --cluster-yes
……
Moving slot 16381 from 127.0.0.1:6381 to 127.0.0.1:6379: 
Moving slot 16382 from 127.0.0.1:6381 to 127.0.0.1:6379: 
Moving slot 16383 from 127.0.0.1:6381 to 127.0.0.1:6379:

./redis-cli --cluster del-node 127.0.0.1:6379 e3d110e6bda857031747f21b60e00d8bd3071c4d
>>> Removing node e3d110e6bda857031747f21b60e00d8bd3071c4d from cluster 127.0.0.1:6379
>>> Sending CLUSTER FORGET messages to the cluster...
>>> Sending CLUSTER RESET SOFT to the deleted node.
#
```

## 集群全局命令

```sh
cluster nodes 列出Redis Cluster各节点信息与槽位分布
redis-cli -p 6401 cluster nodes

cluster info 输出集群整体信息
redis-cli -p 6401 cluster info
```

## 集群节点命令

```sh
cluster replicate 将当前节点与指定node_id的主节点建立复制
cluster forget 将指定node_id的节点从集群中移除
[root@VM-32-26-centos bin]# ./redis-cli -c -h 127.0.0.1 -p 6401 cluster forget c0331f8d562a992930b14504ce68390407354ce4
OK
[root@VM-32-26-centos bin]#
```

## 其它操作

```sh
ps -ef|grep 7402
kill 1649516
rm -rf //data/redis/data/7402/*
./redis-server /data/redis/conf/redis_7402.conf
./redis-cli -p 6401 --cluster add-node 127.0.0.1:7402 127.0.0.1:6401 --cluster-slave --cluster-master-id 18d36784879469a0c26d867193b6098360b473e6
```

# redis主从哨兵和集群的区别

- 一、架构不同
  　　redis主从：一主多从；
  　　redis集群：多主多从；
- 二、存储不同
  　　redis主从：主节点和从节点都是存储所有数据；
  　　redis集群：数据的存储是通过hash计算16384的槽位，算出要将数据存储的节点，然后进行存储；
- 三、选举不同
  　　redis主从：通过启动redis自带的哨兵（sentinel）集群进行选举，也可以是一个哨兵
  　　　　选举流程：1、先发现主节点fail的哨兵，将成为哨兵中的leader，之后的主节点选举将通过这个leader进行故障转移操作，从存活的slave中选举新的master，新　　的master选举同集群的master节点选举类似；
  　　redis集群：集群可以自己进行选举
  　　　　选举流程：1、当主节点挂掉，从节点就会广播该主节点fail；
  　　　　　　　　　2、延迟时间后进行选举（延迟的时间算法为：延迟时间+随机数+rank*1000，从节点数据越多，rank越小，因为主从数据复制是异步进行的，所以　　所有的从节点的数据可能会不同），
  延迟的原因是等待主节点fail广播到所有存活的主节点，否则主节点会拒绝参加选举；
  　　　　　　　　　3、参加选举的从节点向所有的存活的节点发送ack请求，但只有主节点会回复它，并且主节点只会回复第一个到达参加选举的从节点，一半以上的主节点回复，
  该节点就会成为主节点，广播告诉其他节点该节点成为主节点。
- 四、节点扩容不同
  　　redis主从：只能扩容从节点，无法对主节点进行扩容；
  　　redis集群：可以扩容整个主从节点，但是扩容后需要进行槽位的分片，否则无法进行数据写入

# 常用操作

## 关闭、启动

```sh
关闭 /apps/svr/redis-2.8.19/bin/redis-cli -p 6370 shutdown  
启动 /apps/svr/redis-2.8.19/bin/redis-server /apps/conf/redis/redis7900.conf
```

## 基本命令

```sh
#查看所有key
keys *  或  keys ""*""
#查看匹配前缀的keys
keys ""miao*""
#清空redis
flushdb
#随机取出一个key
randomkey
#查看key的类型
type key
#查看数据库中key的数量
dbsize
#查看服务器信息
info
#查看redis正在做什么
monitor
#查看日志
slowlog get
slowlog get 10


redis-cli -p 6381  config set maxmemory 8589934592
redis-cli -p 6381  config get maxmemory

127.0.0.1:6401> client list
id=6 addr=127.0.0.1:59288 laddr=127.0.0.1:6401 fd=20 name= age=3888 idle=1 flags=S db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=20474 argv-mem=0 multi-mem=0 rbs=1024 rbp=0 obl=0 oll=1 omem=20504 tot-me2
id=39 addr=127.0.0.1:39192 laddr=127.0.0.1:6401 fd=22 name= age=627 idle=1 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=26 qbuf-free=20448 argv-mem=10 multi-mem=0 rbs=1024 rbp=0 obl=0 oll=0 omem=0 tot-mem=2
```

# 主从复制命令

| 命令 | 功能 | 备注 |
| --- | --- | --- |
| SLAVEOF  host port | 客户端连接的Redis服务器将成为指定地址的Redis服务器的从服务器 |  |
| SLAVEOF no one | 客户端连接的Redis服务器从从服务器升级为主服务器 |  |
| PSYNC  runid offset | 从服务器向主服务器发送（即从服务器作为主服务器的client）；如果主服务器返回+CONTINE，进行部分重同步，否则进行完整重同步 |  |
| PSYNC  ? -1 | 从服务器向主服务器发送（同上）；进行完整重同步 |  |

# 查找大KEY

```sh
[root@VM-32-26-centos bin]# ./redis-cli -p 6401 --bigkeys

# Scanning the entire keyspace to find biggest keys as well as
# average sizes per key type.  You can use -i 0.1 to sleep 0.1 sec
# per 100 SCAN commands (not usually needed).


-------- summary -------

Sampled 0 keys in the keyspace!
Total key length in bytes is 0 (avg len 0.00)


0 hashs with 0 fields (00.00% of keys, avg size 0.00)
0 lists with 0 items (00.00% of keys, avg size 0.00)
0 strings with 0 bytes (00.00% of keys, avg size 0.00)
0 streams with 0 entries (00.00% of keys, avg size 0.00)
0 sets with 0 members (00.00% of keys, avg size 0.00)
0 zsets with 0 members (00.00% of keys, avg size 0.00)
[root@VM-32-26-centos bin]#
```

# Redis数据类型

## 字符串

Redis中的字符串是一个字节序列。Redis中的字符串是二进制安全的，这意味着它们的长度不由任何特殊的终止字符决定。因此，可以在一个字符串中存储高达512M字节的任何内容。

```sh
127.0.0.1:6401> set name ""yiibai.com"" 
(error) MOVED 5798 127.0.0.1:7401
127.0.0.1:6401> get name
(error) MOVED 5798 127.0.0.1:7401
```

## 散列/哈希  每个散列/哈希可以存储多达2^32 - 1个健-值对(超过40亿个)

```sh
127.0.0.1:6401> HMSET ukey username ""yiibai"" password ""passswd123"" points 200
OK
127.0.0.1:6401> hmget ukey password
1) ""passswd123""
127.0.0.1:6401> HGETALL ukey
1) ""username""
2) ""yiibai""
3) ""password""
4) ""passswd123""
5) ""points""
6) ""200""
```

## 列表

列表的最大长度为2^32 - 1个元素(4294967295，每个列表可容纳超过40亿个元素)
Redis列表只是字符串列表，按插入顺序排序。您可以向Redis列表的头部或尾部添加元素

```sh
127.0.0.1:6401> lpush alist redis 
(integer) 1
127.0.0.1:6401> lpush alist mongodb 
(integer) 2
127.0.0.1:6401> lrange alist 0 1
1) ""mongodb""
2) ""redis""
127.0.0.1:6401> lrange alist 0 0
1) ""mongodb""
127.0.0.1:6401>
```

## 集合

一个集合中的最大成员数量为2^32 - 1(即4294967295，每个集合中元素数量可达40亿个)个

```sh
redis 127.0.0.1:6379> sadd yiibailist redis 
(integer) 1 
redis 127.0.0.1:6379> sadd yiibailist mongodb 
(integer) 1 
redis 127.0.0.1:6379> sadd yiibailist sqlite 
(integer) 1 
redis 127.0.0.1:6379> sadd yiibailist sqlite 
(integer) 0 
redis 127.0.0.1:6379> smembers yiibailist  
1) ""sqlite"" 
2) ""mongodb"" 
3) ""redis""
```

## 可排序集合

```sh
redis 127.0.0.1:6379> zadd yiibaiset 0 redis
(integer) 1 
redis 127.0.0.1:6379> zadd yiibaiset 0 mongodb
(integer) 1 
redis 127.0.0.1:6379> zadd yiibaiset 1 sqlite
(integer) 1 
redis 127.0.0.1:6379> zadd yiibaiset 1 sqlite
(integer) 0 
redis 127.0.0.1:6379> ZRANGEBYSCORE yiibaiset 0 1000  
1) ""mongodb"" 
2) ""redis"" 
3) ""sqlite""
```

# REDIS跟MYSQL数据同步

1、先清除缓存，再更新数据库的方式显然是不行的，可能存在数据永远不正确的情况。
2、先更新数据库再清缓存的方式，虽然可能会存在少数的错误数据的情况，但是相对来说，后续的查询可以得到更新的值。

# 击穿、穿透、雪崩

## 击穿

redis缓存击穿是指某一个非常热点的key(即在客户端搜索的比较多的关键字)突然失效了,这时从客户端发送的大量的请求在redis里找不到这个key，就会去数据里找，最终导致数据库压力过大崩掉。
解决：

- 1.将value的时效设置成永不过期 这种方式非常简单粗暴但是安全可靠。但是非常占用空间对内存消耗也是极大。个人并不建议使用该方法，应该根据具体业务逻辑来操作。
- 2.使用Timetask做一个定时任务 使用Timetask做定时，每隔一段时间对一些热点key进行数据库查询，将查询出的结果更新至redis中。前条件是不会给数据库过大的压力。
- 3.通过synchronized+双重检查机制 当发生reids穿透的时候，这时海量请求发送到数据库。这时我们的解决办法是只让只让一个线程去查询这个热点key，其它线程保持阻塞状态(可以让它们sleep几秒)。
  当这个进入数据库的线程查询出key对应的value时，我们再将其同步至redis的缓存当中，其它线程睡醒以后再重新去redis里边请求数据

## 穿透

因为不良用户恶意频繁查询才会对系统造成很大的问题: key缓存并且数据库不存在，所以每次查询都会查询数据库从而导致数据库崩溃。
解决：

- 1.当类似的请求发过来，无论查出什么结果都放入redis缓存
- 2.拉黑其ip
- 3.对请求的参数进行合法性校验，在判断其不合法的前提下直接return掉
- 4.使用布隆过滤器。布隆过滤器可能会造成误判，从而穿透redis进入DB，但是这个误判概率是非常小的。

## 雪崩

和击穿类似，不同的是击穿是一个热点key某时刻失效，而雪崩是大量的热点key在一瞬间失效
解决：

- 1.设置缓存时,随机初始化其失效时间。如果是redis的key同时失效,可采取该办法,具体失效时间根据业务情况决定…
- 2.将不同的热点key放置到不同的节点上去。因redis一般都是集群部署,将不同的热点key平均的放置到不同节点,也可以有效避免雪崩。
- 3.将value的时效设置成永不过期
- 4.使用Timetask做一个定时任务，在失效之前重新刷redis缓存

# 常用命令的函数调用链

## set

```cpp
#set a 123
dbAdd(redisDb * db, robj * key, robj * val) (\data\redis\src\db.c:189)
setKey(client * c, redisDb * db, robj * key, robj * val, int flags) (\data\redis\src\db.c:270)
setGenericCommand(client * c, int flags, robj * key, robj * val, robj * expire, int unit, robj * ok_reply, robj * abort_reply) (\data\redis\src\t_string.c:111)
setCommand(client * c) (\data\redis\src\t_string.c:302)
call(client * c, int flags) (\data\redis\src\server.c:3374)
processCommand(client * c) (\data\redis\src\server.c:4008)
processCommandAndResetClient(client * c) (\data\redis\src\networking.c:2469)
processInputBuffer(client * c) (\data\redis\src\networking.c:2573)
readQueryFromClient(connection * conn) (\data\redis\src\networking.c:2709)
callHandler(connection * conn, ConnectionCallbackFunc handler) (\data\redis\src\connhelpers.h:79)
connSocketEventHandler(struct aeEventLoop * el, int fd, void * clientData, int mask) (\data\redis\src\connection.c:310)
aeProcessEvents(aeEventLoop * eventLoop, int flags) (\data\redis\src\ae.c:436)
aeMain(aeEventLoop * eventLoop) (\data\redis\src\ae.c:496)
main(int argc, char ** argv) (\data\redis\src\server.c:7156)
```

## meet

```cpp
#cluster meet 127.0.0.1 6381 16381
clusterStartHandshake(char * ip, int port, int cport) (\data\redis\src\cluster.c:1596)
clusterCommand(client * c) (\data\redis\src\cluster.c:5279)
call(client * c, int flags) (\data\redis\src\server.c:3374)
processCommand(client * c) (\data\redis\src\server.c:4008)
processCommandAndResetClient(client * c) (\data\redis\src\networking.c:2469)
processInputBuffer(client * c) (\data\redis\src\networking.c:2573)
readQueryFromClient(connection * conn) (\data\redis\src\networking.c:2709)
callHandler(connection * conn, ConnectionCallbackFunc handler) (\data\redis\src\connhelpers.h:79)
connSocketEventHandler(struct aeEventLoop * el, int fd, void * clientData, int mask) (\data\redis\src\connection.c:310)
aeProcessEvents(aeEventLoop * eventLoop, int flags) (\data\redis\src\ae.c:436)
aeMain(aeEventLoop * eventLoop) (\data\redis\src\ae.c:496)
main(int argc, char ** argv) (\data\redis\src\server.c:7156)
```

## forget

```

```

## hmset

```cpp
#hmset hmkey name ldc passwd ldc sex m age 18
sdsdup(const sds s) (\data\redis\src\sds.c:190)
dbAdd(redisDb * db, robj * key, robj * val) (\data\redis\src\db.c:189)
hashTypeLookupWriteOrCreate(client * c, robj * key) (\data\redis\src\t_hash.c:443)
hsetCommand(client * c) (\data\redis\src\t_hash.c:609)
call(client * c, int flags) (\data\redis\src\server.c:3374)
processCommand(client * c) (\data\redis\src\server.c:4008)
processCommandAndResetClient(client * c) (\data\redis\src\networking.c:2469)
processInputBuffer(client * c) (\data\redis\src\networking.c:2573)
readQueryFromClient(connection * conn) (\data\redis\src\networking.c:2709)
callHandler(connection * conn, ConnectionCallbackFunc handler) (\data\redis\src\connhelpers.h:79)
connSocketEventHandler(struct aeEventLoop * el, int fd, void * clientData, int mask) (\data\redis\src\connection.c:310)
aeProcessEvents(aeEventLoop * eventLoop, int flags) (\data\redis\src\ae.c:436)
aeMain(aeEventLoop * eventLoop) (\data\redis\src\ae.c:496)
main(int argc, char ** argv) (\data\redis\src\server.c:7156)
```

## lpush

```cpp
#lpush lkey mysql redis
dbAdd(redisDb * db, robj * key, robj * val) (\data\redis\src\db.c:189)
pushGenericCommand(client * c, int where, int xx) (\data\redis\src\t_list.c:250)
lpushCommand(client * c) (\data\redis\src\t_list.c:267)
call(client * c, int flags) (\data\redis\src\server.c:3374)
processCommand(client * c) (\data\redis\src\server.c:4008)
processCommandAndResetClient(client * c) (\data\redis\src\networking.c:2469)
processInputBuffer(client * c) (\data\redis\src\networking.c:2573)
readQueryFromClient(connection * conn) (\data\redis\src\networking.c:2709)
callHandler(connection * conn, ConnectionCallbackFunc handler) (\data\redis\src\connhelpers.h:79)
connSocketEventHandler(struct aeEventLoop * el, int fd, void * clientData, int mask) (\data\redis\src\connection.c:310)
aeProcessEvents(aeEventLoop * eventLoop, int flags) (\data\redis\src\ae.c:436)
aeMain(aeEventLoop * eventLoop) (\data\redis\src\ae.c:496)
main(int argc, char ** argv) (\data\redis\src\server.c:7156)
```

## sadd

```cpp
#sadd skey 123 test mysql hello
dbAdd(redisDb * db, robj * key, robj * val) (\data\redis\src\db.c:189)
saddCommand(client * c) (\data\redis\src\t_set.c:312)
call(client * c, int flags) (\data\redis\src\server.c:3374)
processCommand(client * c) (\data\redis\src\server.c:4008)
processCommandAndResetClient(client * c) (\data\redis\src\networking.c:2469)
processInputBuffer(client * c) (\data\redis\src\networking.c:2573)
readQueryFromClient(connection * conn) (\data\redis\src\networking.c:2709)
callHandler(connection * conn, ConnectionCallbackFunc handler) (\data\redis\src\connhelpers.h:79)
connSocketEventHandler(struct aeEventLoop * el, int fd, void * clientData, int mask) (\data\redis\src\connection.c:310)
aeProcessEvents(aeEventLoop * eventLoop, int flags) (\data\redis\src\ae.c:436)
aeMain(aeEventLoop * eventLoop) (\data\redis\src\ae.c:496)
main(int argc, char ** argv) (\data\redis\src\server.c:7156)
```

## zadd

```cpp
#zadd zkey 91 she 92 he 93 me
dbAdd(redisDb * db, robj * key, robj * val) (\data\redis\src\db.c:189)
zaddGenericCommand(client * c, int flags) (\data\redis\src\t_zset.c:1754)
zaddCommand(client * c) (\data\redis\src\t_zset.c:1795)
call(client * c, int flags) (\data\redis\src\server.c:3374)
processCommand(client * c) (\data\redis\src\server.c:4008)
processCommandAndResetClient(client * c) (\data\redis\src\networking.c:2469)
processInputBuffer(client * c) (\data\redis\src\networking.c:2573)
readQueryFromClient(connection * conn) (\data\redis\src\networking.c:2709)
callHandler(connection * conn, ConnectionCallbackFunc handler) (\data\redis\src\connhelpers.h:79)
connSocketEventHandler(struct aeEventLoop * el, int fd, void * clientData, int mask) (\data\redis\src\connection.c:310)
aeProcessEvents(aeEventLoop * eventLoop, int flags) (\data\redis\src\ae.c:436)
aeMain(aeEventLoop * eventLoop) (\data\redis\src\ae.c:496)
main(int argc, char ** argv) (\data\redis\src\server.c:7156)
```

## hash表查找

```cpp
siphash_nocase(const uint8_t * in, const size_t inlen, const uint8_t * k) (\data\redis\src\siphash.c:193)
dictGenCaseHashFunction(const unsigned char * buf, size_t len) (\data\redis\src\dict.c:91)
dictSdsCaseHash(const void * key) (\data\redis\src\server.c:290)
dictFind(dict * d, const void * key) (\data\redis\src\dict.c:521)
dictFetchValue(dict * d, const void * key) (\data\redis\src\dict.c:538)
lookupCommandLogic(dict * commands, robj ** argv, int argc, int strict) (\data\redis\src\server.c:3032)
lookupCommand(robj ** argv, int argc) (\data\redis\src\server.c:3048)
processCommand(client * c) (\data\redis\src\server.c:3697)
processCommandAndResetClient(client * c) (\data\redis\src\networking.c:2469)
processInputBuffer(client * c) (\data\redis\src\networking.c:2573)
readQueryFromClient(connection * conn) (\data\redis\src\networking.c:2709)
callHandler(connection * conn, ConnectionCallbackFunc handler) (\data\redis\src\connhelpers.h:79)
connSocketEventHandler(struct aeEventLoop * el, int fd, void * clientData, int mask) (\data\redis\src\connection.c:310)
aeProcessEvents(aeEventLoop * eventLoop, int flags) (\data\redis\src\ae.c:436)
aeMain(aeEventLoop * eventLoop) (\data\redis\src\ae.c:496)
main(int argc, char ** argv) (\data\redis\src\server.c:7156)
```

## gossip

```cpp
clusterProcessPacket(clusterLink * link) (\data\redis\src\cluster.c:2102)
clusterReadHandler(connection * conn) (\data\redis\src\cluster.c:2758)
callHandler(connection * conn, ConnectionCallbackFunc handler) (\data\redis\src\connhelpers.h:79)
connSocketEventHandler(struct aeEventLoop * el, int fd, void * clientData, int mask) (\data\redis\src\connection.c:310)
aeProcessEvents(aeEventLoop * eventLoop, int flags) (\data\redis\src\ae.c:436)
aeMain(aeEventLoop * eventLoop) (\data\redis\src\ae.c:496)
main(int argc, char ** argv) (\data\redis\src\server.c:7156)
```

## accept接受连接

```cpp
clusterConnAcceptHandler(connection * conn) (\data\redis\src\cluster.c:840)
callHandler(connection * conn, ConnectionCallbackFunc handler) (\data\redis\src\connhelpers.h:79)
connSocketAccept(connection * conn, ConnectionCallbackFunc accept_handler) (\data\redis\src\connection.c:220)
connAccept(connection * conn, ConnectionCallbackFunc accept_handler) (\data\redis\src\connection.h:109)
clusterAcceptHandler(aeEventLoop * el, int fd, void * privdata, int mask) (\data\redis\src\cluster.c:902)
aeProcessEvents(aeEventLoop * eventLoop, int flags) (\data\redis\src\ae.c:436)
aeMain(aeEventLoop * eventLoop) (\data\redis\src\ae.c:496)
main(int argc, char ** argv) (\data\redis\src\server.c:7156)
```

# VSCODE调试redis的配置

```json
cat .vscode/tasks.json 
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build", 
            "type": "shell", 
            "command": "make",
            "args": [
                "CFLAGS=\"-g -O0\""
            ]
        }
    ]
}

cat .vscode/launch.json 
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        
        {
            "name": "redis",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/src/redis-server",
            "args": [
                "redis.conf",
                "--loglevel debug",
                "--cluster-enabled yes",
                "--cluster-config-file nodes-6379.conf"
            ],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "preLaunchTask": "build",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                },
                {
                    "description":  "Set Disassembly Flavor to Intel",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                }
          ]
        }
    ]
}
```

# 进程的文件句柄、端口查看

```sh
lsof -c redis-server
COMMAND    PID USER   FD      TYPE             DEVICE  SIZE/OFF      NODE NAME
redis-ser 7063 root  cwd       DIR              253,2      4096 237077793 /data/redis
redis-ser 7063 root  rtd       DIR              253,2       256        64 /
redis-ser 7063 root  txt       REG              253,2  13815304 381165668 /data/redis/src/redis-server
redis-ser 7063 root  mem       REG              253,2 106176928   6296770 /usr/lib/locale/locale-archive
redis-ser 7063 root  mem       REG              253,2   2156592     10419 /usr/lib64/libc-2.17.so
redis-ser 7063 root  mem       REG              253,2    142144     10450 /usr/lib64/libpthread-2.17.so
redis-ser 7063 root  mem       REG              253,2     43712     31011 /usr/lib64/librt-2.17.so
redis-ser 7063 root  mem       REG              253,2     19248     10426 /usr/lib64/libdl-2.17.so
redis-ser 7063 root  mem       REG              253,2   1136944     10428 /usr/lib64/libm-2.17.so
redis-ser 7063 root  mem       REG              253,2    163312     10411 /usr/lib64/ld-2.17.so
redis-ser 7063 root    0u      CHR             136,15       0t0        18 /dev/pts/15
redis-ser 7063 root    1u      CHR             136,15       0t0        18 /dev/pts/15
redis-ser 7063 root    2u      CHR             136,15       0t0        18 /dev/pts/15
redis-ser 7063 root    3u     unix 0xffff9117b95fb000       0t0  54206230 socket
redis-ser 7063 root    4u     unix 0xffff9117b95f8800       0t0  54206231 socket
redis-ser 7063 root    5r     FIFO               0,13       0t0  54206258 pipe
redis-ser 7063 root    6w     FIFO               0,13       0t0  54206258 pipe
redis-ser 7063 root    7u  a_inode               0,14         0      9082 [eventpoll]
redis-ser 7063 root    8u     IPv4           54209317       0t0       TCP localhost:6379 (LISTEN)
redis-ser 7063 root    9u     IPv6           54212914       0t0       TCP localhost:6379 (LISTEN)
```

# 客户端连接服务端时，为什么服务端触发两次EPOLLOUT
## 原因
1. 客户端connect后，触发服务端accept，触发EPOLLOUT
2. epoll使用et模式
3. redis限制返回客户端的buffer最大64k
4. 当redis返回客户端的包超过64k时,就会多次触发

## 服务端限制返回包最大64k
```cpp
int writeToClient(client *c, int handler_installed) {       //ldc:把c->buf回复给client.  如果handler_installed不为0,则把c->conn->write_handler设置为NULL. handler_installed一直为0
    /* Update total number of writes on server */
    atomicIncr(server.stat_total_writes_processed, 1);

    ssize_t nwritten = 0, totwritten = 0;

    while(clientHasPendingReplies(c)) {
        int ret = _writeToClient(c, &nwritten);
        if (ret == C_ERR) break;
        totwritten += nwritten;
        ……
        if (totwritten > NET_MAX_WRITES_PER_EVENT &&        //ldc:限制每次write包最大为1024*64
            (server.maxmemory == 0 ||
             zmalloc_used_memory() < server.maxmemory) &&
            !(c->flags & CLIENT_SLAVE)) break;
    }

    ……
    if (!clientHasPendingReplies(c)) {      //ldc:如果c->reply的内容为空，则删除epollout事件
        c->sentlen = 0;
        /* Note that writeToClient() is called in a threaded way, but
         * aeDeleteFileEvent() is not thread safe: however writeToClient()
         * is always called with handler_installed set to 0 from threads
         * so we are fine. */
        if (handler_installed) {
            serverAssert(io_threads_op == IO_THREADS_OP_IDLE);
            connSetWriteHandler(c->conn, NULL);
        }
        ……
    }
    ……
    return C_OK;
}
```
## 为什么客户端连接服务端后，服务端会返回那么大的包
```c
#在此处断点
int aeProcessEvents(aeEventLoop *eventLoop, int flags)
{
    ……

            /* Fire the writable event. */
            if (fe->mask & mask & AE_WRITABLE) {
                if (!fired || fe->wfileProc != fe->rfileProc) {
                    fe->wfileProc(eventLoop,fd,fe->clientData,mask);
                    fired++;
                }
            }
   ……
}

#查看客户端的端口
lsof -p 服务端端口
……
redis-ser 51606 root    7u  a_inode               0,14         0      9082 [eventpoll]
redis-ser 51606 root    8u     IPv4           95975218       0t0       TCP localhost:6379 (LISTEN)
redis-ser 51606 root    9u     IPv6           95975219       0t0       TCP localhost:6379 (LISTEN)
redis-ser 51606 root   10u     IPv4           96010078       0t0       TCP localhost:6379->localhost:60760 (ESTABLISHED)
……

#抓包(发送到客户端的包)
tcpdump -i lo dst port 60760

#结果
11:02:30.221954 IP localhost.6379 > localhost.60760: Flags [.], ack 303000843, win 512, options [nop,nop,TS val 2353488535 ecr 2353442526], length 0

11:02:42.906935 IP localhost.6379 > localhost.60760: Flags [.], seq 0:32768, ack 1, win 512, options [nop,nop,TS val 2353501220 ecr 2353442526], length 32768: RESP "ptional" "multiple" "exists" "summary" "Determine if a key exists" "since" "1.0.0" "group" "generic" "complexity" "O(N) where N is the number of keys to check." "history" "3.0.3" "Accepts multiple `key` arguments." "arguments" "name" "key" "type" "key" "key_spec_index" "0" "flags" "multiple" "config" "summary"
……
"optional" "arguments" "name" "min-idle-time" "type" "integer" "token" "IDLE" "since" "6.2.0" "flags" "optional" "name" "start" "type" "string" "name" "end" "type" "string" "name" "count" "type" "integer" "name" "consumer" "type" "string" "flags" "optional" "subscribe" "summary" "Listen for messages published to the given channels" "since" "2.0.0" "group" "pubsub" "complexity" "O(N) where N is the number of channels to subscribe to." "arguments" "name" "channel" "type" "string" "flags" "multiple"

11:03:07.597960 IP localhost.6379 > localhost.60760: Flags [.], ack 1, win 512, options [nop,nop,TS val 2353525911 ecr 2353510438], length 0

# 上面的内容是服务端告诉客户端的命令集合
```
# 查看RDB文件
```sh
# ./redis-check-rdb ../dump.rdb 
[offset 0] Checking RDB file ../dump.rdb
[offset 26] AUX FIELD redis-ver = '7.0.8'
[offset 40] AUX FIELD redis-bits = '64'
[offset 52] AUX FIELD ctime = '1679884024'
[offset 67] AUX FIELD used-mem = '1023800'
[offset 85] AUX FIELD repl-stream-db = '0'
[offset 135] AUX FIELD repl-id = 'b3e2df4983add09fd168d3f4069131e58a6381b1'
[offset 153] AUX FIELD repl-offset = '56527'
[offset 165] AUX FIELD aof-base = '0'
[offset 167] Selecting DB ID 0
[offset 184] Checksum OK
[offset 184] \o/ RDB looks OK! \o/
[info] 1 keys read
[info] 0 expires
[info] 0 already expired
```
```sh
# hexdump -cx ../dump.rdb
0000000   R   E   D   I   S   0   0   1   0 372  \t   r   e   d   i   s
0000000    4552    4944    3053    3130    fa30    7209    6465    7369
0000010   -   v   e   r 005   7   .   0   .   8 372  \n   r   e   d   i
0000010    762d    7265    3705    302e    382e    0afa    6572    6964
0000020   s   -   b   i   t   s 300   @ 372 005   c   t   i   m   e 302
0000020    2d73    6962    7374    40c0    05fa    7463    6d69    c265
0000030 370 376       d 372  \b   u   s   e   d   -   m   e   m 302   8
0000030    fef8    6420    08fa    7375    6465    6d2d    6d65    38c2
0000040 237 017  \0 372 016   r   e   p   l   -   s   t   r   e   a   m
0000040    0f9f    fa00    720e    7065    2d6c    7473    6572    6d61
0000050   -   d   b 300  \0 372  \a   r   e   p   l   -   i   d   (   b
0000050    642d    c062    fa00    7207    7065    2d6c    6469    6228
0000060   3   e   2   d   f   4   9   8   3   a   d   d   0   9   f   d
0000060    6533    6432    3466    3839    6133    6464    3930    6466
0000070   1   6   8   d   3   f   4   0   6   9   1   3   1   e   5   8
0000070    3631    6438    6633    3034    3936    3331    6531    3835
0000080   a   6   3   8   1   b   1 372  \v   r   e   p   l   -   o   f
0000080    3661    3833    6231    fa31    720b    7065    2d6c    666f
0000090   f   s   e   t 302 317 334  \0  \0 372  \b   a   o   f   -   b
0000090    7366    7465    cfc2    00dc    fa00    6108    666f    622d
00000a0   a   s   e 300  \0 376  \0 373 001  \0  \0 001   b 300   { 377
00000a0    7361    c065    fe00    fb00    0001    0100    c062    ff7b
00000b0   B 212 213   > 016 252   R 016                                
00000b0    8a42    3e8b    aa0e    0e52                                
00000b8
```
# rax结构
官网的图
```cpp
 *                    (f) ""
 *                    /
 *                 (i o) "f"
 *                 /   \
 *    "firs"  ("rst")  (o) "fo"
 *              /        \
 *    "first" []       [t   b] "foo"
 *                     /     \
 *           "foot" ("er")    ("ar") "foob"
 *                    /          \
 *          "footer" []          [] "foobar"
```
消费者组的图
![](pic/rax.png)

# 源码阅读网站
https://fossies.org/dox/redis-7.0.10/structredisServer.html
# 源码文件描述

```cpp
acl.c                 ACL权限控制
adlist.c              1
adlist.h              1
ae.c                  服务端和客户端实现-事件驱动
ae_epoll.c            服务端和客户端实现-事件驱动
ae_evport.c           1
ae.h                  1
ae_kqueue.c           1
ae_select.c           1
anet.c                服务端和客户端实现-网络连接
anet.h                1
aof.c                 持久化-aof
asciilogo.h           logo图形
atomicvar.h           原子操作
bio.c                 1
bio.h                 1
bitops.c              1
blocked.c             1
call_reply.c          1
call_reply.h          1
childinfo.c           1
cli_common.c          1
cli_common.h          1
cluster.c             其它-集群
cluster.h             1
commands              1
commands.c            1
config.c              1
config.h              1
connection.c          1
connection.h          1
connhelpers.h         1
crc16.c               1
crc16_slottable.h     1
crc64.c               1
crc64.h               1
crcspeed.c            1
crcspeed.h            1
db.c                  数据库的底层实现
debug.c               1
debugmacro.h          1
defrag.c              1
dict.c                基本数据结构-字典
dict.h                1
endianconv.c          1
endianconv.h          1
eval.c                1
evict.c               淘汰过期KEY
expire.c              处理过期KEY
fmacros.h             1
function_lua.c        1
functions.c           1
functions.h           1
geo.c                 1
geo.h                 1
geohash.c             1
geohash.h             1
geohash_helper.c      1
geohash_helper.h      1
help.h                1
hyperloglog.c         1
intset.c              基本数据结构-整数集合
intset.h              1
latency.c             1
latency.h             1
lazyfree.c            1
listpack.c            基本数据结构-Streams
listpack.h            1
listpack_malloc.h     1
localtime.c           1
lolwut5.c             1
lolwut6.c             1
lolwut.c              1
lolwut.h              1
lzf_c.c               1
lzf_d.c               1
lzf.h                 1
lzfP.h                1
Makefile              1
memtest.c             1
mkreleasehdr.sh       1
module.c              1
modules               1
monotonic.c           1
monotonic.h           1
mt19937-64.c          1
mt19937-64.h          1
multi.c               1
networking.c          服务端和客户端实现-网络连接
notify.c              1
object.c              数据类型的底层实现-redis对象
pqsort.c              1
pqsort.h              1
pubsub.c              1
quicklist.c           基本数据结构-快速链表
quicklist.h           1
rand.c                1
rand.h                1
rax.c                 RAX树
rax.h                 1
rax_malloc.h          1
rdb.c                 持久化-rdb
rdb.h                 1
redisassert.c         1
redisassert.h         1
redis-benchmark       1
redis-benchmark.c     压测工具
redis-check-aof       1
redis-check-aof.c     1
redis-check-rdb       1
redis-check-rdb.c     1
redis-cli             1
redis-cli.c           服务端和客户端实现-客户端程序
redismodule.h         1
redis-sentinel        1
redis-server          1
redis-trib.rb         1
release.c             1
release.h             1
replication.c         其它-主从复制
resp_parser.c         1
resp_parser.h         1
rio.c                 1
rio.h                 1
script.c              1
script.h              1
script_lua.c          1
script_lua.h          1
sdsalloc.h            1
sds.c                 基本数据结构-动态字符串
sds.h                 1
sentinel.c            其它-哨兵
server.c              服务端和客户端实现-服务端程序
server.h              1
setcpuaffinity.c      CPU绑核
setproctitle.c        1
sha1.c                1
sha1.h                1
sha256.c              1
sha256.h              1
siphash.c             1
slowlog.c             1
slowlog.h             1
solarisfixes.h        1
sort.c                1
sparkline.c           1
sparkline.h           1
stream.h              1
syncio.c              1
syscheck.c            1
syscheck.h            1
testhelp.h            1
t_hash.c              数据类型的底层实现-字典
timeout.c             1
t_list.c              数据类型的底层实现-列表
tls.c                 1
tracking.c            1
t_set.c               数据类型的底层实现-集合
t_stream.c            数据类型的底层实现-数据流
t_string.c            数据类型的底层实现-字符串
t_zset.c              数据类型的底层实现-有序集合
util.c                1
util.h                1
version.h             1
ziplist.c             基本数据结构-压缩列表
ziplist.h             1
zipmap.c              1
zipmap.h              1
zmalloc.c             1
zmalloc.h             1
```

# redis跨机房部署方案
Redis的区域感知节点（Redis Cross-Region Replication）功能也受到广泛的关注，并且可以简化跨机房部署的架设过程，使跨机房部署更加便捷、高效、简单。
```
# 配置源和目标节点
# 将SRC IP设置为源节点的 IP 地址
# 将DST IP 设置为目标节点的 IP 地址
SRC_IP= "127.0.0.1"
DST_IP= "128.0.0.1"
# 配置Replication
# Replication 位置: 源节点
redis-cli -h SRC_IP -a  config set repl-role 0 
redis-cli -h SRC_IP -a  config set repl-id "REDIS_SRC" 
redis-cli -h SRC_IP -a  config set repl-ip "$DST_IP" 
# Replication 位置: 目标节点
redis-cli -h DST_IP -a  config set repl-role 1
redis-cli -h DST_IP -a  config set repl-id "REDIS_DST"
redis-cli -h DST_IP -a  config set repl-ip "$SRC_IP"
# 启动Replication
redis-cli -h DST_IP slaveof $SRC_IP 6379
```

REDIS 开发规范
```
1.KEY命名规范
1)控制key名的长度，使用具有清晰含义的key名
2)key以字母开头，可使用小写字母字母、数字、符号（.）、符号（:）
3)分隔统一使用:
4)命名规则：业务模块:业务子系统:业务定义:其他:value类型

2.开发规范
  1) 业务连接redis时需使用连接池，禁止使用短连接
  2) 业务需定义数据的生命周期，对key设置合理的过期时间，统计key的热度，及时清理冷数据
  3) 根据业务场景选择适用的数据类型：
       String：适用于普通的key/value存储，建议value控制在10k内
       Hash：适用于用hash分割命名空间，防止key冲突，建议field控制在5000内
       List：适用于各种队列，如单向队列，双向队列，循环队列等，建议元素控制在5000内
       Set：适用于存储非重复数据，建议元素控制在5000内
       Zset：适用于优先级队列，建议元素控制在5000内
  4) 业务应用应与redis部署在同一区域，禁止跨墙访问redis
  5) 禁止使用高危命令，如keys、flushall、fluashdb、select等
  6) 禁止耗时较久的操作，如未确认数据量就直接进行smembers、zrange0,-1、hgetall等操作
  7) 控制key的大小（10k），避免出现big key
  8) 非必要不使用monitor命令，确需使用时，不要长时间使用，用完即停
  9) 建议使用批量操作提高效率，如pipeline
  10) 无关联性的业务尽量使用不同集群，避免业务干扰
  11) 业务代码中正确配置集群连接地址，禁止将集群当单机使用
  12) 控制每个Redis实例的容量，单分片（物理机）大于32G的容量需求扩容通过增加分片实现
  13) 把Redis当缓存使用，而非数据库
  14) 建议每个数据库应有窗口维护时间，大批量操作应放在维护时间实施

  15）非必要不使用hash tag，避免数据倾斜

  16）禁止同一集群跨数据中心部署
```
https://developer.aliyun.com/article/1009125
```

```
# 其它
一、键值设计
1. key名设计
•	(1)【建议】: 可读性和可管理性
以业务名(或数据库名)为前缀(防止key冲突)，用冒号分隔，比如业务名:表名:id
ugc:video:1
•	(2)【建议】：简洁性
保证语义的前提下，控制key的长度，当key较多时，内存占用也不容忽视，例如：
user:{uid}:friends:messages:{mid}简化为u:{uid}:fr:m:{mid}。
•	(3)【强制】：不要包含特殊字符
反例：包含空格、换行、单双引号以及其他转义字符
2. value设计
•	(1)【强制】：拒绝bigkey(防止网卡流量、慢查询)
string类型控制在10KB以内，hash、list、set、zset元素个数不要超过5000。
反例：一个包含200万个元素的list。
非字符串的bigkey，不要使用del删除，使用hscan、sscan、zscan方式渐进式删除，同时要注意防止bigkey过期时间自动删除问题(例如一个200万的zset设置1小时过期，会触发del操作，造成阻塞，而且该操作不会不出现在慢查询中(latency可查))，查找方法和删除方法
•	(2)【推荐】：选择适合的数据类型。
例如：实体类型(要合理控制和使用数据结构内存编码优化配置,例如ziplist，但也要注意节省内存和性能之间的平衡)
反例：
set user:1:name tom
set user:1:age 19
set user:1:favor football
正例:
hmset user:1 name tom age 19 favor football
3.【推荐】：控制key的生命周期，redis不是垃圾桶。
建议使用expire设置过期时间(条件允许可以打散过期时间，防止集中过期)，不过期的数据重点关注idletime。
二、命令使用
1.【推荐】 O(N)命令关注N的数量
例如hgetall、lrange、smembers、zrange、sinter等并非不能使用，但是需要明确N的值。有遍历的需求可以使用hscan、sscan、zscan代替。
2.【推荐】：禁用命令
禁止线上使用keys、flushall、flushdb等，通过redis的rename机制禁掉命令，或者使用scan的方式渐进式处理。
3.【推荐】合理使用select
redis的多数据库较弱，使用数字进行区分，很多客户端支持较差，同时多业务用多数据库实际还是单线程处理，会有干扰。
4.【推荐】使用批量操作提高效率
原生命令：例如mget、mset。
非原生命令：可以使用pipeline提高效率。
但要注意控制一次批量操作的元素个数 (例如500以内，实际也和元素字节数有关)。
注意两者不同：
1. 原生是原子操作，pipeline是非原子操作。
2. pipeline可以打包不同的命令，原生做不到
3. pipeline需要客户端和服务端同时支持。
5.【建议】Redis事务功能较弱，不建议过多使用
Redis的事务功能较弱(不支持回滚)，而且集群版本(自研和官方)要求一次事务操作的key必须在一个slot上(可以使用hashtag功能解决)
6.【建议】Redis集群版本在使用Lua上有特殊要求：
•	1.所有key都应该由 KEYS 数组来传递，redis.call/pcall 里面调用的redis命令，key的位置，必须是KEYS array, 否则直接返回error，"-ERR bad lua script for redis cluster, all the keys that the script uses should be passed using the KEYS array"
•	2.所有key，必须在1个slot上，否则直接返回error, "-ERR eval/evalsha command keys must in same slot"
7.【建议】必要情况下使用monitor命令时，要注意不要长时间使用。
三、客户端使用
1.【推荐】
避免多个应用使用一个Redis实例
正例：不相干的业务拆分，公共数据做服务化。
2.【推荐】
使用带有连接池的数据库，可以有效控制连接，同时提高效率，标准使用方式：
执行命令如下：
Jedis jedis = null;
try {
    jedis = jedisPool.getResource();
    //具体的命令
    jedis.executeCommand()
} catch (Exception e) {
    logger.error("op key {} error: " + e.getMessage(), key, e);
} finally {
    //注意这里不是关闭连接，在JedisPool模式下，Jedis会被归还给资源池。
    if (jedis != null)
        jedis.close();
}
下面是JedisPool优化方法的文章:
•	Jedis常见异常汇总
•	JedisPool资源池优化
3.【建议】
高并发下建议客户端添加熔断功能(例如netflix hystrix)
4.【推荐】
设置合理的密码，如有必要可以使用SSL加密访问（阿里云Redis支持）
5.【建议】
根据业务类型，选好maxmemory-policy(最大内存淘汰策略)，设置好过期时间。
默认策略是volatile-lru，即超过最大内存后，在过期键中使用lru算法进行key的剔除，保证不过期数据不被删除，但是可能会出现OOM问题。
其他策略如下：
•	allkeys-lru：根据LRU算法删除键，不管数据有没有设置超时属性，直到腾出足够空间为止。
•	allkeys-random：随机删除所有键，直到腾出足够空间为止。
•	volatile-random:随机删除过期键，直到腾出足够空间为止。
•	volatile-ttl：根据键值对象的ttl属性，删除最近将要过期数据。如果没有，回退到noeviction策略。
•	noeviction：不会剔除任何数据，拒绝所有写入操作并返回客户端错误信息"(error) OOM command not allowed when used memory"，此时Redis只响应读操作。
四、相关工具
1.【推荐】：数据同步
redis间数据同步可以使用：redis-port
2.【推荐】：big key搜索
redis大key搜索工具
3.【推荐】：热点key寻找(内部实现使用monitor，所以建议短时间使用)
facebook的redis-faina
阿里云Redis已经在内核层面解决热点key问题，欢迎使用。
五 附录：删除bigkey
1. 下面操作可以使用pipeline加速。
2. redis 4.0已经支持key的异步删除，欢迎使用。
1. Hash删除: hscan + hdel
2. List删除: ltrim
3. Set删除: sscan + srem
4. SortedSet删除: zscan + zrem
击穿
redis缓存击穿是指某一个非常热点的key(即在客户端搜索的比较多的关键字)突然失效了,这时从客户端发送的大量的请求在redis里找不到这个key，就会去数据里找，最终导致数据库压力过大崩掉。 解决：
•	1.将value的时效设置成永不过期 这种方式非常简单粗暴但是安全可靠。但是非常占用空间对内存消耗也是极大。个人并不建议使用该方法，应该根据具体业务逻辑来操作。
•	2.使用Timetask做一个定时任务 使用Timetask做定时，每隔一段时间对一些热点key进行数据库查询，将查询出的结果更新至redis中。前条件是不会给数据库过大的压力。
•	3.通过synchronized+双重检查机制 当发生reids穿透的时候，这时海量请求发送到数据库。这时我们的解决办法是只让只让一个线程去查询这个热点key，其它线程保持阻塞状态(可以让它们sleep几秒)。 当这个进入数据库的线程查询出key对应的value时，我们再将其同步至redis的缓存当中，其它线程睡醒以后再重新去redis里边请求数据
穿透
因为不良用户恶意频繁查询才会对系统造成很大的问题: key缓存并且数据库不存在，所以每次查询都会查询数据库从而导致数据库崩溃。 解决：
•	1.当类似的请求发过来，无论查出什么结果都放入redis缓存
•	2.拉黑其ip
•	3.对请求的参数进行合法性校验，在判断其不合法的前提下直接return掉
•	4.使用布隆过滤器。布隆过滤器可能会造成误判，从而穿透redis进入DB，但是这个误判概率是非常小的。
雪崩
和击穿类似，不同的是击穿是一个热点key某时刻失效，而雪崩是大量的热点key在一瞬间失效 解决：
•	1.设置缓存时,随机初始化其失效时间。如果是redis的key同时失效,可采取该办法,具体失效时间根据业务情况决定…
•	2.将不同的热点key放置到不同的节点上去。因redis一般都是集群部署,将不同的热点key平均的放置到不同节点,也可以有效避免雪崩。
•	3.将value的时效设置成永不过期
•	4.使用Timetask做一个定时任务，在失效之前重新刷redis缓存
REDIS跟MYSQL数据同步
1、先清除缓存，再更新数据库的方式显然是不行的，可能存在数据永远不正确的情况。 
2、先更新数据库再清缓存的方式，虽然可能会存在少数的错误数据的情况，但是相对来说，后续的查询可以得到更新的值。
Redis数据类型
字符串
127.0.0.1:6401> set name ""yiibai.com"" 
(error) MOVED 5798 127.0.0.1:7401
127.0.0.1:6401> get name
(error) MOVED 5798 127.0.0.1:7401
散列/哈希可以存储多达2^32 - 1个健-值对(超过40亿个)
127.0.0.1:6401> HMSET ukey username ""yiibai"" password ""passswd123"" points 200
OK
127.0.0.1:6401> hmget ukey password
1) ""passswd123""
127.0.0.1:6401> HGETALL ukey
1) ""username""
2) ""yiibai""
3) ""password""
4) ""passswd123""
5) ""points""
6) ""200""
列表的最大长度为2^32 - 1个元素(4294967295，每个列表可容纳超过40亿个元素) Redis列表只是字符串列表，按插入顺序排序。您可以向Redis列表的头部或尾部添加元素
127.0.0.1:6401> lpush alist redis 
(integer) 1
127.0.0.1:6401> lpush alist mongodb 
(integer) 2
127.0.0.1:6401> lrange alist 0 1
1) ""mongodb""
2) ""redis""
127.0.0.1:6401> lrange alist 0 0
1) ""mongodb""
127.0.0.1:6401>
一个集合中的最大成员数量为2^32 - 1(即4294967295，每个集合中元素数量可达40亿个)
redis 127.0.0.1:6379> sadd yiibailist redis 
(integer) 1 
redis 127.0.0.1:6379> sadd yiibailist mongodb 
(integer) 1 
redis 127.0.0.1:6379> sadd yiibailist sqlite 
(integer) 1 
redis 127.0.0.1:6379> sadd yiibailist sqlite 
(integer) 0 
redis 127.0.0.1:6379> smembers yiibailist  
1) ""sqlite"" 
2) ""mongodb"" 
3) ""redis""
可排序集合
redis 127.0.0.1:6379> zadd yiibaiset 0 redis
(integer) 1 
redis 127.0.0.1:6379> zadd yiibaiset 0 mongodb
(integer) 1 
redis 127.0.0.1:6379> zadd yiibaiset 1 sqlite
(integer) 1 
redis 127.0.0.1:6379> zadd yiibaiset 1 sqlite
(integer) 0 
redis 127.0.0.1:6379> ZRANGEBYSCORE yiibaiset 0 1000  
1) ""mongodb"" 
2) ""redis"" 
Redis 6.0 新特性
多线程
在Redis 6.0中，最受关注的还是其新增的多线性特性、一直以来，大家所熟知的都是Redis的单线程。
虽然数据删除、RDB的生成、AOF重写等功能可以使用后台线程或者子进程来处理，但网络IO的处理到这个命令的处理，一直都是单线程进行的。随着网络硬件性能的提升，单线程处理网络请求的速度低于网络硬件的速度时，会导致了Redis的性能瓶颈会出现在网络IO上。
为了解决这个性能瓶颈，一种是让网络请求不在内核里执行，即使用用户态网络协议栈代替内核网络协议栈，一种是采用多IO线程处理网络需求，从并发度的角度来提高网络请求处理的能力。虽然避开内核可以很好地提升请求的处理效率，但使用用户态网络协议栈，需要修改Redis源码中网络相关的部分，这会带来额外的开发工作同时新的变动也可能会带来新的bug，影响redis的稳定性。
所以在6.0的版本中，Redis官方采用了第二种方法，使用多IO来处理网络请求，在命令的读写操作上，仍是使用单线程来处理。
这样做主要是因为，出现瓶颈的一般都是在网络请求处理上，使用多IO并行处理就提升了整体的处理性能。在命令的处理上继续使用单线程，也避免了事务原子性、锁互斥、资源争用等来带的性能损耗。在实现上，大致分为以下四步：
     （1）服务端与客户端建议socket连接并分配处理线程
     （2）IO线程读取并解析客户端请求
     （3）主线程执行请求的命令操作，将返回的结果写入缓冲区
     （4）IO线程回写socket和主线程清空全局队列
ACL权限控制
 在Redis 6.0之前，Redis实例只有一个默认用户，可以设置为无密码访问，也可以针对这个用户设置密码。
这个默认用户可以拥有最大权限，可以执行所有的命令。规避高危命令只能通过重命名的方式来避免客户端的直接调用。
为了更细力度的控制访问权限，Redis 6.0版本开始支持了多用户的创建以及权限的控制；我们可以使用acl setuser来创建用户，使用（+）（-）来控制用户的权限。同时还可以以key为力度来设置访问权限，具体是通过~key的全前缀来实现。  
Tracking
 相比于之前版本，Redis实现了Tracking功能，也就是客户端缓存功能。
Redis客户端可以把读取的数据缓存在业务应用本地，那么应用就可以在本地快速读取数据了。
本地缓存同时会带来这样一个问题：当数据被修改或者过期了，如何通知客户端处理这部分变化的数据。在Redis 6.0 中的Tracking功能中，通过两种模式来解决这个问题。
一种是普通模式，可以通过client tracking on|off来控制开关。在这个模式下，Redis实例会在服务端记录客户端读取过的key并监控这个key是否有修改；一旦key发生了变化，就会通知客户端缓存失效了，此后不会再次发送这个key的变化，除非客户端再次读取了这个key。
另一种模式是广播模式，在这个模式下，服务端会给客户端广播所有key的失效情况，缺点是当有key被频繁改动时，服务端需要发送大量的广播，就会消耗大量的网络带宽。
在实际情况中，最优的方案是吧希望tracking的key的前缀进行注册，当带有注册前缀的key被修改时，服务端会把失效消息广播给所有注册的客户端。此功能需要客户端使用前面提到的RESP3 协议，在RESP 2 协议中，需要使用重定向模式才能实现。
Redis Cluster规模的限制因素
Redis Cluster 能保存的数据量以及支撑的吞吐量，跟集群的实例规模密切相关。Redis 官方给出了 Redis Cluster 的规模上限，就是一个集群运行 1000 个实例。
为了避免过多的心跳消息挤占集群带宽，我们可以调大 cluster-node-timeout值，比如说调大到 20 秒或 25 秒。这样一来， PONG 消息接收超时的情况就会有所缓解，单实例也不用频繁地每秒执行 10 次心跳发送操作了。
当然，我们也不要把 cluster-node-timeout 调得太大，否则，如果实例真的发生了故障，我们就需要等待 cluster-node-timeout 时长后，才能检测出这个故障，这又会导致实际的故障恢复时间被延长，会影响到集群服务的正常使用。为了验证调整 cluster-node-timeout 值后，是否能减少心跳消息占用的集群网络带宽，可以在调整 cluster-node-timeout 值的前后，使用 tcpdump 命令抓取实例发送心跳信息网络包的情况。
Redis事务机制
Redis 实现事务
事务的执行过程包含三个步骤，Redis 提供了 MULTI、EXEC 两个命令来完成这三个步骤。
第一步，客户端要使用一个命令显式地表示一个事务的开启。在 Redis 中，这个命令就是MULTI。
第二步，客户端把事务中本身要执行的具体操作（例如增删改数据）发送给服务器端。这些操作就是 Redis 本身提供的数据读写命令，例如 GET、SET 等。不过，这些命令虽然被客户端发送到了服务器端，但 Redis 实例只是把这些命令暂存到一个命令队列中，并不会立即执行。
第三步，客户端向服务器端发送提交事务的命令，让数据库实际执行第二步中发送的具体操作。Redis 提供的 EXEC 命令就是执行事务提交的。当服务器端收到 EXEC 命令后，才会实际执行命令队列中的所有命令。
Redis 的事务机制能保证哪些属性
如果事务正常执行，没有发生任何错误，那么，MULTI 和 EXEC 配合使用，就可以保证多个操作都完成。但是，如果事务执行发生错误了，原子性还能保证吗？我们需要分三种情况来看。
第一种情况是，在执行 EXEC 命令前，客户端发送的操作命令本身就有错误（比如语法错误，使用了不存在的命令），在命令入队时就被 Redis 实例判断出来了。对于这种情况，在命令入队时，Redis 就会报错并且记录下这个错误。此时，我们还能继续提交命令操作。等到执行了 EXEC 命令之后，Redis 就会拒绝执行所有提交的命令操作，返回事务失败的结果。这样一来，事务中的所有命令都不会再被执行了，保证了原子性。
命令，但是，这个命令只能用来主动放弃事务执行，把暂存的命令队列清空，起不到回滚的效果。日志并没有开启，那么实例重启后，数据也都没法恢复了，此时，也就谈不上原子性了。
Redis性能问题排查
单个实例的 OPS 能够达到 10W 左右。但也正因此如此，当我们在使用 Redis 时，如果发现操作延迟变大的情况，就会与我们的预期不符。
如果发现业务服务 API 响应延迟变长，首先需要先排查服务内部，究竟是哪个环节拖慢了整个服务。
比较高效的做法是，在服务内部集成链路追踪，也就是在服务访问外部依赖的出入口，记录下每次请求外部依赖的响应延时。如果发现确实是操作 Redis 的这条链路耗时变长了，那么此刻需要把焦点关注在业务服务到 Redis 这条链路上。
从业务服务到 Redis 这条链路变慢的原因可能也有 2 个：业务服务器到 Redis 服务器之间的网络存在问题，例如网络线路质量不佳，网络数据包在传输时存在延迟、丢包等情况；Redis 本身存在问题，需要进一步排查是什么原因导致 Redis 变慢。通常来说，第一种情况发生的概率比较小，如果是服务器之间网络存在问题，那部署在这台业务服务器上的所有服务都会发生网络延迟的情况，此时你需要联系网络运维同事，让其协助解决网络问题。
从 Redis 角度来排查，是否存在导致变慢的场景，以及都有哪些因素会导致 Redis 的延迟增加，然后针对性地进行优化。
为了避免业务服务器到 Redis 服务器之间的网络延迟，需要直接在 Redis 服务器上测试实例的响应延迟情况。执行以下命令，就可以测试出这个实例 60 秒内的最大响应延迟：
$ redis-cli -h 127.0.0.1 -p 6379 --intrinsic-latency 60
还可以使用以下命令，查看一段时间内 Redis 的最小、最大、平均访问延迟：
$ redis-cli -h 127.0.0.1 -p 6379 --latency-history -i 1
导致 Redis 变慢的因素。
①使用复杂度过高的命令
首先，第一步，通过查看慢日志，我们就可以知道在什么时间点，执行了哪些命令比较耗时。
如果应用程序执行的 Redis 命令有以下特点，那么有可能会导致操作延迟变大：
经常使用 O(N) 以上复杂度的命令，例如 SORT、SUNION、ZUNIONSTORE 聚合类命令；使用 O(N) 复杂度的命令，但 N 的值非常大
第一种情况导致变慢的原因在于，Redis 在操作内存数据时，时间复杂度过高，要花费更多的 CPU 资源。第二种情况导致变慢的原因在于，Redis 一次需要返回给客户端的数据过多，更多时间花费在数据协议的组装和网络传输过程中。
②操作bigkey
如果查询慢日志发现，并不是复杂度过高的命令导致的，而都是 SET / DEL 这种简单命令出现在慢日志中，那么你就要怀疑实例否写入了 bigkey。
③集中过期
如果发现，平时在操作 Redis 时，并没有延迟很大的情况发生，但在某个时间点突然出现一波延时，其现象表现为：变慢的时间点很有规律，例如某个整点，或者每间隔多久就会发生一波延迟。如果是出现这种情况，那么你需要排查一下，业务代码中是否存在设置大量 key 集中过期的情况。
如果有大量的 key 在某个固定时间点集中过期，在这个时间点访问 Redis 时，就有可能导致延时变大。
一般集中过期使用的是 expireat / pexpireat 命令，需要在代码中搜索这个关键字。
实例上限maxmory
在Redis中，是支持给实例设置内存上限的，在当做缓存使用的场景下，一般会设置此值，同时会设置数据淘汰策略，那么就有可能导致Redis变慢。
原因在于当Redis内存使用达到了设置的maxmemory值，因内存中没哟空间写入新的数据，每次进行数据写入之前，都必须先将内存中的一部分数据淘汰出来。数据淘汰出内存，是需要消耗时间的，消耗时间的长短，取决于当前Redis实例的淘汰策略。
现在Redis有八种淘汰策略，分别是：allkeys-lru、volatile-lru、allkeys-random、volatile-random、allkeys-ttl、noeviction（默认）、allkeys-lfu、volatile-lfu。具体使用哪种策略，需要根据具体的业务场景来决定。较为常用的是 allkeys-lru / volatile-lru，即从实例中随机取出一批 key，然后淘汰掉一个最少访问的key，然后取下一批key与之前的key比较，淘汰掉最少访问的key，接着重复以上步骤，直至内存使用将至maxmomey一下。
fork耗时长
为了保证Redis的数据安全，根据业务需求，会开启RDB或者AOF rewrite功能。这两个功能开启之后，在执行时，主进程会创建一个子进程进行数据的持久化。在创建子进程的过程中，会调用到系统的fork函数，在fork过程中，主进程需要拷贝自己的内存页表给子进程，如果实例较大，拷贝的过程就越久；并且fork过程会消耗大量的cpu资源，fork执行期间，Redis实例无法响应客户端的请求。
可以通过info命令查看 latest_fork_usec项（微秒），这是参数显示了主进程在 fork 子进程期间，整个实例阻塞无法处理客户端请求的时间。可以根据这个参数判断实例无法响应客户端请求的时间长短。
内存大页
如果系统开启了内存大页机制，会允许应用程序以2M为单位申请内存，而常规来说，一般是以4k为单位申请的。内存页申请的大小变大了，那么耗时也就增加了。在fork函数执行完成之后，主进程就可以接受客户端的请求了，但此时采用的是写时复制来操作内存数据。写时复制是需要申请新的内存来存放数据，如果开启了大页，就算客户端只修改1k的数据，Redis也会以2M为单位向操作系统申请内存，耗时就会增加，从而导致延迟，影响性能。
AOF
Redis支持AOF进行数据的持久化，在开启了AOF功能后，Redis会把执行后的写命令写入到AOF文件内存中，然后再根据配置的AOF刷盘策略，把AOF内存数据刷到磁盘上。Redis提供了以下三种策略：
appendfsync always：主线程每次执行写操作之后立即刷盘，优点是数据安全性高，缺点是会占用大量的磁盘IO；
appendfsync no：主线程每次写数据只写内存就返回，数据刷盘交给操作系统觉得，优点是对性能的影响最小，但数据安全性最低，宕机丢失的数据取决于系统刷盘时机；
appendfsync everysec：主线程每次写数据只写内存就返回，后台线程每1秒执行一次刷盘，相当于前两种策略的折中方案，最多丢失1秒的数据。
Redis运用场景总结
1、缓存 
2、分布式锁 
3、消息队列 
4、全局ID、计数器
基于incrby命令实现原子性的递增
     场景：分布式序列号生成（分库分表）、秒杀、限制接口请求数、限制接口调用次数、限制手机信息发送条数、文章阅读数、点赞数等
5、排行榜
      基于sortedset进行热点数据的排序
      场景：点赞排行榜、热度排行榜等各类需要排序的榜单
6、其他使用场景：购物车、限流、位统计、抽奖、点赞、好友关系、签到打卡、推荐模型等
内存碎片
在使用Redis的过程中，有时会发现一个现象：在使用过过程中，为了释放内存，会对Redis中存放的数据进行删除，在删除大量数据后，使用top命令查看时，会发现Redis占用了大量的内存。
造成这个现象的原因是，当数据删除后，Redis释放的内存空间会由内存分配器管理，不会立即将空间返回给操作系统。那么，在操作系统看来，Redis还是占用了大量的内存。
因为被Redis删除的数据在内存中的位置极大概率并不是连续的，那么这些不连续的空间在后续可能会处于一种闲置的状态。并且每个数据所占用的空间大小不一，会导致Redis虽然有空间但是却无法用来保存数据。那么，会导致Redis的内存使用率会降低，同时也会降低Redis运行机器的成本回报率。这种闲置状态的内存，虽然从理论上来看，是可以存储数据的，但实际上因为空间的不连续无法进程存储，这种状态的内存空间，称之为内存碎片。
内存碎片的形成大致分为两种：
一是：内存分配器的分配策略。一般内存分配器是按固定大小进行分配的，并不是完全按照应用程序申请的内存空间大小给程序分配。Redis 可以使用 libc、jemalloc、tcmalloc 多种内存分配器来分配内存，默认使用jemalloc。
jemalloc 的分配策略之一，是按照一系列固定的大小划分内存空间，例如 8 字节、16 字节、32 字节、48 字节，…, 2KB、4KB、8KB 等。当程序申请的内存最接近某个固定值时，jemalloc 会给它分配相应大小的空间。
这样的分配方式本身是为了减少分配次数。例如，Redis 申请一个 20 字节的空间保存数据，jemalloc 就会分配 32 字节，此时，如果应用还要写入 10 字节的数据，Redis 就不用再向操作系统申请空间了，因为刚才分配的 32 字节已经够用了，这就避免了一次分配操作。
但是，如果 Redis 每次向分配器申请的内存空间大小不一样，这种分配方式就会有形成碎片的风险，而这正好与第二点原因息息相关。
二是：键值对大小不一和删改操作。在不同的业务中操作的键值对可能不一样，那么申请内存空间分配时，申请的大小就不一样。因为内存分配器是按固定大小分配内存的，那么无论是申请空间大于还是小于这个值，只要不是键值对不是固定空间大小的整数倍，都会造成一定的碎片。再则，已经存储的键值对在后续的业务中，也有可能被删除或者修改，可能就会导致空间的额外占用或者释放，也会造成碎片。
那么，一旦大量的内存水片存在，Redis的内存实际利用率就会降低。对于内存数据库，内存利用率直接影响数据库运行效率，为了能监控到内存的使用情况，可以通过Redis自身的INFO命令来进行查看具体信息。
>INFO memory
# Memory
used_memory:4997764624
used_memory_human:4.65G
used_memory_rss:5314207744
used_memory_rss_human:4.95G
…
mem_fragmentation_ratio:1.06
mem_fragmentation_ratio就是Redis当前的内存碎片率。它是由used_memory_rss（操作系统实际分配空间）/used_memory（Redis实际申请空间）得到的。一般情况下，1<mem_fragmentation_ratio<1.5这个区间是合理的，因为前文提到的两点因素是不可避免的的。但mem_fragmentation_ratio>1.5时，那么就代表内存碎片率超过50%了，那么就需要尽快清理内存碎片了。
内存碎片的清理，最直观的是可以通过重启Redis实现，但重启可能会导致数据丢失（未开启持久化），或者加载数据时间耗费太久影响使用（AOF/RDB过大）。还有一种方法，从Redis 4.0版本开始，Redis本身提供了一种内存碎片自动清理的办法，即将内存中的数据拷贝存放在一起，将之前不连续的空间释放变成连续空间。需要注意的是，碎片的整理也是有代价的，在整理过程中进行数据拷贝是在主线程中进行，那么意味着其他命令的响应可能会有延迟。为了降低带来的性能影响，Redis可以通过activedefrag参数控制是否开启自动清理功能，并且通过active-defrag-ignore-bytes和active-defrag-threshold-lower来设置自动触发阈值，只有同时满足了才会进行自动清理。同时，通过active-defrag-cycle-min和active-defrag-cycle-max来限制CPU资源的使用，尽量减少碎片清理带来的请求处理的延迟。
数据倾斜
Redis Cluster集群中，数据会按照一定的分布规则分散到不同的实例上保存，数据都会先按照 CRC16 算法的计算值对 Slot（逻辑槽）取模，同时，所有的 Slot 又会由运维管理员分配到不同的实例上。

当数据量倾斜发生时，数据在切片集群的多个实例上分布不均衡，大量数据集中到了一个或几个实例上。这主要有三个原因，分别是某个实例上保存了bigkey、Slot 分配不均衡以及 Hash Tag。
缓存污染
所谓的缓存污染，就是在一些特定的场景下，有些数据被放入缓存中使用，后续就很少使用或者不再使用，这部分数据一直留在内存中占用空间，称之为缓存污染。

要解决缓存污染，我们也能很容易想到解决方案，那就是得把不会再被访问的数据筛选出来并淘汰掉。这样就不用等到缓存被写满以后，再逐一淘汰旧数据之后，才能写入新数据了。而哪些数据能留存在缓存中，是由缓存的淘汰策略决定的。
缓存淘汰策略
 
备份恢复之AOF
Redis在AOF中设置了数据刷盘的控制机制，通过appendfsync参数进行控制，有三种值可选：
ALWAYS：同步写入，每个写命令执行完立马同步将日志写回磁盘；
EVERYSEC：每秒写入，每个写命令执行完，只是先把日志写到 AOF 文件的内存缓冲区，每隔一秒把缓冲区中的内容写入磁盘；
NO：操作系统控制的写回，每个写命令执行完，只是先把日志写到 AOF 文件的内存缓冲区，由操作系统决定何时将缓冲区内容写回磁盘。
AOF的写入是以命令追加的形式，也就意味着AOF文件大小会越来越大，文件越大占用的空间就越大，用来恢复的时间就会越长。为了兼顾数据存储与效率，AOF重写机制应运而生。
AOF重写是将旧文件中的多条命令，合并成最新的一条数据操作命令。在恢复时，仅需执行最新的命令即可。
AOF重写是由后台线程bgrewriteaof来完成，意味着不会阻塞主线程。
备份恢复之RDB
除了AOF备份，Redis还提供了另外一种数据持久化方案：RDB内存快照，即保存内存中的数据在某一个时刻的状态。
在发生故障或者宕机的时候，可以通过持久化的RDB文件进行数据恢复。但需要注意的是，RDB记载的是某一时刻的数据，而不是数据的操作命令，就意味着仅能恢复到快照那一刻的数据。
Redis提供了save和bgsave两个命令来生成RDB文件，save是在主线程中执行，会导致阻塞；bgsave会创建一个子进程。专门用于RDB文件，避免了主线程的的阻塞，是Redis的默认配置。
虽然bgsave操作可以避免阻塞主线程，但是备份期间能不能进行正常的写操作也很重要。在快照期间，为了保持快照的完整性，一般都是可以读，不能修改。
为了快照备份而暂时不能写，对弈Redis来说，是不可以接受的。为了解决这个问题，Redis借助了操作系统提供的写时复制技术（COW），在执行快照的同事，也可以处理写操作。
Redis数据同步方案
Redis-shake是阿里云Redis&MongoDB团队开源的用于redis数据同步的工具。
基本原理
Redis-shake的基本原理就是模拟一个从节点加入源redis集群，首先进行全量拉取并回放，然后进行增量的拉取（通过psync命令）。
proxy支持

 

