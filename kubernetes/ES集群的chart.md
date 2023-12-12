- [chart 配置](#chart-配置)
- [对应的 \_help.tpl](#对应的-_helptpl)
- [Configuration](#configuration)
- [docker 安装 Elasticsearch](#docker-安装-elasticsearch)

# chart 配置
```yaml
# Source: elasticsearch/templates/poddisruptionbudget.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: "elasticsearch-master-pdb"  # 为PodDisruptionBudget资源指定名称
spec:
  maxUnavailable: 1  # 允许的最大不可用Pod数量为1
  selector:
    matchLabels:
      app: "elasticsearch-master"  # 选择带有app标签为elasticsearch-master的Pod
---
# Source: elasticsearch/templates/service.yaml
kind: Service
apiVersion: v1
metadata:
  name: elasticsearch-master  # Elasticsearch服务的名称
  labels:
    heritage: "Helm"  # 这个标签表示这个对象是由 Helm 创建的
    release: "release-name"  # 这个标签表示这个对象属于哪个 Helm release
    chart: "elasticsearch"  # 这个标签表示这个对象是由哪个 Helm chart 创建的
    app: "elasticsearch-master"  # 这个标签可以用来识别运行的应用程序
  annotations:
    {}  # 注释部分为空

spec:
  type: ClusterIP  # 服务类型为ClusterIP
  selector:
    release: "release-name"  # 选择带有release标签为release-name的Pod
    chart: "elasticsearch"  # 选择带有chart标签为elasticsearch的Pod
    app: "elasticsearch-master"  # 选择带有app标签为elasticsearch-master的Pod
  publishNotReadyAddresses: false  # 不发布未准备好的地址
  ports:
  - name: http
    protocol: TCP
    port: 9200
  - name: transport
    protocol: TCP
    port: 9300
---
# Source: elasticsearch/templates/service.yaml
kind: Service
apiVersion: v1
metadata:
  name: elasticsearch-master-headless  # Elasticsearch Headless服务的名称
  labels:
    heritage: "Helm"  # 标签heritage指定为Helm
    release: "release-name"  # 标签release指定为release-name
    chart: "elasticsearch"  # 标签chart指定为elasticsearch
    app: "elasticsearch-master"  # 标签app指定为elasticsearch-master
  annotations:
    service.alpha.kubernetes.io/tolerate-unready-endpoints: "true"  # 允许不准备好的端点

spec:
  clusterIP: None  # 集群IP设置为None，用于StatefulSet主机名的解析
  publishNotReadyAddresses: true  # 创建端点，即使相关的Pod没有准备好
  selector:
    app: "elasticsearch-master"  # 选择带有app标签为elasticsearch-master的Pod
  ports:
  - name: http
    port: 9200
  - name: transport
    port: 9300
---
# Source: elasticsearch/templates/statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch-master  # StatefulSet的名称
  labels:
    heritage: "Helm"  # 标签heritage指定为Helm
    release: "release-name"  # 标签release指定为release-name
    chart: "elasticsearch"  # 标签chart指定为elasticsearch
    app: "elasticsearch-master"  # 标签app指定为elasticsearch-master
  annotations:
    esMajorVersion: "7"  # Elasticsearch的主要版本号为7

spec:
  serviceName: elasticsearch-master-headless  # 服务名称设置为elasticsearch-master-headless
  selector:
    matchLabels:
      app: "elasticsearch-master"  # 选择带有app标签为elasticsearch-master的Pod
  replicas: 3  # 副本数量为3
  podManagementPolicy: Parallel  # Pod管理策略为Parallel
  updateStrategy:
    type: RollingUpdate  # 更新策略为RollingUpdate
  volumeClaimTemplates:
  - metadata:
      name: elasticsearch-master
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 30Gi  # 存储请求为30Gi

  template:
    metadata:
      name: "elasticsearch-master"  # Pod模板的名称
      labels:
        release: "release-name"  # 标签release指定为release-name
        chart: "elasticsearch"  # 标签chart指定为elasticsearch
        app: "elasticsearch-master"  # 标签app指定为elasticsearch-master
      annotations:
        {}  # 注释部分为空

    spec:
      securityContext:
        fsGroup: 1000  # 文件系统组设置为1000
        runAsUser: 1000  # 以用户ID 1000运行
      automountServiceAccountToken: true  # 自动挂载服务账号令牌
      affinity:  # 设置 Pod 亲和性和反亲和性
        podAntiAffinity:  # 表示我们要设置的是 Pod 的反亲和性
          requiredDuringSchedulingIgnoredDuringExecution:  # 表示 Kubernetes 在调度 Pod 时必须满足的反亲和性条件
          - labelSelector:  # 用于选择满足特定条件的标签
              matchExpressions:  # 用于定义标签选择器的匹配表达式
              - key: app  # 表示我们要匹配的标签的键是 “app”
                operator: In  # 表示我们要检查 “app” 标签的值是否在给定的列表中
                values:  # 
                - "elasticsearch-master"  # 防止同一节点上有多个elasticsearch-master Pod
            topologyKey: kubernetes.io/hostname
      terminationGracePeriodSeconds: 120  # 终止期限为120秒
      volumes:
      enableServiceLinks: true  # 启用服务链接
      initContainers:  # 初始化容器
      - name: configure-sysctl  # 容器名称：configure-sysctl
        securityContext:  # 安全上下文
          runAsUser: 0  # 以用户ID 0（root用户）运行
          privileged: true  # 具有特权
        image: "docker.elastic.co/elasticsearch/elasticsearch:7.17.1"  # 使用的镜像
        imagePullPolicy: "IfNotPresent"  # 镜像拉取策略：如果本地不存在，则拉取
        command: ["sysctl", "-w", "vm.max_map_count=262144"]  # 执行的命令：设置vm.max_map_count为262144
        resources:  # 资源限制（此处未指定具体资源限制）
          {}  # 注释部分为空

      containers:  # 容器
      - name: "elasticsearch"  # 容器名称：elasticsearch
        securityContext:  # 安全上下文
          capabilities:  # 能力
            drop:  # 放弃
            - ALL  # 所有
          runAsNonRoot: true  # 以非root用户运行
          runAsUser: 1000  # 以用户ID 1000运行
        image: "docker.elastic.co/elasticsearch/elasticsearch:7.17.1"  # 使用的镜像
        imagePullPolicy: "IfNotPresent"  # 镜像拉取策略：如果本地不存在，则拉取
        readinessProbe:  # 就绪探针（此处未指定具体探针配置）
          exec:
            command:
              - bash
              - -c
              - |
                set -e
                # If the node is starting up wait for the cluster to be ready (request params: "wait_for_status=green&timeout=1s" )
                # Once it has started only check that the node itself is responding
                START_FILE=/tmp/.es_start_file

                #
                # If the node is starting up wait for the cluster to be ready (request params: "wait_for_status=green&timeout=1s" )
                #  如果节点正在启动，请等待集群准备就绪（请求参数： "wait_for_status=green&timeout=1s" ）
                # 一旦启动，只需检查节点本身是否响应

                # Disable nss cache to avoid filling dentry cache when calling curl
                # This is required with Elasticsearch Docker using nss < 3.52
                # 禁用nss缓存以避免在调用curl时填充dentry缓存
                # 在使用nss < 3.52的Elasticsearch Docker中需要此选项
                export NSS_SDB_USE_CACHE=no

                http () {
                  local path="${1}"
                  local args="${2}"
                  set -- -XGET -s

                  if [ "$args" != "" ]; then
                    set -- "$@" $args
                  fi

                  if [ -n "${ELASTIC_PASSWORD}" ]; then
                    set -- "$@" -u "elastic:${ELASTIC_PASSWORD}"
                  fi

                  curl --output /dev/null -k "$@" "http://127.0.0.1:9200${path}"
                }

                if [ -f "${START_FILE}" ]; then
                  echo 'Elasticsearch is already running, lets check the node is healthy'
                  HTTP_CODE=$(http "/" "-w %{http_code}")
                  RC=$?
                  if [[ ${RC} -ne 0 ]]; then
                    echo "curl --output /dev/null -k -XGET -s -w '%{http_code}' \${BASIC_AUTH} http://127.0.0.1:9200/ failed with RC ${RC}"
                    exit ${RC}
                  fi
                  # ready if HTTP code 200, 503 is tolerable if ES version is 6.x
                  if [[ ${HTTP_CODE} == "200" ]]; then
                    exit 0
                  elif [[ ${HTTP_CODE} == "503" && "7" == "6" ]]; then
                    exit 0
                  else
                    echo "curl --output /dev/null -k -XGET -s -w '%{http_code}' \${BASIC_AUTH} http://127.0.0.1:9200/ failed with HTTP code ${HTTP_CODE}"
                    exit 1
                  fi

                else
                  echo 'Waiting for elasticsearch cluster to become ready (request params: "wait_for_status=green&timeout=1s" )'
                  if http "/_cluster/health?wait_for_status=green&timeout=1s" "--fail" ; then
                    touch ${START_FILE}
                    exit 0
                  else
                    echo 'Cluster is not yet ready (request params: "wait_for_status=green&timeout=1s" )'
                    exit 1
                  fi
                fi
          failureThreshold: 3  # 故障阈值为3
          initialDelaySeconds: 10  # 初始延迟秒数为10
          periodSeconds: 10  # 周期秒数为10
          successThreshold: 3  # 成功阈值为3
          timeoutSeconds: 5  # 超时秒数为5
        ports:
        - name: http
          containerPort: 9200  # 容器端口为9200
        - name: transport
          containerPort: 9300  # 容器端口为9300
        resources:
          limits:
            cpu: 1000m  # CPU限制为1000m
            memory: 2Gi  # 内存限制为2Gi
          requests:
            cpu: 1000m  # CPU请求为1000m
            memory: 2Gi  # 内存请求为2Gi
        env:
          - name: node.name
            valueFrom:
              fieldRef:
                fieldPath: metadata.name
          - name: cluster.initial_master_nodes
            value: "elasticsearch-master-0,elasticsearch-master-1,elasticsearch-master-2,"
          - name: discovery.seed_hosts
            value: "elasticsearch-master-headless"
          - name: cluster.name
            value: "elasticsearch"
          - name: network.host
            value: "0.0.0.0"
          - name: cluster.deprecation_indexing.enabled
            value: "false"
          - name: node.data
            value: "true"
          - name: node.ingest
            value: "true"
          - name: node.master
            value: "true"
          - name: node.ml
            value: "true"
          - name: node.remote_cluster_client
            value: "true"
        volumeMounts:
          - name: "elasticsearch-master"
            mountPath: /usr/share/elasticsearch/data
---
# Source: elasticsearch/templates/test/test-elasticsearch-health.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "release-name-ewlbl-test"  # 测试Pod的名称
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-delete-policy": hook-succeeded  # Helm钩子删除策略为hook-succeeded

spec:
  securityContext:
    fsGroup: 1000  # 文件系统组设置为1000
    runAsUser: 1000  # 以用户ID 1000运行
  containers:
  - name: "release-name-riqwz-test"  # 测试容器的名称
    image: "docker.elastic.co/elasticsearch/elasticsearch:7.17.1"
    imagePullPolicy: "IfNotPresent"
    command:
      - "sh"
      - "-c"
      - |
        #!/usr/bin/env bash -e
        curl -XGET --fail 'elasticsearch-master:9200/_cluster/health?wait_for_status=green&timeout=1s'
  restartPolicy: Never  # 重启策略为Never
```

# 对应的 _help.tpl
```yaml
{{/* vim: set filetype=mustache: */}}  # 设置文件类型为mustache
{{/*
Expand the name of the chart.
*/}}  # 扩展chart的名称
{{- define "elasticsearch.name" -}}  # 定义一个名为"elasticsearch.name"的模板
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}  # 如果.Values.nameOverride存在，则使用它，否则使用.Chart.Name。然后将结果截断到63个字符，并删除末尾的"-"
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}  # 创建一个默认的完全限定应用名称。我们将其截断到63个字符，因为一些Kubernetes名称字段受此限制（由DNS命名规范规定）。
{{- define "elasticsearch.fullname" -}}  # 定义一个名为"elasticsearch.fullname"的模板
{{- $name := default .Chart.Name .Values.nameOverride -}}  # 如果.Values.nameOverride存在，则使用它，否则使用.Chart.Name。将结果赋值给$name变量。
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}  # 将.Release.Name和$name变量连接起来，然后将结果截断到63个字符，并删除末尾的"-"
{{- end -}}

{{- define "elasticsearch.uname" -}}  # 定义一个名为"elasticsearch.uname"的模板
{{- if empty .Values.fullnameOverride -}}  # 如果.Values.fullnameOverride为空
{{- if empty .Values.nameOverride -}}  # 如果.Values.nameOverride为空
{{ .Values.clusterName }}-{{ .Values.nodeGroup }}  # 使用.Values.clusterName和.Values.nodeGroup连接起来
{{- else -}}
{{ .Values.nameOverride }}-{{ .Values.nodeGroup }}  # 使用.Values.nameOverride和.Values.nodeGroup连接起来
{{- end -}}
{{- else -}}
{{ .Values.fullnameOverride }}  # 使用.Values.fullnameOverride
{{- end -}}
{{- end -}}
{{/*
Generate certificates when the secret doesn't exist
*/}}  # 当Secret不存在时生成证书
{{- define "elasticsearch.gen-certs" -}}  # 定义一个名为"elasticsearch.gen-certs"的模板
{{- $certs := lookup "v1" "Secret" .Release.Namespace ( printf "%s-certs" (include "elasticsearch.uname" . ) ) -}}  # 查找名为"{elasticsearch.uname}-certs"的Secret
{{- if $certs -}}  # 如果找到了Secret
tls.crt: {{ index $certs.data "tls.crt" }}  # 获取tls.crt的值
tls.key: {{ index $certs.data "tls.key" }}  # 获取tls.key的值
ca.crt: {{ index $certs.data "ca.crt" }}  # 获取ca.crt的值
{{- else -}}  # 如果没有找到Secret
{{- $altNames := list ( include "elasticsearch.masterService" . ) ( printf "%s.%s" (include "elasticsearch.masterService" .) .Release.Namespace ) ( printf "%s.%s.svc" (include "elasticsearch.masterService" .) .Release.Namespace ) -}}  # 创建一个包含master服务名称、命名空间和服务名称的列表
{{- $ca := genCA "elasticsearch-ca" 365 -}}  # 生成一个名为"elasticsearch-ca"的CA证书，有效期为365天
{{- $cert := genSignedCert ( include "elasticsearch.masterService" . ) nil $altNames 365 $ca -}}  # 使用CA证书为master服务生成一个签名证书，有效期为365天
tls.crt: {{ $cert.Cert | toString | b64enc }}  # 获取证书的公钥，并将其转换为字符串并进行Base64编码
tls.key: {{ $cert.Key | toString | b64enc }}  # 获取证书的私钥，并将其转换为字符串并进行Base64编码
ca.crt: {{ $ca.Cert | toString | b64enc }}  # 获取CA证书的公钥，并将其转换为字符串并进行Base64编码
{{- end -}}
{{- end -}}

{{- define "elasticsearch.masterService" -}}  # 定义一个名为"elasticsearch.masterService"的模板
{{- if empty .Values.masterService -}}  # 如果.Values.masterService为空
{{- if empty .Values.fullnameOverride -}}  # 如果.Values.fullnameOverride为空
{{- if empty .Values.nameOverride -}}  # 如果.Values.nameOverride为空
{{ .Values.clusterName }}-master  # 使用.Values.clusterName和"-master"连接起来
{{- else -}}
{{ .Values.nameOverride }}-master  # 使用.Values.nameOverride和"-master"连接起来
{{- end -}}
{{- else -}}
{{ .Values.fullnameOverride }}  # 使用.Values.fullnameOverride
{{- end -}}
{{- else -}}
{{ .Values.masterService }}  # 使用.Values.masterService
{{- end -}}
{{- end -}}

{{- define "elasticsearch.endpoints" -}}  # 定义一个名为"elasticsearch.endpoints"的模板
{{- $replicas := int (toString (.Values.replicas)) }}  # 将.Values.replicas转换为字符串，然后转换为整数，将结果赋值给$replicas变量
{{- $uname := (include "elasticsearch.uname" .) }}  # 引入名为"elasticsearch.uname"的模板，并传入当前的上下文（"."），将结果赋值给$uname变量
  {{- range $i, $e := untilStep 0 $replicas 1 -}}  # 对从0到$replicas的整数进行迭代，步长为1
{{ $uname }}-{{ $i }},  # 使用$uname变量和迭代变量$i连接起来，并添加一个逗号
  {{- end -}}
{{- end -}}

{{- define "elasticsearch.roles" -}}  # 定义一个名为"elasticsearch.roles"的模板
{{- range $.Values.roles -}}  # 对.Values.roles进行迭代
{{ . }},  # 输出每个角色，并添加一个逗号
{{- end -}}
{{- end -}}

{{- define "elasticsearch.esMajorVersion" -}}  # 定义一个名为"elasticsearch.esMajorVersion"的模板
{{- if .Values.esMajorVersion -}}  # 如果.Values.esMajorVersion存在
{{ .Values.esMajorVersion }}  # 输出.Values.esMajorVersion的值
{{- else -}}  # 如果.Values.esMajorVersion不存在
{{- $version := int (index (.Values.imageTag | splitList ".") 0) -}}  # 将.Values.imageTag分割成列表，取第一个元素，然后转换为整数，将结果赋值给$version变量
  {{- if and (contains "docker.elastic.co/elasticsearch/elasticsearch" .Values.image) (not (eq $version 0)) -}}  # 如果.Values.image包含"docker.elastic.co/elasticsearch/elasticsearch"，并且$version不等于0
{{ $version }}  # 输出$version的值
  {{- else -}}  # 如果上述条件不满足
8  # 输出8
  {{- end -}}
{{- end -}}
{{- end -}}

{{/*
Use the fullname if the serviceAccount value is not set
*/}}  # 如果serviceAccount值未设置，则使用fullname
{{- define "elasticsearch.serviceAccount" -}}  # 定义一个名为"elasticsearch.serviceAccount"的模板
{{- .Values.rbac.serviceAccountName | default (include "elasticsearch.uname" .) -}}  # 如果.Values.rbac.serviceAccountName存在，则使用它，否则使用名为"elasticsearch.uname"的模板的输出结果
{{- end -}}
```

# Configuration

| Parameter                            | Description                                                                                                                                                                                                                                                                                                                                      | Default                                                                                   |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| `antiAffinityTopologyKey`          | The[anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity) topology key. By default this will prevent multiple Elasticsearch nodes from running on the same Kubernetes node                                                                                                                  | `kubernetes.io/hostname`                                                                |
| `antiAffinity`                     | Setting this to hard enforces the[anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#affinity-and-anti-affinity) rules. If it is set to soft it will be done "best effort". Other values will be ignored                                                                                                             | `hard`                                                                                  |
| `clusterHealthCheckParams`         | The[Elasticsearch cluster health status params](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-health.html#request-params) that will be used by readiness [probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/) command                                                      | `wait_for_status=green&timeout=1s`                                                      |
| `clusterName`                      | This will be used as the Elasticsearch[cluster.name](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster.name.html) and should be unique per cluster in the namespace                                                                                                                                                           | `elasticsearch`                                                                         |
| `createCert`                       | This will automatically create the SSL certificates                                                                                                                                                                                                                                                                                              | `true`                                                                                  |
| `enableServiceLinks`               | Set to false to disabling service links, which can cause slow pod startup times when there are many services in the current namespace.                                                                                                                                                                                                           | `true`                                                                                  |
| `envFrom`                          | Templatable string to be passed to the[environment from variables](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#configure-all-key-value-pairs-in-a-configmap-as-container-environment-variables) which will be appended to the `envFrom:` definition for the container                                       | `[]`                                                                                    |
| `esConfig`                         | Allows you to add any config files in `/usr/share/elasticsearch/config/` such as `elasticsearch.yml` and `log4j2.properties`. See [values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) for an example of the formatting                                                                                  | `{}`                                                                                    |
| `esJavaOpts`                       | [Java options](https://www.elastic.co/guide/en/elasticsearch/reference/current/jvm-options.html) for Elasticsearch. This is where you could configure the [jvm heap size](https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html)                                                                                              | `""`                                                                                    |
| `esJvmOptions`                     | [Java options](https://www.elastic.co/guide/en/elasticsearch/reference/current/jvm-options.html) for Elasticsearch. Override the default JVM options by adding custom options files . See [values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) for an example of the formatting                                   | `{}`                                                                                    |
| `esMajorVersion`                   | Deprecated. Instead, use the version of the chart corresponding to your ES minor version. Used to set major version specific configuration. If you are using a custom image and not running the default Elasticsearch version you will need to set this to the version you are running (e.g.`esMajorVersion: 6`)                               | `""`                                                                                    |
| `extraContainers`                  | Templatable string of additional `containers` to be passed to the `tpl` function                                                                                                                                                                                                                                                             | `""`                                                                                    |
| `extraEnvs`                        | Extra[environment variables](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/#using-environment-variables-inside-of-your-config) which will be appended to the `env:` definition for the container                                                                                                 | `[]`                                                                                    |
| `extraInitContainers`              | Templatable string of additional `initContainers` to be passed to the `tpl` function                                                                                                                                                                                                                                                         | `""`                                                                                    |
| `extraVolumeMounts`                | Templatable string of additional `volumeMounts` to be passed to the `tpl` function                                                                                                                                                                                                                                                           | `""`                                                                                    |
| `extraVolumes`                     | Templatable string of additional `volumes` to be passed to the `tpl` function                                                                                                                                                                                                                                                                | `""`                                                                                    |
| `fullnameOverride`                 | Overrides the `clusterName` and `nodeGroup` when used in the naming of resources. This should only be used when using a single `nodeGroup`, otherwise you will have name conflicts                                                                                                                                                         | `""`                                                                                    |
| `healthNameOverride`               | Overrides `test-elasticsearch-health` pod name                                                                                                                                                                                                                                                                                                 | `""`                                                                                    |
| `hostAliases`                      | Configurable[hostAliases](https://kubernetes.io/docs/concepts/services-networking/add-entries-to-pod-etc-hosts-with-host-aliases/)                                                                                                                                                                                                                  | `[]`                                                                                    |
| `httpPort`                         | The http port that Kubernetes will use for the healthchecks and the service. If you change this you will also need to set[http.port](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-http.html#_settings) in `extraEnvs`                                                                                                  | `9200`                                                                                  |
| `imagePullPolicy`                  | The Kubernetes[imagePullPolicy](https://kubernetes.io/docs/concepts/containers/images/#updating-images) value                                                                                                                                                                                                                                       | `IfNotPresent`                                                                          |
| `imagePullSecrets`                 | Configuration for[imagePullSecrets](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-pod-that-uses-your-secret) so that you can use a private registry for your image                                                                                                                                 | `[]`                                                                                    |
| `imageTag`                         | The Elasticsearch Docker image tag                                                                                                                                                                                                                                                                                                               | `8.5.1`                                                                                 |
| `image`                            | The Elasticsearch Docker image                                                                                                                                                                                                                                                                                                                   | `docker.elastic.co/elasticsearch/elasticsearch`                                         |
| `ingress`                          | Configurable[ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) to expose the Elasticsearch service. See [values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) for an example                                                                                                              | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |
| `initResources`                    | Allows you to set the[resources](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/) for the `initContainer` in the StatefulSet                                                                                                                                                                                | `{}`                                                                                    |
| `keystore`                         | Allows you map Kubernetes secrets into the keystore. See the[config example](https://github.com/elastic/helm-charts/blob/main/elasticsearch/examples/config/values.yaml) and [how to use the keystore](https://github.com/elastic/helm-charts/blob/main/elasticsearch/README.md#how-to-use-the-keystore)                                               | `[]`                                                                                    |
| `labels`                           | Configurable[labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) applied to all Elasticsearch pods                                                                                                                                                                                                                   | `{}`                                                                                    |
| `lifecycle`                        | Allows you to add[lifecycle hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/). See [values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) for an example of the formatting                                                                                                          | `{}`                                                                                    |
| `masterService`                    | The service name used to connect to the masters. You only need to set this if your master `nodeGroup` is set to something other than `master`. See [Clustering and Node Discovery](https://github.com/elastic/helm-charts/blob/main/elasticsearch/README.md#clustering-and-node-discovery) for more information                                 | `""`                                                                                    |
| `maxUnavailable`                   | The[maxUnavailable](https://kubernetes.io/docs/tasks/run-application/configure-pdb/#specifying-a-poddisruptionbudget) value for the pod disruption budget. By default this will prevent Kubernetes from having more than 1 unhealthy pod in the node group                                                                                          | `1`                                                                                     |
| `minimumMasterNodes`               | The value for[discovery.zen.minimum_master_nodes](https://www.elastic.co/guide/en/elasticsearch/reference/current/discovery-settings.html#minimum_master_nodes). Should be set to `(master_eligible_nodes / 2) + 1`. Ignored in Elasticsearch versions >= 7                                                                                       | `2`                                                                                     |
| `nameOverride`                     | Overrides the `clusterName` when used in the naming of resources                                                                                                                                                                                                                                                                               | `""`                                                                                    |
| `networkHost`                      | Value for the[network.host Elasticsearch setting](https://www.elastic.co/guide/en/elasticsearch/reference/current/network.host.html)                                                                                                                                                                                                                | `0.0.0.0`                                                                               |
| `networkPolicy`                    | The[NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/) to set. See `values.yaml` for an example                                                                                                                                                                                                            | `{http.enabled: false,transport.enabled: false}`                                        |
| `nodeAffinity`                     | Value for the[node affinity settings](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#node-affinity-beta-feature)                                                                                                                                                                                                                | `{}`                                                                                    |
| `nodeGroup`                        | This is the name that will be used for each group of nodes in the cluster. The name will be `clusterName-nodeGroup-X` , `nameOverride-nodeGroup-X` if a `nameOverride` is specified, and `fullnameOverride-X` if a `fullnameOverride` is specified                                                                                     | `master`                                                                                |
| `nodeSelector`                     | Configurable[nodeSelector](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector) so that you can target specific nodes for your Elasticsearch cluster                                                                                                                                                                    | `{}`                                                                                    |
| `persistence`                      | Enables a persistent volume for Elasticsearch data. Can be disabled for nodes that only have[roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html) which don't require persistent data                                                                                                                          | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |
| `podAnnotations`                   | Configurable[annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/) applied to all Elasticsearch pods                                                                                                                                                                                                         | `{}`                                                                                    |
| `podManagementPolicy`              | By default Kubernetes[deploys StatefulSets serially](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#pod-management-policies). This deploys them in parallel so that they can discover each other                                                                                                                            | `Parallel`                                                                              |
| `podSecurityContext`               | Allows you to set the[securityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) for the pod                                                                                                                                                                                                                      | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |
| `podSecurityPolicy`                | Configuration for create a pod security policy with minimal permissions to run this Helm chart with `create: true`. Also can be used to reference an external pod security policy with `name: "externalPodSecurityPolicy"`                                                                                                                   | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |
| `priorityClassName`                | The name of the[PriorityClass](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/#priorityclass). No default is supplied as the PriorityClass must be created first                                                                                                                                                         | `""`                                                                                    |
| `protocol`                         | The protocol that will be used for the readiness[probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/). Change this to `https` if you have `xpack.security.http.ssl.enabled` set                                                                                                                | `http`                                                                                  |
| `rbac`                             | Configuration for creating a role, role binding and ServiceAccount as part of this Helm chart with `create: true`. Also can be used to reference an external ServiceAccount with `serviceAccountName: "externalServiceAccountName"`, or automount the service account token                                                                  | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |
| `readinessProbe`                   | Configuration fields for the readiness[probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/)                                                                                                                                                                                                        | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |
| `replicas`                         | Kubernetes replica count for the StatefulSet (i.e. how many pods)                                                                                                                                                                                                                                                                                | `3`                                                                                     |
| `resources`                        | Allows you to set the[resources](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/) for the StatefulSet                                                                                                                                                                                                         | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |
| `roles`                            | A list with the specific[roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html) for the `nodeGroup`                                                                                                                                                                                                            | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |
| `schedulerName`                    | Name of the[alternate scheduler](https://kubernetes.io/docs/tasks/administer-cluster/configure-multiple-schedulers/#specify-schedulers-for-pods)                                                                                                                                                                                                    | `""`                                                                                    |
| `secret.enabled`                   | Enable Secret creation for Elasticsearch credentials                                                                                                                                                                                                                                                                                             | `true`                                                                                  |
| `secret.password`                  | Initial password for the elastic user                                                                                                                                                                                                                                                                                                            | `""` (generated randomly)                                                               |
| `secretMounts`                     | Allows you easily mount a secret as a file inside the StatefulSet. Useful for mounting certificates and other secrets. See[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) for an example                                                                                                                  | `[]`                                                                                    |
| `securityContext`                  | Allows you to set the[securityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) for the container                                                                                                                                                                                                                | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |
| `service.annotations`              | [LoadBalancer annotations](https://kubernetes.io/docs/concepts/services-networking/service/#ssl-support-on-aws) that Kubernetes will use for the service. This will configure load balancer if `service.type` is `LoadBalancer`                                                                                                                 | `{}`                                                                                    |
| `service.enabled`                  | Enable non-headless service                                                                                                                                                                                                                                                                                                                      | `true`                                                                                  |
| `service.externalTrafficPolicy`    | Some cloud providers allow you to specify the[LoadBalancer externalTrafficPolicy](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#preserving-the-client-source-ip). Kubernetes will use this to preserve the client source IP. This will configure load balancer if `service.type` is `LoadBalancer` | `""`                                                                                    |
| `service.httpPortName`             | The name of the http port within the service                                                                                                                                                                                                                                                                                                     | `http`                                                                                  |
| `service.labelsHeadless`           | Labels to be added to headless service                                                                                                                                                                                                                                                                                                           | `{}`                                                                                    |
| `service.labels`                   | Labels to be added to non-headless service                                                                                                                                                                                                                                                                                                       | `{}`                                                                                    |
| `service.loadBalancerIP`           | Some cloud providers allow you to specify the[loadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) IP. If the `loadBalancerIP` field is not specified, the IP is dynamically assigned. If you specify a `loadBalancerIP` but your cloud provider does not support the feature, it is ignored.           | `""`                                                                                    |
| `service.loadBalancerSourceRanges` | The IP ranges that are allowed to access                                                                                                                                                                                                                                                                                                         | `[]`                                                                                    |
| `service.nodePort`                 | Custom[nodePort](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport) port that can be set if you are using `service.type: nodePort`                                                                                                                                                                                        | `""`                                                                                    |
| `service.transportPortName`        | The name of the transport port within the service                                                                                                                                                                                                                                                                                                | `transport`                                                                             |
| `service.publishNotReadyAddresses` | Consider that all endpoints are considered "ready" even if the Pods themselves are not                                                                                                                                                                                                                                                           | `false`                                                                                 |
| `service.type`                     | Elasticsearch[Service Types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)                                                                                                                                                                                                                    | `ClusterIP`                                                                             |
| `sysctlInitContainer`              | Allows you to disable the `sysctlInitContainer` if you are setting [sysctl vm.max_map_count](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html#vm-max-map-count) with another method                                                                                                                          | `enabled: true`                                                                         |
| `sysctlVmMaxMapCount`              | Sets the[sysctl vm.max_map_count](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html#vm-max-map-count) needed for Elasticsearch                                                                                                                                                                                  | `262144`                                                                                |
| `terminationGracePeriod`           | The[terminationGracePeriod](https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods) in seconds used when trying to stop the pod                                                                                                                                                                                                | `120`                                                                                   |
| `tests.enabled`                    | Enable creating test related resources when running `helm template` or `helm test`                                                                                                                                                                                                                                                           | `true`                                                                                  |
| `tolerations`                      | Configurable[tolerations](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/)                                                                                                                                                                                                                                                  | `[]`                                                                                    |
| `transportPort`                    | The transport port that Kubernetes will use for the service. If you change this you will also need to set[transport port configuration](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-transport.html#_transport_settings) in `extraEnvs`                                                                                | `9300`                                                                                  |
| `updateStrategy`                   | The[updateStrategy](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) for the StatefulSet. By default Kubernetes will wait for the cluster to be green after upgrading each pod. Setting this to `OnDelete` will allow you to manually delete each pod during upgrades                                                      | `RollingUpdate`                                                                         |
| `volumeClaimTemplate`              | Configuration for the[volumeClaimTemplate for StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#stable-storage). You will want to adjust the storage (default `30Gi` ) and the `storageClassName` if you are using a different storage class                                                                 | see[values.yaml](https://github.com/elastic/helm-charts/blob/main/elasticsearch/values.yaml) |


# docker 安装 Elasticsearch
https://www.elastic.co/guide/en/elasticsearch/reference/master/docker.html#docker-prod-prerequisites
```sh
docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```