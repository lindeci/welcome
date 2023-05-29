- [网上资料](#网上资料)
- [安装时OS调优](#安装时os调优)
- [consistency](#consistency)

# 网上资料

    官网 https://www.elastic.co/guide/index.html
    书籍
    《Elasticsearch权威指南（中文版）》
    社区
    中文社区 https://elasticsearch.cn/
    Elastic 社区 Meetup https://meetup.elasticsearch.cn/event/index.html （最后一次举办时间时间：2019-11-16）
    Elastic 中国社区官方博客 https://blog.csdn.net/UbuntuTouch

# 安装时OS调优

```sh
sudo groupadd es
sudo useradd es -g es

mkdir -p /data
chmod 777 /data
sudo su - es
cd /data

# 关闭透明大页
test -e /sys/kernel/mm/transparent_hugepage/enabled && cat /sys/kernel/mm/transparent_hugepage/enabled | grep never && echo never > /sys/kernel/mm/transparent_hugepage/enabled && (grep '# ES TRANSPARENT_HUGEPAGE SET' /etc/rc.local || echo 'echo never > /sys/kernel/mm/transparent_hugepage/enabled # ES TRANSPARENT_HUGEPAGE SET' >> /etc/rc.local)

echo 6553500 > /proc/sys/fs/file-max
# grep "file-max" /etc/sysctl.conf || echo "fs.file-max=6553500" >> /etc/sysctl.conf
# grep "max_map_count" /etc/sysctl.conf || echo "vm.max_map_count=655360" >> /etc/sysctl.conf
echo -e "
#BEGIN ES SET
vm.max_map_count=655360
fs.file-max=6553500
kernel.core_pattern=/data/coredump/core-%e-%p-%t
net.ipv4.ip_local_port_range=32768 61000
kernel.pid_max=98304
kernel.threads-max=8241675
net.ipv4.tcp_tw_reuse=1
net.ipv4.tcp_window_scaling=1
net.ipv4.tcp_max_syn_backlog=4096
net.core.somaxconn=4096
net.core.netdev_max_backlog=2000
vm.swappiness=0
net.ipv4.tcp_keepalive_time=5
net.ipv4.tcp_keepalive_intvl=2
net.ipv4.tcp_keepalive_probes=5
net.ipv4.tcp_retries2=6
#END ES SET
" >> /etc/sysctl.conf

grep '# BEGIN ES SET' /etc/profile || echo -e "
# BEGIN ES SET
ulimit -HSn 600000
export HISTSIZE=5000
umask 0022
export ES_JAVA_HOME=/data/elasticsearch-7.17.0/jdk
export PATH=$ES_JAVA_HOME/bin:$PATH
export CLASSPATH=.:$ES_JAVA_HOME/lib/dt.jar:$ES_JAVA_HOME/lib/tools.jar
ulimit -c unlimited
# END ES SET
" >> /etc/profile


test -f /proc/sys/fs/nr_open && nr_open=`cat /proc/sys/fs/nr_open` && echo $nr_open | grep -E "[0-9]+" && [ $nr_open -lt 1000000 ] && echo '1048576' > /proc/sys/fs/nr_open
test -e /etc/security/limits.conf && (grep '# BEGIN ES SET' /etc/security/limits.conf || echo -e "
# BEGIN ES SET
* hard nofile 65536
* soft nofile 65536
*       hard    memlock    unlimited
*       soft    memlock    unlimited
*          -    nofile     1000000
# END ES SET
" >> /etc/security/limits.conf )


test -e /etc/security/limits.d/80-nofile.conf && (grep '# BEGIN ES SET' /etc/security/limits.d/80-nofile.conf || echo -e "
# BEGIN ES SET
*          -    nofile     1000000
# END ES SET
" >> /etc/security/limits.d/80-nofile.conf )

sudo sysctl -p
```



# 配置模板

```
cat elasticsearch-7.17.0/config/elasticsearch.yml | grep -v \#
cluster.name: es-cluster
node.name: node-02
node.master: true
node.data: true
node.ingest: true
path.data: /data/elasticsearch-7.17.0/data
path.logs: /data/elasticsearch-7.17.0/logs
bootstrap.memory_lock: true
network.host: 0.0.0.0
http.port: 9200
discovery.seed_hosts: ["1.1.1.1", "1.1.1.2", "1.1.1.3"]
cluster.initial_master_nodes: ["node-01", "node-02", "node-03"]
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.client_authentication: required
xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
xpack.security.transport.ssl.truststore.path: elastic-certificates.p12
xpack.security.audit.enabled: true
```

# 生成证书和设置密码

```
bin/elasticsearch-certutil ca
bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12

./bin/elasticsearch-setup-passwords interactive
```

# Kibana配置

```
cat config/kibana.yml | egrep -v '^#|^$'
server.port: 5601
server.host: "1.1.1.1"
server.publicBaseUrl: "http://1.1.1.1:5601"
elasticsearch.hosts: ["http://1.1.1.1:9200","http://1.1.1.2:9200","http://1.1.1.1:9200"]
elasticsearch.username: "elastic"
elasticsearch.password: "elastic"
i18n.locale: "zh-CN"
```

# consistency

https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-index_.html#index-wait-for-active-shards

ObGMYDi5Xh4EL5Ls9VYKwoWj

# 慢日志设置

### 索引慢速日志记录设置

```
PUT testindex-slowlogs/_settings{
    "index.indexing.slowlog.threshold.index.warn": "0ms",
    "index.indexing.slowlog.threshold.index.info": "0ms",
    "index.indexing.slowlog.threshold.index.debug": "0ms",
    "index.indexing.slowlog.threshold.index.trace": "0ms",
    "index.indexing.slowlog.level": "trace",
    "index.indexing.slowlog.source": "1000"
}
```

### Search Slow Logging 设置

因为搜索分两阶段 query、fetch,所有查询慢日志分为两类

```
PUT testindex-slowlogs/_settings{    "index.search.slowlog.threshold.query.warn": "0ms",
    "index.search.slowlog.threshold.query.info": "0ms",
    "index.search.slowlog.threshold.query.debug": "0ms",
    "index.search.slowlog.threshold.query.trace": "0ms",
    "index.search.slowlog.threshold.fetch.warn": "0ms",
    "index.search.slowlog.threshold.fetch.info": "0ms",
    "index.search.slowlog.threshold.fetch.debug": "0ms",
    "index.search.slowlog.threshold.fetch.trace": "0ms"
}
```

### 清除慢日志设置

```
PUT testindex-slowlogs/_settings{
    "index.search.slowlog.threshold.query.warn": "",
    "index.search.slowlog.threshold.query.info": "",
    "index.search.slowlog.threshold.query.debug": "",
    "index.search.slowlog.threshold.query.trace": "",
    "index.search.slowlog.threshold.fetch.warn": "",
    "index.search.slowlog.threshold.fetch.info": "",
    "index.search.slowlog.threshold.fetch.debug": "",
    "index.search.slowlog.threshold.fetch.trace": ""
}
```

### 重置慢日志为默认值

```
PUT testindex-slowlogs/_settings{
    "index.search.slowlog.threshold.query.warn": null,
    "index.search.slowlog.threshold.query.info": null,
    "index.search.slowlog.threshold.query.debug": null,
    "index.search.slowlog.threshold.query.trace": null,
    "index.search.slowlog.threshold.fetch.warn": null,
    "index.search.slowlog.threshold.fetch.info": null,
    "index.search.slowlog.threshold.fetch.debug": null,
    "index.search.slowlog.threshold.fetch.trace": null
}
```

# 审计日志

需要license授权(收费)的功能。
开启审计

```yml
xpack.security.audit.enabled=true
```

指定审计输出中包含哪些事件，一共包含这些事件：

```
access_denied, 
access_granted, 
anonymous_access_denied, 
authentication_failed, 
connection_denied, 
tampered_request, 
run_as_denied, 
run_as_granted
```

从输出中排除某些事件。默认情况下，不排除任何事件

```
xpack.security.audit.logfile.events.include
xpack.security.audit.logfile.events.exclude
xpack.security.audit.logfile.events.emit_request_body
```

# 导出索引映射

```
GET your_index_name/_mapping > your_mapping_file.json
```
