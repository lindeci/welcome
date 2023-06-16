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
- [reindex添加白名单](#reindex添加白名单)
- [导出索引映射](#导出索引映射)
- [强制索引刷盘](#强制索引刷盘)
- [给索引添加字段](#给索引添加字段)
- [索引健康状态修复演示](#索引健康状态修复演示)
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
- [字段index属性介绍](#字段index属性介绍)
- [对查询的结果的JSON节点进行选择](#对查询的结果的json节点进行选择)
- [分页搜索](#分页搜索)
- [字段的index设置测试](#字段的index设置测试)
  - [总结](#总结)
- [设置别名](#设置别名)
- [将一个索引设置为只读](#将一个索引设置为只读)
- [修改字段类型流程](#修改字段类型流程)
- [清空索引中的文档](#清空索引中的文档)
- [设置路由的例子](#设置路由的例子)
- [创建data stream例子](#创建data-stream例子)
- [\_cat命令集](#_cat命令集)
- [\_cluster命令集](#_cluster命令集)


# 网上资料

```
官网 https://www.elastic.co/guide/index.html
书籍
《Elasticsearch权威指南（中文版）》
社区
中文社区 https://elasticsearch.cn/
Elastic 社区 Meetup https://meetup.elasticsearch.cn/event/index.html （最后一次举办时间时间：2019-11-16）
Elastic 中国社区官方博客 https://blog.csdn.net/UbuntuTouch
```

# 安装时OS调优

```sh
sudo groupadd es
sudo useradd es -g es

sudo mkdir -p /data
sudo chmod 777 /data
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

# reindex添加白名单

reindex.remote.whitelist: "1.1.1.1:9201, 1.1.1.2:9201"

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

# 索引健康状态修复演示

```
GET _cat/indices?v&health=red
GET _cat/indices?v&health=yellow
```

发现索引 `.kibana_task_manager`变成了yellow
进行修复

```
# 清理数据
POST /.kibana_task_manager/_delete_by_query?conflicts=proceed&pretty
{
  "query": {
    "match_all": {}
  }
}
# 把从副本数设置为1
PUT /.kibana_task_manager/_settings
{
    "number_of_replicas": 0
}
#把从副本数设置为2
PUT /.kibana_task_manager/_settings
{
    "number_of_replicas": 1
}
```

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

# 字段index属性介绍

当在 Elasticsearch 中将字段的 `index` 设置为 `false` 时，该字段将不会被索引，也不会出现在倒排索引中。这意味着该字段的内容不可搜索，无法通过搜索查询来匹配或过滤。

设置字段的 `index` 为 `false` 主要有以下效果：

1. **节省磁盘空间**：不将该字段索引可以减少占用的磁盘空间。对于大型文本字段或不需要搜索的字段，这可以节省宝贵的存储资源。
2. **提高索引和搜索性能**：通过禁用字段的索引，可以减少索引过程中的处理时间和资源消耗。在索引和搜索操作中跳过不需要的字段可以提高整体性能。
3. **隐藏字段内容**：将字段的 `index` 设置为 `false` 可以防止字段的内容被搜索和检索。这对于包含敏感信息或不希望公开的字段很有用。

请注意，将字段的 `index` 设置为 `false` 后，您将无法使用该字段进行搜索、聚合、排序等操作。如果需要在某些情况下进行这些操作，您可以将字段的 `index` 设置为 `true` 或根据需要进行灵活的字段配置。

# 对查询的结果的JSON节点进行选择

```
GET /my_index/_search?size=10&filter_path=hits.hits
```

# 分页搜索

如果每页显示 5 条结果，下面的命令可以得到 1-3 页的结果：

```
GET /_search?size=5
GET /_search?size=5&from=5
GET /_search?size=5&from=10
```

Elasticsearch 默认最多返回 10000 个文档。

每种分页方式的特点:

1. from+size 支持跳页，不适合深分页。
2. scroll 不支持跳页，适合拉取大量数据，不适合大量并发。
3. search_after 不支持跳页，适合拉取大量数据。

scroll 和 search_after 都可以用于深分页，search_after 需要提供一个主键字段进行排序，默
认为 _shard_doc，它是 shard index 与 Lucene 内部 ID 的组合值。在服务端保存的上下文
要比 scroll 小，目前官方推荐使用 search_after

search_after 要求数据中存在一个无重复，可以用于排序的字段

# 字段的index设置测试

构造数据

```
DELETE my_index

PUT /my_index
{
  "mappings": {
    "properties": {
      "title": {
        "type": "keyword",
        "index": true
      },
      "description": {
        "type": "keyword",
        "index": false
      },
      "click": {
        "type": "long",
        "index": true
      },
      "call": {
        "type": "long",
        "index": false
      },
      "author":{
        "type": "text",
        "index": true
      },
      "comment":{
        "type": "text",
        "index": false
      }
    }
  }
}
POST /my_index/_doc/1
{
  "title": "Example Document1",
  "description": "This is a sample document1.",
  "click": 1,
  "call": 1,
  "author": "This is a sample document1.",
  "comment": "This is a sample document1."
}
POST /my_index/_doc/2
{
  "title": "Example Document2",
  "description": "This is a sample document2.",
  "click": 2,
  "call": 2,
  "author": "This is a sample document2.",
  "comment": "This is a sample document2."
}
POST /my_index/_doc/3
{
  "title": "Example Document3",
  "description": "This is a sample document3.",
  "click": 3,
  "call": 3,
  "author": "This is a sample document3.",
  "comment": "This is a sample document3."
}
```

keyword 字段，不管是"index": false还是"index": true，都能排序

```
POST /my_index/_search
{
  "sort": [
    {
      "title": "desc"
    },
    {
      "description": "desc"
    }
  ]
}
```

long 字段，不管是"index": false还是"index": true，都能排序、聚合

```
GET /my_index/_search
{
  "size": 0,
  "aggs": {
    "avg_click": {
      "avg": {
        "field": "click"
      }
    },
    "max_click": {
      "max": {
        "field": "click"
      }
    },
    "min_call": {
      "min": {
        "field": "call"
      }
    }
  }
}
```

text 字段不允许排序，下面脚本返回失败

```
POST /my_index/_search
{
  "sort": [
    {
      "author": "desc"
    }
  ]
}
```

text 字段设置"index": false时，不允许全文检索，下面脚本返回失败

```
POST /my_index/_search
{
  "query": {
    "match": {
      "author": "document3"
    }
  }
}
```

keyword 字段设置"index": false时，不允许查询、模糊查询，下面脚本返回失败

```
GET /my_index/_search
{
  "query": {
    "terms": {
      "description": ["This is a sample document3."]
    }
  }
}

GET /my_index/_search
{
  "query": {
    "prefix": {
      "description": "This is a sample document3."
    }
  }
}
```

long 字段设置"index": false时，不允许查询，下面脚本返回失败

```
GET /my_index/_search
{
  "query": {
    "range": {
      "call": {
        "gte": 0,
        "lte": 5000000
      }
    }
  }
}
```

## 总结

1. 如果字段设置"index": false，那么查询语句中的query不能查询该字段
2. text 字段不允许排序、聚合
3. 非 text 字段，"index"的设置不影响其排序、聚合

# 设置别名

```json
PUT my_index
{
  "aliases": {
      "ldc_index": {
        "is_write_index": true
      }
  }
}
```

`is_write_index`：举例来说，假设你有两个索引，logs_2023_06 和 logs_2023_07，你可以设置一个别名 logs_write，并将 is_write_index 设置为 true 对于最新的索引 logs_2023_07。这样，当你通过 logs_write 别名写入数据时，数据将被写入到 logs_2023_07 索引。

根据别名查看索引名
```
GET /_cat/aliases?v
或者
GET /_alias/ldc_index
```

# 将一个索引设置为只读
```
PUT /my_index/_settings
{
    "index.blocks.read_only": true
}
# 恢复可写
PUT /my_index/_settings
{
    "index.blocks.read_only": false
}
```

# 修改字段类型流程
```json
1、创建新的索引
PUT /new_index_name
{
    "mappings": {
        "properties": {
            "field_name": {
                "type": "new_type"
            }
        }
    }
}

2、使用 _reindex API 将数据从旧索引复制到新索引：
PUT /old_index_name/_settings
{
    "index.blocks.read_only": true
}

POST /_reindex
{
    "source": {
        "index": "old_index_name"
    },
    "dest": {
        "index": "new_index_name"
    }
}
3、（可选）如果你使用别名，更新别名指向新的索引：
POST /_aliases
{
  "actions": [
    {
      "remove": {
        "index": "old_index_name",
        "alias": "your_alias_name"
      }
    },
    {
      "add": {
        "index": "new_index_name",
        "alias": "your_alias_name"
      }
    }
  ]
}
4、删除旧索引：
PUT /old_index_name/_settings
{
    "index.blocks.read_only": false
}
DELETE /old_index_name
```

# 清空索引中的文档
```json
POST /my_index/_delete_by_query?conflicts=proceed&pretty
{
  "query": {
    "match_all": {}
  }
}
```

# 设置路由的例子
不像别的数据库可以设置表级别的分片键。  
ES需要每次插入、查询文档时，都需要指定分片键的值的
```
# 如果希望按title字段分片，则插入文档时，按title字段的具体值去指定路由
POST my_index/_doc/1?routing=string1
{"title":"string1"}

# 查询时，需要按具体的值去指定的分片上去查询
GET my_index/_search?routing=string1
```

# 创建data stream例子
```json
# 日志类型的data stream
DELETE _ilm/policy/logx_policy_test
# 创建索引生命周期策略
PUT _ilm/policy/logx_policy_test
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "1d",
        "actions": {
          "set_priority": {
            "priority": 100
          },
          "rollover": {
            "max_age": "2d",
            "max_docs": 500000000,
            "max_size": "50gb"
          }
        }
      },
      "warm": {
        "min_age": "1d",
        "actions": {
          "set_priority": {
            "priority": 50
          },
          "allocate": {
            "include": {
              "data": "warm"
            }
          }
        }
      },
      "cold": {
        "min_age": "1d",
        "actions": {
          "set_priority": {
            "priority": 0
          },
          "allocate": {
            "number_of_replicas": 1,
            "include": {
              "data": "cold"
            }
          }
        }
      },
      "delete": {
        "min_age": "7d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}

DELETE _index_template/logx-template_test
# 创建索引模板
PUT _index_template/logx-template_test
{
  "index_patterns": [
    "logx-*"
  ],
  "priority": 1,
  "data_stream": {},
  "template": {
    "settings": {
      "index": {
        "number_of_shards": "2",
        "number_of_replicas": "1",
        "lifecycle.name": "logx_policy_test"
      }
    }
  }
}

DELETE /_data_stream/logx-business
# 创建data_stream
PUT /_data_stream/logx-business


PUT /logx-business/_bulk?refresh
{"create":{ }}
{ "@timestamp": "2020-12-08T11:04:05.000Z", "user": { "id": "vlb44hny" }, "message": "Loginattempt failed" }
{"create":{ }}
{ "@timestamp": "2020-12-08T12:06:07.000Z", "user": { "id": "8a4f500d" }, "message": "Login successful" }
{"create":{ }}
{ "@timestamp": "2020-12-09T13:07:08.000Z", "user": { "id": "l7gk7f82" }, "message": "Logout successful"}

GET logx-business/_mapping
GET /logx-business/_search
GET /logx-business/_search?size=10&filter_path=hits.hits
```

# _cat命令集

末尾添加 ?v可以打印字段标题

| /_cat/aliases                       | 查看别名接口              |
| ----------------------------------- | ------------------------- |
| /_cat/aliases/{alias}               |                           |
| /_cat/allocation                    | 查看分配资源接口          |
| /_cat/count                         | 查看文档个数接口          |
| /_cat/count/{index}                 |                           |
| /_cat/fielddata                     | 查看字段分配情况接口      |
| /_cat/fielddata/{fields}            |                           |
| /_cat/health                        | 查看健康状态接口          |
| /_cat/indices                       | 查看索引信息接口          |
| /_cat/indices/{index}               |                           |
| /_cat/master                        | 查看master信息接口        |
| /_cat/ml/anomaly_detectors          | 查看异常信息接口          |
| /_cat/ml/anomaly_detectors/{job_id} |                           |
| /_cat/ml/data_frame/analytics       |                           |
| /_cat/ml/data_frame/analytics/{id}  |                           |
| /_cat/ml/datafeeds                  |                           |
| /_cat/ml/datafeeds/{datafeed_id}    |                           |
| /_cat/ml/trained_models             |                           |
| /_cat/ml/trained_models/{model_id}  |                           |
| /_cat/nodeattrs                     | 查看nodes资源配置信息接口 |
| /_cat/nodes                         | 查看nodes负载信息接口     |
| /_cat/pending_tasks                 | 查看正在挂起的任务接口    |
| /_cat/plugins                       | 查看插件接口              |
| /_cat/recovery                      | 查看修复状态接口          |
| /_cat/recovery/{index}              |                           |
| /_cat/repositories                  |                           |
| /_cat/segments                      | 查看lucence的段信息接口   |
| /_cat/segments/{index}              |                           |
| /_cat/shards                        | 查看分片信息接口          |
| /_cat/shards/{index}                |                           |
| /_cat/snapshots/{repository}        |                           |
| /_cat/tasks                         |                           |
| /_cat/templates                     | 查看索引模板              |
| /_cat/thread_pool                   | 查看线程池接口            |
| /_cat/thread_pool/{thread_pools}    |                           |
| /_cat/transforms                    |                           |
| /_cat/transforms/{transform_id}     |                           |


# _cluster命令集

| **描述**                                | **命令**         | **示例**                                    |
| --------------------------------------------- | ---------------------- | ------------------------------------------------- |
| **查看集群健康状态接口**                | _cluster/health        | /_cluster/health?level=shards``            |
| /_cluster/health/test1,test2                  |                        |                                                   |
| **查看集群状况接口**                    | _cluster/state         | /_cluster/state/_all/foo,bar``             |
| /_cluster/state/metadata,routing_table?pretty |                        |                                                   |
| **查看集群统计信息接口**                | _cluster/stats         | /_cluster/stats?human&pretty                      |
| **查看集群挂起的任务接口**              | _cluster/pending_tasks | /_cluster/pending_tasks                           |
| **集群重新路由操作**                    | _cluster/reroute       |                                                   |
| **更新集群设置**                        | _cluster/settings      | /_cluster/settings                                |
| **节点状态**                            | _nodes/stats           | /_nodes/nodeId1,nodeId2/stats``            |
| /_nodes/stats                                 |                        |                                                   |
| **节点信息**                            | _nodes                 | /_nodes/nodeId1,nodeId2/info/jvm,process`` |
| /_nodes/nodeId1,nodeId2/_all                  |                        |                                                   |
| **节点的热线程**                        | _nodes/hot_threads     | /_nodes/nodeId1,nodeId2/hot_threads``      |
| /_nodes/hot_threads                           |                        |                                                   |
