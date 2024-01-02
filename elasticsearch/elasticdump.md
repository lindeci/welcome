# 参考文档
https://github.com/elasticsearch-dump/elasticsearch-dump

# docer 安装
```sh
docker pull elasticdump/elasticsearch-dump
# docker tag elasticdump/elasticsearch-dump registrytest.qevoc.com/public/elasticdump/elasticsearch-dump
# docker push  registrytest.qevoc.com/public/elasticdump/elasticsearch-dump
# docker login  registrytest.qevoc.com
docker save elasticdump/elasticsearch-dump >elasticsearch-dump.tar
```
# 备份数据
```sh
docker run --rm -ti -v /opt/data:/tmp/data elasticdump/elasticsearch-dump \
--input=http://elastic:elastic@1.1.1.1:9200/test \
--output=/tmp/data/test.json \
--type=data --limit=10000
```

# 加载镜像
```sh
docker load < elasticsearch-dump.tar
```

# 还原数据
```sh
docker run --rm -ti -v /opt/data:/tmp/data elasticdump/elasticsearch-dump \
--input=./device_model.json \
--output=http://elastic:elastic@1.1.1.2:9200/device_model \
--type=data
```

# 检查数据
```sh
curl -XPOST 'http://1.1.1.2:9200/device_model/_count?pretty' -uelastic:elastic
```



docker run --rm -ti -v /opt/data:/tmp/data elasticdump/elasticsearch-dump \
--input=http://elastic:elastic@172.1.1.141:9200/gateway_elastic \
--output= /tmp/data/ \
--type=data


# 导出数据
```
docker run --rm -ti -v /opt/data:/tmp/data elasticdump/elasticsearch-dump bash
# 如果 ES 开启 https
export NODE_TLS_REJECT_UNAUTHORIZED='0'
# 导出解析器
elasticdump   --input=https://elastic:elastic@172.1.1.2:9200/test_user   --output=/tmp/test_user.json   --type=analyzer
# 导出映射
elasticdump   --input=https://elastic:elastic@172.1.1.2:9200/test_user   --output=/tmp/test_user.json   --type=mapping
# 导出数据
elasticdump   --input=https://elastic:elastic@172.1.1.2:9200/test_user   --output=/tmp/test_user.json   --type=data

```

# 官方例子
https://www.npmjs.com/package/elasticdump/v/6.103.0

```
# Copy an index from production to staging with analyzer and mapping:
elasticdump \
  --input=http://production.es.com:9200/my_index \
  --output=http://staging.es.com:9200/my_index \
  --type=analyzer
elasticdump \
  --input=http://production.es.com:9200/my_index \
  --output=http://staging.es.com:9200/my_index \
  --type=mapping
elasticdump \
  --input=http://production.es.com:9200/my_index \
  --output=http://staging.es.com:9200/my_index \
  --type=data

# Backup index data to a file:
elasticdump \
  --input=http://production.es.com:9200/my_index \
  --output=/data/my_index_mapping.json \
  --type=mapping
elasticdump \
  --input=http://production.es.com:9200/my_index \
  --output=/data/my_index.json \
  --type=data

# Backup and index to a gzip using stdout:
elasticdump \
  --input=http://production.es.com:9200/my_index \
  --output=$ \
  | gzip > /data/my_index.json.gz

# Backup the results of a query to a file
elasticdump \
  --input=http://production.es.com:9200/my_index \
  --output=query.json \
  --searchBody="{\"query\":{\"term\":{\"username\": \"admin\"}}}"
  
# Specify searchBody from a file
elasticdump \
  --input=http://production.es.com:9200/my_index \
  --output=query.json \
  --searchBody=@/data/searchbody.json  

# Copy a single shard data:
elasticdump \
  --input=http://es.com:9200/api \
  --output=http://es.com:9200/api2 \
  --input-params="{\"preference\":\"_shards:0\"}"

# Backup aliases to a file
elasticdump \
  --input=http://es.com:9200/index-name/alias-filter \
  --output=alias.json \
  --type=alias

# Import aliases into ES
elasticdump \
  --input=./alias.json \
  --output=http://es.com:9200 \
  --type=alias

# Backup templates to a file
elasticdump \
  --input=http://es.com:9200/template-filter \
  --output=templates.json \
  --type=template

# Import templates into ES
elasticdump \
  --input=./templates.json \
  --output=http://es.com:9200 \
  --type=template

# Split files into multiple parts
elasticdump \
  --input=http://production.es.com:9200/my_index \
  --output=/data/my_index.json \
  --fileSize=10mb

# Import data from S3 into ES (using s3urls)
elasticdump \
  --s3AccessKeyId "${access_key_id}" \
  --s3SecretAccessKey "${access_key_secret}" \
  --input "s3://${bucket_name}/${file_name}.json" \
  --output=http://production.es.com:9200/my_index

# Export ES data to S3 (using s3urls)
elasticdump \
  --s3AccessKeyId "${access_key_id}" \
  --s3SecretAccessKey "${access_key_secret}" \
  --input=http://production.es.com:9200/my_index \
  --output "s3://${bucket_name}/${file_name}.json"

# Import data from MINIO (s3 compatible) into ES (using s3urls)
elasticdump \
  --s3AccessKeyId "${access_key_id}" \
  --s3SecretAccessKey "${access_key_secret}" \
  --input "s3://${bucket_name}/${file_name}.json" \
  --output=http://production.es.com:9200/my_index
  --s3ForcePathStyle true
  --s3Endpoint https://production.minio.co

# Export ES data to MINIO (s3 compatible) (using s3urls)
elasticdump \
  --s3AccessKeyId "${access_key_id}" \
  --s3SecretAccessKey "${access_key_secret}" \
  --input=http://production.es.com:9200/my_index \
  --output "s3://${bucket_name}/${file_name}.json"
  --s3ForcePathStyle true
  --s3Endpoint https://production.minio.co

# Import data from CSV file into ES (using csvurls)
elasticdump \
  # csv:// prefix must be included to allow parsing of csv files
  # --input "csv://${file_path}.csv" \
  --input "csv:///data/cars.csv"
  --output=http://production.es.com:9200/my_index \
  --csvSkipRows 1    # used to skip parsed rows (this does not include the headers row)
  --csvDelimiter ";" # default csvDelimiter is ','
```

# multielasticdump
```
export NODE_TLS_REJECT_UNAUTHORIZED='0'
# 导出
multielasticdump   --direction=dump   --match='^protocol_v1.1$'  --input=https://elastic:elastic@172.1.1.2:9200   --ignoreType=''   --output=/tmp --includeType='data,mapping,analyzer,alias,settings,template'
# 导入
multielasticdump   --direction=load   --match='^protocol_v1.1$'  --output=https://elastic:elastic@172.1.1.3:9200   --ignoreType=''   --input=/tmp --includeType='data,mapping,analyzer,alias,settings,template'
```