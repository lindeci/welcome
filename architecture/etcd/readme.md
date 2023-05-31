# 官网

https://github.com/etcd-io/etcd

# 概述

etcd is a distributed reliable key-value store for the most critical data of a distributed system

# 安装

安装配置页面
http://play.etcd.io/install

```sh
# make sure etcd process has write access to this directory
# remove this directory if the cluster is new; keep if restarting etcd
rm -rf /data/etcd/s1


# to write service file for etcd with Docker
cat > /tmp/s1.service <<EOF
[Unit]
Description=etcd with Docker
Documentation=https://github.com/coreos/etcd

[Service]
Restart=always
RestartSec=5s
TimeoutStartSec=0
LimitNOFILE=40000

ExecStart=/usr/bin/docker \
  run \
  --rm \
  --net=host \
  --name etcd-v3.3.8-1 \
  --volume=/data/etcd/s1:/etcd-data \
  gcr.io/etcd-development/etcd:v3.3.8 \
  /usr/local/bin/etcd \
  --name s1 \
  --data-dir /etcd-data \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:3380,s3=http://localhost:4380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new \
  --auto-compaction-retention 1

ExecStop=/usr/bin/docker stop etcd-v3.3.8-1

[Install]
WantedBy=multi-user.target
EOF
sudo mv /tmp/s1.service /etc/systemd/system/s1.service

#######################################################################################
# make sure etcd process has write access to this directory
# remove this directory if the cluster is new; keep if restarting etcd
rm -rf /data/etcd/s2


# to write service file for etcd with Docker
cat > /tmp/s2.service <<EOF
[Unit]
Description=etcd with Docker
Documentation=https://github.com/coreos/etcd

[Service]
Restart=always
RestartSec=5s
TimeoutStartSec=0
LimitNOFILE=40000

ExecStart=/usr/bin/docker \
  run \
  --rm \
  --net=host \
  --name etcd-v3.3.8-2 \
  --volume=/data/etcd/s2:/etcd-data \
  gcr.io/etcd-development/etcd:v3.3.8 \
  /usr/local/bin/etcd \
  --name s2 \
  --data-dir /etcd-data \
  --listen-client-urls http://localhost:3379 \
  --advertise-client-urls http://localhost:3379 \
  --listen-peer-urls http://localhost:3380 \
  --initial-advertise-peer-urls http://localhost:3380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:3380,s3=http://localhost:4380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new \
  --auto-compaction-retention 1

ExecStop=/usr/bin/docker stop etcd-v3.3.8-2

[Install]
WantedBy=multi-user.target
EOF
sudo mv /tmp/s2.service /etc/systemd/system/s2.service

#######################################################################################
# make sure etcd process has write access to this directory
# remove this directory if the cluster is new; keep if restarting etcd
rm -rf /data/etcd/s3


# to write service file for etcd with Docker
cat > /tmp/s3.service <<EOF
[Unit]
Description=etcd with Docker
Documentation=https://github.com/coreos/etcd

[Service]
Restart=always
RestartSec=5s
TimeoutStartSec=0
LimitNOFILE=40000

ExecStart=/usr/bin/docker \
  run \
  --rm \
  --net=host \
  --name etcd-v3.3.8-3 \
  --volume=/data/etcd/s3:/etcd-data \
  gcr.io/etcd-development/etcd:v3.3.8 \
  /usr/local/bin/etcd \
  --name s3 \
  --data-dir /etcd-data \
  --listen-client-urls http://localhost:4379 \
  --advertise-client-urls http://localhost:4379 \
  --listen-peer-urls http://localhost:4380 \
  --initial-advertise-peer-urls http://localhost:4380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:3380,s3=http://localhost:4380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new \
  --auto-compaction-retention 1

ExecStop=/usr/bin/docker stop etcd-v3.3.8-3

[Install]
WantedBy=multi-user.target
EOF
sudo mv /tmp/s3.service /etc/systemd/system/s3.service
```

# 运维命令

```sh
# to start service
sudo systemctl daemon-reload
sudo systemctl cat s1.service
sudo systemctl enable s1.service
sudo systemctl start s1.service

# to get logs from service
sudo systemctl status s1.service -l --no-pager
sudo journalctl -u s1.service -l --no-pager|less
sudo journalctl -f -u s1.service

# to stop service
sudo systemctl stop s1.service
sudo systemctl disable s1.service
#######################################################################################
# to start service
sudo systemctl daemon-reload
sudo systemctl cat s2.service
sudo systemctl enable s2.service
sudo systemctl start s2.service

# to get logs from service
sudo systemctl status s2.service -l --no-pager
sudo journalctl -u s2.service -l --no-pager|less
sudo journalctl -f -u s2.service

# to stop service
sudo systemctl stop s2.service
sudo systemctl disable s2.service
#######################################################################################
# to start service
sudo systemctl daemon-reload
sudo systemctl cat s3.service
sudo systemctl enable s3.service
sudo systemctl start s3.service

# to get logs from service
sudo systemctl status s3.service -l --no-pager
sudo journalctl -u s3.service -l --no-pager|less
sudo journalctl -f -u s3.service

# to stop service
sudo systemctl stop s3.service
sudo systemctl disable s3.service
#######################################################################################
systemctl start s1.service
systemctl start s2.service
systemctl start s3.service

systemctl stop s1.service
systemctl stop s2.service
systemctl stop s3.service
```

# 检查状态

```sh
ETCD_VER=v3.3.8

# choose either URL
GOOGLE_URL=https://storage.googleapis.com/etcd
GITHUB_URL=https://github.com/coreos/etcd/releases/download
DOWNLOAD_URL=${GOOGLE_URL}

rm -f /data/etcd-${ETCD_VER}-linux-amd64.tar.gz
rm -rf /data/test-etcd && mkdir -p /data/test-etcd

curl -L ${DOWNLOAD_URL}/${ETCD_VER}/etcd-${ETCD_VER}-linux-amd64.tar.gz -o /data/etcd-${ETCD_VER}-linux-amd64.tar.gz
tar xzvf /data/etcd-${ETCD_VER}-linux-amd64.tar.gz -C /data/test-etcd --strip-components=1

# sudo cp /data/test-etcd/etcd* [YOUR_EXEC_DIR]
# sudo mkdir -p /usr/local/bin/ && sudo cp /data/test-etcd/etcd* /usr/local/bin/

/data/test-etcd/etcd --version
ETCDCTL_API=3 /data/test-etcd/etcdctl version



ETCDCTL_API=3 /data/test-etcd/etcdctl \
  --endpoints localhost:2379,localhost:3379,localhost:4379 \
  endpoint health
```

或者用容器去检查状态

```sh
# to use 'docker' command to check the status
/usr/bin/docker \
  exec \
  etcd-v3.3.8-1 \
  /bin/sh -c "export ETCDCTL_API=3 && /usr/local/bin/etcdctl --endpoints localhost:2379,localhost:3379,localhost:4379 endpoint health"
```





# yum 安装和使用


ETCD 是一个高可用的分布式 key-value 存储系统，常用于服务发现、配置管理等场景。以下是在 YUM 安装 ETCD 后的常用运维命令：

1. 启动 ETCD

```
systemctl start etcd
```

2. 停止 ETCD

```
systemctl stop etcd
```

3. 重启 ETCD

```
systemctl restart etcd
```

4. 查看 ETCD 运行状态

```
systemctl status etcd
```

5. 查看 ETCD 集群状态

```
etcdctl cluster-health
```

6. 查看 ETCD 中存储的所有键值对

```
etcdctl ls /
```

7. 查看 ETCD 中指定键的值

```
etcdctl get key
```

8. 设置 ETCD 中指定键的值

```
etcdctl set key value
```

9. 删除 ETCD 中指定键值对

```
etcdctl del key
```

10. 备份 ETCD 数据

```
ETCDCTL_API=3 etcdctl snapshot save /path/to/snapshot.db
```

以上是常用的 ETCD 运维命令，可以通过这些命令来管理 ETCD 集群，并进行数据的读写、备份等操作。
