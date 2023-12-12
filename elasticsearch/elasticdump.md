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

