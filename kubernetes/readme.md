- [官网](#官网)
- [简述](#简述)
- [组件](#组件)
- [安装部署](#安装部署)
  - [选择容器运行时](#选择容器运行时)
    - [Step 1: Installing containerd](#step-1-installing-containerd)
    - [Step 2: Installing runc](#step-2-installing-runc)
    - [Step 3: Installing CNI plugins](#step-3-installing-cni-plugins)
    - [Interacting with containerd via CLI](#interacting-with-containerd-via-cli)
    - [Customizing containerd](#customizing-containerd)
    - [配置 systemd cgroup 驱动](#配置-systemd-cgroup-驱动)
  - [安装和配置先决条件](#安装和配置先决条件)
    - [转发 IPv4 并让 iptables 看到桥接流量](#转发-ipv4-并让-iptables-看到桥接流量)
  - [cgroup 驱动](#cgroup-驱动)
  - [为 kube-apiserver 创建负载均衡器](#为-kube-apiserver-创建负载均衡器)
    - [部署 keepalived](#部署-keepalived)
    - [部署 haproxy](#部署-haproxy)
    - [启动服务并配置开机自启](#启动服务并配置开机自启)
  - [使用 kubeadm 引导集群](#使用-kubeadm-引导集群)
    - [安装 kubeadm](#安装-kubeadm)
    - [安装 kubeadm、kubelet 和 kubectl](#安装-kubeadmkubelet-和-kubectl)
  - [安装网络插件](#安装网络插件)
    - [如何实现 Kubernetes 的网络模型](#如何实现-kubernetes-的网络模型)
    - [联网和网络策略](#联网和网络策略)
    - [选择Flannel](#选择flannel)
  - [安装 Kubernetes 组件](#安装-kubernetes-组件)
  - [安装 kubectl](#安装-kubectl)
  - [部署 Kubernetes Dashboard](#部署-kubernetes-dashboard)

# 官网

https://kubernetes.io/

# 简述

Kubernetes, also known as K8s, is an open-source system for automating deployment, scaling, and management of containerized applications.

# 组件

![](pic/components-of-kubernetes.svg)

刚安装好后的容器运行时
```sh
CONTAINER           IMAGE               CREATED             STATE               NAME                      ATTEMPT             POD ID              POD
89318ae58b31d       f6f496300a2ae       2 hours ago         Running             kube-scheduler            1                   769f36a2b3b5e       kube-scheduler-node
d4bfd964df0c5       4be79c38a4bab       2 hours ago         Running             kube-controller-manager   1                   6904055ad1fd9       kube-controller-manager-node
be9cacad0b995       ea1030da44aa1       2 hours ago         Running             kube-proxy                0                   dbf4fc93d67f3       kube-proxy-ncf5t
f70b0357f3066       bb5e0dde9054c       2 hours ago         Running             kube-apiserver            0                   d60cbe5d5c2b7       kube-apiserver-node
7f8671f52b936       73deb9a3f7025       2 hours ago         Running             etcd                      0                   a07f2ffc53097       etcd-node
```

# 安装部署

Kubeadm 是 Kubernetes 官方提供的一种快速创建集群的方式。在使用 Kubeadm 部署生产环境之前，需要先确保满足以下先决条件：

- 至少拥有三个节点，每个节点必须具备 2 个 CPU、2 GB 内存和 20 GB 的可用磁盘空间；
- 操作系统为 Ubuntu 16.04+、Debian 9+、CentOS 7+ 或 RHEL 7+；
- 安装并配置好 Docker；
- 所有节点之间的网络连通性。

## 选择容器运行时

现在流行containerd
参考：https://kubernetes.io/zh-cn/docs/setup/production-environment/container-runtimes/#containerd
参考：https://github.com/containerd/containerd/blob/main/docs/getting-started.md

### Step 1: Installing containerd

```sh
wget https://github.com/containerd/containerd/releases/download/v1.6.23/containerd-1.6.23-linux-amd64.tar.gz

tar xvf containerd-1.6.23-linux-amd64.tar.gz -C /data/containerd-1.6.23

export PATH=/data/containerd-1.6.23/bin:$PATH

wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service
# 注意修改下面的内容
# 把 ExecStart=/usr/local/bin/containerd 改为 ExecStart=/data/containerd-1.6.23/bin/containerd
cp containerd.service /etc/systemd/system/containerd.service
systemctl daemon-reload
systemctl enable --now containerd
```

### Step 2: Installing runc

```sh
wget https://github.com/opencontainers/runc/releases/download/v1.1.9/runc.amd64
install -m 755 runc.amd64 /usr/local/sbin/runc
```

### Step 3: Installing CNI plugins

```sh
wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz

mkdir -p /opt/cni/bin
tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.3.0.tgz
```

### Interacting with containerd via CLI

| Name        | Community             | API    | Target             | Web site                                                                                                                                        |
| ----------- | --------------------- | ------ | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `ctr`     | containerd            | Native | For debugging only | (None, see `ctr --help` to learn the usage)                                                                                                   |
| `nerdctl` | containerd (non-core) | Native | General-purpose    | [https://github.com/containerd/nerdctl](https://github.com/containerd/nerdctl)                                                                     |
| `crictl`  | Kubernetes SIG-node   | CRI    | For debugging only | [https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md](https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md) |

### Customizing containerd

```
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml

sudo systemctl restart containerd
```

### 配置 systemd cgroup 驱动

结合 runc 使用 systemd cgroup 驱动，在 /etc/containerd/config.toml 中设置：

```toml
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  ...
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
```

如果你应用此更改，请确保重新启动 containerd：

```sh
sudo systemctl restart containerd
```

## 安装和配置先决条件
### 转发 IPv4 并让 iptables 看到桥接流量
```sh
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# 设置所需的 sysctl 参数，参数在重新启动后保持不变
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# 应用 sysctl 参数而不重新启动
sudo sysctl --system
```
通过运行以下指令确认 br_netfilter 和 overlay 模块被加载：
```sh
lsmod | grep br_netfilter
lsmod | grep overlay
```
通过运行以下指令确认 net.bridge.bridge-nf-call-iptables、net.bridge.bridge-nf-call-ip6tables 和 net.ipv4.ip_forward 系统变量在你的 sysctl 配置中被设置为 1：
```sh
sysctl net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables net.ipv4.ip_forward
```
## cgroup 驱动
在 Linux 上，控制组（CGroup）用于限制分配给进程的资源。

可用的 cgroup 驱动有两个：
1. cgroupfs
2. systemd

cgroupfs 驱动是 kubelet 中默认的 cgroup 驱动。   
当 systemd 是初始化系统时， 不 推荐使用 cgroupfs 驱动，因为 systemd 期望系统上只有一个 cgroup 管理器。
```sh
#怎么判断 systemd 是不是初始化系统时
ps --no-headers -o comm 1
# 如果输出结果为 systemd，则表示您的系统使用 systemd 作为初始化系统。
```

## 为 kube-apiserver 创建负载均衡器
选择 keepalived and haproxy
### 部署 keepalived
```sh
yum install keepalived  haproxy -y
# 配置 keepalived
! /etc/keepalived/keepalived.conf
! Configuration File for keepalived
global_defs {
    router_id LVS_DEVEL
}
vrrp_script check_apiserver {
  script "/etc/keepalived/check_apiserver.sh"
  interval 3
  weight -2
  fall 10
  rise 2
}

vrrp_instance VI_1 {
    state ${STATE}
    interface ${INTERFACE}
    virtual_router_id ${ROUTER_ID}
    priority ${PRIORITY}
    authentication {
        auth_type PASS
        auth_pass ${AUTH_PASS}
    }
    virtual_ipaddress {
        ${APISERVER_VIP}
    }
    track_script {
        check_apiserver
    }
}
```
- ${STATE} is MASTER for one and BACKUP for all other hosts, hence the virtual IP will initially be assigned to the MASTER.
- ${INTERFACE} is the network interface taking part in the negotiation of the virtual IP, e.g. eth0.
- ${ROUTER_ID} should be the same for all keepalived cluster hosts while unique amongst all clusters in the same subnet. Many distros pre-configure its value to 51.
- ${PRIORITY} should be higher on the control plane node than on the backups. Hence 101 and 100 respectively will suffice.
- ${AUTH_PASS} should be the same for all keepalived cluster hosts, e.g. 42
- ${APISERVER_VIP} is the virtual IP address negotiated between the keepalived cluster hosts.

配置keeplived健康检查脚本
```sh
vi /etc/keepalived/check_apiserver.sh

#!/bin/sh

errorExit() {
    echo "*** $*" 1>&2
    exit 1
}

APISERVER_VIP=172.1.1.201
APISERVER_DEST_PORT=8443

curl --silent --max-time 2 --insecure https://localhost:${APISERVER_DEST_PORT}/ -o /dev/null || errorExit "Error GET https://localhost:${APISERVER_DEST_PORT}/"
if ip addr | grep -q ${APISERVER_VIP}; then
    curl --silent --max-time 2 --insecure https://${APISERVER_VIP}:${APISERVER_DEST_PORT}/ -o /dev/null || errorExit "Error GET https://${APISERVER_VIP}:${APISERVER_DEST_PORT}/"
fi
```
### 部署 haproxy
```sh
#修改主机名
hostnamectl set-hostname k8s-master1
hostnamectl set-hostname k8s-master2
hostnamectl set-hostname k8s-master3
#修改hosts文件
172.1.1.196 k8s-master1
172.1.1.197 k8s-master2
172.1.1.198 k8s-master3
172.1.1.201 k8svip
```
配置 haproxy
```sh
# /etc/haproxy/haproxy.cfg
#---------------------------------------------------------------------
# Global settings
#---------------------------------------------------------------------
global
    log /dev/log local0
    log /dev/log local1 notice
    daemon

#---------------------------------------------------------------------
# common defaults that all the 'listen' and 'backend' sections will
# use if not designated in their block
#---------------------------------------------------------------------
defaults
    mode                    http
    log                     global
    option                  httplog
    option                  dontlognull
    option http-server-close
    option forwardfor       except 127.0.0.0/8
    option                  redispatch
    retries                 1
    timeout http-request    10s
    timeout queue           20s
    timeout connect         5s
    timeout client          20s
    timeout server          20s
    timeout http-keep-alive 10s
    timeout check           10s

#---------------------------------------------------------------------
# apiserver frontend which proxys to the control plane nodes
#---------------------------------------------------------------------
frontend apiserver
    bind *:8443
    mode tcp
    option tcplog
    default_backend apiserver

#---------------------------------------------------------------------
# round robin balancing for apiserver
#---------------------------------------------------------------------
backend apiserver
    option httpchk GET /healthz
    http-check expect status 200
    mode tcp
    option ssl-hello-chk
    balance     roundrobin
        server k8s-master1 172.1.1.196:6443 check
        server k8s-master2 172.1.1.197:6443 check
        server k8s-master3 172.1.1.198:6443 check
```
### 启动服务并配置开机自启
```sh
systemctl enable haproxy --now
systemctl enable keepalived --now
```

## 使用 kubeadm 引导集群
### 安装 kubeadm
### 安装 kubeadm、kubelet 和 kubectl
无包管理器的情况

安装 CNI 插件（大多数 Pod 网络都需要）：
```sh
CNI_PLUGINS_VERSION="v1.3.0"
ARCH="amd64"
DEST="/opt/cni/bin"
sudo mkdir -p "$DEST"
curl -L "https://github.com/containernetworking/plugins/releases/download/${CNI_PLUGINS_VERSION}/cni-plugins-linux-${ARCH}-${CNI_PLUGINS_VERSION}.tgz" | sudo tar -C "$DEST" -xz
```
```sh
DOWNLOAD_DIR="/usr/local/bin"
sudo mkdir -p "$DOWNLOAD_DIR"
```
安装 crictl（kubeadm/kubelet 容器运行时接口（CRI）所需）
```sh
CRICTL_VERSION="v1.27.0"
ARCH="amd64"
curl -L "https://github.com/kubernetes-sigs/cri-tools/releases/download/${CRICTL_VERSION}/crictl-${CRICTL_VERSION}-linux-${ARCH}.tar.gz" | sudo tar -C $DOWNLOAD_DIR -xz
```
安装 kubeadm、kubelet、kubectl 并添加 kubelet 系统服务：
```sh
RELEASE="$(curl -sSL https://dl.k8s.io/release/stable.txt)"
ARCH="amd64"
cd $DOWNLOAD_DIR
sudo curl -L --remote-name-all https://dl.k8s.io/release/${RELEASE}/bin/linux/${ARCH}/{kubeadm,kubelet}
sudo chmod +x {kubeadm,kubelet}

RELEASE_VERSION="v0.15.1"
curl -sSL "https://raw.githubusercontent.com/kubernetes/release/${RELEASE_VERSION}/cmd/kubepkg/templates/latest/deb/kubelet/lib/systemd/system/kubelet.service" | sed "s:/usr/bin:${DOWNLOAD_DIR}:g" | sudo tee /etc/systemd/system/kubelet.service
sudo mkdir -p /etc/systemd/system/kubelet.service.d
curl -sSL "https://raw.githubusercontent.com/kubernetes/release/${RELEASE_VERSION}/cmd/kubepkg/templates/latest/deb/kubeadm/10-kubeadm.conf" | sed "s:/usr/bin:${DOWNLOAD_DIR}:g" | sudo tee /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
```
激活并启动 kubelet
```sh
systemctl enable --now kubelet
```

## 安装网络插件
Kubernetes 定义了一种简单、一致的网络模型，基于扁平网络结构的设计，无需将主机端口与网络端口进行映射便可以进行高效地通讯，也无需其他组件进行转发。该模型也使应用程序很容易从虚拟机或者主机物理机迁移到 Kubernetes 管理的 pod 中。

集群网络系统是 Kubernetes 的核心部分，但是想要准确了解它的工作原理可是个不小的挑战。
下面列出的是网络系统的的四个主要问题：

1. 高度耦合的容器间通信：这个已经被[Pod](https://kubernetes.io/zh-cn/docs/concepts/workloads/pods/)
   和`localhost` 通信解决了。
2. Pod 间通信：这是本文档讲述的重点。
3. Pod 与 Service 间通信：涵盖在[Service](https://kubernetes.io/zh-cn/docs/concepts/services-networking/service/) 中。
4. 外部与 Service 间通信：也涵盖在 Service 中。
### 如何实现 Kubernetes 的网络模型
网络模型由每个节点上的容器运行时实现。最常见的容器运行时使用 Container Network Interface (CNI) 插件来管理其网络和安全功能。 

### 联网和网络策略
https://kubernetes.io/zh-cn/docs/concepts/cluster-administration/addons/#networking-and-network-policy

### 选择Flannel
```sh
wget https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```


## 安装 Kubernetes 组件

[官网链接](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl)
在所有节点上安装 Kubernetes 组件，包括 kubeadm、kubelet 和 kubectl。可以使用以下命令：

## 安装 kubectl

```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

## 部署 Kubernetes Dashboard

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.4.0/aio/deploy/recommended.yaml
```
