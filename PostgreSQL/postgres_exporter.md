- [官网](#官网)
- [下载镜像](#下载镜像)
- [加载镜像](#加载镜像)
- [运行](#运行)
- [grafana监控](#grafana监控)

# 官网


# 下载镜像
```
docker run   --net=host   -e DATA_SOURCE_NAME="postgresql://postgres:password@localhost:5432/postgres?sslmode=disable"   docker.io/prometheuscommunity/postgres-exporter

docker save prometheuscommunity/postgres-exporter > postgres-exporter.tar
```

# 加载镜像
```
docker load < postgres-exporter.tar
```

# 运行
```
docker run -d --net=host -e DATA_SOURCE_NAME="postgresql://postgres:12345@localhost:5432/postgres?sslmode=disable" prometheuscommunity/postgres-exporter
```


# grafana监控
参考 https://www.cnblogs.com/ilifeilong/p/10543876.html