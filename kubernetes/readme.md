- [官网](#官网)
- [简述](#简述)
- [组件](#组件)
- [安装部署](#安装部署)
  - [安装 Kubernetes 组件](#安装-kubernetes-组件)
  - [安装 kubectl](#安装-kubectl)
  - [部署 Kubernetes Dashboard](#部署-kubernetes-dashboard)

# 官网
https://kubernetes.io/
# 简述 
Kubernetes, also known as K8s, is an open-source system for automating deployment, scaling, and management of containerized applications.
# 组件
![](pic/components-of-kubernetes.svg)

# 安装部署

Kubeadm 是 Kubernetes 官方提供的一种快速创建集群的方式。在使用 Kubeadm 部署生产环境之前，需要先确保满足以下先决条件：

    至少拥有三个节点，每个节点必须具备 2 个 CPU、2 GB 内存和 20 GB 的可用磁盘空间；
    操作系统为 Ubuntu 16.04+、Debian 9+、CentOS 7+ 或 RHEL 7+；
    安装并配置好 Docker；
    所有节点之间的网络连通性。
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