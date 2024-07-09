- [mogodb vs es](#mogodb-vs-es)
- [日常运维命令](#日常运维命令)
  - [建库、建用户、授权](#建库建用户授权)
  - [DDL](#ddl)
  - [DML](#dml)
- [开发规范](#开发规范)
- [分片操作](#分片操作)
  - [分片方式](#分片方式)
  - [片键选择因素](#片键选择因素)
- [软件层面优化](#软件层面优化)
  - [设置WiredTiger的cacheSizeGB](#设置wiredtiger的cachesizegb)
  - [2.2 分配足够的Oplog空间](#22-分配足够的oplog空间)
  - [2.3 启用Log Rotation日志切换](#23-启用log-rotation日志切换)
  - [2.4 设置journal日志刷新时间和flush时间](#24-设置journal日志刷新时间和flush时间)
- [mongodb5.0时序解决方案](#mongodb50时序解决方案)
  - [单机测试](#单机测试)
  - [集群模式](#集群模式)
  - [时序表限制 ：](#时序表限制-)
- [慢查询分析](#慢查询分析)
  - [MongoDB慢查询分析](#mongodb慢查询分析)
  - [开启 Profiling 功能](#开启-profiling-功能)
  - [通过system.profile进行分析](#通过systemprofile进行分析)
  - [筛选条件中的语句](#筛选条件中的语句)
  - [explain 对执行语句进行分析](#explain-对执行语句进行分析)
- [压测](#压测)
- [增量备份归档及数据清理](#增量备份归档及数据清理)
- [备份脚本](#备份脚本)
- [开启慢查询](#开启慢查询)
- [强制副本集从节点提升为主实例](#强制副本集从节点提升为主实例)
- [数据分段备份和清理](#数据分段备份和清理)
- [查看副本集延迟问题](#查看副本集延迟问题)
- [脚本统计集合结构信息](#脚本统计集合结构信息)
- [脚本统计集合数据量](#脚本统计集合数据量)
- [启停命令](#启停命令)

# mogodb vs es
MOGODB比ES优势：事务、灵活备份、跨集群数据同步

# 日常运维命令
## 建库、建用户、授权
use modb_func;
db.createUser({user:"modb_func",pwd:"modb_func",roles:[{role:"readWrite",db:"modb_func"}]})
## DDL
```
1、集合重命名
db.sz.renameCollection("sz43");

2、创建索引
db.getCollection("msg_conclusion_log").createIndex(
{ "create_time": NumberInt("1")},
{ name: "create_time_1",
background: true
});

db.getCollection("user_msglist").createIndex(
{ "send_date": NumberInt("1"),"sendid": NumberInt("1"),"recvid": NumberInt("1")},
{ name: "send_date_sendid_recvid_1",
background: true
});

3、如何替换json中的json字符串
3.1 对于数据量小的非生产的场景 用mongoexport导出数据，再用 sed -i 's#osstest.qevoc.com/startwine/#osstest.qevoc.com/startwine-test/#g' RuleBonus_0531.json 进行修改
3.2 用replace批量替换
```
## DML
```
mongo shell 查询数据显示不全，可设置 DBQuery.shellBatchSize= 50，就可显示全数据。
1、更新数据加条件过滤
db.work_stat.updateMany({
$and: [{ deviceId:"00014786"},
{ name: "A座大堂白班-赵宁祥" }]
}, { $set: {
name: "保绿测试",
subjectionName:"保绿部"}})

db.cl21.updateOne({ "_id" : ObjectId("6674ee152a66a1635db5c322") }, { $set: {"StatusName" : "Scheduled-sz"}})


2、查询语句 in id
db.cap_device_msg_handle_received.find({"_id" : { $in :[NumberLong("6414822817352582907"),NumberLong("6414822817352582903"),NumberLong("6414822817352582893")]}}).explain()

3.前缀查询
db.bar.find({ name: { $regex: '^sz' } })
{ "_id" : ObjectId("65bb3f7784801a5fe4fba081"), "x" : 1000001, "name" : "sz12", "name1" : "MACLEAN", "name2" : "MACLEAN", "name3" : "MACLEAN" }
{ "_id" : ObjectId("65bb3f9284801a5fe4fba082"), "x" : 1000001, "name" : "sz888", "name1" : "MACLEAN", "name2" : "MACLEAN", "name3" : "MACLEAN" }

4.查看最新数据
db.work_stat.find().sort({"beginTime" :-1}).limit(2).pretty()
{
"_id" : ObjectId("65d1f0c0b7a12b1b2025b160"),
"beginTime" : ISODate("2024-02-18T11:53:52.299Z"),
"endTime" : ISODate("2024-02-18T11:53:52.299Z"),
"workLength" : 0,
"areaName" : "负1层非机动车停放区域",
"name" : "B座1-3-5--马艳丽",
"sex" : 0,
"deviceId" : "20002555",
"subjectionName" : "保洁组",
"_class" : "com.mote.entity.WorkStat"
}

5.查范围 数据
db.user_msglist_month.find({
"senddate": {
"$gte": NumberLong("1710864000000000"),
"$lt": NumberLong("1710904812000000")
}
})

db.AbpAuditLogs.find({"ExecutionTime" :{"$lt": ISODate("2024-02-21T06:00:53.499Z")}}).count()

6.查看某个字段不为空的数据
db.RuleBonus_bak.find({ "vipConfigs": { $exists: true, $ne: null }})
```

# 开发规范
```
1、命名规范
1.1 库名、集合名使用数字字母下划线,长度最多64个字符,推荐使用业务标识命名
1.2 不能和系统库重合(admin,local,test,config)
1.3 大小写敏感,推荐全部小写
1.4 集合名称禁止以system.开头
1.5 禁止使用_id比如向_id中写入自定义内容
1.6 索引建立命名统一以idx_开头命名

2、使用规范
2.1 建议同一集合内保持数据结构一致，为性能放弃集合内可以字段不一样的特性
2.2 针对超长文本采用压缩存储,防止查询导致网卡阻塞
2.3 研发评估数据量增长较大的表通知dba进行数据分片，研发提供分片键字段
2.4 查询语句一定要走索引,避免全表扫描
2.5 数组内元素查询需要使用 $elemMatch
2.6 更新脚本命名为*.js，脚步头部需要use 库语句，脚本多条语句时内部语句用分号分割

3、索引规范
3.1 索引也遵循联合索引最左匹配原则,建立联合索引时要注意
3.2 分片集合建立索引必须包涵分片键
3.3 规避索引失效场景: 正则表达式及非操作符，如 $nin, $not, 算术运算符，$mod等
3.4 尽量不为数组元素创建索引,一旦指定数组元素索引,MONGO会给数组每个元素都创建索引,导致整体索引体积迅速增大
3.5 建立索引需要使用后台建立语句，即加上 background:true
```

# 分片操作
```
use TSDB
sh.enableSharding("TSDB")
db.createCollection("weather")


sh.shardCollection("TSDB.weather",{"ts":1,"source":1});（默认的范围分片）

sh.shardCollection("TSDB.weather",{"source":"hashed"});（hash分片）

以上两种分片方式二选一
db.weather.createIndex( {"source": 1,"ts": 1 },{background:true})  # 这里的1表示升序，第一个中括号是联合索引。background 表示后台执行
```

## 分片方式
MongoDB提供了基于哈希(hashed)和基于范围(Range)2种分片方式

**哈希分片**
```
sh.shardCollection("database.collection",{<field> : "hashed" } )
```

**范围分片**  
范围分片，可以选择单字段或者多字段
```
sh.shardCollection("database.collection",{<shard key>})
```
## 片键选择因素
分片键的选择需要综合考虑分片键的基数、频率和变化率  
基数：记录数  
频率：跟区分度有关  
变化率：更新频率

# 软件层面优化
## 设置WiredTiger的cacheSizeGB
通过cacheSizeGB选项配置控制WiredTiger引擎使用内存的上限，默认配置在系统可用内存的60%左右。如果一台机器上只部署一个mongod，mongod可以使用所有可用内存，则使用默认配置即可。如果一台机器上部署多个mongod，或者mongod跟其他的一些进程一起部署，则需要根据分给mongod的内存配额来配置cacheSizeGB，按配额的60%左右配置即可。通过配置文件配置cacheSizeGB
## 2.2 分配足够的Oplog空间
类似 MYSQL 的 BINLOG

Oplog是MongoDB local库下的一个固定集合，Secondary就是通过查看Primary 的oplog这个集合来进行复制的。Oplog可以说是MongoDB Replication的纽带。Oplog是固定大小的，它只能保存特定数量的操作日志。如果oplog size过大，会浪费存储空间；如果oplog size过小，老的oplog记录很快就会被覆盖，那么宕机的节点很容易出现无法同步数据的现象，因此设置合理的oplog大小对mongodb很重要。MongoDB默认将其大小设置为可用disk空间的5%（默认最小为1G，最大为50G）。

这里设置oplog为10000MB.
## 2.3 启用Log Rotation日志切换
防止MongoDB的log文件无限增大，占用太多磁盘空间。使用Log Rotation并及时清理历史日志文件，在配置文件配置如下红框设置。

logRotate：日志回转，防止一个日志文件特别大，可选值：rename，重命名日志文件，默认值；reopen，使用Linux日志rotate特性，关闭并重新打开次日志文件，可以避免日志丢失，但是logAppend必须为true。

timeStampFormat：指定日志格式的时间戳格式，可选值：ctime，显示时间戳Wed Dec 31 18:17:54.811；Iso8601-utc，显示时间戳以协调通用时间（UTC）在ISO-8601中的格式，例如，纽约时代的开始时间:1970-01-01t00:00: 00.000z；iso8601-local，显示当地时间ISO-8601格式显示时间戳
## 2.4 设置journal日志刷新时间和flush时间
类似 MYSQL 的 REDOLOG

commitIntervalMs：mongod的journal日志刷新值范围从1到500毫秒。较低的值增加了journal的耐久性，以牺牲性能为代价，在WiredTiger引擎上，默认的日志提交间隔为100毫秒，增大commitIntervalMs可以降低磁盘的IO压力，起到一定的优化作用。不过一般情况下，不建议修改。

syncPeriodSecs：mongod使用fsync操作将数据flush到磁盘的时间间隔，默认值为60（单位：秒），增大该值也可以降低磁盘IO压力，起到一定优化作用。一般情况下，强烈建议不要修改此值。mongod将变更的数据写入journal后再写入内存，并间歇性的将内存数据flush到磁盘中，即延迟写入磁盘，有效提升磁盘效率。此指令不影响journal存储，仅对mongod有效。

# mongodb5.0时序解决方案
官方文档地址：https://www.mongodb.com/developer/how-to/new-time-series-collections/

5.0提供了time-series collections
## 单机测试
```
db.createCollection("weather", {
  timeseries: {
    timeField: "ts",
    metaField: "source",
    granularity: "minutes"
  },
    expireAfterSeconds: 9000
});

一条时序数据
{
   "_id" : ObjectId("60c0d44894c10494260da31e"),
   "source" : {sensorId: 123, region: "americas"},
   "airPressure" : 99 ,
   "windSpeed" : 22,
   "temp" : { "degreesF": 39,
              "degreesC": 3.8
            },
   "ts" : ISODate("2021-05-20T10:24:51.303Z")
}

插入语句实例
db.weather.insertMany([{
   "source": {"sensorId": 5581, "region": "americas"},
   "ts": ISODate("2021-05-18T00:00:00.000Z")
}, {
   "source": {"sensorId": 5571, "region": "americas"},
   "ts": ISODate("2021-05-18T08:00:00.000Z")
}, {
   "source": {"sensorId": 5572, "region": "americas"},
   "ts": ISODate("2021-05-18T12:00:00.000Z")
}, {
   "source": {"sensorId": 5573, "region": "americas"},
   "ts": ISODate("2021-05-18T16:00:00.000Z")
}, {
   "source": {"sensorId": 5574, "region": "americas"},
   "ts": ISODate("2021-05-18T20:00:00.000Z")
}, {
   "source": {"sensorId": 5575, "region": "americas"},
   "ts": ISODate("2021-05-19T00:00:00.000Z")
}, {
   "source": {"sensorId": 5576, "region": "americas"},
   "ts": ISODate("2021-05-19T04:00:00.000Z")
}, {
   "source": {"sensorId": 5577, "region": "americas"},
   "ts": ISODate("2021-05-19T08:00:00.000Z")
}, {
   "source": {"sensorId": 5578, "region": "americas"},
   "ts": ISODate("2021-05-19T12:00:00.000Z")
}, {
   "source": {"sensorId": 5579, "region": "americas"},
   "ts": ISODate("2021-05-19T16:00:00.000Z")
}, {
   "source": {"sensorId": 5580, "region": "americas"},
   "ts": ISODate("2021-05-19T20:00:00.000Z")
}])

建立索引
db.weather.createIndex({ "source.region": 1,"source.sensorId": 1, "ts": 1 })
```
## 集群模式
```
use TSDB
sh.enableSharding("TSDB")
db.createCollection("weather", {
  timeseries: {
    timeField: "Ts",
    metaField: "Source",
    granularity: "seconds"
  },
  expireAfterSeconds: 315360000
});
sh.shardCollection( "TSDB.weather", { "Source.eqid": 1 } )
db.weather.createIndex({ "Source.eqid": 1,"Ts": 1 },{background:true})
```
功能字段说明：

    timeField
    字段为时序字段，其类型必须为MongoDB支持的时间类型比如 ISODate("2021-05-20T10:24:51.303Z") 。

    metaField
    为元数据字段，可用来创建二级索引，可以是一个嵌套的json对象，也可以是一个GUID或者字符串，用于唯一标识时间序列的来源（实际测试发现集群模式必须是嵌套字段）。MongoDB会自动将一段时间内具有相同metaField的测量值聚合到一起并做，以消除存储层中该字段的重复。

    granularity
    为粒度字段，即时序数据的更新频率，默认为秒级( seconds )。

    expireAfterSeconds
    过期字段，并非新增字段。时序数据配上TTL索引，让时序数据可以自动淘汰。

如果建时序表的时候指定了 expireAfterSeconds ，则不需要再创建TTL索引了。之后想修改时间需要使用 collMod 命令。未来还可以配合Atlas在线归档（ Online Archive ）功能来进行使用。

## 时序表限制 ：

    append only，不支持更新/删除
    不支持Change Streams，Realm Sync 或 Atlas Search
    只能在metaField和timeField上创建二级索引等
    5.0.6之后社区版支持分片

# 慢查询分析
## MongoDB慢查询分析

开启 Profiling 功能，开启后会在运行的实例上收集有关MongoDB的写操作，游标，数据库命令等，可以在数据库级别开启该工具，也可以在实例级别开启。
该工具会把收集到的所有都写入到system.profile集合中，该集合是一个capped collection http://docs.mongodb.org/manual/tutorial/manage-the-database-profiler/
查询system.profile集合中，查询时间长的语句，比如执行超过200ms的再通过.explain()解析影响行数，分析原因
优化查询语句 或 增加索引

## 开启 Profiling 功能

mongo shell 中开启

进入mongo shell，输入以下指令开启
```
db.setProfilingLevel(2);
```
开启级别说明：
- 0：关闭，不收集任何数据。
- 1：收集慢查询数据，默认是100毫秒。
- 2：收集所有数据

如果在集合下操作，仅对该集合里的操作生效，在所有集合下面设置或者在启动mongodb时设置，则对整个实例生效

启动时开启
```
mongod --profile=1 --slowms=200
```
配置文件修改，正常启动
```
profile = 1
slowms = 200
```
其它指令：
```
# 查看状态：级别和时间
db.getProfilingStatus()

# 查看级别
db.getProfilingLevel()

# 设置级别和时间
db.setProfilingLevel(1,200)

# 关闭Profiling
db.setProfilingLevel(0)

# 删除system.profile集合
db.system.profile.drop()

# 创建一个新的system.profile集合，大小为1M
db.createCollection( "system.profile", { capped: true, size:1000000 } )

# 重新开启Profiling
db.setProfilingLevel(1)
```
## 通过system.profile进行分析

http://docs.mongodb.org/manual/reference /database-profiler/

通过 `db.system.profile.find()` 可查询记录的操作语句， 如下的例子：
```
{
"op" : "insert",
"ns" : "Gps905.onlineTemp",
"command" : {
"insert" : "onlineTemp",
"ordered" : true,
"$db" : "Gps905"
},
"ninserted" : 1,
"keysInserted" : 1,
"numYield" : 0,
"locks" : {
"Global" : {
"acquireCount" : {
"r" : NumberLong(1),
"w" : NumberLong(1)
}
},
"Database" : {
"acquireCount" : {
"w" : NumberLong(1)
}
},
"Collection" : {
"acquireCount" : {
"w" : NumberLong(1)
}
}
},
"responseLength" : 60,
"protocol" : "op_query",
"millis" : 105,
"ts" : ISODate("2022-06-29T08:41:51.858Z"),
"client" : "127.0.0.1",
"allUsers" : [],
"user" : ""
}
```
其中重要字段含义如下
- op：操作类型，有insert、query、update、remove、getmore、command
- ns：操作的数据库和集合
- millis：操作所花时间，毫秒
- ts：时间戳

如果millis的值较大，就需要进行优化

比如query操作的例子  
https://blog.csdn.net/weixin_34174105/article/details/91779187
```
{
"op" : "query", #操作类型，有insert、query、update、remove、getmore、command
"ns" : "onroad.route_model", #操作的集合
"query" : {
"$query" : {
"user_id" : 314436841,
"data_time" : {
"$gte" : 1436198400
}
},
"$orderby" : {
"data_time" : 1
}
},
"ntoskip" : 0, #指定跳过skip()方法 的文档的数量。
"nscanned" : 2, #为了执行该操作，MongoDB在 index 中浏览的文档数。 一般来说，如果 nscanned 值高于 nreturned 的值，说明数据库为了找到目标文档扫描了很多文档。这时可以考虑创建索引来提高效率。
"nscannedObjects" : 1, #为了执行该操作，MongoDB在 collection中浏览的文档数。
"keyUpdates" : 0, #索引更新的数量，改变一个索引键带有一个小的性能开销，因为数据库必须删除旧的key，并插入一个新的key到B-树索引
"numYield" : 1, #该操作为了使其他操作完成而放弃的次数。通常来说，当他们需要访问还没有完全读入内存中的数据时，操作将放弃。这使得在MongoDB为了放弃操作进行数据读取的同时，还有数据在内存中的其他操作可以完成
"lockStats" : { #锁信息，R：全局读锁；W：全局写锁；r：特定数据库的读锁；w：特定数据库的写锁
"timeLockedMicros" : { #该操作获取一个级锁花费的时间。对于请求多个锁的操作，比如对 local 数据库锁来更新 oplog ，该值比该操作的总长要长（即 millis ）
"r" : NumberLong(1089485),
"w" : NumberLong(0)
},
"timeAcquiringMicros" : { #该操作等待获取一个级锁花费的时间。
"r" : NumberLong(102),
"w" : NumberLong(2)
}
},
"nreturned" : 1, // 返回的文档数量
"responseLength" : 1669, // 返回字节长度，如果这个数字很大，考虑值返回所需字段
"millis" : 544, #消耗的时间（毫秒）
"execStats" : { #一个文档,其中包含执行 查询 的操作，对于其他操作,这个值是一个空文件， system.profile.execStats 显示了就像树一样的统计结构，每个节点提供了在执行阶段的查询操作情况。
"type" : "LIMIT", ##使用limit限制返回数
"works" : 2,
"yields" : 1,
"unyields" : 1,
"invalidates" : 0,
"advanced" : 1,
"needTime" : 0,
"needFetch" : 0,
"isEOF" : 1, #是否为文件结束符
"children" : [
{
"type" : "FETCH", #根据索引去检索指定document
"works" : 1,
"yields" : 1,
"unyields" : 1,
"invalidates" : 0,
"advanced" : 1,
"needTime" : 0,
"needFetch" : 0,
"isEOF" : 0,
"alreadyHasObj" : 0,
"forcedFetches" : 0,
"matchTested" : 0,
"children" : [
{
"type" : "IXSCAN", #扫描索引键
"works" : 1,
"yields" : 1,
"unyields" : 1,
"invalidates" : 0,
"advanced" : 1,
"needTime" : 0,
"needFetch" : 0,
"isEOF" : 0,
"keyPattern" : "{ user_id: 1.0, data_time: -1.0 }",
"boundsVerbose" : "field #0['user_id']: [314436841, 314436841], field #1['data_time']: [1436198400, inf.0]",
"isMultiKey" : 0,
"yieldMovedCursor" : 0,
"dupsTested" : 0,
"dupsDropped" : 0,
"seenInvalidated" : 0,
"matchTested" : 0,
"keysExamined" : 2,
"children" : [ ]
}]}]},
"ts" : ISODate("2022-06-29T08:41:51.858Z"), #该命令在何时执行
"client" : "127.0.0.1", #链接ip或则主机
"allUsers" : [
{
"user" : "martin_v8",
"db" : "onroad"
}
],
"user" : ""
}

type字段的参数：

COLLSCAN #全表扫描
IXSCAN #索引扫描
FETCH #根据索引去检索指定document
SHARD_MERGE #将各个分片返回数据进行merge
SORT #表明在内存中进行了排序（与老版本的scanAndOrder:true一致）
LIMIT #使用limit限制返回数
SKIP #使用skip进行跳过
IDHACK #针对_id进行查询
SHARDING_FILTER #通过mongos对分片数据进行查询
COUNT #利用db.coll.explain().count()之类进行count运算
COUNTSCAN #count不使用Index进行count时的stage返回
COUNT_SCAN #count使用了Index进行count时的stage返回
SUBPLA #未使用到索引的$or查询的stage返回
TEXT #使用全文索引进行查询时候的stage返回
PROJECTION #限定返回字段时候stage的返回
```

如果nscanned数很大，或者接近记录总数（文档数），那么可能没有用到索引查询，而是全表扫描。

如果 nscanned 值高于 nreturned 的值，说明数据库为了找到目标文档扫描了很多文档。这时可以考虑创建索引来提高效率。

## 筛选条件中的语句
```
# 返回大于100毫秒慢的操作
db.system.profile.find({ millis : { $gt : 100 } } ).pretty()

# 返回最近的10条记录 {$natrual: -1} 代表按插入数序逆序
db.system.profile.find().sort({ ts : -1 }).limit(10).pretty()

# 返回所有的操作，除command类型的
db.system.profile.find( { op: { $ne : 'command' } }).pretty()

# 返回特定集合
db.system.profile.find( { ns : 'mydb.test' } ).pretty()

# 从一个特定的时间范围内返回信息
db.system.profile.find({ ts : { $gt : new ISODate("2015-10-18T03:00:00Z"), $lt : new ISODate("2015-10-19T03:40:00Z")}}).pretty()

# 特定时间，限制用户，按照消耗时间排序
db.system.profile.find( { ts : { $gt : newISODate("2015-10-12T03:00:00Z") , $lt : newISODate("2015-10-12T03:40:00Z") } }, { user : 0 } ).sort( { millis : -1 } )

# 查看最新的 Profile 记录：
db.system.profile.find().sort({$natural:-1}).limit(1)

# 列出最近5 条执行时间超过1ms的 Profile 记录
show profile
```

## explain 对执行语句进行分析

https://docs.mongodb.org/manual/reference/database-profiler/

同MySQL类似，MongoDB 也提供了一个 explain 命令获知系统如何处理查询请求。
以下利用 explain 命令，针对执行语句进行优化。
```
SECONDARY> db.route_model.find({ "user_id" : 313830621, "data_time" : { "$lte" : 1443715200, "$gte" : 1443542400 } }).explain()
{
"cursor" : "BtreeCursor user_id_1_data_time_-1", #返回游标类型，有BasicCursor和BtreeCursor，后者意味着使用了索引。
"isMultiKey" : false,
"n" : 23, #返回的文档行数。
"nscannedObjects" : 23, #这是MongoDB按照索引指针去磁盘上查找实际文档的次数。如果查询包含的查询条件不是索引的一部分，或者说要求返回不在索引内的字段，MongoDB就必须依次查找每个索引条目指向的文档。
"nscanned" : 23, #如果有使用索引，那么这个数字就是查找过的索引条目数量，如果本次查询是一次全表扫描，那么这个数字就代表检查过的文档数目
"nscannedObjectsAllPlans" : 46,
"nscannedAllPlans" : 46,
"scanAndOrder" : false, #MongoDB是否在内存中对结果集进行了排序
"indexOnly" : false, #MongoDB是否只使用索引就能完成此次查询
"nYields" : 1, #为了让写入请求能够顺利执行，本次查询暂停暂停的次数。如果有写入请求需求处理，查询会周期性的释放他们的锁，以便写入能够顺利执行
"nChunkSkips" : 0,
"millis" : 1530, #数据库执行本次查询所耗费的毫秒数。这个数字越小，说明效率越高
"indexBounds" : { #这个字段描述了索引的使用情况，给出了索引的遍历范围
"user_id" : [
[
313830621,
313830621
]
],
"data_time" : [
[
1443715200,
1443542400
]
]
},
"server" : "a7cecd4f9295:27017",
"filterSet" : false,
"stats" : {
"type" : "FETCH",
"works" : 25,
"yields" : 1,
"unyields" : 1,
"invalidates" : 0,
"advanced" : 23,
"needTime" : 0,
"needFetch" : 0,
"isEOF" : 1,
"alreadyHasObj" : 0,
"forcedFetches" : 0,
"matchTested" : 0,
"children" : [
{
"type" : "IXSCAN",#这里使用了索引
"works" : 23,
"yields" : 1,
"unyields" : 1,
"invalidates" : 0,
"advanced" : 23,
"needTime" : 0,
"needFetch" : 0,
"isEOF" : 1,
"keyPattern" : "{ user_id: 1.0, data_time: -1.0 }",
"boundsVerbose" : "field #0['user_id']: [313830621.0, 313830621.0], field #1['data_time']: [1443715200.0, 1443542400.0]",
"isMultiKey" : 0,
"yieldMovedCursor" : 0,
"dupsTested" : 0,
"dupsDropped" : 0,
"seenInvalidated" : 0,
"matchTested" : 0,
"keysExamined" : 23,
"children" : [ ]
}]}}
```

# 压测
```
time ./bin/ycsb run mongodb -s -threads 200 -P workloads/workloada -p mongodb.url="mongodb://172.1.1.1:27017/foo"
```

# 增量备份归档及数据清理
```sh
#!/bin/bash

#备份归档
backdir=$1
btime=`date +\%Y\%m\%d`
cpus=`cat /proc/cpuinfo | grep 'processor' | wc -l`

ip1=$(ip addr | awk '/^[0-9]+: / {}; /inet.*global/ {print gensub(/(.*)\/(.*)/, "\\1", "g", $2)}' | head -n 1)
mongoexport -h 172.1.1.1 -uroot -pabc123 -d sz -c cap_device_received --port=40001 --authenticationDatabase=admin --query '{"$and":[{"ExpiresAt": {"$gte":{"$date":"2023-11-10T00:00:00.001Z"}}},{"ExpiresAt": {"$lte":{"$date":"2023-11-15T23:59:59.999Z"}}}]}'  -j $usecpus --out=$backdir/$btime/$ip1/cap_device_received_archivist_2023_11_10_00-2023_11_15_23_59_59_999.json

#上传备份到OSS
/usr/bin/s3cmd sync $backdir/$btime/$ip1/cap_device_received_archivist_2023_11_10_00-2023_11_15_23_59_59_999.json  s3://db-backup-prod-gz/mongodb/archivist_mongodb/

#清理
echo 'db.cap_data_center_received.remove({"$and":[{"ExpiresAt": {"$gte":ISODate("2023-11-14T07:39:22.047Z")}},{"ExpiresAt": {"$lte":ISODate("2023-11-17T07:39:22.047Z")}}]})'|mongo localhost:40001/sz -uroot -pabc123 --authenticationDatabase admin
```
# 备份脚本
```sh
#!/bin/bash
backdir_pwd='/data/data_backup/'
usern='root'
passw='xxxx'
dbn='signlanguage'
datee=`date +%Y_%m_%d_%H_%M_%S`
bak_dir="${dbn}_$datee"

mkdir ${backdir_pwd}${bak_dir}
mongodump --host=172.1.1.1 --username=${usern} --password=${passw} --port=27017 --authenticationDatabase admin --db=$dbn --out ${backdir_pwd}${bak_dir}

cd $backdir_pwd
tar -cf - ${bak_dir} | lz4 -c > ${bak_dir}.tar.lz4
#rm -fr ${backdir_pwd}${bak_dir}
find ${backdir_pwd}* -name "*.tar.lz4" -mtime +3 -exec rm -rfv {} \;
# 解压 lz4 -d xxxx.tar.lz4 ;tar xvf xxxx.tar

1 0 * * * sh /data/data_backup/mongo_backup.sh
```
# 开启慢查询
```
低版本在每个分片数据节点主节点上执行，高版本只需要再 mongos 节点上执行
db.setProfilingLevel(1, { slowms: 100})

查看慢查询等级和记录时间
db.getProfilingStatus()

在分片副本 节点上 admin查询慢日志
db.system.profile.find().limit(10).sort( { ts : -1 } ).pretty()
```
# 强制副本集从节点提升为主实例
```
一、
1.位于从实例上执行cfg=rs.conf()
2.需要设置需要的_id为主库
cfg.members=[cfg.members[1]]
3.执行集群重新设置 rs.reconfig(cfg, {force: true});
4.rs.status()

二、设置副本集权重
///////////////////////////////
conf = rs.conf()
conf.members[0].priority = 10 // 索引号从0开始，每次递增1，类似数组
conf.members[1].priority = 5
conf.members[2].priority = 2

使用rs.reconfig()命令应用新的配置。这将更新副本集的权重设置。
javascript
rs.reconfig(conf)
```

# 数据分段备份和清理
```sh
#!/bin/bash
date1=$1
date2=$2

echo 'db.CloudLog.find({"$and":[{"SendTime": {"$gte":ISODate("'$date1'")}},{"SendTime": {"$lte":ISODate("'$date2'")}}]}).count()'|mongo localhost:30000/91iotdb|grep -vE 'MongoDB|bye|session|mongodb'
sleep 20
echo '开始备份...'
/opt/mongodb-database-tools-rhel70-x86_64-100.6.1/bin/mongoexport -h localhost -d 91iotdb -c CloudLog --port=30000 --query '{"$and":[{"SendTime": {"$gte":{"$date":"'${date1}'"}}},{"SendTime": {"$lte":{"$date":"'$date2'"}}}]}' --out=CloudLog_"$1"_"$2".json
sleep 20
echo '开始清理数据...'
sleep 10
echo 'db.CloudLog.remove({"$and":[{"SendTime": {"$gte":ISODate("'$date1'")}},{"SendTime": {"$lte":ISODate("'$date2'")}}]})'|mongo localhost:30000/91iotdb

time sh 91iot_db_cloudlog_backup.sh "2023-07-27T08:00:00.000Z" "2023-07-27T19:00:00.000Z"
```

# 查看副本集延迟问题
```
rsshd1:SECONDARY>rs.printSlaveReplicationInfo()
source: 172.1.1.112:40001
syncedTo: Tue Dec 26 2023 16:21:45 GMT+0800 (CST)
9 secs (0 hrs) behind the primary
source: 172.1.1.102:40001
syncedTo: Tue Dec 26 2023 16:21:55 GMT+0800 (CST)
-1 secs (0 hrs) behind the primary


rsshd1:PRIMARY> db.printReplicationInfo()
configured oplog size: 51200MB
log length start to end: 170106secs (47.25hrs)
oplog first event time: Sun Dec 24 2023 17:58:58 GMT+0800 (CST)
oplog last event time: Tue Dec 26 2023 17:14:04 GMT+0800 (CST)
now: Tue Dec 26 2023 17:14:04 GMT+0800 (CST)


修改oplog空间大小（单台）
db.adminCommand({replSetResizeOplog:1,minRetentionHours:8,size:51200}) 
```

# 脚本统计集合结构信息
```sh
1.利用variety.js解析
https://github.com/variety/variety


2.脚本
#!/bin/bash
 
#user='xxx'
#passw='xxx'
host='172.1.1.1'
port=27010
db='hgr'
 
tabs=$(echo "show collections"|mongo ${host}:${port}/${db}|grep -vE 'version|not match|session|compressors|=|Warning|delivers|upcoming|installation|https|switched|bye' )
 
for t in $tabs;do
   echo ' ' && echo '+------------------------------------------+' && echo '|'"${db}.${t}"'                                   |'
   mongo  ${host}:${port}/${db}  --eval "var collection = '${t}'" variety.js|grep -vE 'Variety|MongoDB|Implicit|Version|Using|connecting'
done
```

# 脚本统计集合数据量
```sh
#!/bin/bash
 
ip='xxx.xx.xx.xx'
port=xxxx
db='91iotdb'
#user=
#passw=
 
mongo -host ${ip}:${port} <<EOF 2>/dev/null|grep -vE 'version|not match|session|compressors|=|Warning|delivers|upcoming|installation|https|switched|bye' >collec
use ${db};
show tables;
EOF
 
cos=`wc -l collec|cut -d' ' -f1`
for n in `seq $cos`;do
  collname=$(sed -n "$n"p collec)
  cz=$(mongo ${ip}:${port}/${db} --eval "db.getCollection(\"$collname\").count()"|grep -vE 'version|not match|session|compressors')
echo $cz,$collname
done
```

```
排序统计以降序排列
sh mon_list.sh |sort -rn -t',' -k1 

计算库下面的集合总数据量
sh mon_list.sh |sort -rn -t',' -k1 |awk -F ',' '{sum+=$1}END{print sum}'
```

# 启停命令
```sh
systemctl start mongod_multiple_mongos@1.service
systemctl start mongod_multiple_cinfig@1.service
systemctl start mongod_multiple_shard@1.service
systemctl stop mongod_multiple_mongos@1.service
systemctl stop mongod_multiple_cinfig@1.service
systemctl stop mongod_multiple_shard@1.service

启动
su - mongodb -c "/usr/local/mongodb/bin/mongos --config /data/mongodb/30002/conf/mongo_route.yml &"
su - mongodb -c "/usr/local/mongodb/bin/mongod --config /data/mongodb/conf/mongo_config.yml &"
su - mongodb -c "/usr/local/mongodb/bin/mongod --config /data/mongodb/conf/mongo_shard1.yml &"

关闭实例
kill -2 pid
```