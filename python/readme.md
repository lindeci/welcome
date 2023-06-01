```sh
pip3 uninstall numpy
pip3 uninstall scipy
pip3 uninstall matplotlib

pip3 install numpy --no-warn-script-location
pip3 install scipy
pip3 install matplotlib --no-warn-script-location
```

# 离线安装pip、etcd、elasticsearch依赖包

```shell

yum install python36
yum install python-pip
# 下载pip
python3 -m pip download --dest /tmp/pip_deps pip --index-url https://mirrors.aliyun.com/pypi/simple/ 

# 下载 etcd 依赖包
python3 -m pip install --upgrade pip
yum install -y gcc gcc-c++ mpfr-devel libmpc-devel glibc-devel glibc-headers kernel-devel
python3 -m pip download --dest /tmp/etcd_deps etcd3 --index-url https://mirrors.aliyun.com/pypi/simple/

# 下载 elasticsearch 依赖包
python3 -m pip download --dest /tmp/elasticsearch_deps elasticsearch==7.17.0 --index-url https://mirrors.aliyun.com/pypi/simple/
```

```sh
#在不能上外网的机器上安装依赖包
pip3 install --upgrade /data/pip_deps/pip-21.3.1-py3-none-any.whl
python3 -m pip install --no-index --find-links=/data/elasticsearch_deps elasticsearch
python3 -m pip install --no-index --find-links=/data/etcd_deps etcd3
```

# 问题

发现etcd服务端是api v2版本

```
etcdctl --version
etcdctl version: 3.3.11
API version: 2
```

需要重新安装python-etcd包

```
python3 -m pip download --dest /tmp/etcd_deps python-etcd --index-url https://mirrors.aliyun.com/pypi/simple/
```

python3 -m pip install --no-index --find-links=/data/etcd_deps python-etcd
