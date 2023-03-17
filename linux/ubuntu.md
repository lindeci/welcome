# 查看系统版本
```sh
#操作系统的发行版号和操作系统版本
ubuntu@VM-32-14-ubuntu:~$ uname -a
Linux VM-32-14-ubuntu 5.15.0-48-generic #54-Ubuntu SMP Fri Aug 26 13:26:29 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
#查看版本号
ubuntu@VM-32-14-ubuntu:~$ uname -v
#54-Ubuntu SMP Fri Aug 26 13:26:29 UTC 2022
#发行版本信息
ubuntu@VM-32-14-ubuntu:~$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 22.04 LTS
Release:        22.04
Codename:       jammy
#Linux版本信息及类型
ubuntu@VM-32-14-ubuntu:~$ cat /etc/issue
Ubuntu 22.04 LTS \n \l
#Linux内核的信息
ubuntu@VM-32-14-ubuntu:~$ cat /proc/version
Linux version 5.15.0-48-generic (buildd@lcy02-amd64-080) (gcc (Ubuntu 11.2.0-19ubuntu1) 11.2.0, GNU ld (GNU Binutils for Ubuntu) 2.38) #54-Ubuntu SMP Fri Aug 26 13:26:29 UTC 2022
```

# 安装docker
```sh
1、安装docker：sudo apt-get install -y docker.io
2、启动docker服务：systemctl start docker
3、设置开机启动：systemctl enable docker
4、查看docker状态：systemctl status docker
5、停止docker服务：systemctl stop docker
6、查看docker版本：docker version
```

# 非root用户运行docker
```sh
1、添加docker用户组：sudo groupadd docker
    执行以上命令会提示已存在，原因是在安装docker时已自动创建。
2、将指定用户添加到用户组（username为你的用户名）：sudo gpasswd -a username docker
3、查看是否添加成功：cat /etc/group | grep ^docker
4、重启docker：sudo systemctl restart docker
5、更新用户组：newgrp docker
6、执行docker命令，比如：docker ps -a
```

# 允许root远程连接
```sh
sudo vi /etc/ssh/sshd_config
#PermitRootLogin prohibit-password 改为
PermitRootLogin yes
sudo systemctl restart sshd
```

# 卸载软件
```sh
apt-get --purge remove xxxxx
```

# gdb attach使用
```sh
ps命令查看进程id。
执行gdb attach pid即可调试正在运行的程序。
info proc显示当前程序可执行文件相关信息（name，pwd）
```

# ubuntu iptables重启生效
```sh
iptables-save >/etc/iptables.roles
pre-up iptables-restore < /etc/iptables.roles
```

# 查看并修改DNS
```sh
resolvectl status
sudo vi /etc/systemd/resolved.conf
sudo systemctl restart systemd-resolved.service
```