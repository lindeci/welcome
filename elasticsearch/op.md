- [网上资料](#网上资料)
- [安装时OS调优](#安装时os调优)
- [配置模板](#配置模板)
- [生成证书和设置密码](#生成证书和设置密码)
- [Kibana配置](#kibana配置)
- [consistency](#consistency)
- [慢日志设置](#慢日志设置)
    - [索引慢速日志记录设置](#索引慢速日志记录设置)
    - [Search Slow Logging 设置](#search-slow-logging-设置)
    - [清除慢日志设置](#清除慢日志设置)
    - [重置慢日志为默认值](#重置慢日志为默认值)
- [审计日志](#审计日志)
- [添加白名单](#添加白名单)
- [导出索引映射](#导出索引映射)
- [强制索引刷盘](#强制索引刷盘)
- [给索引添加字段](#给索引添加字段)
- [查看任务](#查看任务)
- [使用SQL查询](#使用sql查询)
- [时区](#时区)
- [删除字段](#删除字段)
- [直接复制索引](#直接复制索引)
- [字段类型](#字段类型)
- [使用pipeline添加时间戳字段](#使用pipeline添加时间戳字段)
- [字段映射参数](#字段映射参数)
- [查看版本](#查看版本)
- [指定查询的目标节点](#指定查询的目标节点)
- [异步复制控制参数](#异步复制控制参数)


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
# 添加白名单


# 导出索引映射

```
GET your_index_name/_mapping > your_mapping_file.json
```

# 强制索引刷盘

```
POST /索引名称/_refresh
```

# 给索引添加字段

```
POST test-10/_update_by_query?conflicts=proceed&scroll=2m
{
  "query": {
    "bool": {
      "must_not": {
        "exists": {
          "field": "@timestamp"
        }
      }
    }
  },
  "script": {
    "source": "ctx._source['@timestamp'] = new Date()"
  }
} 
```

- _update_by_query：表示使用update_by_query API，这个API允许以批量方式更新满足特定条件的文档。
- conflicts=proceed：表示更新操作中可能出现的冲突以继续执行。
- scroll=2m：表示设定滚动查询的过期时间为2分钟。
- max_docs=100000：表示每个滚动查询批次最多处理10万个文档。如果结果集超过该限制，则滚动查询将被分成多个批次进行处理。
- "script": {"source": "ctx._source['@timestamp'] = new Date()"}：表示修改操作，将每个文档的“@timestamp”字段更新为当前时间。
- ctx是update_by_query API中的一个内置对象，代表上下文（context）对象。
- ctx._source是上下文中的一个属性，表示当前要操作的文档对象。

# 查看任务

```
GET _tasks/<task_id>
```

# 使用SQL查询

```
POST _sql?format=txt
{
  "query":"SELECT host_ip, COUNT(*) FROM my-index WHERE status='success' GROUP BY host_ip"
}

```

# 时区

在Elasticsearch中，日期类型的字段默认是使用UTC时间。当你插入一个文档时，如果没有明确将时间转换成UTC时间并指定时区，它会默认将本地时间转换成UTC时间存储。

# 删除字段

```
POST /cf_rfem_hist_price/_update_by_query
{
  "script": "ctx._source.remove(\"@timestamp\")",
  "query": {
    "exists": {
      "field": "@timestamp"
    }
  }
}
```

# 直接复制索引

[Reindex API | Elasticsearch Guide [7.17] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docs-reindex.html)

```
POST _reindex
{
  "source": {
    "index": "cf_rfem_hist_price",
    "size": 10,
    "query": {
      "match_all": {}
    }
  },
  "dest": {
    "index": "cf_rfem_hist_price_bak"
  },
  "script": {
    "source": "ctx._source.remove('@timestamp')"
  }
}
```

# 字段类型

| 字段类型    | 描述                                     |
| ----------- | ---------------------------------------- |
| text        | 用于全文本搜索和分析的文本字段           |
| keyword     | 关键字字段，用于精确匹配和聚合           |
| date        | 日期字段，可以存储日期和时间             |
| long        | 长整型字段                               |
| integer     | 整型字段                                 |
| short       | 短整型字段                               |
| byte        | 字节字段                                 |
| double      | 双精度浮点型字段                         |
| float       | 单精度浮点型字段                         |
| boolean     | 布尔型字段                               |
| binary      | 二进制数据字段                           |
| geo_point   | 地理位置字段，用于存储经纬度坐标         |
| geo_shape   | 地理形状字段，用于存储复杂的地理形状数据 |
| ip          | IP地址字段                               |
| completion  | 用于自动补全的字段类型                   |
| token_count | 令牌计数字段，用于跟踪文本字段的令牌数量 |
| nested      | 嵌套对象字段，用于存储嵌套的JSON对象     |
| object      | 对象字段，用于存储JSON对象               |

# 使用pipeline添加时间戳字段

```
DELETE _ingest/pipeline/add_timestamp
PUT _ingest/pipeline/add_timestamp
{
  "description": "Add @timestamp field as a timestamp",
  "processors": [
    {
      "script": {
        "source": "ctx['@timestamp'] = new Date().getTime();"
      }
    }
  ]
}

DELETE your_index
POST your_index/_doc?pipeline=add_timestamp
{
  "your_field": "your_value"
}
GET your_index/_search
```

显示结果：

```
"_source" : {
          "your_field" : "your_value",
          "@timestamp" : 1685926937718
        }
```

# 字段映射参数

```json
{
  "mappings": {  // 定义索引的映射
    "doc": {  // 定义文档类型
      "properties": {  // 定义文档的字段
        "batch_number": {  // 定义名为 "batch_number" 的字段
          "type": "text",  // 字段类型为 "text"
          "fields": {  // 定义多字段(用于为同一个字段定义多个不同的映射。每个多字段都可以具有自己独立的数据类型和参数设置，这样在同一个字段上可以应用不同的分析器、存储方式或其他处理逻辑。)
            "keyword": {  // 定义名为 "keyword" 的子字段
              "type": "keyword",  // 子字段类型为 "keyword"
              "ignore_above": 256  // 限制子字段的字符串长度上限为 256
            }
          }
        }
      }
    }
  }
}

```

| 参数                   | 说明                                                       |
| ---------------------- | ---------------------------------------------------------- |
| type                   | 字段的数据类型                                             |
| index                  | 字段是否被索引                                             |
| store                  | 字段是否被存储                                             |
| analyzer               | 分析器用于分析字段的内容                                   |
| search_analyzer        | 查询时使用的分析器                                         |
| normalizer             | 规范化器用于标准化字段的内容                               |
| format                 | 格式化日期字段的日期格式                                   |
| null_value             | 字段的默认空值                                             |
| doc_values             | 字段是否启用 Doc Values，用于排序、聚合和脚本操作          |
| coerce                 | 字段是否尝试将字符串类型的值强制转换为字段的类型           |
| ignore_malformed       | 是否忽略格式错误的字段值                                   |
| scaling_factor         | 数字字段的缩放因子，用于改变字段的精度和范围               |
| ignore_above           | 字符串字段截断长度上限                                     |
| ignore_below           | 字符串字段截断长度下限                                     |
| similarity             | 字段的相似度算法                                           |
| copy_to                | 将字段值复制到指定的其他字段                               |
| fields                 | 定义多字段，允许在一个字段上应用多个不同的分析器或存储方式 |
| coerce                 | 尝试将字段的值强制转换为字段的数据类型                     |
| dynamic                | 动态映射的行为设置，用于控制新字段的自动映射行为           |
| enabled                | 字段是否启用                                               |
| include_in_all         | 字段是否包含在 `_all`字段中                              |
| index_options          | 控制字段在倒排索引中的存储方式                             |
| norms                  | 控制字段的归一化因子的计算方式                             |
| position_increment_gap | 控制在同一位置出现的多个词项之间的间隔                     |
| similarity             | 字段的相似度算法                                           |
| term_vector            | 控制文档中每个词项的存储方式                               |

# 查看版本
```
GET /
```
返回
```
{
  "name" : "es01",
  "cluster_name" : "es-cluster",
  "cluster_uuid" : "zwgsf3m7Rmaj64SfgbH0PA",
  "version" : {
    "number" : "7.17.0",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "bee86328705acaa9a6daede7140defd4d9ec56bd",
    "build_date" : "2022-01-28T08:36:04.875279988Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```
# 指定查询的目标节点
将查询发送到名为node_A的节点上执行
```
GET /idx/_search?preference=node_A
{
  "query": {
    "match_all": {}
  }
}
```
将查询限制为只在副本分片上执行
```
GET /idx/_search?preference=_only_nodes:replica
{
  "query": {
    "match_all": {}
  }
}
```
# 异步复制控制参数
```
PUT idx/_settings
{
  "index.number_of_replicas": 1,
  "index.write.wait_for_active_shards": "1"
}
```
1. `index.number_of_replicas`: 这个参数定义了索引的副本数。将副本数设置为大于0的值，以便在多个节点上创建副本。默认值为1。

2. `index.write.wait_for_active_shards`: 此参数定义了写入操作需要等待的活跃分片的副本数。活跃分片是指主分片和其副本。默认值为"1"，表示只需主分片写入成功即可返回响应。可以设置为"all"，以等待所有分片的副本写入成功。

