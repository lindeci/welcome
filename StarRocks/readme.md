- [StarRocks 是什么](#starrocks-是什么)
- [适用场景](#适用场景)
- [OLAP 多维分析](#olap-多维分析)
- [实时数据仓库](#实时数据仓库)
- [高并发查询](#高并发查询)
- [系统架构](#系统架构)
  - [存算分离](#存算分离)
    - [节点介绍](#节点介绍)
    - [存储](#存储)
    - [缓存](#缓存)
- [产品特性](#产品特性)
  - [MPP 分布式执行框架](#mpp-分布式执行框架)
  - [全面向量化执行引擎](#全面向量化执行引擎)
  - [存储计算分离](#存储计算分离)
  - [CBO 优化器](#cbo-优化器)
  - [可实时更新的列式存储引擎](#可实时更新的列式存储引擎)
  - [智能的物化视图](#智能的物化视图)
  - [数据湖分析](#数据湖分析)
- [微信社区群](#微信社区群)
- [数据类型](#数据类型)
  - [数值类型](#数值类型)
  - [字符串类型](#字符串类型)
  - [日期类型](#日期类型)
  - [半结构化类型](#半结构化类型)
  - [其他类型](#其他类型)
- [表设计](#表设计)
  - [Catalogs](#catalogs)
  - [数据库](#数据库)
  - [表](#表)
  - [物化视图](#物化视图)
  - [视图](#视图)
  - [权限系统](#权限系统)
- [表概览](#表概览)
  - [表结构入门](#表结构入门)
  - [表类型](#表类型)
  - [数据分布](#数据分布)
    - [分区](#分区)
    - [分桶](#分桶)
  - [索引](#索引)
  - [约束](#约束)
  - [更多特性](#更多特性)
- [各类表的能力对比](#各类表的能力对比)
  - [Key 列和排序键](#key-列和排序键)
  - [Key 列和 Value 列的数据类型](#key-列和-value-列的数据类型)
  - [数据变更](#数据变更)
- [主键表](#主键表)
  - [工作原理](#工作原理)
  - [使用说明](#使用说明)
- [明细表](#明细表)
  - [适用场景](#适用场景-1)
  - [创建表](#创建表)
- [聚合表](#聚合表)
  - [适用场景](#适用场景-2)
  - [原理](#原理)
  - [创建表](#创建表-1)
- [数据分布](#数据分布-1)
  - [分区](#分区-1)
  - [创建和管理分区](#创建和管理分区)
    - [Range 分区](#range-分区)
    - [List 分区](#list-分区)
  - [管理分区](#管理分区)
    - [增加分区](#增加分区)
    - [删除分区](#删除分区)
    - [恢复分区](#恢复分区)
    - [查看分区](#查看分区)
  - [设置分桶](#设置分桶)
    - [随机分桶（自 v3.1）](#随机分桶自-v31)
    - [哈希分桶](#哈希分桶)
    - [查看分桶数量](#查看分桶数量)
  - [建表后优化数据分布（自 3.2）](#建表后优化数据分布自-32)
  - [最佳实践](#最佳实践)
  - [表达式分区](#表达式分区)
    - [时间函数表达式分区](#时间函数表达式分区)
    - [列表达式分区（自 v3.1）](#列表达式分区自-v31)
    - [使用限制](#使用限制)
  - [List 分区](#list-分区-1)
    - [使用限制](#使用限制-1)
  - [动态分区](#动态分区)
    - [修改表的动态分区属性](#修改表的动态分区属性)
  - [临时分区](#临时分区)
    - [创建临时分区](#创建临时分区)
- [索引](#索引-1)
  - [内置索引](#内置索引)
    - [前缀索引](#前缀索引)
    - [Ordinal 索引](#ordinal-索引)
    - [ZoneMap 索引](#zonemap-索引)
  - [手动创建的索引](#手动创建的索引)
    - [Bitmap 索引](#bitmap-索引)
    - [Bloom filter 索引](#bloom-filter-索引)
    - [N-Gram bloomfilter 索引](#n-gram-bloomfilter-索引)
    - [全文倒排索引](#全文倒排索引)
- [前缀索引和排序键](#前缀索引和排序键)
- [Bitmap 索引](#bitmap-索引-1)
- [Bloom filter 索引](#bloom-filter-索引-1)
  - [索引原理](#索引原理)
- [N-Gram bloom filter 索引](#n-gram-bloom-filter-索引)
- [全文倒排索引](#全文倒排索引-1)
- [数据压缩](#数据压缩)
- [加速查询](#加速查询)
  - [CBO 统计信息](#cbo-统计信息)
  - [同步物化视图](#同步物化视图)
      - [相关概念](#相关概念)
    - [创建同步物化视图](#创建同步物化视图)
    - [最佳实践](#最佳实践-1)
  - [异步物化视图](#异步物化视图)
    - [使用场景](#使用场景)
- [Colocate Join](#colocate-join)
- [使用 Lateral Join 实现列转行](#使用-lateral-join-实现列转行)
- [Query Cache](#query-cache)
  - [应用场景](#应用场景)
- [管理手册](#管理手册)
  - [运维集群](#运维集群)
    - [扩容缩容 StarRocks](#扩容缩容-starrocks)
    - [管理 BE 黑名单](#管理-be-黑名单)
    - [备份与恢复](#备份与恢复)

# StarRocks 是什么
StarRocks 是新一代极速全场景 MPP (Massively Parallel Processing) 数据库

# 适用场景
StarRocks 可以满足企业级用户的多种分析需求，包括 OLAP (Online Analytical Processing) 多维分析、定制报表、实时数据分析和 Ad-hoc 数据分析等。

# OLAP 多维分析
- 用户行为分析
- 用户画像、标签分析、圈人
- 高维业务指标报表
- 自助式报表平台
- 业务问题探查分析
- 跨主题业务分析
- 财务报表
- 系统监控分析

# 实时数据仓库
StarRocks 设计和实现了主键表，能够实时更新数据并极速查询，可以秒级同步 TP (Transaction Processing) 数据库的变化，构建实时数仓，业务场景包括：

- 电商大促数据分析
- 物流行业的运单分析
- 金融行业绩效分析、指标计算
- 直播质量分析
- 广告投放分析
- 管理驾驶舱
- 探针分析APM（Application Performance Management）
  
# 高并发查询
StarRocks 通过良好的数据分布特性，灵活的索引以及物化视图等特性，可以解决面向用户侧的分析场景，业务场景包括：

- 广告主报表分析
- 零售行业渠道人员分析
- SaaS 行业面向用户分析报表
- Dashboard 多页面分析

# 系统架构
StarRocks 架构简洁，整个系统的核心只有 FE（Frontend）、BE (Backend) 或 CN (Compute Node) 两类进程，方便部署与维护，节点可以在线水平扩展，元数据和业务数据都有副本机制，确保整个系统无单点。StarRocks 提供 MySQL 协议接口，支持标准 SQL 语法。用户可通过 MySQL 客户端方便地查询和分析 StarRocks 中的数据。

下图展示了存算一体到存算分离的架构演进
![](https://docs.starrocks.io/zh/assets/images/architecture_evolution-739e923fb30eddd1d76715af2cef9706.png)

## 存算分离
StarRocks 存算分离技术在现有存算一体架构的基础上，将计算和存储进行解耦。在存算分离新架构中，数据持久化存储在更为可靠和廉价的远程对象存储（比如 S3）或 HDFS 上。CN 本地磁盘只用于缓存热数据来加速查询。在本地缓存命中的情况下，存算分离可以获得与存算一体架构相同的查询性能。存算分离架构下，用户可以动态增删计算节点，实现秒级的扩缩容。存算分离大大降低了数据存储成本和扩容成本，有助于实现资源隔离和计算资源的弹性伸缩。

与存算一体架构类似，存算分离版本拥有同样简洁的架构，整个系统依然只有 FE 和 CN 两种服务进程，用户唯一需要额外提供的是后端对象存储。

![](https://docs.starrocks.io/zh/assets/images/architecture_shared_data-15f84aa90555acb41e0865850d74c8c3.png)

### 节点介绍
存算分离架构下，FE 的功能保持不变。BE 原有的存储功能被抽离，数据存储从本地存储 (local storage) 升级为共享存储 (shared storage)。BE 节点升级为无状态的 CN 节点，只缓存热数据。CN 会执行数据导入、查询计算、缓存数据管理等任务。

### 存储

目前，StarRocks 存算分离技术支持如下后端存储方式，用户可根据需求自由选择：

    兼容 AWS S3 协议的对象存储系统（支持主流的对象存储系统如 AWS S3、Google GCP、阿里云 OSS、腾讯云 COS、百度云 BOS、华为云 OBS 以及 MinIO 等）
    Azure Blob Storage
    传统数据中心部署的 HDFS

在数据格式上，StarRocks 存算分离数据文件与存算一体保持一致，各种索引技术在存算分离表中也同样适用，不同的是，描述数据文件的元数据（如 TabletMeta 等）被重新设计以更好地适应对象存储。

### 缓存

为了提升存算分离架构的查询性能，StarRocks 构建了分级的数据缓存体系，将最热的数据缓存在内存中，距离计算最近，次热数据则缓存在本地磁盘，冷数据位于对象存储，数据根据访问频率在三级存储中自由流动。

查询时，热数据通常会直接从缓存中命中，而冷数据则需要从对象存储中读取并填充至本地缓存，以加速后续访问。通过内存、本地磁盘、远端存储，StarRocks 存算分离构建了一个多层次的数据访问体系，用户可以指定数据冷热规则以更好地满足业务需求，让热数据靠近计算，真正实现高性能计算和低成本存储。

StarRocks 存算分离的统一缓存允许用户在建表时决定是否开启缓存。如果开启，数据写入时会同步写入本地磁盘以及后端对象存储，查询时，CN 节点会优先从本地磁盘读取数据，如果未命中，再从后端对象存储读取原始数据并同时缓存在本地磁盘。

同时，针对未被缓存的冷数据，StarRocks 也进行了针对性优化，可根据应用访问模式，利用数据预读技术、并行扫描技术等手段，减少对于后端对象存储的访问频次，提升查询性能。

# 产品特性
## MPP 分布式执行框架
在 MPP 执行框架中，一条查询请求会被拆分成多个物理计算单元，在多机并行执行。每个执行节点拥有独享的资源（CPU、内存）。MPP 执行框架能够使得单个查询请求可以充分利用所有执行节点的资源，所以单个查询的性能可以随着集群的水平扩展而不断提升。
![](https://docs.starrocks.io/zh/assets/images/1.1-3-mpp-4e71d2992c780d0e208a849750b88f76.png)

如上图所示，StarRocks 会将一个查询在逻辑上切分为多个逻辑执行单元（Query Fragment）。按照每个逻辑执行单元需要处理的计算量，每个逻辑执行单元会由一个或者多个物理执行单元来具体实现。物理执行单元是最小的调度单位。一个物理执行单元会被调度到集群某个 BE 上执行。一个逻辑执行单元可以包括一个或者多个执行算子，如图中的 Fragment 包括了 Scan，Project，Aggregate。每个物理执行单元只处理部分数据。由于每个逻辑执行单元处理的复杂度不一样，所以每个逻辑执行单元的并行度是不一样的，即，不同逻辑执行单元可以由不同数目的物理执行单元来具体执行，以提高资源使用率，提升查询速度
![](https://docs.starrocks.io/zh/assets/images/1.1-4-mpp-5e90a2b69a04d566fb226e9b6f35726c.png)

与很多数据分析系统采用的 Scatter-Gather 分布式执行框架不同，MPP分布式执行框架可以利用更多的资源处理查询请求。在 Scatter-Gather 框架中，只有 Gather 节点能处理最后一级的汇总计算。而在 MPP 框架中，数据会被 Shuffle 到多个节点，并且由多个节点来完成最后的汇总计算。在复杂计算时（比如高基数 Group By，大表 Join 等操作），StarRocks 的 MPP 框架相对于 Scatter-Gather 模式的产品有明显的性能优势。

## 全面向量化执行引擎
StarRocks 通过实现全面向量化引擎，充分发挥了 CPU 的处理能力。全面向量化引擎按照列式的方式组织和处理数据。StarRocks 的数据存储、内存中数据的组织方式，以及 SQL 算子的计算方式，都是列式实现的。按列的数据组织也会更加充分的利用 CPU 的 Cache，按列计算会有更少的虚函数调用以及更少的分支判断从而获得更加充分的 CPU 指令流水。

另一方面，StarRocks 的全面向量化引擎通过向量化算法充分的利用 CPU 提供的 SIMD（Single Instruction Multiple Data）指令。这样 StarRocks 可以用更少的指令数目，完成更多的数据操作。经过标准测试集的验证，StarRocks的全面向量化引擎可以将执行算子的性能，整体提升 3~10 倍。

除了使用向量化技术实现所有算子外，StarRocks 还在执行引擎中实现了其他的优化。比如 StarRocks 实现了 Operation on Encoded Data 的技术。对于字符串字段的操作，StarRocks 在无需解码情况下就可以直接基于编码字段完成算子执行，比如实现关联算子、聚合算子、表达式算子计算等。这可以极大的降低 SQL 在执行过程中的计算复杂度。通过这个优化手段，相关查询速度可以提升 2 倍以上。

## 存储计算分离
StarRocks 3.0 版本支持了全新的存算分离模式，实现了计算与存储的完全解耦、计算节点弹性扩缩容、高性能热数据缓存。存算分离模式下 StarRocks 具备灵活弹性、高性能、高可靠、低成本等特点。
![](https://docs.starrocks.io/zh/assets/images/share_data_arch-36623ac2dd77e06b5d8efb2a20971ac7.png)
存算分离模式下，存储与计算解耦，各自独立服务，独立扩缩容，解决了在存算一体模式下的计算与存储等比例扩缩容所带来的资源浪费问题。计算节点可以实现秒级的动态扩缩容，提升计算资源的利用率。

存储层利用对象存储近乎无限的容量，以及数据高可用的特性实现数据的海量存储和持久化。支持包括 AWS S3，Azure Blob Storage，Google Cloud Storage，阿里云 OSS，腾讯云 COS，火山引擎 TOS，华为云 OBS，以及各类兼容 S3 协议的对象存储，同时也支持 HDFS 存储。

部署模式上用户可以选择基于公有云、私有云、本地机房部署。StarRocks 存算分离也支持基于 Kubernetes 部署，并提供了相应的 Operator 方便用户自动化部署。

StarRocks 存算分离模式与存算一体模式功能保持一致，写入及热数据查询性能也与存算一体基本持平。用户在存储分离模式下也可以实现数据更新、数据湖分析、物化视图加速等多种场景。
## CBO 优化器
![](https://docs.starrocks.io/zh/assets/images/1.1-5-cbo-9c0501b7304c015c0bb7d1e4bb050c4c.png)
在多表关联查询场景下，仅靠优秀的执行引擎没有办法获得最极致的执行性能。因为这类场景下，不同执行计划的复杂度可能会相差几个数量级。查询中关联表的数目越大，可能的执行计划就越多，在众多的可能中选择一个最优的计划，这是一个 NP-Hard 的问题。只有优秀的查询优化器，才能选择出相对最优的查询计划，从而实现极致的多表分析性能。

StarRocks 从零设计并实现了一款全新的，基于代价的优化器 CBO（Cost Based Optimizer）。该优化器是 Cascades Like 的，在设计时，针对 StarRocks 的全面向量化执行引擎进行了深度定制，并进行了多项优化和创新。该优化器内部实现了公共表达式复用，相关子查询重写，Lateral Join，Join Reorder，Join 分布式执行策略选择，低基数字典优化等重要功能和优化。目前，该优化器已可以完整支持 TPC-DS 99 条 SQL 语句。

由于全新 CBO 的支持，StarRocks 能比同类产品更好地支持多表关联查询，特别是复杂的多表关联查询，让全面向量化引擎能够发挥极致的性能。

## 可实时更新的列式存储引擎
StarRocks 实现了列式存储引擎，数据以按列的方式进行存储。通过这样的方式，相同类型的数据连续存放。一方面，数据可以使用更加高效的编码方式，获得更高的压缩比，降低存储成本。另一方面，也降低了系统读取数据的 I/O 总量，提升了查询性能。此外，在大部分 OLAP 场景中，查询只会涉及部分列。相对于行存，列存只需要读取部分列的数据，能够极大地降低磁盘 I/O 吞吐。

StarRocks 能够支持秒级的导入延迟，提供准实时的服务能力。StarRocks 的存储引擎在数据导入时能够保证每一次操作的 ACID。一个批次的导入数据生效是原子性的，要么全部导入成功，要么全部失败。并发进行的各个事务相互之间互不影响，对外提供 Snapshot Isolation 的事务隔离级别。
![](https://docs.starrocks.io/zh/assets/images/1.1-6-realtime-64610eff65f57901b981c2cc025e7189.png)
StarRocks 存储引擎不仅能够提供高效的 Partial Update 操作，也能高效处理 Upsert 类操作。使用 Delete-and-insert 的实现方式，通过主键索引快速过滤数据，避免读取时的 Sort 和 Merge 操作，同时还可以充分利用其他二级索引，在大量更新的场景下，仍然可以保证查询的极速性能。

## 智能的物化视图
![](https://docs.starrocks.io/zh/assets/images/1.1-7-mv-7fb0ae6f680ae698965d29b4a7a6911d.png)
StarRocks 支持用户使用物化视图（materialized view）进行查询加速和数仓分层。不同于一些同类产品的物化视图需要手动和原表做数据同步，StarRocks 的物化视图可以自动根据原始表更新数据。只要原始表数据发生变更，物化视图的更新也同步完成，不需要额外的维护操作就可以保证物化视图能够维持与原表一致。不仅如此，物化视图的选择也是自动进行的。StarRocks 在进行查询规划时，如果有合适的物化视图能够加速查询，StarRocks 自动进行查询改写(query rewrite)，将查询自动定位到最适合的物化视图上进行查询加速。

StarRocks 的物化视图可以按需灵活创建和删除。用户可以在使用过程中视实际使用情况来判断是否需要创建或删除物化视图。StarRocks 会在后台自动完成物化视图的相关调整。

StarRocks 的物化视图可以替代传统的 ETL 建模流程，用户无需在上游应用处做数据转换，可以在使用物化视图时完成数据转换，简化了数据处理流程。

例如图中，最底层 ODS 的湖上数据可以通过 External Catalog MV 来构建 DWD 层的 normalized table；并且可以通过多表关联的物化视图来构建 DWS 层的宽表 (denormalized table)；最上层可以进一步构建实时的物化视图来支撑高并发的查询，提供更加优异的查询性能。

## 数据湖分析
![](https://docs.starrocks.io/zh/assets/images/1.1-8-dla-f6fb2e38076e0e148ec52f484e595206.png)
StarRocks 不仅能高效的分析本地存储的数据，也可以作为计算引擎直接分析数据湖中的数据。用户可以通过 StarRocks 提供的 External Catalog，轻松查询存储在 Apache Hive、Apache Iceberg、Apache Hudi、Delta Lake 等数据湖上的数据，无需进行数据迁移。支持的存储系统包括 HDFS、S3、OSS，支持的文件格式包括 Parquet、ORC、CSV。

如上图所示，在数据湖分析场景中，StarRocks 主要负责数据的计算分析，而数据湖则主要负责数据的存储、组织和维护。使用数据湖的优势在于可以使用开放的存储格式和灵活多变的 schema 定义方式，可以让 BI/AI/Adhoc/报表等业务有统一的 single source of truth。而 StarRocks 作为数据湖的计算引擎，可以充分发挥向量化引擎和 CBO 的优势，大大提升了数据湖分析的性能。

# 微信社区群
![](https://docs.starrocks.io/zh/assets/images/wechat_scan-d61961ba1045282af6ec960c0be54ed8.png)

# 数据类型
## 数值类型
- TINYINT
- SMALLINT
- INT
- BIGINT
- LARGEINT
- DECIMAL
- DOUBLE
- FLOAT
- BOOLEAN
- PERCENTILE
## 字符串类型
- CHAR
- STRING  
  等价于 VARCHAR(65533)
- VARCHAR
- BINARY  
  暂不支持 BINARY/VARBINARY 类型的列作为明细表、主键表、更新表的分区键、分桶键、维度列，并且不支持用于 JOIN、GROUP BY、ORDER BY 子句
## 日期类型
- DATE
- DATETIME
## 半结构化类型
- ARRAY  
  数组列的定义形式为 ARRAY<type>，其中 type 表示数组内的元素类型。数组元素目前支持以下数据类型：BOOLEAN、TINYINT、SMALLINT、INT、BIGINT、LARGEINT、FLOAT、DOUBLE、VARCHAR、CHAR、DATETIME、DATE、JSON、BINARY (3.0 及以后）、MAP (3.1 及以后）、STRUCT (3.1 及以后）、Fast Decimal (3.1 及以后)。
- JSON
- MAP
- STRUCT  
  STRUCT 是一种复杂数据类型，可以存储不同数据类型的元素（也称字段），例如 <a INT, b STRING>
## 其他类型
- BITMAP  
  BITMAP 与 HLL (HyperLogLog) 类似，常用来加速 count distinct 的去重计数使用。您可以通过 bitmap 函数进行集合的各种操作，相比 HLL 可以获得更精确的结果。但是 BITMAP 需要消耗更多的内存和磁盘资源，另外 BITMAP 只能支持整数类型的聚合，如果是字符串等类型需要采用字典进行映射。
- HLL  
  HyperLogLog 类型，用于近似去重。HLL 是基于 HyperLogLog 算法的工程实现，用于保存 HyperLogLog 计算过程的中间结果，HLL 类型的列只能作为表的 value 列类型，通过聚合来不断的减少数据量，以此来实现加快查询的目的。基于 HLL 到的是一个估算结果，误差大概在 1% 左右。

# 表设计
StarRocks 使用 Internal Catalog 来管理内部数据，使用 External Catalog 来连接数据湖中的数据。存储在 StarRocks 中的数据都包含在 Internal Catalog 下，Internal Catalog 可以包含一个或多个数据库。数据库用于存储、管理和操作 StarRocks 中的数据，可用于管理多种对象，包括表、物化视图、视图等。StarRocks 采用权限系统来管理数据访问权限，定义了用户对哪些对象可以执行哪些操作，提高数据安全性。
![](https://docs.starrocks.io/zh/assets/images/Catalog_db_tbl-e7e05f2c4430964e96826f47a4a6224e.png)
## Catalogs
Catalog 分为 Internal catalog 和 External catalog。Internal catalog 是内部数据目录，用于管理导入至 StarRocks 中的数据以及内部的物化视图等。

External catalog 是外部数据目录，用于连接数据湖中的数据。您可以将 StarRocks 作为查询引擎，直接查询湖上数据，无需导入数据至 StarRocks。

## 数据库
数据库是包含表、视图、物化视图等对象的集合，用于存储、管理和操作数据。

## 表
StarRocks 中的表分为两类：内部表和外部表。

## 物化视图
物化视图是特殊的物理表，能够存储基于基表的预计算结果。当您对基表执行复杂查询时，StarRocks 可以自动复用物化视图中的预计算结果，实现查询透明加速、湖仓加速和数据建模等业务需求。物化视图分为同步物化视图和异步物化视图。其中异步物化视图能力更加强大，能够存储基于多个基表（内部表和外部表）的预计算结果，并且支持丰富的聚合算子。

## 视图
视图（也叫逻辑视图）是虚拟表，不实际存储数据，其中所展示的数据来自于基表生成的查询结果。每次在查询中引用某个视图时，都会运行定义该视图的查询。

## 权限系统
权限决定了哪些用户可以对哪些特定对象执行哪些特定的操作。StarRocks 采用了两种权限模型：基于用户标识的访问控制和基于角色的访问控制。您可以将权限赋予给角色然后通过角色传递权限给用户，或直接赋予权限给用户标识。

# 表概览
表是数据存储单元。理解 StarRocks 中的表结构，以及如何设计合理的表结构，有利于优化数据组织，提高查询效率。相比于传统的数据库，StarRocks 会以列的方式存储 JSON、ARRAY 等复杂的半结构化数据，保证高效查询。 

## 表结构入门
```sql
CREATE DATABASE example_db;

USE example_db;

CREATE TABLE user_access (
    uid int,
    name varchar(64),
    age int, 
    phone varchar(16),
    last_access datetime,
    credits double
)
ORDER BY (uid, name);

DESCRIBE user_access;
+-------------+-------------+------+-------+---------+-------+
| Field       | Type        | Null | Key   | Default | Extra |
+-------------+-------------+------+-------+---------+-------+
| uid         | int         | YES  | true  | NULL    |       |
| name        | varchar(64) | YES  | true  | NULL    |       |
| age         | int         | YES  | false | NULL    |       |
| phone       | varchar(16) | YES  | false | NULL    |       |
| last_access | datetime    | YES  | false | NULL    |       |
| credits     | double      | YES  | false | NULL    |       |
+-------------+-------------+------+-------+---------+-------+

SHOW CREATE TABLE user_access\G
*************************** 1. row ***************************
       Table: user_access
Create Table: CREATE TABLE `user_access` (
  `uid` int(11) NULL COMMENT "",
  `name` varchar(64) NULL COMMENT "",
  `age` int(11) NULL COMMENT "",
  `phone` varchar(16) NULL COMMENT "",
  `last_access` datetime NULL COMMENT "",
  `credits` double NULL COMMENT ""
) ENGINE=OLAP 
DUPLICATE KEY(`uid`, `name`)
DISTRIBUTED BY RANDOM
ORDER BY(`uid`, `name`)
PROPERTIES (
"bucket_size" = "4294967296",
"compression" = "LZ4",
"fast_schema_evolution" = "true",
"replicated_storage" = "true",
"replication_num" = "3"
);
```
指定明细表中前两列为排序列，构成排序键。数据按排序键排序后存储，有助于查询时的快速索引。

## 表类型
StarRocks 提供四种类型的表，包括明细表、主键表、聚合表和更新表，适用于存储多种业务数据，例如原始数据、实时频繁更新的数据和聚合数据。

- 明细表简单易用，表中数据不具有任何约束，相同的数据行可以重复存在。该表适用于存储不需要约束和预聚合的原始数据，例如日志等。
- 主键表能力强大，具有唯一性非空约束。该表能够在支撑实时更新、部分列更新等场景的同时，保证查询性能，适用于实时查询。
- 聚合表适用于存储预聚合后的数据，可以降低聚合查询时所需扫描和计算的数据量，极大提高聚合查询的效率。
- 更新表适用于实时更新的业务场景，目前已逐渐被主键表取代。

## 数据分布
StarRocks 采用分区+分桶的两级数据分布策略，将数据均匀分布各个 BE 节点。查询时能够有效裁剪数据扫描量，最大限度地利用集群的并发性能，从而提升查询性能。
![](https://docs.starrocks.io/zh/assets/images/table_overview-2bf1cedfc3be7f074b1ddc5d6831289f.png)

### 分区
第一层级为分区。表中数据可以根据分区列（通常是时间和日期）分成一个个更小的数据管理单元。查询时，通过分区裁剪，可以减少扫描的数据量，显著优化查询性能。

StarRocks 提供简单易用的分区方式，即表达式分区。此外还提供较灵活的分区方式，即 Range 分区和 List 分区。

### 分桶
第二层级为分桶。同一个分区中的数据通过分桶，划分成更小的数据管理单元。并且分桶以多副本形式（默认为3）均匀分布在 BE 节点上，保证数据的高可用。

StarRocks 提供两种分桶方式：
- 哈希分桶：根据数据的分桶键值，将数据划分至分桶。选择查询时经常使用的条件列组成分桶键，能有效提高查询效率。
- 随机分桶：随机划分数据至分桶。这种分桶方式更加简单易用。

## 索引
索引是一种特殊的数据结构，相当于数据的目录。查询条件命中索引列时，StarRocks 能够快速定位到满足条件的数据的位置。

StarRocks 提供内置索引，包括前缀索引、Ordinal 索引和 ZoneMap 索引。也支持用户手动创建索引，以提高查询效率，包括 Bitmap 和 Bloom Filter 索引。

## 约束
约束用于确保数据的完整性、一致性和准确性。主键表的 Primary Key 列具有唯一非空约束，聚合表的 Aggregate Key 列和更新表的 Unique Key 列具有唯一约束。

## 更多特性
除了上述常用的特性之外，您还可以根据业务需求使用更多的特性，设计更加健壮的表结构，例如通过 Bitmap 和 HLL 列来加速去重计数，指定生成列或者自增列来加速部分查询，配置灵活的数据自动降冷策略来降低运维成本，配置 Colocate Join 来加速多表 JOIN 查询。

# 各类表的能力对比
## Key 列和排序键
|  |主键表 (Primary Key table)	|明细表 (Duplicate Key table)	|聚合表 (Aggregate table)	|更新表 (Unique Key table)|
|--|--|--|--|--|
|Key 列和唯一约束	|主键 PRIMARY KEY 具有唯一约束和非空约束。	|DUPLICATE KEY 不具有唯一约束。	|聚合键 AGGREGATE KEY 具有唯一约束。	|唯一键 UNIQUE KEY 具有唯一约束。|
|Key 列和数据变更的关系（逻辑关系）|如果新数据的主键值与表中原数据的主键值相同，则存在唯一约束冲突，此时新数据会替代原数据。与更新表相比，主键表增强了其底层存储引擎，已经可以取代更新表。|Duplicate Key 不具有唯一约束，因此如果新数据的 Duplicate Key 与表中原数据相同，则新旧数据都会存在表中。|如果新数据与表中原数据存在唯一约束冲突，则会根据聚合键和 Value 列的聚合函数聚合新旧数据。|如果新数据与表中原数据存在唯一约束冲突，则新数据会替代原数据。更新表实际可以视为聚合函数为 replace 的聚合表。|
|Key 列和排序键的关系|自 3.0.0 起，主键表中两者解耦。主键表支持使用 ORDER BY 指定排序键和使用 PRIMARY KEY 指定主键。|自 3.3.0 起，明细表支持使用 ORDER BY 指定排序键，如果同时使用 ORDER BY 和 DUPLICATE KEY，则 DUPLICATE KEY 无效。|自 3.3.0 起，聚合表中两者解耦。聚合表支持使用 ORDER BY 指定排序键和使用 AGGREGATE KEY 指定聚合键。排序键和聚合键中的列需要保持一致，但是列的顺序不需要保持一致。|自 3.3.0 起，更新表中两者解耦。更新表支持使用 ORDER BY 指定排序键和使用 UNIQUE KEY 指定唯一键。排序键和唯一键中的列需要保持一致，但是列的顺序不需要保持一致。|
|Key 列和排序键支持的数据类型|数值（包括整型、布尔）、字符串、时间日期。|数值（包括整型、布尔、Decimal）、字符串、时间日期。|数值（包括整型、布尔、Decimal）、字符串、时间日期。|数值（包括整型、布尔、Decimal）、字符串、时间日期。|
|Key 和分区/分桶列的关系|分区列、分桶列必须在主键中。|无|分区列、分桶列必须在聚合键中。|分区列、分桶列必须在唯一键中。|
## Key 列和 Value 列的数据类型
表中 Key 列支持数据类型为数值（包括整型、布尔和 DECIMAL）、字符串、时间日期。

而表中 Value 列支持基础的数据类型，包括数值、字符串、时间日期。不同类型的表中 Value 列对于 BITMAP、HLL 以及半结构化类型的支持度不同

## 数据变更

# 主键表
其主要优势在于支撑实时数据更新的同时，也能保证高效的复杂即席查询性能。在实时分析业务中采用主键表，用最新的数据实时分析出结果来指导决策，使得数据分析不再受限于 T+1 数据延迟。

主键表中的主键具有唯一非空约束，用于唯一标识数据行。如果新数据的主键值与表中原数据的主键值相同，则存在唯一约束冲突，此时新数据会替代原数据。

可适用于如下场景：
- 实时对接事务型数据至 StarRocks。事务型数据库中，除了插入数据外，一般还会涉及较多更新和删除数据的操作，因此事务型数据库的数据同步至 StarRocks 时，建议使用主键表。通过 Flink-CDC 等工具直接对接 TP 的 Binlog，实时同步增删改的数据至主键表，可以简化数据同步流程，并且相对于 Merge-On-Read 策略的更新表，查询性能能够提升 3~10 倍。
- 利用部分列更新轻松实现多流 JOIN。在用户画像等分析场景中，一般会采用大宽表方式来提升多维分析的性能，同时简化数据分析师的使用模型。而这种场景中的上游数据，往往可能来自于多个不同业务（比如来自购物消费业务、快递业务、银行业务等）或系统（比如计算用户不同标签属性的机器学习系统），主键表的部分列更新功能就很好地满足这种需求，不同业务直接各自按需更新与业务相关的列即可，并且继续享受主键表的实时同步增删改数据及高效的查询性能。

## 工作原理
更新表和聚合表整体上采用了 Merge-On-Read 的策略。虽然写入时处理简单高效，但是读取时需要在线 Merge 多个版本的数据文件。并且由于 Merge 算子的存在，谓词和索引无法下推至底层数据，会严重影响查询性能。

然而为了兼顾实时更新和查询性能，主键表的元数据组织、读取、写入方式完全不同。主键表采用了 Delete+Insert 策略，借助主键索引配合 DelVector 的方式实现，保证在查询时只需要读取具有相同主键值的数据中的最新数据。如此可以避免 Merge 多个版本的数据文件，并且谓词和索引可以下推到底层数据，所以可以极大提升查询性能。

## 使用说明
```sql
CREATE TABLE orders2 (
    order_id bigint NOT NULL,
    dt date NOT NULL,
    merchant_id int NOT NULL,
    user_id int NOT NULL,
    good_id int NOT NULL,
    good_name string NOT NULL,
    price int NOT NULL,
    cnt int NOT NULL,
    revenue int NOT NULL,
    state tinyint NOT NULL
)
PRIMARY KEY (order_id,dt,merchant_id)
PARTITION BY date_trunc('day', dt)
DISTRIBUTED BY HASH (merchant_id)
ORDER BY (dt,merchant_id)
PROPERTIES (
    "enable_persistent_index" = "true"
);
```

# 明细表
明细表是默认创建的表类型。如果在建表时未指定任何 key，默认创建的是明细表。

建表时支持定义排序键。如果查询的过滤条件包含排序键，则 StarRocks 能够快速地过滤数据，提高查询效率。

明细表适用于日志数据分析等场景，支持追加新数据，不支持修改历史数据。

## 适用场景

    分析原始数据，例如原始日志、原始操作记录等。

    查询方式灵活，不需要局限于预聚合的分析方式。

    导入日志数据或者时序数据，主要特点是旧数据不会更新，只会追加新的数据。
## 创建表
```sql
CREATE TABLE detail (
    event_time DATETIME NOT NULL COMMENT "datetime of event",
    event_type INT NOT NULL COMMENT "type of event",
    user_id INT COMMENT "id of user",
    device_code INT COMMENT "device code",
    channel INT COMMENT "")
ORDER BY (event_time, event_type);
```

# 聚合表
建表时可以定义聚合键并且为 value 列指定聚合函数。当多条数据具有相同的聚合键时，value 列会进行聚合。并且支持单独定义排序键，如果查询的过滤条件包含排序键，则 StarRocks 能够快速地过滤数据，提高查询效率。

在分析统计和汇总数据时，聚合表能够减少查询时所需要处理的数据，提升查询效率。

## 适用场景

适用于分析统计和汇总数据。比如:
- 通过分析网站或 APP 的访问流量，统计用户的访问总时长、访问总次数。
- 广告厂商为广告主提供的广告点击总量、展示总量、消费统计等。
- 通过分析电商的全年交易数据，获得指定季度或者月份中，各类消费人群的爆款商品。

在这些场景中，数据查询和导入，具有以下特点：
- 多为汇总类查询，比如 SUM、MAX、MIN等类型的查询。
- 不需要查询原始的明细数据。
- 旧数据更新不频繁，只会追加新的数据。

## 原理
从数据导入至数据查询阶段，聚合表内部同一聚合键的数据会多次聚合，聚合的具体时机和机制如下：

    数据导入阶段：数据按批次导入至聚合表时，每一个批次的数据形成一个版本。在一个版本中，同一聚合键的数据会进行一次聚合。

    后台文件合并阶段 (Compaction) ：数据分批次多次导入至聚合表中，会生成多个版本的文件，多个版本的文件定期合并成一个大版本文件时，同一聚合键的数据会进行一次聚合。

    查询阶段：所有版本中同一聚合键的数据进行聚合，然后返回查询结果。

因此，聚合表中数据多次聚合，能够减少查询时所需要的处理的数据量，进而提升查询的效率。

## 创建表
```sql
CREATE TABLE aggregate_tbl (
    site_id LARGEINT NOT NULL COMMENT "id of site",
    date DATE NOT NULL COMMENT "time of event",
    city_code VARCHAR(20) COMMENT "city_code of user",
    pv BIGINT SUM DEFAULT "0" COMMENT "total page views"
)
AGGREGATE KEY(site_id, date, city_code)
DISTRIBUTED BY HASH(site_id);
```

# 数据分布
并且 StarRocks 通过设置分区 + 分桶的方式来实现数据分布。

- 第一层为分区：在一张表中，可以进行分区，支持的分区方式有表达式分区、Range 分区和 List 分区，或者不分区（即全表只有一个分区）。
- 第二层为分桶：在一个分区中，必须进行分桶。支持的分桶方式有哈希分桶和随机分桶。

Random 分布
```sql
CREATE TABLE site_access1 (
    event_day DATE,
    site_id INT DEFAULT '10', 
    pv BIGINT DEFAULT '0' ,
    city_code VARCHAR(100),
    user_name VARCHAR(32) DEFAULT ''
)
DUPLICATE KEY (event_day,site_id,pv);
-- 没有设置任何分区和分桶方式，默认为 Random 分布（目前仅支持明细表）
```

Hash 分布
```sql
CREATE TABLE site_access2 (
    event_day DATE,
    site_id INT DEFAULT '10',
    city_code SMALLINT,
    user_name VARCHAR(32) DEFAULT '',
    pv BIGINT SUM DEFAULT '0'
)
AGGREGATE KEY (event_day, site_id, city_code, user_name)
-- 设置分桶方式为哈希分桶，并且必须指定分桶键
DISTRIBUTED BY HASH(event_day,site_id); 
```

Range + Random 分布
```sql
CREATE TABLE site_access3 (
    event_day DATE,
    site_id INT DEFAULT '10', 
    pv BIGINT DEFAULT '0' ,
    city_code VARCHAR(100),
    user_name VARCHAR(32) DEFAULT ''
)
DUPLICATE KEY(event_day,site_id,pv)
-- 设为分区方式为表达式分区，并且使用时间函数的分区表达式（当然您也可以设置分区方式为 Range 分区）
PARTITION BY date_trunc('day', event_day);
-- 没有设置分桶方式，默认为随机分桶（目前仅支持明细表）
```

Range + Hash 分布
```sql
CREATE TABLE site_access4 (
    event_day DATE,
    site_id INT DEFAULT '10',
    city_code VARCHAR(100),
    user_name VARCHAR(32) DEFAULT '',
    pv BIGINT SUM DEFAULT '0'
)
AGGREGATE KEY(event_day, site_id, city_code, user_name)
-- 设为分区方式为表达式分区，并且使用时间函数的分区表达式（当然您也可以设置分区方式为 Range 分区）
PARTITION BY date_trunc('day', event_day)
-- 设置分桶方式为哈希分桶，必须指定分桶键
DISTRIBUTED BY HASH(event_day, site_id);
```

List + Random 分布
```sql
CREATE TABLE t_recharge_detail1 (
    id bigint,
    user_id bigint,
    recharge_money decimal(32,2), 
    city varchar(20) not null,
    dt date not null
)
DUPLICATE KEY(id)
-- 设为分区方式为表达式分区，并且使用列分区表达式（当然您也可以设置分区方式为 List 分区）
PARTITION BY (city);
-- 没有设置分桶方式，默认为随机分桶（目前仅支持明细表）
```

List + Hash 分布
```sql
CREATE TABLE t_recharge_detail2 (
    id bigint,
    user_id bigint,
    recharge_money decimal(32,2), 
    city varchar(20) not null,
    dt date not null
)
DUPLICATE KEY(id)
-- 设为分区方式为表达式分区，并且使用列分区表达式（当然您也可以设置分区方式为 List 分区）
PARTITION BY (city)
-- 设置分桶方式为哈希分桶，并且必须指定分桶键
DISTRIBUTED BY HASH(city,id); 
```
## 分区
分区用于将数据划分成不同的区间。分区的主要作用是将一张表按照分区键拆分成不同的管理单元，针对每一个管理单元选择相应的存储策略，比如分桶数、冷热策略、存储介质、副本数等。StarRocks 支持在一个集群内使用多种存储介质，您可以将新数据所在分区放在 SSD 盘上，利用 SSD 优秀的随机读写性能来提高查询性能，将旧数据存放在 SATA 盘上，以节省数据存储的成本。

## 创建和管理分区
### Range 分区
分区列为日期类型
```sql
CREATE TABLE site_access(
    event_day DATE,
    site_id INT,
    city_code VARCHAR(100),
    user_name VARCHAR(32),
    pv BIGINT SUM DEFAULT '0'
)
AGGREGATE KEY(event_day, site_id, city_code, user_name)
PARTITION BY RANGE(event_day)(
    PARTITION p1 VALUES LESS THAN ("2020-01-31"),
    PARTITION p2 VALUES LESS THAN ("2020-02-29"),
    PARTITION p3 VALUES LESS THAN ("2020-03-31")
)
DISTRIBUTED BY HASH(site_id);
```

分区列为整数类型
```sql
CREATE TABLE site_access(
    datekey INT,
    site_id INT,
    city_code SMALLINT,
    user_name VARCHAR(32),
    pv BIGINT SUM DEFAULT '0'
)
AGGREGATE KEY(datekey, site_id, city_code, user_name)
PARTITION BY RANGE (datekey) (
    PARTITION p1 VALUES LESS THAN ("20200131"),
    PARTITION p2 VALUES LESS THAN ("20200229"),
    PARTITION p3 VALUES LESS THAN ("20200331")
)
DISTRIBUTED BY HASH(site_id);
```

分区列值为字符串
```sql
CREATE TABLE site_access (
     event_time  varchar(100),
     site_id INT,
     city_code SMALLINT,
     user_name VARCHAR(32),
     pv BIGINT DEFAULT '0'
)
PARTITION BY RANGE(str2date(event_time, '%Y-%m-%d'))(
    START ("2021-01-01") END ("2021-01-10") EVERY (INTERVAL 1 DAY)
)
DISTRIBUTED BY HASH(site_id);
```

### List 分区

## 管理分区
### 增加分区
```sql
ALTER TABLE site_access
ADD PARTITION p4 VALUES LESS THAN ("2020-04-30")
DISTRIBUTED BY HASH(site_id);
```
### 删除分区
```sql
ALTER TABLE site_access
DROP PARTITION p1;
```
说明：分区中的数据不会立即删除，会在 Trash 中保留一段时间（默认为一天）。如果误删分区，可以通过 RECOVER 命令恢复分区及数据。

### 恢复分区
```sql
RECOVER PARTITION p1 FROM site_access;
```

### 查看分区
```sql
SHOW PARTITIONS FROM site_access;
```

## 设置分桶
### 随机分桶（自 v3.1）
仅支持明细表

没有使用 DISTRIBUTED BY xxx 语句，即表示默认由 StarRocks 使用随机分桶，并且由 StarRocks 自动设置分桶数量。

```sql
CREATE TABLE site_access2(
    event_day DATE,
    site_id INT DEFAULT '10', 
    pv BIGINT DEFAULT '0' ,
    city_code VARCHAR(100),
    user_name VARCHAR(32) DEFAULT ''
)
DUPLICATE KEY(event_day,site_id,pv)
DISTRIBUTED BY RANDOM BUCKETS 8; -- 手动设置分桶数量为 8
```
### 哈希分桶
注意事项

    建表时，如果使用哈希分桶，则必须指定分桶键。
    组成分桶键的列仅支持整型、DECIMAL、DATE/DATETIME、CHAR/VARCHAR/STRING 数据类型。
    自 3.2 起，建表后支持通过 ALTER TABLE 修改分桶键。
```sql
CREATE TABLE site_access(
    event_day DATE,
    site_id INT DEFAULT '10',
    city_code VARCHAR(100),
    user_name VARCHAR(32) DEFAULT '',
    pv BIGINT SUM DEFAULT '0'
)
AGGREGATE KEY(event_day, site_id, city_code, user_name)
PARTITION BY RANGE(event_day) (
    PARTITION p1 VALUES LESS THAN ("2020-01-31"),
    PARTITION p2 VALUES LESS THAN ("2020-02-29"),
    PARTITION p3 VALUES LESS THAN ("2020-03-31")
)
DISTRIBUTED BY HASH(site_id);
```

```sql
-- 手动指定所有分区中分桶数量
ALTER TABLE site_access
DISTRIBUTED BY HASH(site_id,city_code) BUCKETS 30;
-- 手动指定部分分区中分桶数量
ALTER TABLE site_access
partitions p20230104
DISTRIBUTED BY HASH(site_id,city_code)  BUCKETS 30;
-- 手动指定新增分区中分桶数量
ALTER TABLE site_access
ADD PARTITION p20230106 VALUES [('2023-01-06'), ('2023-01-07'))
DISTRIBUTED BY HASH(site_id,city_code) BUCKETS 30;
```

### 查看分桶数量
```sql
SHOW PARTITIONS xxxxx
```

## 建表后优化数据分布（自 3.2）
```sql
ALTER TABLE t DISTRIBUTED BY HASH(k1, k2) BUCKETS 20;
-- 如果是 StarRocks 的版本是 3.1及以上，并且使用的是明细表，则建议直接改成默认分桶设置，即随机分桶并且由 StarRocks 自动设置分桶数量
ALTER TABLE t DISTRIBUTED BY RANDOM;

-- 如果表为主键表，当业务的查询模式有较大变化，经常需要用到表中另外几个列作为条件列时，则可以调整排序键。如下：
ALTER TABLE t ORDER BY k2, k1;
```

## 最佳实践
对于 StarRocks 而言，分区和分桶的选择是非常关键的。在建表时选择合理的分区键和分桶键，可以有效提高集群整体性能。因此建议在选择分区键和分桶键时，根据业务情况进行调整。

- 数据倾斜  
    如果业务场景中单独采用倾斜度大的列做分桶，很大程度会导致访问数据倾斜，那么建议采用多列组合的方式进行数据分桶。
- 高并发  
    分区和分桶应该尽量覆盖查询语句所带的条件，这样可以有效减少扫描数据，提高并发。
- 高吞吐  
    尽量把数据打散，让集群以更高的并发扫描数据，完成相应计算。
- 元数据管理  
    Tablet 过多会增加 FE/BE 的元数据管理和调度的资源消耗。

## 表达式分区
### 时间函数表达式分区
```sql
PARTITION BY expression
...
[ PROPERTIES( 'partition_live_number' = 'xxx' ) ]

expression ::=
    { date_trunc ( <time_unit> , <partition_column> ) |
      time_slice ( <partition_column> , INTERVAL <N> <time_unit> [ , boundary ] ) }
```
示例：
```sql
CREATE TABLE site_access1 (
    event_day DATETIME NOT NULL,
    site_id INT DEFAULT '10',
    city_code VARCHAR(100),
    user_name VARCHAR(32) DEFAULT '',
    pv BIGINT DEFAULT '0'
)
DUPLICATE KEY(event_day, site_id, city_code, user_name)
PARTITION BY date_trunc('day', event_day)
DISTRIBUTED BY HASH(event_day, site_id);
```
如果您希望引入分区生命周期管理，即仅保留最近一段时间的分区，删除历史分区，则可以使用 partition_live_number 设置只保留最近多少数量的分区。
```sql
CREATE TABLE site_access2 (
    event_day DATETIME NOT NULL,
    site_id INT DEFAULT '10',
    city_code VARCHAR(100),
    user_name VARCHAR(32) DEFAULT '',
    pv BIGINT DEFAULT '0'
) 
DUPLICATE KEY(event_day, site_id, city_code, user_name)
PARTITION BY date_trunc('month', event_day)
DISTRIBUTED BY HASH(event_day, site_id)
PROPERTIES(
    "partition_live_number" = "3" -- 只保留最近 3 个分区
);
```

### 列表达式分区（自 v3.1）
```sql
PARTITION BY expression
...
[ PROPERTIES( 'partition_live_number' = 'xxx' ) ]

expression ::=
    ( <partition_columns> )
    
partition_columns ::=
    <column>, [ <column> [,...] ]
```
示例：
```sql
CREATE TABLE t_recharge_detail1 (
    id bigint,
    user_id bigint,
    recharge_money decimal(32,2), 
    city varchar(20) not null,
    dt varchar(20) not null
)
DUPLICATE KEY(id)
PARTITION BY (dt,city)
DISTRIBUTED BY HASH(`id`);
```
### 使用限制

    自 v3.1.0 起，StarRocks 存算分离模式支持时间函数表达式分区。并且自 v3.1.1 起 StarRocks 存算分离模式支持列表达式分区。
    使用 CTAS 建表时暂时不支持表达式分区。
    暂时不支持使用 Spark Load 导入数据至表达式分区的表。
    使用 ALTER TABLE <table_name> DROP PARTITION <partition_name> 删除列表达式分区时，分区直接被删除并且不能被恢复。
    列表达式分区暂时不支持备份与恢复。
    如果使用表达式分区，则仅支持回滚到 2.5.4 及以后的版本。
## List 分区
```sql
PARTITION BY LIST (partition_columns)（
    PARTITION <partition_name> VALUES IN (value_list)
    [, ...]
)

partition_columns::= 
    <column> [,<column> [, ...] ]

value_list ::=
    value_item [, value_item [, ...] ]

value_item ::=
    { <value> | ( <value> [, <value>, [, ...] ] ) }    
```

```sql
CREATE TABLE t_recharge_detail4 (
    id bigint,
    user_id bigint,
    recharge_money decimal(32,2), 
    city varchar(20) not null,
    dt varchar(20) not null
) ENGINE=OLAP
DUPLICATE KEY(id)
PARTITION BY LIST (dt,city) (
   PARTITION p202204_California VALUES IN (
       ("2022-04-01", "Los Angeles"),
       ("2022-04-01", "San Francisco"),
       ("2022-04-02", "Los Angeles"),
       ("2022-04-02", "San Francisco")
    ),
   PARTITION p202204_Texas VALUES IN (
       ("2022-04-01", "Houston"),
       ("2022-04-01", "Dallas"),
       ("2022-04-02", "Houston"),
       ("2022-04-02", "Dallas")
   )
)
DISTRIBUTED BY HASH(`id`);
```
### 使用限制

    不支持动态和批量创建 List 分区。
    StarRocks 存算分离模式 从 3.1.1 版本开始支持该功能。
    使用 ALTER TABLE <table_name> DROP PARTITION <partition_name>; 分区直接被删除并且不能被恢复。
    List 分区暂时不支持备份与恢复。
    异步物化视图暂不支持基于使用 List 分区的基表创建。
## 动态分区
```sql
CREATE TABLE site_access(
event_day DATE,
site_id INT DEFAULT '10',
city_code VARCHAR(100),
user_name VARCHAR(32) DEFAULT '',
pv BIGINT DEFAULT '0'
)
DUPLICATE KEY(event_day, site_id, city_code, user_name)
PARTITION BY RANGE(event_day)(
PARTITION p20200321 VALUES LESS THAN ("2020-03-22"),
PARTITION p20200322 VALUES LESS THAN ("2020-03-23"),
PARTITION p20200323 VALUES LESS THAN ("2020-03-24"),
PARTITION p20200324 VALUES LESS THAN ("2020-03-25")
)
DISTRIBUTED BY HASH(event_day, site_id)
PROPERTIES(
    "dynamic_partition.enable" = "true",
    "dynamic_partition.time_unit" = "DAY",
    "dynamic_partition.start" = "-3",
    "dynamic_partition.end" = "3",
    "dynamic_partition.prefix" = "p",
    "dynamic_partition.history_partition_num" = "0"
);
```
### 修改表的动态分区属性
```sql
ALTER TABLE site_access SET("dynamic_partition.enable"="false");
ALTER TABLE site_access SET("dynamic_partition.enable"="true");
```

## 临时分区
您可以在一张已经定义分区规则的分区表上，创建临时分区，并为这些临时分区设定单独的数据分布策略。在原子覆盖写操作或调整分区分桶策略时候，您可以将临时分区作为临时可用的数据载体。您可以为临时分区设定的数据分布策略包括分区范围、分桶数、以及部分属性，例如副本数、存储介质。

在以下应用场景中，您可以使用临时分区功能：

- 原子覆盖写操作  
    如果您需要重写某一正式分区的数据，同时保证重写过程中可以查看数据，您可以先创建一个对应的临时分区，将新的数据导入到临时分区后，通过替换操作，原子地替换原有正式分区，生成新正式分区。对于非分区表的原子覆盖写操作，请参考 ALTER TABLE - SWAP。
- 调整分区数据的查询并发  
    如果您需要修改某一正式分区的分桶数，您可以先创建一个对应分区范围的临时分区，并指定新的分桶数，然后通过 INSERT INTO 命令将原有正式分区的数据导入到临时分区中，通过替换操作，原子地替换原有正式分区，生成新正式分区。
- 修改分区策略  
    如果您希望修改正式分区的分区范围，例如合并多个小分区为一个大分区，或将一个大分区分割成多个小分区，您可以先建立对应合并或分割后范围的临时分区，然后通过 INSERT INTO 命令将原有正式分区的数据导入到临时分区中，通过替换操作，原子地替换原有正式分区，生成新正式分区。

### 创建临时分区
创建一个临时分区
```sql
ALTER TABLE <table_name> 
ADD TEMPORARY PARTITION <temporary_partition_name> VALUES [("value1"), {MAXVALUE|("value2")})]
[(partition_desc)]
[DISTRIBUTED BY HASH(<bucket_key>)];
```

```sql
ALTER TABLE <table_name> 
ADD TEMPORARY PARTITION <temporary_partition_name> VALUES LESS THAN {MAXVALUE|(<"value">)}
[(partition_desc)]
[DISTRIBUTED BY HASH(<bucket_key>)];
```

批量创建临时分区
```sql
ALTER TABLE <table_name>
ADD TEMPORARY PARTITIONS START ("value1") END ("value2") EVERY {(INTERVAL <num> <time_unit>)|<num>}
[(partition_desc)]
[DISTRIBUTED BY HASH(<bucket_key>)];
```
示例
```sql
ALTER TABLE site_access
ADD TEMPORARY PARTITION tp1 VALUES [("2020-01-01"), ("2020-02-01"));
```

注意事项

    临时分区的分区列和原有正式分区相同，且不可修改。
    临时分区的分区名称不能和正式分区以及其他临时分区重复。
    一张表所有临时分区之间的分区范围不可重叠，但临时分区的范围和正式分区范围可以重叠。

查看临时分区
```sql
SHOW TEMPORARY PARTITIONS FROM site_access;
```

使用临时分区进行替换

您可以通过以下命令使用临时分区替换原有正式分区，形成新正式分区。分区替换成功后，原有正式分区和临时分区被删除且不可恢复。

# 索引
StarRocks 提供了丰富的索引类型，主要分为以下两类：
- StarRocks 自动创建的索引，称为内置索引，包括前缀索引、Ordinal 索引、ZoneMap 索引。
- StarRocks 同时也支持用户手动创建索引，包括 Bitmap 索引和 Bloom filter 索引。

## 内置索引
### 前缀索引
数据写入时候自动生成前缀索引。具体来说，写入时数据按照指定的排序键排序，并且每写入 1024 行数据构成一个逻辑数据块（Data Block），在前缀索引表中存储一个索引项，内容为该逻辑数据块中第一行数据的排序列组成的前缀。 当查询的过滤条件命中前缀索引的前缀，则可以快速定位符合条件的数据，减少扫描的数据量，从而查询性能可以得到显著提升。
### Ordinal 索引
底层存储数据时，StarRocks 实际上采用列式存储。每一列数据以 Date Page 为单位分块存储，每个 Data Page 大小一般为 64*1024 个字节（data_page_size = 64 * 1024）。每一个列 Date Page 会对应生成一条 Ordinal 索引项，记录 Data Page 的起始行号等信息。这样 Ordinal 索引提供了通过行号来查找列 Data Page 数据页的物理地址。其他索引查找数据时，最终都要通过 Ordinal 索引查找列 Data Page 的位置。
![](https://docs.starrocks.io/zh/assets/images/3.1-2-35880a0641f7872015b7fb2e414cf2c7.png)

### ZoneMap 索引
ZoneMap 索引存储了每块数据统计信息，统计信息包括 Min 最大值、Max 最小值、HasNull 空值、HasNotNull 不全为空的信息。在查询时，StarRocks 可以根据这些统计信息，快速判断这些数据块是否可以过滤掉，从而减少扫描数据量，提升查询速度。

在实现上，“每块”数据可以是一个 Segment，也可以是一个列的一个 Data Page，相应的 ZoneMap 索引有两种：一种是存每个 Segment 的统计信息，另一种是存每个 Data Page 的统计信息

## 手动创建的索引
### Bitmap 索引
Bitmap 索引适用于较高基数列的查询和多个低基数列的组合查询，并且此时 Bitmap 索引对查询的过滤效果比较好，至少可以过滤掉 999/1000 的数据。
### Bloom filter 索引
Bloom filter 索引适用于基数较高的列，比如 ID 列，但是存在一定的误判率。
### N-Gram bloomfilter 索引
N-Gram bloom filter 索引是一种特殊的 Bloom filter 索引，通常用于加速 LIKE 查询或 ngram_search 和 ngram_search_case_insensitive 函数的运算速度。
### 全文倒排索引
全文倒排索引可以快速定位到与关键词匹配的数据行，能够加速全文检索。

# 前缀索引和排序键
并且数据写入的过程中会自动生成前缀索引。数据按照指定的排序键排序后，每写入 1024 行数据构成一个逻辑数据块（Data Block），在前缀索引表中存储一个索引项，内容为该逻辑数据块中第一行数据的排序列组成的前缀。

通过这样两层的排序结构，查询时就可以使用二分查找快速跳过不符合条件的数据。


注意事项
- 前缀字段的数量不超过 3 个，前缀索引项的最大长度为 36 字节。
- 前缀字段中 CHAR、VARCHAR、STRING 类型的列只能出现一次，并且处在末尾位置。
- 如果表中通过 ORDER BY 指定了排序键，就根据排序键构建前缀索引；如果没有通过 ORDER BY 指定排序键，就根据 Key 列构建前缀索引。

```sql
CREATE TABLE user_access (
    uid int,
    name varchar(64),
    age int, 
    phone varchar(16),
    last_access datetime,
    credits double
)
ORDER BY (uid, name);
```

# Bitmap 索引
注意事项  
支持优化的查询  
Bitmap 索引适用于优化等值 = 查询、[NOT] IN 范围查询、>，>=，<，<= 查询、 IS NULL 查询。不适用于优化 !=，[NOT] LIKE 查询。

```sql
CREATE TABLE `lineorder_partial` (
  `lo_orderkey` int(11) NOT NULL COMMENT "",
  `lo_orderdate` int(11) NOT NULL COMMENT "",
  `lo_orderpriority` varchar(16) NOT NULL COMMENT "",
  `lo_quantity` int(11) NOT NULL COMMENT "",
  `lo_revenue` int(11) NOT NULL COMMENT "",
   INDEX lo_orderdate_index (lo_orderdate) USING BITMAP
) ENGINE=OLAP 
DUPLICATE KEY(`lo_orderkey`)
DISTRIBUTED BY HASH(`lo_orderkey`) BUCKETS 1;
```

# Bloom filter 索引
Bloom filter 索引可以快速判断表的数据文件中是否可能包含要查询的数据，如果不包含就跳过，从而减少扫描的数据量。Bloom filter 索引空间效率高，适用于基数较高的列，如 ID 列。如果一个查询条件命中前缀索引列，StarRocks 会使用前缀索引快速返回查询结果。但是前缀索引的长度有限，如果想要快速查询一个非前缀索引列且该列基数较高，即可为这个列创建 Bloom filter 索引。

## 索引原理

例如，在表 table1 的 column1 列上创建 Bloom filter 索引，然后执行一个 SQL 查询 Select xxx from table1 where column1 = something; 命中索引，那么在扫描表的数据文件时会出现两种情况：

    如果 Bloom filter 索引判断一个数据文件中不存在目标数据，那 StarRocks 会跳过该文件，从而提高查询效率。
    如果 Bloom filter 索引判断一个数据文件中可能存在目标数据，那 StarRocks 会读取该文件确认目标数据是否存在。注意，这里仅仅是判断该文件中可能包含目标数据。Bloom filter 索引有一定的误判率，也称为假阳性概率 (False Positive Probability)，即判断某行中包含目标数据，而实际上该行并不包含目标数据的概率。

```sql
CREATE TABLE table1
(
    k1 BIGINT,
    k2 LARGEINT,
    v1 VARCHAR(2048) REPLACE,
    v2 SMALLINT DEFAULT "10"
)
ENGINE = olap
PRIMARY KEY(k1, k2)
DISTRIBUTED BY HASH (k1, k2)
PROPERTIES("bloom_filter_columns" = "k1,k2");
```

# N-Gram bloom filter 索引

# 全文倒排索引
```sql
CREATE TABLE `t` (
  `k` BIGINT NOT NULL COMMENT "",
  `v` STRING COMMENT "",
   INDEX idx (v) USING GIN("parser" = "english")
) ENGINE=OLAP 
DUPLICATE KEY(`k`)
DISTRIBUTED BY HASH(`k`) BUCKETS 1
PROPERTIES (
"replicated_storage" = "false"
);

SELECT * FROM t WHERE t.value MATCH "starrocks";

表达式谓词：(NOT) LIKE、(NOT) MATCH
```

# 数据压缩
StarRocks 支持四种数据压缩算法：LZ4、Zstandard（或 zstd）、zlib 和 Snappy。
```sql
CREATE TABLE `data_compression` (
  `id`      INT(11)     NOT NULL     COMMENT "",
  `name`    CHAR(200)   NULL         COMMENT ""
)
ENGINE=OLAP 
UNIQUE KEY(`id`)
COMMENT "OLAP"
DISTRIBUTED BY HASH(`id`)
PROPERTIES (
"compression" = "ZSTD"
);
```

# 加速查询
## CBO 统计信息

本文介绍 StarRocks CBO 优化器（Cost-based Optimizer）的基本概念，以及如何为 CBO 优化器采集统计信息来优化查询计划。StarRocks 2.4 版本引入直方图作为统计信息，提供更准确的数据分布统计。

## 同步物化视图

- 单表聚合	仅部分聚合函数
- 多表关联	否
- 查询改写	是
- 刷新策略	导入同步刷新
- 基表      仅支持基于 Default Catalog 的单表构建
#### 相关概念


    基表（Base Table）

    物化视图的驱动表。

    对于 StarRocks 的同步物化视图，基表仅可以是 Default catalog 中的单个内部表。StarRocks 支持在明细表、聚合表上创建同步物化视图。

    刷新（Refresh）

    StarRocks 同步物化视图中的数据将在数据导入基表时自动更新，无需手动调用刷新命令。

    查询改写（Query Rewrite）

    查询改写是指在对已构建了物化视图的基表进行查询时，系统自动判断是否可以复用物化视图中的预计算结果处理查询。如果可以复用，系统会直接从相关的物化视图读取预计算结果，以避免重复计算消耗系统资源和时间。

    StarRocks 的同步物化视图支持部分聚合算子的查询改写。详细信息，请参见 聚合函数匹配关系。
### 创建同步物化视图
```sql
CREATE MATERIALIZED VIEW store_amt AS
SELECT store_id, SUM(sale_amt)
FROM sales_records
GROUP BY store_id;
```
查看同步物化视图构建状态
```sql
SHOW ALTER MATERIALIZED VIEW\G
```
### 最佳实践
精确去重

## 异步物化视图
相较于同步物化视图，异步物化视图支持多表关联以及更加丰富的聚合算子。异步物化视图可以通过手动调用或定时任务的方式刷新，并且支持刷新部分分区，可以大幅降低刷新成本。除此之外，异步物化视图支持多种查询改写场景，实现自动、透明查询加速。
### 使用场景

如果您的数据仓库环境中有以下需求，我们建议您创建异步物化视图：

    加速重复聚合查询

    假设您的数仓环境中存在大量包含相同聚合函数子查询的查询，占用了大量计算资源，您可以根据该子查询建立异步物化视图，计算并保存该子查询的所有结果。建立成功后，系统将自动改写查询语句，直接查询异步物化视图中的中间结果，从而降低负载，加速查询。

    周期性多表关联查询

    假设您需要定期将数据仓库中多张表关联，生成一张新的宽表，您可以为这些表建立异步物化视图，并设定定期刷新规则，从而避免手动调度关联任务。异步物化视图建立成功后，查询将直接基于异步物化视图返回结果，从而避免关联操作带来的延迟。

    数仓分层

    假设您的基表中包含大量原始数据，查询需要进行复杂的 ETL 操作，您可以通过对数据建立多层异步物化视图实现数仓分层。如此可以将复杂查询分解为多层简单查询，既可以减少重复计算，又能够帮助维护人员快速定位问题。除此之外，数仓分层还可以将原始数据与统计数据解耦，从而保护敏感性原始数据。

    湖仓加速

    查询数据湖可能由于网络延迟和对象存储的吞吐限制而变慢。您可以通过在数据湖之上构建异步物化视图来提升查询性能。此外，StarRocks 可以智能改写查询以使用现有的物化视图，省去了手动修改查询的麻烦。

```sql
CREATE MATERIALIZED VIEW order_mv
DISTRIBUTED BY HASH(`order_id`)
REFRESH ASYNC START('2022-09-01 10:00:00') EVERY (interval 1 day)
AS SELECT
    order_list.order_id,
    sum(goods.price) as total
FROM order_list INNER JOIN goods ON goods.item_id1 = order_list.item_id2
GROUP BY order_id;
```
手动刷新异步物化视图
```sql
-- 异步调用刷新任务。
REFRESH MATERIALIZED VIEW order_mv;
-- 同步调用刷新任务。
REFRESH MATERIALIZED VIEW order_mv WITH SYNC MODE;
```

# Colocate Join
Colocate Join 功能是分布式系统实现 Join 数据分布的策略之一，能够减少数据多节点分布时 Join 操作引起的数据移动和网络传输，从而提高查询性能。

在 StarRocks 中使用 Colocate Join 功能，您需要在建表时为其指定一个 Colocation Group（CG），同一 CG 内的表需遵循相同的 Colocation Group Schema（CGS），即表对应的分桶副本具有一致的分桶键、副本数量和副本放置方式。如此可以保证同一 CG 内，所有表的数据分布在相同一组 BE 节点上。当 Join 列为分桶键时，计算节点只需做本地 Join，从而减少数据在节点间的传输耗时，提高查询性能。因此，Colocate Join，相对于其他 Join，例如 Shuffle Join 和 Broadcast Join，可以有效避免数据网络传输开销，提高查询性能。

Colocate Join 支持等值 Join。

# 使用 Lateral Join 实现列转行
「行列转化」是 ETL 处理过程中常见的操作。Lateral Join 功能能够将每行数据和内部的子查询或者 Table Function 关联。通过 Lateral Join 与 Unnest 功能配合，您可以实现一行转多行的功能。Unnest 是一种 Table Function，可以把数组类型转化成 Table 的多行。更多信息，参见 unnest。

# Query Cache
StarRocks 提供的 Query Cache 特性，可以帮助您极大地提升聚合查询的性能。开启 Query Cache 后，每次处理聚合查询时，StarRocks 都会将本地聚合的中间结果缓存于内存中。这样，后续收到相同或类似的聚合查询时，StarRocks 就能够直接从 Query Cache 获取匹配的聚合结果，而无需从磁盘读取数据并进行计算，大大节省查询的时间和资源成本，并提升查询的可扩展性。在大量用户同时对复杂的大数据集执行相同或类似查询的高并发场景下，Query Cache 的优势尤为明显。

## 应用场景

Query Cache 可以生效的典型应用场景有如下特点：

    查询多为宽表模型下的单表聚合查询或星型模型下简单多表 JOIN 的聚合查询。
    聚合查询以非 GROUP BY 聚合和低基数 GROUP BY 聚合为主。
    查询的数据以按时间分区追加的形式导入，并且在不同时间分区上的访问表现出冷热性。
# 管理手册
## 运维集群
### 扩容缩容 StarRocks
扩缩容 FE 集群  
扩缩容 BE 集群
### 管理 BE 黑名单
### 备份与恢复
在 AWS S3 中创建仓库

备份数据快照
```sql
BACKUP SNAPSHOT sr_hub.sr_member_backup
TO test_repo
ON (sr_member);
```

恢复或迁移数据

```sql
RESTORE SNAPSHOT sr_hub.sr_member_backup
FROM test_repo
ON (sr_member)
PROPERTIES (
    "backup_timestamp"="2023-02-07-14-45-53-143",
    "replication_num" = "1"
);
```