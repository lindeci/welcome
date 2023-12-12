# 使用datastream
SkyWalking 会自动创建所需的 Elasticsearch 索引。您不需要手动创建索引。SkyWalking 使用模板来定义索引的映射和设置。当 SkyWalking 首次启动时，它会检查 Elasticsearch 中是否存在所需的模板。如果模板不存在，SkyWalking 会自动创建它们。然后，当 SkyWalking 将数据写入 Elasticsearch 时，Elasticsearch 会根据模板自动创建所需的索引。

在 SkyWalking 8.7.0 及更高版本中，SkyWalking 支持使用 Elasticsearch 的 DataStream 功能来存储数据。要启用此功能，您需要在 SkyWalking 的配置文件中将 `storage.elasticsearch.enableDataStream` 设置为 `true`。

在`application.yml`中配置
```
storage:
  elasticsearch:
    enableDataStream: true
```