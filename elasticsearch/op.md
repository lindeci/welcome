- [网上资料](#网上资料)
- [kill 进程](#kill-进程)
- [安装时OS调优](#安装时os调优)
- [配置模板](#配置模板)
- [生成证书和设置密码](#生成证书和设置密码)
- [Kibana配置](#kibana配置)
- [开启 https 功能](#开启-https-功能)
- [logstash 使用 p12 凭证](#logstash-使用-p12-凭证)
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
- [取消任务](#取消任务)
- [释放空间](#释放空间)
- [使用SQL查询](#使用sql查询)
- [时区](#时区)
- [删除字段](#删除字段)
- [直接复制索引](#直接复制索引)
- [字段类型](#字段类型)
- [日期字段类型](#日期字段类型)
- [使用pipeline添加时间戳字段](#使用pipeline添加时间戳字段)
- [字段映射参数](#字段映射参数)
- [查看版本](#查看版本)
- [指定查询的目标节点](#指定查询的目标节点)
- [异步复制控制参数](#异步复制控制参数)
- [字段index属性介绍](#字段index属性介绍)
- [对查询的结果的JSON节点进行选择](#对查询的结果的json节点进行选择)
- [分页搜索](#分页搜索)
- [字段的index属性设置测试](#字段的index属性设置测试)
  - [总结](#总结)
- [设置别名](#设置别名)
- [将一个索引设置为只读](#将一个索引设置为只读)
- [修改字段类型流程](#修改字段类型流程)
- [清空索引中的文档](#清空索引中的文档)
- [设置路由的例子](#设置路由的例子)
- [data stream 的限制](#data-stream-的限制)
- [创建data stream例子](#创建data-stream例子)
- [创建 data\_stream 模板](#创建-data_stream-模板)
- [多个条件模糊匹配查询](#多个条件模糊匹配查询)
- [批量删除索引中的文档](#批量删除索引中的文档)
- [只删除数据](#只删除数据)
- [安装分词器](#安装分词器)
- [使用S3接口进行备份恢复](#使用s3接口进行备份恢复)
- [查看 索引 是否可用状态](#查看-索引-是否可用状态)
- [重启 data 节点导致索引变 yellow 分析](#重启-data-节点导致索引变-yellow-分析)
  - [可能的情况](#可能的情况)
  - [重启数据节点时节省索引副本恢复时间的办法](#重启数据节点时节省索引副本恢复时间的办法)
    - [思路](#思路)
    - [集群正确重启方式](#集群正确重启方式)
  - [重启过程的原理](#重启过程的原理)
  - [某案例分析](#某案例分析)
- [索引调整分片数量的考虑因素](#索引调整分片数量的考虑因素)
- [把创建索引的脚本导入ES](#把创建索引的脚本导入es)
- [聚合查询](#聚合查询)
  - [统计有哪些不同的数值](#统计有哪些不同的数值)
  - [多个维度聚合](#多个维度聚合)
- [使用kibana API 创建索引模式](#使用kibana-api-创建索引模式)
- [curl 删除 索引](#curl-删除-索引)
- [添加只读用户](#添加只读用户)
- [修改密码](#修改密码)
- [统计 ingress 日志的异常信息](#统计-ingress-日志的异常信息)
- [权限讲解](#权限讲解)
  - [Elasticsearch 权限说明](#elasticsearch-权限说明)
- [命令行授权](#命令行授权)
- [别名操作](#别名操作)
- [null 值测试](#null-值测试)
- [\_cat命令集](#_cat命令集)
- [\_cluster命令集](#_cluster命令集)
- [问题处理](#问题处理)
  - [1、TOO\_MANY\_REQUESTS/12/disk usage exceeded flood-stage watermark](#1too_many_requests12disk-usage-exceeded-flood-stage-watermark)
  - [2、扩容磁盘空间](#2扩容磁盘空间)
  - [](#)


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

# kill 进程
```sh
kill $(ps -ef | grep -v grep | grep "org.elasticsearch.bootstrap.Elasticsearch -d" | awk '{print $2}')
sleep 15
ps -ef|grep -v grep | grep "org.elasticsearch.bootstrap.Elasticsearch -d"
rm -rf /data/*
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
grep '# BEGIN ES SET' /etc/sysctl.conf || echo -e "
# BEGIN ES SET
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
# END ES SET
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
CPU最大性能模式
```sh
tuned-adm profile throughput-performance

source /etc/profile
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
elasticsearch-certutil 官网介绍 ：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/certutil.html#certutil-ca

```
bin/elasticsearch-certutil ca --days 10950 --pass '' --out elastic-stack-ca.p12
bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12 --days 10950 --pass '' --ca-pass '' --out elastic-certificates.p12


./bin/elasticsearch-setup-passwords interactive
su - es -c'/data/elasticsearch-7.17.0/bin/elasticsearch-setup-passwords auto --batch'

重置密码，并且随机生成新密码
bin/elasticsearch-reset-password -u elastic

```
`bin/elasticsearch-certutil ca`和`bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12`这两个命令是Elasticsearch的证书工具elasticsearch-certutil的命令，用于生成和管理用于Elastic Stack的传输层安全(TLS)的证书。

- `bin/elasticsearch-certutil ca`命令用于生成新的证书颁发机构(CA)。默认情况下，它会生成一个PKCS#12格式的输出文件，该文件包含CA证书和CA的私钥。如果你指定了`--pem`参数，该命令会生成一个zip文件，其中包含PEM格式的证书和私钥。你可以将这些文件作为输入，用于elasticsearch-certutil的cert模式。

- `bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12`命令用于生成X.509证书和私钥。默认情况下，它会为单个实例生成一个证书和密钥。所有由此命令生成的证书都由CA签名，除非指定了`--self-signed`参数。你必须使用`--ca`或者`--ca-cert`和`--ca-key`参数提供你自己的CA，除非指定了`--self-signed`。

实战介绍：https://opster.com/guides/elasticsearch/security/elasticsearch-cluster-security/

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

# 开启 https 功能
在ES添加参数(所有的节点，包括数据节点，都需要开启HTTPS)
```sh
xpack.security.http.ssl.enabled: true 
xpack.security.http.ssl.keystore.path: elastic-certificates.p12
xpack.security.http.ssl.truststore.path: elastic-certificates.p12
```
在kibana 中调整
```sh
elasticsearch.hosts: ["https://172.1.1.228:9200","https://172.1.1.229:9200","https://172.1.1.230:9200"]
elasticsearch.ssl.certificateAuthorities: [ "/data/kibana-7.17.0-linux-x86_64/config/elastic-certificates.p12" ]
elasticsearch.ssl.verificationMode: none
```
crul 访问要添加参数 -k
```
curl -XGET 'https://172.1.1.229:9200/_cluster/health?pretty' -uelastic:elastic -k
``````

# logstash 使用 p12 凭证
```sh
output {
elasticsearch {
            hosts => ["https://172.1.1.2:9200"]
            index => "%{__tag__:_namespace_}"
            user => "elastic"
            action => "create"
            ilm_enabled => true
            password => "elastic"
            ssl_certificate_verification => true
            truststore => "/usr/share/logstash/elastic-certificates.p12"
            truststore_password => ""
		} 
}
```
不需要认证的话，可以这么设置
```
hosts => ["https://172.1.1.2:9200","https://172.1.1.3:9200","https://172.1.1.4:9200"]
        user => "elastic"
        timeout => 30
        password => "elastic"
        index => "gys-iam-%{_container_name_}"
        action => "create"
        ilm_enabled => true
        ssl_certificate_verification => false
        ssl => true
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

# 取消任务
```
POST _tasks/-DFDapzISfyYVJhuQqyhRw:374987396/_cancel
```

# 释放空间
1. 执行合并操作：在Kibana控制台中，使用`forcemerge` API来合并索引的段（segments）。合并操作将减少磁盘上的碎片化，并释放未使用的空间。

   ```shell
   POST /<index_name>/_forcemerge?max_num_segments=1
   ```

   在上面的命令中，将`<index_name>`替换为你要释放空间的索引名称。`max_num_segments=1`表示将所有段合并为一个。

   请注意，合并操作可能会对Elasticsearch的性能产生一定影响，特别是对于大型索引。因此，在生产环境中，建议在负载较低的时候执行此操作。

2. 等待合并完成：合并操作可能需要一段时间来完成，具体时间取决于索引的大小和硬件性能。你可以使用以下命令来检查合并操作的进度：

   ```shell
   GET /<index_name>/_refresh
   GET /<index_name>/_segments
   ```

   `/_refresh`命令将刷新索引以获取最新的段信息，`/_segments`命令将返回段的详细信息，包括合并操作的进度。

请注意，在执行任何操作之前，请确保备份你的数据，并根据你的具体需求进行测试和评估。合并操作可能会导致一些I/O和CPU开销，因此在执行此操作时，要确保有足够的资源和适当的时间窗口。

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

需要注意的是，ignore_above 参数只适用于 keyword 类型的字段。  
对于 text 类型的字段，Elasticsearch 并没有提供直接的方式来限制字段的长度。  
如果你需要限制 text 类型字段的长度，你可能需要在应用程序中进行处理，比如在索引数据之前先检查字段的长度。

# 日期字段类型
比如：
```json
"access_time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||strict_date_optional_time||epoch_millis",
                "index": "true"
            } 
```
这意味着该字段可以接受三种不同格式的日期和时间值：
- "yyyy-MM-dd HH:mm:ss"：这种格式表示日期和时间值应该以 年-月-日 时:分:秒 的形式提供。例如，"2023-09-04 10:45:05"。
- "strict_date_optional_time"：这种格式表示日期和时间值应该符合 ISO 8601 标准。例如，"2023-09-04T10:45:05.000Z"。
- "epoch_millis"：这种格式表示日期和时间值应该以自 Unix 纪元（1970 年 1 月 1 日）以来的毫秒数提供。例如，"1693897505000"。

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

# 字段的index属性设置测试

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
// 或者
POST /_aliases
{
  "actions": [
    {
      "add": {
        "index": "a1",
        "alias": "a"
      }
    },
    {
      "add": {
        "index": "b1",
        "alias": "b"
      }
    },
    {
      "add": {
        "index": "c1",
        "alias": "c"
      }
    }
  ]
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
# data stream 的限制
Elasticsearch的Data Stream是一种特殊类型的索引，它主要用于存储时间序列数据。相比于普通索引，Data Stream有一些限制和特性：

1. **仅追加存储**：Data Stream主要用于存储仅追加的时间序列数据。这意味着你只能向Data Stream中添加新的文档，而不能修改或删除已经存在的文档。

2. **必须包含@timestamp字段**：每个写入到Data Stream的文档必须包含@timestamp字段。这个字段用于表示文档的时间戳，它必须是date类型或者date_nanos类型。

3. **无法直接访问后备索引**：Data Stream由一个或多个后备索引组成。这些后备索引实际上存储了Data Stream中的数据，但是你不能直接访问这些后备索引。你只能通过Data Stream来访问这些数据。

4. **无法使用别名**：在Elasticsearch中，别名是一种可以用来引用一个或多个索引的方式。但是，你不能为Data Stream创建别名。

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

# 创建 data_stream 模板
```sh
-- 建立 datastream 模板
PUT _index_template/ceph-template     -- 这里的 ceph-template 是模板名称
{
  "index_patterns": [
    "ceph-logs*"   -- 匹配的 datastream 名称
  ],
  "priority": 1,	-- 索引模板的优先级，一个datastream同时匹配到多个模板时，会用到
  "data_stream": {},	-- 表示这个模式是用于数据流
  "template": {
    "settings": {
      "index": {
        "number_of_shards": "16",	-- 建议一个分片不超过100G（比如14天的日志量是14T，那么可以设置为16分片，刚好每个分片100G）
        "number_of_replicas": "1",	-- 建议默认一个从副本
        "lifecycle.name ": "14-days-default"	--	关联生命周期模板，有很多模板，比如7、14、30、90、180等，还可以设置滚动策略
      }
    },
	"mappings": {     -- 映射规则，规范同普通索引的映射规则
		"_meta": {
				"software_version_mapping": "1.0",
				"description": "升级包(te_iot_upgrade_package)"
		},
		"_default_": {
		  "_all": {
			"enabled": false
		  }
		},
		"properties": {
			"id": {
				"type": "keyword",
				"index": "true"
			},
			"package_name": {
				"type": "text",
				"analyzer": "ik_max_word",
				"fields": {
					"keyword": {
						"type": "keyword"
					}
				},
				"index": "true"
			},
			"version": {
				"type": "keyword",
				"index": "true"
			},
			"create_time": {
				"type": "date",
				"format": "yyyy-MM-dd HH:mm:ss||strict_date_optional_time||epoch_millis",
				"index": "false"
			}
		}
	  }
  }
}

-- 建立对应的 datastream
PUT /_data_stream/ceph-logs-test  -- 要求跟模板中的 ceph-logs* 对应
```

# 多个条件模糊匹配查询
```json
{
  "query": {
    "bool": {
      "filter": {
        "bool": {
          "must": [
            {
              "wildcard": {
                "fieldName": "*value1*"  // 第一个模糊条件
              }
            },
            {
              "wildcard": {
                "fieldName": "*value2*"  // 第二个模糊条件
              }
            },
            // 添加更多的模糊条件
          ]
        }
      }
    }
  }
}
```

# 批量删除索引中的文档
```
POST smartpark-jf/_delete_by_query?scroll=5m&conflicts=proceed&timeout=5m&slices=50
{
  "query": {
    "range": {
      "@timestamp": {
        "lt": "2023-06-16T00:00:00Z"
      }
    }
  },
  "size": 10000
}
```
在SSD上，上面的参数在性能上表现优异，平均每秒删除上万个文档
# 只删除数据
```
POST /ldc_elastic/_delete_by_query
{
  "query": { 
    "match_all": {} 
  }
}
```

# 安装分词器
IK 中文分词器
插件下载地址：https://github.com/medcl/elasticsearch-analysis-ik/releases
（注意必须下载和使用的Elasticsearch 匹配的版本）

1. 执行插件安装命令：
./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.17.0/elasticsearch-analysis-ik-7.17.3.zip  
或者
./bin/elasticsearch-plugin install file:///data/elasticsearch-7.17.0/bin/elasticsearch-analysis-ik-7.17.0.zip
2. 重启ES 即生效
3. 检查是否安装成功  
GET _cat/plugins

# 使用S3接口进行备份恢复
1. 申请S3桶
```
访问地址：osstest.xxx.com
AK：xxxxxxxxxxxxxxxxxxxx
SK：xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
存储桶：es-backup-test-ldc
容量：20GB
```
2.	在ES所有节点上安装S3插件

```sh
#下载 repository-s3 到 bin 目录
cd /data/elasticsearch-7.17.0/bin/
wget https://artifacts.elastic.co/downloads/elasticsearch-plugins/repository-s3/repository-s3-7.17.0.zip
cd /data/elasticsearch-7.17.0/
./bin/elasticsearch-plugin install  file:///data/elasticsearch-7.17.0/bin/repository-s3-7.17.0.zip

# 如果有网络的话可以直接安装
sudo bin/elasticsearch-plugin install --batch repository-s3
```
#需要重启ES
```sh
bin/elasticsearch -d
```
3.	配置存储库
```json
PUT _snapshot/my_s3_repository
{
  "type": "s3",
  "settings": {
    "bucket": "es-backup-test-ldc",
    "region": "us",
    "access_key":"xxxxxxxxxxxxxxxxxxxx",
    "secret_key":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "protocol":"https",
    "endpoint": "osstest.xxx.com",
    "path_style_access": "true",
    "signer_override": "S3SignerType",
    "compress": true,
    "base_path": "backup",
    "chunk_size": "10gb",
    "max_restore_bytes_per_sec": "100mb",
    "max_snapshot_bytes_per_sec": "40mb",
    "readonly": "false",
    "storage_class": "standard"
    
  }
}
```
```sh
# 记得设置 allow_insecure_settings，要不注册S3时会报错
echo "-Des.allow_insecure_settings=true" >> config/jvm.options
```
4.	备份索引
```json
PUT /_snapshot/my_s3_repository/snapshot_1?wait_for_completion=true
{
  "indices": "shard_scale_test,new_shard_scale_test",
  "ignore_unavailable": true,
  "include_global_state": false,
  "metadata": {
    "taken_by": "lindeci",
    "taken_because": "ES backup test."
    }
}
```
在Kibana上查看备份结果
 
5.	恢复索引
```json
在kibana上选择需要恢复得快照
 
选择需要恢复的索引，重命名索引的名字（可选）
 
允许对恢复后的索引进行调整（比如分片数、副本数）
 
确认恢复
 
查看恢复进度
``` 
6.	检查恢复的结果

7. 查看 snapshot 的配置
```sh
GET _snapshot/backup-repo
```
8. 查看 备份列表
```sh
GET _cat/snapshots/backup-repo?v
```
9. 另外一种注册 snapshots 的办法
```json
bin/elasticsearch-plugin install repository-s3
bin/elasticsearch-keystore add s3.client.default.access_key
bin/elasticsearch-keystore add s3.client.default.secret_key

PUT _snapshot/backup-repository
{
	"type": "s3",
	"settings": {
		"endpoint":"xx.xx.com",
		"path_style_access": "true",
		"region": "us",
		"compress" : "true",
		"bucket": "elastic",
		"storageclass": "STANDARD"
	}
}
# 注意：设置后需要重启才能生效
```
10. 在kibana上调整快照得保留时间  
它会设置文件在S3中的过期时间，回收工作交给S3执行。

# 查看 索引 是否可用状态
```
GET /_cat/indices?v

health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .apm-agent-configuration        QT5dCRf2SSuB7QUAeMRPgQ   1   1          0            0       452b           226b
green  open   test-14                         vkra2dZHSEyoJbwGeOr81Q  20   2   23336827            0      9.9gb          3.2gb
green  open   test-15                         dpvPPPqlRbWILxvBgUf6KA  20   2   23328360            0      9.9gb          3.3gb
green  open   test-12                         Ic9_Xp18Q4ydNqwn95WlDg  20   2   23328549            0      9.8gb          3.2gb
green  open   test-13                         4tGx1mesQz6MFICs2OQxmw  20   2   23327710            0      9.8gb          3.2gb
green  open   test-11                         PtwYnDVuQH6yCBMAkF0DGg  20   2   23327104            0      9.8gb          3.2gb
green  open   .tasks                          j7ULxampSJ-0EehI1fdF8Q   1   1         10            0      101kb         50.5kb
green  open   .security-7                     -1EpN5-XRduAOyk1h0YhqA   1   1         60            0    520.4kb        260.2kb
green  open   .kibana_7.17.0_001              f4Xx9ADcQjCyAM2qkfB7gg   1   1        155           16      4.8mb          2.4mb
green  open   .apm-custom-link                oGnbOEEPSMGJWAjCnGgKLQ   1   1          0            0       452b           226b
green  open   .async-search                   kvnS9MxOT5GCpt5cnzOwQQ   1   1          0            0      6.8kb          3.4kb
green  open   .kibana_task_manager_7.17.0_001 owVOHGapReG9DVvDG31YHQ   1   1         18         2095    679.5kb        375.5kb
green  open   .orphaned-logstash-2023.04.07   XNtur_TKSNizGiIRmhQ2SA   6   1         15            0    174.9kb         87.4kb
``` 
# 重启 data 节点导致索引变 yellow 分析
## 可能的情况
```yaml
INDEX_CREATED: 集群正在创建索引。
CLUSTER_RECOVERED: 集群处于重启阶段。
INDEX_OPENED: 正在重新打开一个已经关闭的索引。NEW_INDEX_RESTORED:还原数据到一个新索引。
EXISTING_INDEX_RESTORED: 还原数据到一个已经关闭的索引。
REPLICA_ADDED: 索引的设置被修改，副本数增加。
REROUTE_CANCELLED: 由于reroute命令被取消导致有一些分片没有被分配。
REINITIALIZED: 由于一个分片的状态重新退回到初始化导致。
REALLOCATED_REPLICA: 副本位置变化导致未分配。


只有下面几个状态是明确地由于分片错误导致的：

ALLOCATION_FAILED: 由于配置原因或者资源问题导致未分配情况。
DANGLING_INDEX_IMPORTED: 副本在节点离线情况下被修改，在这个副本回到集群中时会产生此问题。
```
ES提供了healthAPI供我们查询集群的状态和发现问题的原因：
参考文档：https://www.elastic.co/guide/en/elasticsearch/reference/7.17/cluster-health.html
```yaml
GET _cluster/health: 检测集群的健康状态，可以使用这个API检测集群的节点数量
GET _cluster/health?level=indices: 查看全部索引的状态，找出有问题的索引
GET _cluster/health/index_name: 检测某个索引的状态，分析问题
GET _cluster/health?level=shards: 查看分片分配的情况，寻找未分配的分片
GET _cluster/allocation/explain: 查看第一个未分配分配的故障原因
```
## 重启数据节点时节省索引副本恢复时间的办法
### 思路
- 在重启节点之前禁用副本分配，以避免不必要的I/O操作1。
- 调整集群的相关设置来加快分配速度。例如，您可以调整`cluster.routing.allocation.node_concurrent_recoveries`和`indices.recovery.max_bytes_per_sec`等参数来加快分片恢复速度。
- 您还可以调整集群的延迟分配超时时间，以避免集群认为节点失效而发起均衡。例如，您可以在重启节点前使用以下命令来调整延迟分配超时时间：
```yaml
PUT /_all/_settings
{
  "settings": {
    "index.unassigned.node_left.delayed_timeout": "5m"
  }
}
```
### 集群正确重启方式
在elasticsearch集群中，当集群发现某个节点关闭时，将延迟一分钟后（默认）再开始将该节点上的分片复制到集群中的其他节点，这可能涉及很多I / O。由于该节点不久将要重新启动，因此该I / O是不必要的
1. 禁止分片自动分布
```yaml
curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "cluster.routing.allocation.enable": "primaries"
  }
}
```
2. 执行同步刷新
```yaml
curl -X POST "localhost:9200/_flush/synced?pretty"
```
注意：  
执行同步刷新时，请检查响应以确保没有失败。尽管请求本身仍返回200 OK状态，但在响应正文中列出了由于挂起索引操作而失败的同步刷新操作。如果失败，请重新发出请求。

3. 重启所有节点  
等所有节点启动完成后，可以通过执行如下请求查看集群状态
```yaml
curl -X GET "localhost:9200/_cat/health?pretty"
curl -X GET "localhost:9200/_cat/nodes?pretty"
```
4. 启用分片自动分布  
当所有节点都已加入集群并恢复了其主要分片后，可通过恢复cluster.routing.allocation.enable为其默认值来重新启用分配：
```yaml
curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
{
  "persistent": {
    "cluster.routing.allocation.enable": null
  }
}
```
重新启用分配后，集群便开始将副本分片分配给数据节点。此时，恢复索引和搜索是安全的，但是如果您可以等待直到成功分配了所有主分片和副本分片并且所有节点的状态为，集群就会恢复得更快green。

可以使用_cat/health和 _cat/recoveryAPI 监视进度
```yaml
curl -X GET "localhost:9200/_cat/health?pretty"
curl -X GET "localhost:9200/_cat/recovery?pretty"
```
## 重启过程的原理
在Elasticsearch中，当一个节点重新加入集群时，它会与主节点进行握手并协商恢复本地分片。在这个过程中，主节点会将集群中最新的元数据发送给该节点，并与该节点上的本地分片进行比较。如果发现本地分片落后于集群中的最新状态，那么主节点会安排对该分片进行增量恢复，以便将其追赶到最新状态

## 某案例分析
并没有分配副本失败，只是分配比较慢  

可以尝试使用`_cluster/allocation/explain` API来查看分配失败的原因  
可以尝试使用`_cluster/reroute` API来手动重新分配分片
```sh
GET _cluster/allocation/explain
{
  "index": "my-index-000001",
  "shard": 0,
  "primary": true
}
这个命令会返回一个JSON对象，其中包含了关于该分片为什么未能分配的详细信息
```

分配速度比较慢
可以调整`cluster.routing.allocation.node_concurrent_recoveries`和`indices.recovery.max_bytes_per_sec`等参数来加快分片恢复速度
```json
GET /_cluster/settings?include_defaults=true&filter_path=**.node_concurrent_recoveries,**.max_bytes_per_sec
```
返回

```json
{
  "defaults" : {
    "cluster" : {
      "routing" : {
        "allocation" : {
          "node_concurrent_recoveries" : "2"
        }
      }
    },
    "ccr" : {
      "indices" : {
        "recovery" : {
          "max_bytes_per_sec" : "40mb"
        }
      }
    },
    "indices" : {
      "recovery" : {
        "max_bytes_per_sec" : "40mb"
      }
    }
  }
}
```
# 索引调整分片数量的考虑因素
主分片不是越多越好，因为主分片越多，Elasticsearch性能开销也会越大。建议单个节点上同一索引的shard个数不要超5个1。此外，每个分片的大小也应该在合理范围内，一般建议一个分片大小在30~50GB之间。

在 Elasticsearch 中，索引的分片数量是在索引创建时通过设置来确定的，一旦确定就不能更改。如果您发现需要调整分片数量，那么您需要重新索引所有源文档，这个过程称为重新索引。

重新索引是指创建一个与原索引结构属性基本相同的新索引，然后将原索引中的数据复制到新索引中。在新索引中，除了需要变更的地方（例如分片数），其他所有属性都与原索引相同1。

在重新索引过程中，您不需要禁止对原索引的数据写入和更新。虽然重建索引比较耗时，但可以在没有停机的情况下完成。
```json
POST _reindex 
{ 
 "source": {  
   "index": "students1" 
  }, 
 "dest": { 
   "index": "students2" 
  } 
} 
```
_reindex 操作会将源索引的快照数据复制到目标索引。这意味着，在 _reindex 过程中，如果源索引持续有数据写入，这些新写入的数据不会自动同步到目标索引。

_reindex 可以添加过滤条件

想要修改索引的字段类型、分片数量或重命名索引，您需要使用 _reindex API 来重新索引数据。

# 把创建索引的脚本导入ES
```url
curl -X PUT "172.1.1.2:9200/te_te_user"  -uxxxxx:xxxxx  -H 'Content-Type: application/json' -d @te_te_user.json
```

# 聚合查询
## 统计有哪些不同的数值
```sql
GET test/_search
{
  "size": 0,
  "query": {
    "range": {
      "@timestamp": {
        "gte": "2023-08-02"
      }
    }
  },
  "aggs": {
    "log_levels": {
      "terms": {
        "field": "level.keyword",
        "size": 10
      }
    }
  }
}

POST _sql?format=txt
{
  "query": "SELECT level.keyword FROM \"test\" WHERE \"@timestamp\" >= '2023-08-02' GROUP BY level.keyword"
}
```
```sql
curl -X POST "https://172.1.1.1:9200/_sql?format=json" -uelastic:elastic -k -H 'Content-Type: application/json' -d'
{
  "query": "SELECT COUNT(*) as cnt FROM \"logs-ceph-foshan-ssd\" WHERE \"@timestamp\" >= NOW() - INTERVAL 5 MINUTES"
}'
```
## 多个维度聚合
```json
GET test/_search
{
  "size": 0,
  "aggs": {
    "api_logs": {
      "filter": {
        "range": {
          "@timestamp": {
            "gte": "now-180d/d"
          }
        }
      },
      "aggs": {
        "slow_api_count": {
          "filter": {
            "range": {
              "time": {
                "gt": "2023-08-05 00:00:00.000"
              }
            }
          }
        },
        "ERROR_count": {
          "filter": {
            "term": {
              "level.keyword": "ERROR"
            }
          }
        },
        "INFO_count": {
          "filter": {
            "term": {
              "level.keyword": " INFO"
            }
          }
        },
        "WARN_count": {
          "filter": {
            "term": {
              "level.keyword": " WARN"
            }
          }
        }
      }
    }
  }
}
```
# 使用kibana API 创建索引模式
ES中不能创建索引模式

kibana在页面每次只能创建一个索引模式，大批量创建索引模式时，需要调用接口
```sh
curl -f -XPOST -H 'Content-Type: application/json' -H 'kbn-version: 7.17.0' -uelastic:elastic http://172.1.1.2:5601/s/te_xxxx/api/saved_objects/index-pattern -d "{\"attributes\":{\"title\":\"te_iot_xxxx\",\"timeFieldName\":\"create_time\"}}"

# te_xxxx 表示 工作空间
# te_iot_xxxx 表示 索引模式 名字

# 对应的删除索引模式脚本

curl -f -XDELETE -H 'kbn-version: 7.17.0' -H 'kbn-xsrf: anything' -uelastic:elastic http://172.1.1.2:5601/s/te_xxxx/api/saved_objects/index-pattern/te_iot_xxxx
```

# curl 删除 索引
url  -X DELETE  'http://172.1.1.3:9200/.ds-xxx-2023.10.21-001211' -uelastic:xxxx

# 添加只读用户
```json
POST /_security/role/cmdb_read
{
  "indices": [
    {
      "names": [ "*" ],
      "privileges": [ "read" ]
    }
  ]
}

POST /_security/user/cmdb_read
{
  "password" : "cmdb@123",
  "roles" : [ "cmdb_read"]
}
```

# 修改密码
```curl
curl -u elastic:123456 -XPOST 'localhost:9200/_security/user/elastic/_password' -H "Content-Type: application/json" -d'
{
  "password" : "xxxxxxx"
}'
```
```yml
POST /_security/user/elastic/_password
{
  "password" : "xxxxxxx"
}
```


# 统计 ingress 日志的异常信息
```sh
#!/bin/bash
yum install -y jq

if [ -z "${begin_time}" ]; then
    begin_time=$(date -d"-120 seconds" '+%Y-%m-%dT%H:%M:%S')
fi

while true
do
	end_time=$(date -d"-60 seconds" '+%Y-%m-%dT%H:%M:%S')
	warnings=`curl -X POST "http://172.1.1.1:9200/_sql?format=json" -uelastic:111 -H 'Content-Type: application/json' -d "{\"query\": \"SELECT COUNT(*) as cnt FROM \\\"ingress-nginx\\\" WHERE status between 400 and 599 and upstream_status between 400 and 599 and \\\"@timestamp\\\" between '$begin_time' and '$end_time' and proxy_upstream_name like 'evoc1-diving%'\"}" | jq -r '.rows[0] | @tsv'`

	cat <<EOF | curl --data-binary @- http://172.1.3.1:9001/metrics/job/nfs-$instance_ip/instance/$instance_ip
	# TYPE warnings
	warnings $warnings
	EOF
	
	begin_time=$end_time
	sleep 60
done
```

```sh
cat eslog-script.sh
#!/bin/bash
instance_ip=1.1.1.9
begin_time=$(TZ='UTC+0'  date -d"-60 seconds" '+%Y-%m-%dT%H:%M:%S')
end_time=$(TZ='UTC+0'  date -d"seconds" '+%Y-%m-%dT%H:%M:%S')
#ES的地址串
ES_url=172.1.1.3:9200
#ES的用户密码
ES_user=elastic:xxxxx
#项目列表
project_list=("qiandong" "diving" "promotion")
#索引名字
index_name=ingress-nginx

for project in "${project_list[@]}"
do
  #计算4xx的个数
  warnings_total=`curl -X POST "$ES_url/_sql?format=json" -u$ES_user -H 'Content-Type: application/json' -d "{\"query\": \"SELECT COUNT(*) as cnt FROM \\\"$index_name\\\" WHERE (status between 400 and 599 or upstream_status between 400 and 599) and \\\"@timestamp\\\" between '$begin_time' and '$end_time' and proxy_upstream_name like '$project%'\"}" | jq -r '.rows[0] | @tsv'`
  #计算总数
  total=`curl -X POST "$ES_url/_sql?format=json" -u$ES_user -H 'Content-Type: application/json' -d "{\"query\": \"SELECT COUNT(*) as cnt FROM \\\"$index_name\\\" WHERE \\\"@timestamp\\\" between '$begin_time' and '$end_time' and proxy_upstream_name like '$project%'\"}" | jq -r '.rows[0] | @tsv'`
  #计算占比
  if [ "$total" -eq 0 ]; then
    percent=0
  else
    percent=$(echo "scale=2; $warnings_total / $total * 100" | bc)
  fi
  
  # 发送邮件告警，发送的内容有 $project $warnings_total $total $percent
done


#cat <<EOF | curl --data-binary @- http://1.1.3.1:9001/metrics/job/es-$instance_ip/instance/$instance_ip
  # TYPE warnings_num
#  es_warnings $warnings_num


#EOF
```
重写
```sh
#!/bin/bash
instance_ip=1.1.1.9
begin_time=$(TZ='UTC+0'  date -d"-60 seconds" '+%Y-%m-%dT%H:%M:%S')
end_time=$(TZ='UTC+0'  date -d"seconds" '+%Y-%m-%dT%H:%M:%S')
#ES的地址串
ES_url=172.1.1.3:9200
#ES的用户密码
ES_user=elastic:xxxxx
#项目列表
project_list=("qiandong" "evoc1-diving" "evoc1-promotion")
#索引名字
#index_name=ingress-nginx
index_name=logs-prod-ingress-nginx

for project in "${project_list[@]}"
do
  #计算4xx的个数
  warnings_total=`curl -s -X POST "$ES_url/_sql?format=json" -u$ES_user -H "Content-Type: application/json" -d '{"query": "SELECT COUNT(*) as cnt FROM \"'$index'\" WHERE (status between 400 and 599 or upstream_status between 400 and 599) and \"@timestamp\" between '\'$begin_time\'' and '\'$end_time\'' and proxy_upstream_name like '\'$project%\''"}' | jq -r '.rows[0] | @tsv'` 
  #计算总数
  total=`curl -s -X POST "$ES_url/_sql?format=json" -u$ES_user -H "Content-Type: application/json" -d '{"query": "SELECT COUNT(*) as cnt FROM \"'$index'\" WHERE \"@timestamp\" between '\'$begin_time\'' and '\'$end_time\'' and proxy_upstream_name like '\'$project%\''"}' | jq -r '.rows[0] | @tsv'`
  #计算占比
  if [ "$total" -eq 0 ]; then
    percent=0
  else
    percent=$(echo "scale=2; $warnings_total / $total * 100" | bc)
  fi
  
  # 发送邮件告警，发送的内容有 $project $warnings_total $total $percent
  echo $project $warnings_total $total $percent
done
```

ELASTICSEARCH NGINX LOGS 这个grafana模板很炫

# 权限讲解
## Elasticsearch 权限说明

**all**：执行索引或数据流的所有操作。

**auto_configure**：允许自动创建索引和数据流。当不存在目标索引或数据流时，会自动创建索引或数据流。

**create**：允许索引文档，可以覆盖任何现有文档，但不能更新现有文档。

**create_doc**：仅允许创建新文档，不能覆盖或更新现有文档。

**create_index**：允许创建索引或数据流。创建索引请求可能包含要添加到创建后索引的别名。

**delete**：允许删除文档。

**delete_index**：允许删除索引或数据流。

**index**：允许索引（包括覆盖）和更新文档。

**maintenance**：允许刷新、刷新缓冲区、同步刷新和强制合并索引管理操作。没有读取或写入索引数据或管理索引的权限。

**manage**：所有监控权限加上索引和数据流管理（别名、分析、清除缓存、关闭、删除、是否存在、刷新、映射、打开、字段能力、强制合并、刷新、设置、搜索分片、验证查询）。

**manage_follow_index**：管理跟随索引生命周期的所有操作，包括创建跟随索引、关闭跟随索引以及将其转换为常规索引。此权限仅在包含跟随索引的集群中需要。

**manage_ilm**：所有与管理索引或数据流的策略执行相关的索引生命周期管理操作。这包括重试策略和从索引或数据流中删除策略等操作。

**manage_leader_index**：管理领导索引生命周期的所有操作，包括忘记跟随者。此权限仅在包含领导索引的集群中需要。

**monitor**：所有监控所需的操作（恢复、段信息、索引统计信息和状态）。

**read**：对操作的只读访问（count、explain、get、mget、get indexed scripts、more like this、multi percolate/search/termvector、percolate、scroll、clear_scroll、search、suggest、tv）。

**read_cross_cluster**：从远程集群对搜索操作的只读访问。

**view_index_metadata**：对索引和数据流元数据的只读访问（别名、是否存在、字段功能、字段映射、获取索引、获取数据流、ilm explain、映射、搜索分片、设置、验证查询）。此权限主要供 Kibana 用户使用。

**write**：对文档执行所有写操作的权限，包括索引、更新和删除文档的权限，以及执行批量操作的权限，并允许作为这些操作结果的动态映射更新。
```
auto_configure create create_doc create_index delete delete_index index manage_ilm read view_index_metadata write
# 剔除 delete_index 权限
auto_configure create create_doc create_index delete index manage_ilm read view_index_metadata write
```
# 命令行授权
```json
PUT /_security/role/iot
{
  "cluster": ["all"],
  "indices": [
    {
      "names": ["te_iot_*"],
      "privileges": ["auto_configure", "create", "create_doc", "create_index", "delete", "index", "manage_ilm", "read", "view_index_metadata", "write"]
    }
  ]
}

PUT /_security/user/iot
{
  "password" : "iot@123",
  "roles" : [ "iot" ],
  "full_name" : "iot"
}
```

# 别名操作
```
# 查看别名关联哪些索引
POST /_aliases
{
  "actions" : [
    { "remove" : { "index" : "xx_xx_tenant_v1.0", "alias" : "xx_xx_tenant" } }
  ]
}
# 删除别名跟索引的关联
POST /_aliases
{
  "actions" : [
    { "remove" : { "index" : "xx_xx_tenant_v1.1", "alias" : "xx_xx_tenant" } }
  ]
}
```
# 查看索引碎片恢复进度
```
GET /_cat/recovery?v
GET /_cat/recovery/shard_scale_test?v
index            shard time  type        stage source_host   source_node target_host   target_node repository snapshot files files_recovered files_percent files_total bytes bytes_recovered bytes_percent bytes_total translog_ops translog_ops_recovered translog_ops_percent
shard_scale_test 0     341ms empty_store done  n/a           n/a         172.16.13.196 es01        n/a        n/a      0     0               0.0%          0           0     0               0.0%          0           0            0                      100.0%
shard_scale_test 0     846ms peer        done  172.16.13.196 es01        172.16.13.197 es02        n/a        n/a      4     4               100.0%        4           4907  4907            100.0%        4907        0            0                      100.0%
shard_scale_test 1     299ms peer        done  172.16.13.197 es02        172.16.13.196 es01        n/a        n/a      4     4               100.0%        4           4693  4693            100.0%        4693        0            0                      100.0%
shard_scale_test 1     224ms empty_store done  n/a           n/a         172.16.13.197 es02        n/a        n/a      0     0               0.0%          0           0     0               0.0%          0           0            0                      100.0%

GET _cluster/settings
返回
{
  "persistent" : { },
  "transient" : { }
}

curl -X GET http://172.1.1.1:9200/_cat/recovery?h=index,shard,time,type,stage,target_host,files,files_percent,bytes,bytes_percent,translog_ops,translog_ops_percent\&v
或者
GET /_cat/recovery?h=index,shard,time,type,stage,target_host,files,files_percent,bytes,bytes_percent,translog_ops,translog_ops_percent&v

index                           shard time  type           stage target_host   files files_percent bytes   bytes_percent translog_ops translog_ops_percent
.kibana_7.17.0_001              0     262ms existing_store done  172.16.13.196 0     100.0%        0       100.0%        0            100.0%
.kibana_7.17.0_001              0     2.1s  peer           done  172.16.13.198 63    100.0%        2546563 100.0%        37           100.0%
.apm-custom-link                0     109ms peer           done  172.16.13.197 0     0.0%          0       0.0%          0            100.0%
.apm-custom-link                0     894ms peer           done  172.16.13.198 1     100.0%        226     100.0%        0            100.0%
.apm-agent-configuration        0     252ms peer           done  172.16.13.196 0     0.0%          0       0.0%          0            100.0%
.apm-agent-configuration        0     1.6s  existing_store done  172.16.13.197 0     100.0%        0       100.0%        0            100.0%
shard_scale_test                0     341ms empty_store    done  172.16.13.196 0     0.0%          0       0.0%          0            100.0%
shard_scale_test                0     846ms peer           done  172.16.13.197 4     100.0%        4907    100.0%        0            100.0%
shard_scale_test                1     299ms peer           done  172.16.13.196 4     100.0%        4693    100.0%        0            100.0%
shard_scale_test                1     224ms empty_store    done  172.16.13.197 0     0.0%          0       0.0%          0            100.0%
.kibana_task_manager_7.17.0_001 0     195ms existing_store done  172.16.13.196 0     100.0%        0       100.0%        0            100.0%
.kibana_task_manager_7.17.0_001 0     41.4s peer           done  172.16.13.198 71    100.0%        296414  100.0%        248744       100.0%
.tasks                          0     1.3s  existing_store done  172.16.13.196 0     100.0%        0       100.0%        0            100.0%
.tasks                          0     291ms peer           done  172.16.13.197 0     0.0%          0       0.0%          0            100.0%
```
# 各节点上已存在的数据
```
GET /_cat/allocation?v
shards disk.indices disk.used disk.avail disk.total disk.percent host          ip            node
    11       69.4mb    11.3gb    187.6gb    198.9gb            5 172.16.13.197 172.16.13.197 es02
    11       69.3mb    12.1gb    186.8gb    198.9gb            6 172.16.13.196 172.16.13.196 es01
```

# 索引分片分配情况
```
GET _cat/shards?v
GET _cat/shards/shard_scale_test?v
index            shard prirep state   docs store ip            node
shard_scale_test 1     r      STARTED    6 4.5kb 172.16.13.196 es01
shard_scale_test 1     p      STARTED    6 4.5kb 172.16.13.197 es02
shard_scale_test 0     p      STARTED    9 4.7kb 172.16.13.196 es01
shard_scale_test 0     r      STARTED    9 4.7kb 172.16.13.197 es02
```
# split操做
```
对索引锁写，以便下面执行split操做
PUT shard_scale_test/_settings
{
    "blocks.write": true
}

写数据测试，确保锁写生效
PUT shard_scale_test/_doc/21
{"title":"hello_21","contend":"contend_21"}


取消索引别名
PUT shard_scale_test/_alias/my_shard_scale_test
GET shard_scale_test/_alias
DELETE shard_scale_test/_alias/my_shard_scale_test
GET shard_scale_test/_alias

开始执行 split 切分索引的操做，new_shard_scale_test，且主shard数量为8
POST shard_scale_test/_split/new_shard_scale_test
{
	"settings": {
    "index.number_of_shards": 8,
    "index.number_of_replicas": 0
  }
}

# 对新的index添加alias
PUT new_shard_scale_test/_alias/my_shard_scale_test
GET new_shard_scale_test/_alias

补充：
查看split的进度，可使用 _cat/recovery 这个api， 或者在 cerebro 界面上查看。

对新索引写数据测试,能够看到失败的
PUT new_shard_scale_test/_doc/21
{"title":"hello_21","contend":"contend_21"}

打开索引的写功能
PUT new_shard_scale_test/_settings
{
    "blocks.write": false
}
再次对新索引写数据测试,能够看到此时，写入是成功的
PUT new_shard_scale_test/_doc/21
{"title":"hello_21","contend":"contend_21"}

删除索引
DELETE shard_scale_test
```
# _cluster/settings 设置
```
PUT _cluster/settings
{ 
  "persistent" :
  { 
     "cluster.routing.rebalance.enable": "none",
       ##允许在一个节点上发生多少并发传入分片恢复。 默认为2。
       ##多数为副本
      "cluster.routing.allocation.node_concurrent_incoming_recoveries":2，
      ##允许在一个节点上发生多少并发传出分片恢复，默认为2.
       ## 多数为主分片
      "cluster.routing.allocation.node_concurrent_outgoing_recoveries":2,
       ##为上面两个的统一简写
      "cluster.routing.allocation.node_concurrent_recoveries":2,
      ##在通过网络恢复副本时，节点重新启动后未分配的主节点的恢复使用来自本地  磁盘的数据。 
      ##这些应该很快，因此更多初始主要恢复可以在同一节点上并行发生。 默认为4。
      "cluster.routing.allocation.node_initial_primaries_recoveries":4,
      ##允许执行检查以防止基于主机名和主机地址在单个主机上分配同一分片的多个实例。 
      ##默认为false，表示默认情况下不执行检查。 此设置仅适用于在同一台计算机上启动多个节点的情况。这个我的理解是如果设置为false，
      ##则同一个节点上多个实例可以存储同一个shard的多个副本没有容灾作用了
      "cluster.routing.allocation.same_shard.host":true
    }
}
```
# 缩容测试
```
PUT _cluster/settings
{
  "transient" : {
    "cluster.routing.allocation.exclude._ip" : "172.16.13.197"
  }
}
执行成功后观察，节点还在集群内
GET _cat/nodes?v
ip            heap.percent ram.percent cpu load_1m load_5m load_15m node.role   master name
172.16.13.198           45          59   1    0.26    0.13     0.10 cdfhilmrstw -      es03
172.16.13.196           48          76   2    0.12    0.11     0.10 cdfhilmrstw *      es01
172.16.13.197           60          73   0    0.02    0.01     0.00 cdfhilmrstw -      es02

但是192.168.0.151和192.168.0.152上面已经没有数据了（第二个字段可以看出）
GET _cat/allocation?v
shards disk.indices disk.used disk.avail disk.total disk.percent host          ip            node
    15       75.8mb    12.3gb    186.6gb    198.9gb            6 172.16.13.196 172.16.13.196 es01
     0           0b    11.1gb    187.8gb    198.9gb            5 172.16.13.197 172.16.13.197 es02
    15       50.6mb     4.3gb    194.6gb    198.9gb            2 172.16.13.198 172.16.13.198 es03

开始缩容
关停1个节点
停止es02上的elasticsearch实例
ps -ef|grep elasticsearch
kill -SIGTERM 54652 54627
ps -ef|grep elasticsearch

观察集群和索引

两个节点已经没了

GET _cat/nodes?v
ip            heap.percent ram.percent cpu load_1m load_5m load_15m node.role   master name
172.16.13.198           12          60   2    0.17    0.09     0.09 cdfhilmrstw -      es03
172.16.13.196           16          76   3    0.26    0.15     0.11 cdfhilmrstw *      es01

GET _cat/allocation?v
shards disk.indices disk.used disk.avail disk.total disk.percent host          ip            node
    15      156.9mb    12.4gb    186.5gb    198.9gb            6 172.16.13.196 172.16.13.196 es01
    15       51.3mb     4.4gb    194.5gb    198.9gb            2 172.16.13.198 172.16.13.198 es03
	
索引健康
GET _cat/indices?v
health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases                9SbjRGZfSxOVtQMB9AW30A   1   1         44           76    162.5mb        120.6mb
green  open   .kibana_7.17.0_001              FiGjsJClR9WeWGxMHOwJvw   1   1        165           19      7.2mb          4.7mb
green  open   .apm-custom-link                6wjGLXxZRL-bZV4sRaWB-w   1   1          0            0       452b           226b
green  open   .apm-agent-configuration        3zBy2kGKTkCcEEjud72c0Q   1   1          0            0       452b           226b
green  open   shard_scale_test                mEg1a0qVSu-8Wi1xAFr3cQ   2   1         15            0     18.7kb          9.3kb
green  open   new_shard_scale_test            v4fm0LclSxagUiQdbOuX0A   8   0         16            2     32.8kb         32.8kb
green  open   .kibana_task_manager_7.17.0_001 RVkFQGMhS1CIZxJ4iIpDgA   1   1         17       312150     37.5mb         31.3mb
green  open   .tasks                          GWlaPX51SEK3Ow-72C_KVQ   1   1          4            0     43.1kb         21.5kb

集群健康
GET _cat/health?v
epoch      timestamp cluster    status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
1668494613 06:43:33  es-cluster green           2         2     30  19    0    0        0             0                  -                100.0%

缩容完成

结论：先禁止数据分配，而后等数据分配完成后，再关停节点，即可无损缩容
```
# 查询仓库
```
查询仓库
GET _snapshot

{
  "my_s3_repository" : {
    "type" : "s3",
    "settings" : {
      "path_style_access" : "true",
      "signer_override" : "S3SignerType",
      "chunk_size" : "10gb",
      "max_restore_bytes_per_sec" : "100mb",
      "storage_class" : "standard",
      "compress" : "true",
      "base_path" : "backup",
      "max_snapshot_bytes_per_sec" : "40mb",
      "bucket" : "es-backup-test-ldc",
      "endpoint" : "osstest.qevoc.com",
      "protocol" : "https",
      "readonly" : "false",
      "region" : "us"
    }
  }
}

通过verify 验证节点仓库是否在所有节点已生效
POST /_snapshot/my_fs_backup/_verify

{
  "nodes" : {
    "x69-suuTTzG5lDQFQg8cbQ" : {
      "name" : "es01"
    },
    "lnOjL2RlTJClMMR0e8An8g" : {
      "name" : "es02"
    },
    "DTt2FGRgTG-fP3cnq5Da5g" : {
      "name" : "es03"
    }
  }
}

Snapshot 快照备份
# wait_for_completion 参数表示是否要同步等Snapshot 创建完成再返回
# PUT 请求如果传参为空则默认备份所有可读索引、流
# my_fs_backup：指定(已创建的)仓库名称
# snapshot_1：指定快照名称
PUT /_snapshot/my_fs_backup/snapshot_1?wait_for_completion=true
{
# indices：指定要进行快照备份的索引、流
"indices": "hundredsman,index_1,index_2",
# ignore_unavailable：忽略不可用的索引和流
"ignore_unavailable": true,
# include_global_state：是否保存集群全局状态
"include_global_state": false,
# metadata：元数据，一些注释性的数据。
"metadata": {
"taken_by": "james",
"taken_because": "Hundreds man fighting for book backup."
}
}


PUT /_snapshot/my_s3_repository/snapshot_1?wait_for_completion=true
{
  "indices": "shard_scale_test,new_shard_scale_test",
  "ignore_unavailable": true,
  "include_global_state": false,
  "metadata": {
    "taken_by": "lindeci",
    "taken_because": "ES backup test."
    }
}

{
  "snapshot" : {
    "snapshot" : "snapshot_1",
    "uuid" : "st_BSc9dSAicoAWPH3xVdQ",
    "repository" : "my_s3_repository",
    "version_id" : 7170099,
    "version" : "7.17.0",
    "indices" : [
      "shard_scale_test",
      "new_shard_scale_test"
    ],
    "data_streams" : [ ],
    "include_global_state" : false,
    "metadata" : {
      "taken_by" : "lindeci",
      "taken_because" : "ES backup test."
    },
    "state" : "SUCCESS",
    "start_time" : "2022-12-12T11:47:19.210Z",
    "start_time_in_millis" : 1670845639210,
    "end_time" : "2022-12-12T11:47:20.612Z",
    "end_time_in_millis" : 1670845640612,
    "duration_in_millis" : 1402,
    "failures" : [ ],
    "shards" : {
      "total" : 10,
      "failed" : 0,
      "successful" : 10
    },
    "feature_states" : [ ]
  }
}
```
# s3 备份
```
PUT /_snapshot/backup-repo/chencheng_backup_20221213_01?wait_for_completion=true
{
  "indices": "device_elastic,gateway_elastic,device_model",
  "ignore_unavailable": true,
  "include_global_state": false,
  "metadata": {
    "taken_by": "lindeci",
    "taken_because": "ES backup device_elastic,gateway_elastic,device_model."
    }
}
访问地址：osstest.qevoc.com
AK：B5JYXZE264Q4IDFKG7S7
SK：5NpkFxdZbgD9ZBrOnzsL8mhhiaWDCJk1Qtz3AnEq
存储桶：es-backup-test-ldc
容量：20GB
```

# snmptrap 的 logstash 测试、配置
```
bin/logstash-plugin list |grep snmp

snmptrap {
        port => "1064"
        community => ["public"]
        host => "192.168.101.204"
    }
	
	
snmptrap -v 2c -c public 172.16.13.196 "" .1.3.6.1.4.1.2021.251.1 sysLocation.0 s "i come from hadoop02 trap message"

91iot.qevoc.com





input {
  udp {
    port => 5044
    type => rsyslog
  }
  snmptrap {
    port => 5044
    community => ["public"]
    type => snmptrap
  }
}

filter {
  if [type] == "rsyslog" {
    grok {
      match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])?: %{GREEDYDATA:syslog_message}" }
      add_field => [ "received_at", "%{@timestamp}" ]
      add_field => [ "received_from", "%{host}" ]
    }
    date {
      match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["172.16.13.196:9200","172.16.13.197:9200","172.16.13.198:9200"]
    index => "network_service_log_v1_%{+YYYY.MM}"
    user => elastic
    password => elastic
  }
  stdout { codec => rubydebug }
}
```

# null 值测试
```sql
PUT /ldc_test
{
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"
      },
      "interface_name": {
        "type": "keyword"
      },
      "interface_var": {
        "type": "text",
        "index": false,
        "analyzer": "ik_max_word"
      }
    }
  }
}

DELETE ldc_test

PUT ldc_test/_bulk
{"index":{"_id":1}}
{"id":1,"interface_name":"test1","interface_var":"test1"}
{"index":{"_id":2}}
{"id":2,"interface_name":"test2","interface_var":"null"}
{"index":{"_id":3}}
{"id":3,"interface_name":"test3","interface_var":""}
{"index":{"_id":4}}
{"id":4,"interface_name":"test4","interface_var":null}
{"index":{"_id":5}}
{"id":5,"interface_name":"test5","interface_var":[]}
{"index":{"_id":6}}
{"id":6,"interface_name":"test6","interface_var":"NULL"}
{"index":{"_id":7}}
{"id":7,"interface_name":"test7","interface_var":"test7"}

POST _sql?format=txt
{
  "query": "SELECT * FROM ldc_test"
}

      id       |interface_name | interface_var 
---------------+---------------+---------------
1              |test1          |test1          
2              |test2          |null           
3              |test3          |               
4              |test4          |null           
5              |test5          |null           
6              |test6          |NULL           
7              |test7          |test7  
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

# 问题处理
## 1、TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark
问题描述
```sh
error=>{"type"=>"cluster_block_exception", "reason"=>"index [xxx] blocked by: [TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark, index has read-only-allow-delete block];"}}
```
问题分析  
磁盘空间紧张导致索引变为只读

问题处理  
```sh
# 清理磁盘空间
# kibana 登录不上去，可以使用下面命令查看索引的大小
curl  -X GET 'https://172.1.1.2:9200/_cat/indices' -uelastic:123456 -k | grep gb
# 然后删除允许删除的非系统索引
curl -X DELETE 'https://172.1.1.2:9200/.xxxx-test-2023.11.30-000024' -uelastic:123456 -k
```
## 2、扩容磁盘空间

## 
# 统计 ingress 最近7天平均响应时间
```
POST _sql?format=txt
{
  "query": """
  SELECT DATE_TRUNC('day', "@timestamp") AS date,
       COUNT(1) AS count, 
       avg(CAST(request_time AS double)) as avg_time
FROM "logs-prod-ingress-nginx"
WHERE request_domain = 'h5.evocqd.com'
  AND "@timestamp" BETWEEN '2024-06-19T00:00:00' AND '2024-06-27T00:00:00'
GROUP BY date
ORDER BY date
  """
}
```

# http 异常 监控 统计
```
cat eslog-script.sh
#!/bin/bash
instance_ip=172.1.1.1
begin_time=$(TZ='UTC+0'  date -d"-60 seconds" '+%Y-%m-%dT%H:%M:%S')
end_time=$(TZ='UTC+0'  date -d"seconds" '+%Y-%m-%dT%H:%M:%S')
warnings_num=$(curl -X POST "http://172.21.16.31:9200/_sql?format=json" -uelastic:ggfw_elastic@123 -H 'Content-Type: application/json' -d "{\"query\": \"SELECT COUNT(*) as cnt FROM \\\"logs-prod-ingress-nginx\\\" WHERE status between 400 and 599 and upstream_status between 400 and 599 and \\\"@timestamp\\\" between '$begin_time' and '$end_time' and proxy_upstream_name like 'evoc1-diving%'\"}" | jq -r '.rows[0] | @tsv')
 
cat <<EOF | curl --data-binary @- http://172.16.3.167:9001/metrics/job/es-$instance_ip/instance/$instance_ip
  # TYPE warnings_num
  es_warnings $warnings_num
EOF
```

# ik 分词器建索引失败
```
PUT appstore_tenant_services_event
{
  "mappings": {
    "properties": {
      "id": { "type": "integer" },
      "create_time": { "type": "date" },
      "event_id": { "type": "keyword" },
      "tenant_id": { "type": "keyword" },
      "service_id": { "type": "keyword" },
      "target": { "type": "keyword" },
      "target_id": { "type": "keyword" },
      "request_body": { "type": "text" },
      "user_name": { "type": "keyword" },
      "start_time": { "type": "keyword" },
      "end_time": { "type": "keyword" },
      "opt_type": { "type": "keyword" },
      "syn_type": { "type": "integer" },
      "status": { "type": "keyword" },
      "final_status": { "type": "keyword" },
      "message": { 
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart_analyzer"
      }
      "reason": { "type": "text" }
    }
  }
}
报错内容：
  "error" : {
    "root_cause" : [
      {
        "type" : "mapper_parsing_exception",
        "reason" : "Failed to parse mapping [_doc]: analyzer [ik_smart_analyzer] has not been configured in mappings"
      }
    ],
    "type" : "mapper_parsing_exception",
    "reason" : "Failed to parse mapping [_doc]: analyzer [ik_smart_analyzer] has not been configured in mappings",
    "caused_by" : {
      "type" : "illegal_argument_exception",
      "reason" : "analyzer [ik_smart_analyzer] has not been configured in mappings"
    }
  },
  "status" : 400
}

修正语句
PUT /appstore_tenant_services_event
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ik_max_word": {
          "type": "custom",
          "tokenizer": "ik_max_word"
        },
        "ik_smart_analyzer": {
          "type": "custom",
          "tokenizer": "ik_smart"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id": { "type": "integer" },
      "create_time": { "type": "date" },
      "event_id": { "type": "keyword" },
      "tenant_id": { "type": "keyword" },
      "service_id": { "type": "keyword" },
      "target": { "type": "keyword" },
      "target_id": { "type": "keyword" },
      "request_body": { "type": "text" },
      "user_name": { "type": "keyword" },
      "start_time": { "type": "keyword" },
      "end_time": { "type": "keyword" },
      "opt_type": { "type": "keyword" },
      "syn_type": { "type": "integer" },
      "status": { "type": "keyword" },
      "final_status": { "type": "keyword" },
      "message": { 
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart"
      },
      "reason": { "type": "text" }
    }
  }
}
```
