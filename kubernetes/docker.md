- [Docker 镜像怎么转换为 Containerd 镜像](#docker-镜像怎么转换为-containerd-镜像)
- [Docker 和 Containerd 之间的一些主要区别](#docker-和-containerd-之间的一些主要区别)
- [Docker 的安装启动](#docker-的安装启动)
- [Docker 的参数](#docker-的参数)
  - [Docker run 的参数](#docker-run-的参数)
- [JAVA打包镜像的Dockerfile](#java打包镜像的dockerfile)
- [打包镜像](#打包镜像)
- [自定义启动参数](#自定义启动参数)
- [docker 导出导入镜像](#docker-导出导入镜像)
- [优化镜像大小](#优化镜像大小)
- [把python代码打包成docker镜像](#把python代码打包成docker镜像)
- [把镜像上传到 harbor](#把镜像上传到-harbor)
- [docker 的centos镜像](#docker-的centos镜像)
- [把容器中的文件拷贝到宿主机](#把容器中的文件拷贝到宿主机)

# Docker 镜像怎么转换为 Containerd 镜像
Docker 镜像和 Containerd 镜像实际上是相同的，因为它们都遵循 OCI 镜像规范。这意味着您可以使用相同的镜像在 Docker 和 Containerd 中运行容器。您不需要将 Docker 镜像转换为 Containerd 镜像，只需将镜像推送到容器仓库，然后在使用 Containerd 的系统上拉取镜像即可。

# Docker 和 Containerd 之间的一些主要区别
Docker 和 Containerd 都是容器运行时，它们都可以用来管理和运行容器。但是，它们之间也有一些区别。下面是一个简单的表格，列出了 Docker 和 Containerd 之间的一些主要区别：

| 特征 | Docker | Containerd |
| --- | --- | --- |
| 组成部分 | Docker 客户端、Docker 守护程序、Containerd 和 runc 等 | 独立的容器运行时 |
| 功能 | 提供了一个简单易用的命令行界面来管理容器，包括镜像管理、网络管理等功能 | 更加轻量级，只包含管理和运行容器所需的最基本功能 |
| 调用链 | 在使用 k8s 时，使用 Docker 的调用链更长，需要经过 dockershim 和 docker | 在使用 k8s 时，使用 Containerd 的调用链更短，不再需要经过 dockershim 和 docker |
| 数据目录 | 默认为 /var/lib/docker | 默认为 /var/lib/containerd |

总之，Docker 和 Containerd 都是优秀的容器运行时，它们各有优势。您可以根据自己的需求选择使用哪一个。

# Docker 的安装启动
```sh
yum install -y docker
systemctl start docker
```

# Docker 的参数
```yml
docker --help

Usage:  docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Common Commands:
  run         Create and run a new container from an image
  exec        Execute a command in a running container
  ps          List containers
  build       Build an image from a Dockerfile
  pull        Download an image from a registry
  push        Upload an image to a registry
  images      List images
  login       Log in to a registry
  logout      Log out from a registry
  search      Search Docker Hub for images
  version     Show the Docker version information
  info        Display system-wide information

Management Commands:
  builder     Manage builds
  buildx*     Docker Buildx (Docker Inc., v0.10.4)
  compose*    Docker Compose (Docker Inc., v2.17.3)
  container   Manage containers
  context     Manage contexts
  image       Manage images
  manifest    Manage Docker image manifests and manifest lists
  network     Manage networks
  plugin      Manage plugins
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes

Swarm Commands:
  swarm       Manage Swarm

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  import      Import the contents from a tarball to create a filesystem image
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  wait        Block until one or more containers stop, then print their exit codes

Global Options:
      --config string      Location of client config files (default "/root/.docker")
  -c, --context string     Name of the context to use to connect to the daemon (overrides DOCKER_HOST env var and default context set with "docker context use")
  -D, --debug              Enable debug mode
  -H, --host list          Daemon socket(s) to connect to
  -l, --log-level string   Set the logging level ("debug", "info", "warn", "error", "fatal") (default "info")
      --tls                Use TLS; implied by --tlsverify
      --tlscacert string   Trust certs signed only by this CA (default "/root/.docker/ca.pem")
      --tlscert string     Path to TLS certificate file (default "/root/.docker/cert.pem")
      --tlskey string      Path to TLS key file (default "/root/.docker/key.pem")
      --tlsverify          Use TLS and verify the remote
  -v, --version            Print version information and quit

Run 'docker COMMAND --help' for more information on a command.

For more help on how to use Docker, head to https://docs.docker.com/go/guides/
```
其中-v既可以查看版本，也可以将主机目录挂载到容器中

## Docker run 的参数
```yml
docker run --help    

Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

Create and run a new container from an image

Aliases:
  docker container run, docker run

Options:
      --add-host list                  Add a custom host-to-IP mapping (host:ip)
  -a, --attach list                    Attach to STDIN, STDOUT or STDERR
      --blkio-weight uint16            Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0)
      --blkio-weight-device list       Block IO weight (relative device weight) (default [])
      --cap-add list                   Add Linux capabilities
      --cap-drop list                  Drop Linux capabilities
      --cgroup-parent string           Optional parent cgroup for the container
      --cgroupns string                Cgroup namespace to use (host|private)
                                       'host':    Run the container in the Docker host's cgroup namespace
                                       'private': Run the container in its own private cgroup namespace
                                       '':        Use the cgroup namespace as configured by the
                                                  default-cgroupns-mode option on the daemon (default)
      --cidfile string                 Write the container ID to the file
      --cpu-period int                 Limit CPU CFS (Completely Fair Scheduler) period
      --cpu-quota int                  Limit CPU CFS (Completely Fair Scheduler) quota
      --cpu-rt-period int              Limit CPU real-time period in microseconds
      --cpu-rt-runtime int             Limit CPU real-time runtime in microseconds
  -c, --cpu-shares int                 CPU shares (relative weight)
      --cpus decimal                   Number of CPUs
      --cpuset-cpus string             CPUs in which to allow execution (0-3, 0,1)
      --cpuset-mems string             MEMs in which to allow execution (0-3, 0,1)
  -d, --detach                         Run container in background and print container ID
      --detach-keys string             Override the key sequence for detaching a container
      --device list                    Add a host device to the container
      --device-cgroup-rule list        Add a rule to the cgroup allowed devices list
      --device-read-bps list           Limit read rate (bytes per second) from a device (default [])
      --device-read-iops list          Limit read rate (IO per second) from a device (default [])
      --device-write-bps list          Limit write rate (bytes per second) to a device (default [])
      --device-write-iops list         Limit write rate (IO per second) to a device (default [])
      --disable-content-trust          Skip image verification (default true)
      --dns list                       Set custom DNS servers
      --dns-option list                Set DNS options
      --dns-search list                Set custom DNS search domains
      --domainname string              Container NIS domain name
      --entrypoint string              Overwrite the default ENTRYPOINT of the image
  -e, --env list                       Set environment variables
      --env-file list                  Read in a file of environment variables
      --expose list                    Expose a port or a range of ports
      --gpus gpu-request               GPU devices to add to the container ('all' to pass all GPUs)
      --group-add list                 Add additional groups to join
      --health-cmd string              Command to run to check health
      --health-interval duration       Time between running the check (ms|s|m|h) (default 0s)
      --health-retries int             Consecutive failures needed to report unhealthy
      --health-start-period duration   Start period for the container to initialize before starting health-retries countdown (ms|s|m|h) (default 0s)
      --health-timeout duration        Maximum time to allow one check to run (ms|s|m|h) (default 0s)
      --help                           Print usage
  -h, --hostname string                Container host name
      --init                           Run an init inside the container that forwards signals and reaps processes
  -i, --interactive                    Keep STDIN open even if not attached
      --ip string                      IPv4 address (e.g., 172.30.100.104)
      --ip6 string                     IPv6 address (e.g., 2001:db8::33)
      --ipc string                     IPC mode to use
      --isolation string               Container isolation technology
      --kernel-memory bytes            Kernel memory limit
  -l, --label list                     Set meta data on a container
      --label-file list                Read in a line delimited file of labels
      --link list                      Add link to another container
      --link-local-ip list             Container IPv4/IPv6 link-local addresses
      --log-driver string              Logging driver for the container
      --log-opt list                   Log driver options
      --mac-address string             Container MAC address (e.g., 92:d0:c6:0a:29:33)
  -m, --memory bytes                   Memory limit
      --memory-reservation bytes       Memory soft limit
      --memory-swap bytes              Swap limit equal to memory plus swap: '-1' to enable unlimited swap
      --memory-swappiness int          Tune container memory swappiness (0 to 100) (default -1)
      --mount mount                    Attach a filesystem mount to the container
      --name string                    Assign a name to the container
      --network network                Connect a container to a network
      --network-alias list             Add network-scoped alias for the container
      --no-healthcheck                 Disable any container-specified HEALTHCHECK
      --oom-kill-disable               Disable OOM Killer
      --oom-score-adj int              Tune host's OOM preferences (-1000 to 1000)
      --pid string                     PID namespace to use
      --pids-limit int                 Tune container pids limit (set -1 for unlimited)
      --platform string                Set platform if server is multi-platform capable
      --privileged                     Give extended privileges to this container
  -p, --publish list                   Publish a container's port(s) to the host
  -P, --publish-all                    Publish all exposed ports to random ports
      --pull string                    Pull image before running ("always", "missing", "never") (default "missing")
  -q, --quiet                          Suppress the pull output
      --read-only                      Mount the container's root filesystem as read only
      --restart string                 Restart policy to apply when a container exits (default "no")
      --rm                             Automatically remove the container when it exits
      --runtime string                 Runtime to use for this container
      --security-opt list              Security Options
      --shm-size bytes                 Size of /dev/shm
      --sig-proxy                      Proxy received signals to the process (default true)
      --stop-signal string             Signal to stop the container
      --stop-timeout int               Timeout (in seconds) to stop a container
      --storage-opt list               Storage driver options for the container
      --sysctl map                     Sysctl options (default map[])
      --tmpfs list                     Mount a tmpfs directory
  -t, --tty                            Allocate a pseudo-TTY
      --ulimit ulimit                  Ulimit options (default [])
  -u, --user string                    Username or UID (format: <name|uid>[:<group|gid>])
      --userns string                  User namespace to use
      --uts string                     UTS namespace to use
  -v, --volume list                    Bind mount a volume
      --volume-driver string           Optional volume driver for the container
      --volumes-from list              Mount volumes from the specified container(s)
  -w, --workdir string                 Working directory inside the container
```

# JAVA打包镜像的Dockerfile
```
FROM registrytest.ldc.com/library/openjdk:8u212-jdk-alpine as runner 
WORKDIR /data 
VOLUME /tmp 
RUN echo "Asia/Shanghai" > /etc/timezone 
EXPOSE 8080 
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:InitialRAMPercentage=40.0 -XX:MinRAMPercentage=20.0 -XX:MaxRAMPercentage=80.0 -XX:-UseAdaptiveSizePolicy  -XX:+HeapDumpOnOutOfMemoryError -XX:ReservedCodeCacheSize=240m -Djava.security.egd=file:/dev/./urandom" 
ENV APP_OPTS="-Dproject.logs.dir=./logs" 
ENTRYPOINT ["/sbin/tini", "--"] 
CMD ["sh", "-c", "java -server $JAVA_OPTS $APP_OPTS  -jar /data/app.jar"] 
COPY  ./${jarPath}/target/*.jar /data/app.jar
```
- `VOLUME ["/tmp", "/var/log"]`

这条指令会在容器中创建两个卷，一个名为 /tmp，另一个名为 /var/log。这些卷可以分别与主机上的 /tmp 目录和 /var/log 目录进行挂载。

您可以使用 VOLUME 指令在 Dockerfile 中创建任意数量的卷。卷可以用于共享数据，运行测试和调试容器。

- `ENTRYPOINT ["/sbin/tini", "--"]`

这条指令会将 /sbin/tini 命令指定为容器的入口点。入口点是容器启动时运行的第一个命令。

/sbin/tini 是一个微型 init 程序，它用于管理容器的进程。它确保容器的进程以安全和可预测的方式启动和停止。

-- 参数告诉 tini 不要从命令行读取任何参数。这对于防止容器从命令行接收意外参数很重要。
- `RUN echo "Asia/Shanghai" > /etc/timezone`

这条指令会在容器中运行 echo 命令，并将 Asia/Shanghai 字符串写入 /etc/timezone 文件。/etc/timezone 文件是容器的时区文件。

- `EXPOSE 8080`

这条指令会将容器的 8080 端口暴露给外部。这意味着您可以通过外部 IP 地址和端口 8080 访问容器。

# 打包镜像
`docker build -t my_test .`

# 自定义启动参数
`docker run -it --rm my_test python hello.py  arg1 arg2 arg3`

-i 选项告诉 Docker 在容器中启动一个交互式 shell。这意味着您可以在容器中输入命令并查看命令的输出。

-t 选项告诉 Docker 在容器中分配一个伪终端。这意味着您可以在容器中看到图形输出。

-it 选项是一个很有用的选项，它可以用于调试容器和测试应用程序。
# docker 导出导入镜像
```
docker save elasticdump/elasticsearch-dump >elasticsearch-dump.tar
docker load < elasticsearch-dump.tar
```

# 优化镜像大小
优化镜像大小的方法有很多，下面是一些常用的技巧：
- **使用多阶段构建**：多阶段构建可以在 Dockerfile 中使用多个基础镜像，并将编译成品、配置文件等从一个阶段复制到另一个阶段，这样我们就可以丢弃不需要的东西。
- **使用轻量化基础镜像**：在 Docker Hub（公共 Docker 仓库）中，有一些镜像可供下载，每个镜像都有不同的特征和大小。通常，相较于基于其他 Linux 发行版（例如 Ubuntu）的镜像，基于 Alpine 或 BusyBox 的镜像非常小。这是因为 Alpine 镜像和类似的其他镜像都经过了优化，其中仅包含最少的必须的软件包。
- **减少镜像层数**：将 dockerfile 中的多条指令合并成一条，通过减少镜像层数的方式达到精简镜像体积的目的。
- **清理无用数据**：删除多余文件，压缩整个系统。

比如把 `FROM python:3.10` 改成 `FROM python:3.10-alpine`

# 把python代码打包成docker镜像
Dockerfile的内容
```sh
FROM python:2.7-alpine
WORKDIR /app
COPY . /app
CMD ["python", "test.py"]
```
test.py 的内容
```python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'HELLO')

httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
```
开始打包
```sh
docker build -t ldc-python-app .
```
查看打包后的镜像
```sh
docker images | grep ldc
ldc-python-app             latest              e0043da907ea   4 minutes ago   71.2MB
```
运行该镜像
```sh
docker run -p 8000:8000 ldc-python-app
```

# 把镜像上传到 harbor
```sh
# 登录到 HARBOR 仓库
docker login https://172.1.1.198:80 -u <您的用户名> -p <您的密码>

# 为镜像打上标签
docker tag ldc-python-app:latest 172.1.1.198:80/mysql/ldc-python-app:latest

# 将镜像推送到 HARBOR 仓库
docker push 172.1.1.198:80/mysql/ldc-python-app:latest
```
具体例子
```sh
# 查看本地镜像
docker images | grep mysql
mysql                    5.7.30          9cfcce23593a   3 years ago     448MB

# 为镜像打上标签
docker tag mysql:5.7.30 dockerhub.kubekey.local/mysql/mysql:5.7.30

# 将镜像推送到 HARBOR 仓库
docker push dockerhub.kubekey.local/mysql/mysql:5.7.30
```

# docker 的centos镜像
```sh
docker pull centos:7.9.2009
docker run -it -v /data/ldc_docker:/data -w /data centos:7.9.2009 bash
```

# 把容器中的文件拷贝到宿主机
