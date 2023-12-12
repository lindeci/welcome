1. 面试官：工作中使用过Zookeeper嘛？你知道它是什么，有什么用途呢？
「小菜鸡的我：」

有使用过的，使用ZooKeeper作为「dubbo的注册中心」，使用ZooKeeper实现「分布式锁」。
ZooKeeper，它是一个开放源码的「分布式协调服务」，它是一个集群的管理者，它将简单易用的接口提供给用户。
可以基于Zookeeper 实现诸如数据发布/订阅、负载均衡、命名服务、分布式协调/通知、集群管理、Master 选举、分布式锁和分布式队列「等功能」。
Zookeeper的「用途」：命名服务、配置管理、集群管理、分布式锁、队列管理
用途跟功能不是一个意思咩？给我一个眼神，让我自己体会

# 安装部署
依赖：JDK，需要安装 java
```sh
wget https://downloads.apache.org/zookeeper/zookeeper-3.7.0/apache-zookeeper-3.7.0-bin.tar.gz

# 配置 data/myid

# 配置conf/zoo.cfg
cat conf/zoo.cfg  | grep -v '#'
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/data/apache-zookeeper-3.7.1-bin/data
dataLogDir=/data/apache-zookeeper-3.7.1-bin/logs
clientPort=2181
autopurge.snapRetainCount=3
autopurge.purgeInterval=1

maxClientCnxns=60
standaloneEnabled=true
admin.enableServer=true
server.1=172.1.1.16:2888:3888
server.2=172.1.1.17:2888:3888
server.3=172.1.1.18:2888:3888

# 启动
./bin/zkServer.sh start
./bin/zkServer.sh status
```