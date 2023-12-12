- [查看 kubesphere 所有 pod,svc](#查看-kubesphere-所有-podsvc)
- [重要的组件](#重要的组件)
  - [kube-apiserver-master](#kube-apiserver-master)
  - [kube-proxy](#kube-proxy)
  - [kube-scheduler-master](#kube-scheduler-master)
  - [coredns](#coredns)
  - [etcd](#etcd)
- [](#)

# 查看 kubesphere 所有 pod,svc
```yaml
kubectl get pod,svc --all-namespaces
NAMESPACE                      NAME                                                     READY   STATUS      RESTARTS          AGE
kube-system                    pod/calico-kube-controllers-846ddd49bc-l4bk8             1/1     Running     81 (6h31m ago)    2d2h
kube-system                    pod/calico-node-9kwnt                                    1/1     Running     0                 2d2h
kube-system                    pod/calico-node-b7cfc                                    1/1     Running     0                 2d2h
kube-system                    pod/calico-node-k9b4l                                    1/1     Running     0                 2d2h
kube-system                    pod/coredns-558b97598-ftshh                              1/1     Running     0                 2d2h
kube-system                    pod/coredns-558b97598-skm9d                              1/1     Running     0                 2d2h
kube-system                    pod/init-pvc-343a1014-ca24-4f3e-a207-0691cfbd5447        0/1     Completed   0                 2d1h
kube-system                    pod/init-pvc-8eb7d510-194b-42b8-9527-c6cca638146c        0/1     Completed   0                 2d1h
kube-system                    pod/kube-apiserver-master01                              1/1     Running     19 (20h ago)      2d2h
kube-system                    pod/kube-apiserver-master02                              1/1     Running     15                2d2h
kube-system                    pod/kube-apiserver-master03                              1/1     Running     19 (20h ago)      2d2h
kube-system                    pod/kube-controller-manager-master01                     1/1     Running     194 (38m ago)     2d2h
kube-system                    pod/kube-controller-manager-master02                     1/1     Running     197 (6h31m ago)   2d2h
kube-system                    pod/kube-controller-manager-master03                     1/1     Running     190 (49m ago)     2d2h
kube-system                    pod/kube-proxy-49dfn                                     1/1     Running     0                 2d2h
kube-system                    pod/kube-proxy-hbk4j                                     1/1     Running     0                 2d2h
kube-system                    pod/kube-proxy-kgnmm                                     1/1     Running     0                 2d2h
kube-system                    pod/kube-scheduler-master01                              1/1     Running     183 (38m ago)     2d2h
kube-system                    pod/kube-scheduler-master02                              1/1     Running     187 (49m ago)     2d2h
kube-system                    pod/kube-scheduler-master03                              1/1     Running     186 (6h31m ago)   2d2h
kube-system                    pod/nodelocaldns-clf97                                   1/1     Running     0                 2d2h
kube-system                    pod/nodelocaldns-g27d9                                   1/1     Running     0                 2d2h
kube-system                    pod/nodelocaldns-wm24c                                   1/1     Running     0                 2d2h
kube-system                    pod/openebs-localpv-provisioner-6f54869bc7-dng9l         1/1     Running     239 (38m ago)     2d2h
kube-system                    pod/snapshot-controller-0                                1/1     Running     0                 2d1h
kubesphere-controls-system     pod/default-http-backend-59d5cf569f-9dvkk                1/1     Running     0                 2d1h
kubesphere-controls-system     pod/kubectl-admin-7ffdf4596b-dhddf                       1/1     Running     0                 2d1h
kubesphere-controls-system     pod/kubesphere-router-lindeci-project-75f5dc9ccd-9vt9q   1/1     Running     0                 2d1h
kubesphere-controls-system     pod/kubesphere-router-lindeci-project-75f5dc9ccd-b2rll   1/1     Running     0                 2d1h
kubesphere-controls-system     pod/kubesphere-router-lindeci-project-75f5dc9ccd-m9r7n   1/1     Running     0                 2d1h
kubesphere-monitoring-system   pod/alertmanager-main-0                                  2/2     Running     0                 2d1h
kubesphere-monitoring-system   pod/alertmanager-main-1                                  2/2     Running     0                 2d1h
kubesphere-monitoring-system   pod/alertmanager-main-2                                  2/2     Running     0                 2d1h
kubesphere-monitoring-system   pod/kube-state-metrics-5474f8f7b-s4tx5                   3/3     Running     0                 2d1h
kubesphere-monitoring-system   pod/node-exporter-9fgg4                                  2/2     Running     0                 2d1h
kubesphere-monitoring-system   pod/node-exporter-t6qcm                                  2/2     Running     0                 2d1h
kubesphere-monitoring-system   pod/node-exporter-zfmlc                                  2/2     Running     0                 2d1h
kubesphere-monitoring-system   pod/notification-manager-deployment-7b586bd8fb-mx4w5     2/2     Running     0                 2d1h
kubesphere-monitoring-system   pod/notification-manager-deployment-7b586bd8fb-w5hss     2/2     Running     0                 2d1h
kubesphere-monitoring-system   pod/notification-manager-operator-64ff97cb98-rwrlz       2/2     Running     254 (49m ago)     2d1h
kubesphere-monitoring-system   pod/prometheus-k8s-0                                     0/2     Pending     0                 2d1h
kubesphere-monitoring-system   pod/prometheus-k8s-1                                     0/2     Pending     0                 2d1h
kubesphere-monitoring-system   pod/prometheus-operator-64b7b4db85-t8zdm                 2/2     Running     0                 2d1h
kubesphere-system              pod/ks-apiserver-848bfd75fd-9gntm                        1/1     Running     0                 2d1h
kubesphere-system              pod/ks-apiserver-848bfd75fd-cmwz6                        1/1     Running     0                 2d1h
kubesphere-system              pod/ks-apiserver-848bfd75fd-kb6xk                        1/1     Running     0                 2d1h
kubesphere-system              pod/ks-console-868887c49f-kdmhz                          1/1     Running     0                 2d1h
kubesphere-system              pod/ks-console-868887c49f-nmxbq                          1/1     Running     0                 2d1h
kubesphere-system              pod/ks-console-868887c49f-xxbkb                          1/1     Running     0                 2d1h
kubesphere-system              pod/ks-controller-manager-67b896bb6d-5xgrd               1/1     Running     127 (6h31m ago)   2d1h
kubesphere-system              pod/ks-controller-manager-67b896bb6d-8z9vf               1/1     Running     129 (49m ago)     2d1h
kubesphere-system              pod/ks-controller-manager-67b896bb6d-gmgkh               1/1     Running     122 (6h38m ago)   2d1h
kubesphere-system              pod/ks-installer-5655f896fb-k449k                        1/1     Running     0                 2d2h
kubesphere-system              pod/minio-6cf4f56956-8lvkq                               1/1     Running     0                 2d1h
kubesphere-system              pod/openpitrix-import-job-76p9z                          0/1     Completed   0                 2d1h
kubesphere-system              pod/redis-7cc8746478-kgzrw                               1/1     Running     0                 2d1h
lindeci-project                pod/elasticsearch-master-0                               1/1     Running     0                 6h18m
lindeci-project                pod/elasticsearch-master-1                               1/1     Running     0                 6h18m
lindeci-project                pod/elasticsearch-master-2                               1/1     Running     0                 6h18m
lindeci-project                pod/ldc-app-hello-deployment-0                           1/1     Running     0                 26h
lindeci-project                pod/ldc-app-hello-deployment-1                           1/1     Running     0                 26h
lindeci-project                pod/ldc-app-hello-deployment-2                           1/1     Running     0                 26h

NAMESPACE                      NAME                                                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                         AGE
default                        service/kubernetes                                  ClusterIP   10.233.0.1      <none>        443/TCP                         2d2h
kube-system                    service/coredns                                     ClusterIP   10.233.0.3      <none>        53/UDP,53/TCP,9153/TCP          2d2h
kube-system                    service/kube-controller-manager-svc                 ClusterIP   None            <none>        10257/TCP                       2d1h
kube-system                    service/kube-scheduler-svc                          ClusterIP   None            <none>        10259/TCP                       2d1h
kube-system                    service/kubelet                                     ClusterIP   None            <none>        10250/TCP,10255/TCP,4194/TCP    2d1h
kubesphere-controls-system     service/default-http-backend                        ClusterIP   10.233.48.105   <none>        80/TCP                          2d1h
kubesphere-controls-system     service/kubesphere-router-lindeci-project           NodePort    10.233.44.158   <none>        80:30291/TCP,443:31552/TCP      2d1h
kubesphere-controls-system     service/kubesphere-router-lindeci-project-metrics   ClusterIP   10.233.53.221   <none>        10254/TCP                       2d1h
kubesphere-monitoring-system   service/alertmanager-main                           ClusterIP   10.233.50.249   <none>        9093/TCP,8080/TCP               2d1h
kubesphere-monitoring-system   service/alertmanager-operated                       ClusterIP   None            <none>        9093/TCP,9094/TCP,9094/UDP      2d1h
kubesphere-monitoring-system   service/kube-state-metrics                          ClusterIP   None            <none>        8443/TCP,9443/TCP               2d1h
kubesphere-monitoring-system   service/node-exporter                               ClusterIP   None            <none>        9100/TCP                        2d1h
kubesphere-monitoring-system   service/notification-manager-controller-metrics     ClusterIP   10.233.44.184   <none>        8443/TCP                        2d1h
kubesphere-monitoring-system   service/notification-manager-svc                    ClusterIP   10.233.62.83    <none>        19093/TCP                       2d1h
kubesphere-monitoring-system   service/notification-manager-webhook                ClusterIP   10.233.16.44    <none>        443/TCP                         2d1h
kubesphere-monitoring-system   service/prometheus-k8s                              ClusterIP   10.233.32.4     <none>        9090/TCP,8080/TCP               2d1h
kubesphere-monitoring-system   service/prometheus-operated                         ClusterIP   None            <none>        9090/TCP                        2d1h
kubesphere-monitoring-system   service/prometheus-operator                         ClusterIP   None            <none>        8443/TCP                        2d1h
kubesphere-system              service/ks-apiserver                                ClusterIP   10.233.28.177   <none>        80/TCP                          2d1h
kubesphere-system              service/ks-console                                  NodePort    10.233.45.148   <none>        80:30880/TCP                    2d1h
kubesphere-system              service/ks-controller-manager                       ClusterIP   10.233.20.161   <none>        443/TCP                         2d1h
kubesphere-system              service/minio                                       ClusterIP   10.233.38.71    <none>        9000/TCP                        2d1h
kubesphere-system              service/redis                                       ClusterIP   10.233.25.87    <none>        6379/TCP                        2d1h
lindeci-project                service/elasticsearch-master                        NodePort    10.233.11.112   <none>        9200:32435/TCP,9300:31777/TCP   6h18m
lindeci-project                service/elasticsearch-master-headless               ClusterIP   None            <none>        9200/TCP,9300/TCP               6h18m
lindeci-project                service/ldc-app-hello                               ClusterIP   None            <none>        8000/TCP                        26h
```

# 重要的组件
## kube-apiserver-master
## kube-proxy
## kube-scheduler-master
## coredns
## etcd
默认是直接安装到宿主机
```sh
whereis etcd
etcd: /etc/etcd.env /usr/local/bin/etcd
```
`cat /etc/etcd.env`
```sh
# Environment file for etcd v3.4.13
ETCD_DATA_DIR=/var/lib/etcd
ETCD_ADVERTISE_CLIENT_URLS=https://172.1.1.198:2379
ETCD_INITIAL_ADVERTISE_PEER_URLS=https://172.1.1.198:2380
ETCD_INITIAL_CLUSTER_STATE=existing
ETCD_METRICS=basic
ETCD_LISTEN_CLIENT_URLS=https://172.1.1.198:2379,https://127.0.0.1:2379
ETCD_ELECTION_TIMEOUT=5000
ETCD_HEARTBEAT_INTERVAL=250
ETCD_INITIAL_CLUSTER_TOKEN=k8s_etcd
ETCD_LISTEN_PEER_URLS=https://172.1.1.198:2380
ETCD_NAME=etcd-master03
ETCD_PROXY=off
ETCD_ENABLE_V2=true
ETCD_INITIAL_CLUSTER=etcd-master01=https://172.1.1.196:2380,etcd-master02=https://172.1.1.197:2380,etcd-master03=https://172.1.1.198:2380
ETCD_AUTO_COMPACTION_RETENTION=8
ETCD_SNAPSHOT_COUNT=10000

# TLS settings
ETCD_TRUSTED_CA_FILE=/etc/ssl/etcd/ssl/ca.pem
ETCD_CERT_FILE=/etc/ssl/etcd/ssl/member-master03.pem
ETCD_KEY_FILE=/etc/ssl/etcd/ssl/member-master03-key.pem
ETCD_CLIENT_CERT_AUTH=true

ETCD_PEER_TRUSTED_CA_FILE=/etc/ssl/etcd/ssl/ca.pem
ETCD_PEER_CERT_FILE=/etc/ssl/etcd/ssl/member-master03.pem
ETCD_PEER_KEY_FILE=/etc/ssl/etcd/ssl/member-master03-key.pem
ETCD_PEER_CLIENT_CERT_AUTH=True

# CLI settings
ETCDCTL_ENDPOINTS=https://127.0.0.1:2379
ETCDCTL_CA_FILE=/etc/ssl/etcd/ssl/ca.pem
ETCDCTL_KEY_FILE=/etc/ssl/etcd/ssl/admin-master03-key.pem
ETCDCTL_CERT_FILE=/etc/ssl/etcd/ssl/admin-master03.pem
```

# 