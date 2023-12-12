- [什么是StatefulSet](#什么是statefulset)
- [保持应用的拓扑状态](#保持应用的拓扑状态)
- [HeadlessService](#headlessservice)

# 什么是StatefulSet
在平时工作中接触到的最常用的Kubernetes控制器是Deployment，但是Deployment只适合于编排“无状态应用”，它会假设一个应用的所有 Pod是完全一样的，互相之间也没有顺序依赖，也无所谓运行在哪台宿主机上。正因为每个Pod都一样，在需要的时候可以水平扩/缩，增加和删除Pod。

和Deployment一样StatefulSet也是一种可以帮助你部署和扩展Kubernetes Pod的控制器，使用Deployment时多数时候你不会在意Pod的调度方式。但当你需要关心Pod的部署顺序、对应的持久化存储或者要求Pod拥有固定的网络标识（即使重启或者重新调度后也不会变）时，StatefulSet控制器会帮助你，完成调度目标。

每个由StatefulSet创建出来的Pod都拥有一个序号（从0开始）和一个固定的网络标识。你还可以在YAML定义中添加VolumeClaimTemplate来声明Pod存储使用的PVC。当StatefulSet部署Pod时，会从编号0到最终编号逐一部署每个Pod，只有前一个Pod部署完成并处于运行状态后，下一个Pod才会开始部署。

![Alt text](pic/StatefulSets_001.webp)

StatefulSet，是在Deployment的基础上扩展出来的控制器，在1.9版本之后才加入Kubernetes控制器家族，它把有状态应用需要保持的状态抽象分为了两种情况：

- 拓扑状态。这种情况意味着，应用的多个实例之间不是完全对等的关系。这些应用实例，必须按照某些顺序启动，比如应用的主节点 A 要先于从节点 B 启动。而如果你把 A 和 B 两个 Pod 删除掉，它们再次被创建出来时也必须严格按照这个顺序才行。并且，新创建出来的 Pod，必须和原来 Pod 的网络标识一样，这样原先的访问者才能使用同样的方法，访问到这个新 Pod。
- 存储状态。这种情况意味着，应用的多个实例分别绑定了不同的存储数据。对于这些应用实例来说，Pod A 第一次读取到的数据，和Pod A 被重新创建后再次读取到的数据，应该是同一份 。这种情况最典型的例子，就是一个数据库应用的多个存储实例。

所以，StatefulSet 的核心功能，就是通过某种方式记录这些状态，然后在 Pod 被重新创建时，能够为新 Pod 恢复这些状态。

# 保持应用的拓扑状态
想要维护应用的拓扑状态，必须保证能用固定的网络标识访问到固定的Pod实例，Kubernetes是通过Headless Service给每个Endpoint（Pod）添加固定网络标识的，所以接下来我们花些时间了解下Headless Service。

# HeadlessService
**Service**是在逻辑抽象层上定义了一组Pod，为他们提供一个统一的固定IP和访问这组Pod的负载均衡策略。
对于 ClusterIP 模式的 Service 来说，它的 A 记录的格式是:
`serviceName.namespace.svc.cluster.local`，当你访问这条 A 记录的时候，它解析到的就是该 Service 的 VIP 地址。
对于指定了 clusterIP=None 的 Headless Service来说，它的A记录的格式跟上面一样，但是访问记录后返回的是Pod的IP地址集合。Pod 也会被分配对应的 DNS A 记录，格式为：`podName.serviceName.namesapce.svc.cluster.local`

普通的Service都有ClusterIP，它其实就是一个虚拟IP，会把请求转发到该Service所代理的某一个Pod上。 

K8S 默认是不会给 Pod 创建 DNS。那怎么才能让DNS通过Service解析Pod的IP呢？所以就有了Headless Service。

`创建Headless Service跟创建普通Service时唯一的不同就是在YAML定义里指定spec:clusterIP: None，也就是不需要ClusterIP的Service。`

下面我创建一个Headless Service代理上面例子中的那两个应用Pod实例，它的YAML定义如下
```
# headless-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: app-headless-svc
spec:
  clusterIP: None # <-- Don't forget!!
  selector:
    app: go-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
```
创建Service的命令  
```
kubectl apply -f headless-service.yaml service/app-headless-svc created
```
Headless Service创建完后，我们再来看一下这个Service在DNS里对应的A记录
```sh
/app # nslookup app-headless-svc.default.svc.cluster.local
Server:     10.96.0.10
Address:    10.96.0.10:53

Name:   app-headless-svc.default.svc.cluster.local
Address: 10.1.0.38
Name:   app-headless-svc.default.svc.cluster.local
Address: 10.1.0.39
```
DNS查询会返回HeadlessService代理的两个Endpoint (Pod)对应的IP，这样客户端就能通过Headless Service拿到每个EndPoint的 IP，如果有需要可以自己在客户端做些负载均衡策略。`Headless Service还有一个重要用处`（也是使用StatefulSet时需要Headless Service的真正原因）`，它会为代理的每一个StatefulSet创建出来的Endpoint也就是Pod添加DNS域名解析，这样Pod之间就可以相互访问。`

`划重点: `
- 这个分配给Pod的DNS域名就是Pod的固定唯一网络标识，即使发生重建和调度DNS域名也不会改变。
- Deployment创建的Pod的名字是随机的，所以HeadlessService不会为Deployment创建出来的Pod单独添加域名解析。

