- [收集系统信息](#收集系统信息)
- [xargs](#xargs)
- [sed](#sed)
- [vi](#vi)
- [bash](#bash)
- [网络调优：](#网络调优)
- [mdadm 删除 软件 RAID](#mdadm-删除-软件-raid)
- [vgextend](#vgextend)
- [lsof](#lsof)
- [cpu开启性能模式](#cpu开启性能模式)
	- [tuned-adm list](#tuned-adm-list)
- [查看透明页](#查看透明页)
- [lvs操作](#lvs操作)
- [硬件时间](#硬件时间)
- [拆掉raid](#拆掉raid)
- [查看是否机械硬盘](#查看是否机械硬盘)
- [查找对应线程所占的 cpu核](#查找对应线程所占的-cpu核)
- [文件句柄](#文件句柄)
- [卷](#卷)
- [cgroup](#cgroup)
	- [查看cgroups的挂载信息](#查看cgroups的挂载信息)
	- [创建group](#创建group)
	- [添加任务进程到cgroup](#添加任务进程到cgroup)
	- [删除 cgroup](#删除-cgroup)
	- [限制cpu使用](#限制cpu使用)
		- [cpu子系统](#cpu子系统)
		- [cpu.shares](#cpushares)
- [查看文件编码](#查看文件编码)
- [查看带宽、流量](#查看带宽流量)
- [man使用](#man使用)
- [free 详解](#free-详解)
	- [手工释放内存](#手工释放内存)
	- [查看内存硬件](#查看内存硬件)
- [systemctl](#systemctl)
- [查看磁盘是否机械盘](#查看磁盘是否机械盘)


# 收集系统信息
```sh
cd /tmp
localip=`ip a show up| grep 'inet '| egrep -v 'scope host|127.0.0|secondary| lo'|head -1|awk '{print $2}'| sed 's/\/.*//g'` && echo $localip
cat << "SYSEOF" |  awk -F '\n' '{if(!NF ){next}}{print "echo;echo;echo;echo;echo;echo '\''########  "$NF"'\'';"$NF}' > sysinfosh
cat /etc/redhat-release;cat /etc/system-release-cpe;uname -a;hostname;hostname -i
cat /etc/hosts
ip a;ifconfig

uptime

lscpu
cat /proc/cpuinfo

df -Th
lsblk
lsblk -ap -o NAME,KNAME,PKNAME,TYPE,FSTYPE,MOUNTPOINT,RA,RO,RM,SIZE,STATE,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,RAND,HCTL,TRAN,REV,VENDOR,MODEL
lsblk -a -o NAME,KNAME,MOUNTPOINT,ROTA,SIZE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,RA,RO,RM

pvdisplay
vgdisplay
lvdisplay

free -h
cat /proc/buddyinfo
cat /proc/meminfo
cat /proc/slabinfo
cat /proc/vmallocinfo
cat /proc/vmstat
cat /proc/zoneinfo
cat /proc/pagetypeinfo
numactl -H

cat /proc/cmdline


cat /etc/sysctl.conf
sysctl -a 


cat /etc/crontab
crontab -u root -l
crontab -u tdsql -l

egrep "^[^#]" /etc/security/limits.conf  /etc/security/limits.d/*
ulimit -Ha
ulimit -Sa


ls -l  /proc
find /proc -maxdepth 1  -type f -size -1k
cat /proc/fb
cat /proc/dma
cat /proc/keys
#cat /proc/kmsg
cat /proc/misc
cat /proc/mtrr
cat /proc/stat
cat /proc/iomem
cat /proc/locks
cat /proc/swaps
cat /proc/crypto
cat /proc/mdstat
cat /proc/uptime
cat /proc/vmstat
cat /proc/cgroups
cat /proc/cmdline
cat /proc/cpuinfo
cat /proc/devices
cat /proc/ioports
cat /proc/loadavg
cat /proc/meminfo
cat /proc/modules
cat /proc/version
cat /proc/consoles
#cat /proc/kallsyms
cat /proc/slabinfo
cat /proc/softirqs
cat /proc/zoneinfo
cat /proc/buddyinfo
cat /proc/diskstats
cat /proc/key-users
cat /proc/schedstat
cat /proc/interrupts
#cat /proc/kpagecount
#cat /proc/kpageflags
cat /proc/partitions
cat /proc/timer_list
cat /proc/execdomains
cat /proc/filesystems
#cat /proc/sched_debug
cat /proc/timer_stats
cat /proc/vmallocinfo
cat /proc/pagetypeinfo
#cat /proc/sysrq-trigger

SYSEOF
cat sysinfosh
bash sysinfosh &>  sysinfoout$localip     #里面命令里面不要出现单引号
ls -l sysinfoout$localip 
less sysinfoout$localip
```
----------------------------------------------------------------------------
# xargs 
```sh
ps aux | grep mysqld | grep -v grep | awk '{print $2}' | xargs -I{} echo {}
```
----------------------------------------------------------------------------
#egrep

----------------------------------------------------------------------------
# sed
```sh
###sed非常规语法
#使用sed命令在cisco行下面添加CCIE；
sed -i "/cisco/a\CCIE" 123.txt

#使用sed命令在network行上面添加一行，内容是Security；
sed -i "/network/i\Security" 123.txt

sed -i -r  's~\r$~~g' 123.txt         #\r\n 换 \n
sed -i -r  's~$~\r~g' 123.txt         #\n换\r\n

一、删除包含匹配字符串的行
## 删除包含baidu.com的所有行
sed -i '/baidu.com/d' domain.file

二、删除匹配行及后所有行
## 删除匹配20160229的行及后面所有行
sed -i '/20160229/,$d' 充值人数.log

三、删除最后3行
tac file|sed 1,3d|tac
```
----------------------------------------------------------------------------
# vi
```sh
:set ff  查看当前文本的模式类型，一般为dos,unix
:set ff=dos  设置为dos模式， 也可以用 sed -i 's/$/\r/' 
:set ff=unix  设置为unix模式，也可以用一下方式转换为unix模式:sed -i 's/.$//g'
 
:set fileencoding查看现在文本的编码
:set fenc=编码  转换当前文本的编码为指定的编码
:set enc=编码  以指定的编码显示文本，但不保存到文件中。
:set nu   显示行号
:set encoding=utf-8 #设置编码格式
:set showmatch   在vi中输入），}时，光标会暂时的回到相匹配的（，{ （如果没有相匹配的就发出错误信息的铃声），编程时很有用

vim取消自动换行
把textwidth调大：
:set textwidth=1000
vim取消自动折行
:set nowrap

Vim快速移动
1、 需要按行快速移动光标时，可以使用键盘上的编辑键Home，快速将光标移动至当前行的行首。除此之外，也可以在命令模式中使用快捷键"^"（即Shift+6）或0（数字0）。
2、 如果要快速移动光标至当前行的行尾，可以使用编辑键End。也可以在命令模式中使用快捷键"$"（Shift+4）。与快捷键"^"和0不同，快捷键"$"前可以加上数字表示移动的行数。例如使用"1$"表示当前行的行尾，"2$"表示当前行的下一行的行尾。
3、h, j, k, l分别代表向左、下、上、右移动。如同许多vim命令一样，可以在这些键前加一个数字，表示移动的倍数。例如，"10j"表示向下移动10行；"10l"表示向右移动10列。
4、在vim中翻页，同样可以使用PageUp和PageDown，不过，像使用上下左右光标一样，你的手指会移出主键盘区。因此，我们通常使用CTRL-B和CTRL-F来进行翻页，它们的功能等同于PageUp和PageDown。CTRL-B和CTRL-F前也可以加上数字，来表示向上或向下翻多少页。
5、命令"gg"移动到文件的第一行，而命令"G"则移动到文件的最后一行。命令"G"前可以加上数字，在这里，数字的含义并不是倍数，而是你打算跳转的行号。例如，你想跳转到文件的第1234行，只需输入"1234G"。
你还可以按百分比来跳转，例如，你想跳到文件的正中间，输入"50%"；如果想跳到75%处，输入"75%"。注意，你必须先输入一个数字，然后输入"%"。如果直接输入"%"，那含义就完全不同了。":help N%"阅读更多细节。在文件中移动，你可能会迷失自己的位置，这时使用"CTRL-G"命令，查看一下自己位置。
6、"f"命令移动到光标右边的指定字符上，例如，"fx"，会把移动到光标右边的第一个'x'字符上。"F"命令则反方向查找，也就是移动到光标左边的指定字符上。
"t"命令和"f"命令的区别在于，它移动到光标右边的指定字符之前。例如，"tx"会移动到光标右边第一个'x'字符的前面。"T"命令是"t"命令的反向版本，它移动到光标左边的指定字符之后。
```
----------------------------------------------------------------------------
# bash
```sh
ctrl+a  行首
ctrl+e  行尾
ctrl+k  清除光标后至行尾的内容
ctrl+u  清除光标前至行首间的所有内容
ctrl+l  清屏，相当于clear
ctrl+z  把当前进程转到后台运行，使用 fg 命令恢复。比如top -d1 然后ctrl+z，到后台，然后fg,重新恢复
```
----------------------------------------------------------------------------
# 网络调优：
```sh
https://baijiahao.baidu.com/s?id=1677502435760515122&wfr=spider&for=pc
```
----------------------------------------------------------------------------
# mdadm 删除 软件 RAID
```sh
https://blog.csdn.net/u010953692/article/details/108858680
1、查看
	mdadm -D /dev/md0
	cat /proc/mdstat
	cat /etc/mdadm/mdadm.conf
	cat /etc/mdadm/mdadm.conf
2、umount /chain
3、	mdadm -S /dev/md0
	lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT
	cat /etc/mdadm/mdadm.conf
	cat /dev/null > /etc/mdadm/mdadm.conf
4、删除元数据
# mdadm --zero-superblock /dev/sda
# mdadm --zero-superblock /dev/sdb
# mdadm --zero-superblock /dev/sdc
# mdadm --zero-superblock /dev/sdd
# lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT
```
----------------------------------------------------------------------------
# vgextend
```sh
 3321  2022-07-18 11:06:29 root pvcreate -f /dev/sda
 3322  2022-07-18 11:08:41 root vgdisplay
 3323  2022-07-18 11:08:49 root vgs
 3324  2022-07-18 11:08:50 root pvs
 3325  2022-07-18 11:09:25 root disk -l
 3326  2022-07-18 11:09:27 root fdisk -l
 3327  2022-07-18 11:10:20 root pvs
 3328  2022-07-18 11:13:52 root dd if=/dev/zero of=/dev/sda bs=512K count=20
 3329  2022-07-18 11:14:02 root pvcreate -f /dev/sda
 3330  2022-07-18 11:14:19 root dd if=/dev/zero of=/dev/sdb bs=512K count=20
 3331  2022-07-18 11:14:25 root dd if=/dev/zero of=/dev/sdc bs=512K count=20
 3332  2022-07-18 11:14:30 root dd if=/dev/zero of=/dev/sdd bs=512K count=20
 3333  2022-07-18 11:14:36 root dd if=/dev/zero of=/dev/sde bs=512K count=20
 3334  2022-07-18 11:14:41 root pvcreate -f /dev/sdb
 3335  2022-07-18 11:14:43 root pvcreate -f /dev/sdc
 3336  2022-07-18 11:14:46 root pvcreate -f /dev/sdd
 3337  2022-07-18 11:14:55 root pvcreate /dev/sde
 3338  2022-07-18 11:14:57 root pvs
 3339  2022-07-18 11:15:19 root history |grep dd
 3340  2022-07-18 11:15:23 root history 
 3341  2022-07-18 11:16:27 root lvs
 3342  2022-07-18 11:16:34 root pvs
 3343  2022-07-18 11:17:09 root vgcreate vgtidb /dev/sda
 3344  2022-07-18 11:18:10 root vgextend vgtidb /dev/sdb 
 3345  2022-07-18 11:18:18 root pvdisplay
 3346  2022-07-18 11:18:39 root vgdisplay
 3347  2022-07-18 11:19:14 root vgextend vgtidb /dev/sdc 
 3348  2022-07-18 11:19:20 root vgextend vgtidb /dev/sdd
 3349  2022-07-18 11:19:25 root vgextend vgtidb /dev/sde
 3350  2022-07-18 11:19:32 root vgdisplay 
 3351  2022-07-18 11:23:26 root lvcreate -L 2.4T -n lvtikv vgtidb
 3352  2022-07-18 11:23:40 root lvdisplay
 3353  2022-07-18 11:24:28 root lvcreate -L 1.6T -n lvtiflash vgtidb
 3354  2022-07-18 11:24:33 root lsblk
 3355  2022-07-18 11:24:48 root df -h
 3356  2022-07-18 11:26:33 root cd /dev/mapper/
 3357  2022-07-18 11:26:35 root ll -rtc
 3358  2022-07-18 11:27:38 root cd 
 3359  2022-07-18 11:27:55 root mkdir /tidb
 3360  2022-07-18 11:28:11 root mkdir /tiflash
 3361  2022-07-18 11:29:38 root mkfs -t ext4 /dev/mapper/vgtidb-lvtikv 
 3362  2022-07-18 11:31:57 root mount -a /dev/mapper/vgtidb-lvtikv /tidb
 3363  2022-07-18 11:31:59 root df -h
 3364  2022-07-18 11:34:48 root lsblk -f
 3365  2022-07-18 11:35:45 root vim /etc/fstab 
 3366  2022-07-18 11:36:58 root cat /etc/fstab 
 3367  2022-07-18 11:41:52 root vim /etc/fstab 
 3368  2022-07-18 11:42:56 root mount -a
 3369  2022-07-18 11:43:32 root mkfs -t ext4 /dev/mapper/vgtidb-lvtiflash 
 3370  2022-07-18 11:44:30 root mount -a
 3371  2022-07-18 11:44:33 root df -h
 3372  2022-07-18 11:45:11 root umount
 3373  2022-07-18 11:45:19 root umount /tidb 
 3374  2022-07-18 11:45:22 root df -h
 3375  2022-07-18 11:45:28 root umount /tidb 
 3376  2022-07-18 11:45:30 root df -h
 3377  2022-07-18 11:45:36 root vim /etc/fstab 
 3378  2022-07-18 11:46:13 root mount -a
 3379  2022-07-18 11:46:16 root df -h
 3380  2022-07-18 11:46:26 root lsblk
 3381  2022-07-18 13:54:48 root cd /dev/mapper/
 3382  2022-07-18 13:54:48 root ls
 3383  2022-07-18 13:54:53 root ll -rtc
 3384  2022-07-18 13:54:59 root cd ..
 3385  2022-07-18 13:55:01 root ll -rtc
 3386  2022-07-18 13:55:03 root cd 
 3387  2022-07-18 13:55:08 root cd /dev/
 3388  2022-07-18 13:55:09 root ll -rtc
 3389  2022-07-18 13:55:45 root cd 
 3390  2022-07-18 13:55:47 root fdisk -l
 ```
----------------------------------------------------------------------------
# lsof
```sh
lsof -i tcp:31487
```
----------------------------------------------------------------------------
# cpu开启性能模式
```sh
cpupower frequency-info -o
```
Centos 7.8 开启性能模式
tuned-adm profile throughput-performance
检查是否开启性能模式
tuned-adm active
或
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
或
cpupower frequency-info --policy

查看支持的参数
tuned-adm list
----------------------------------------------------------------------------
# 查看透明页
```sh
cat /sys/kernel/mm/transparent_hugepage/
```
----------------------------------------------------------------------------
# lvs操作
```sh
ipvsadm –A –t <VIP>:<Port> -s <schedule: rr|wrr|lc|wlc|lblc|lblcr|dh|sh|sed|nq>
添加
ipvsadm -A -t 88.4.38.86:15004 -s sed
ipvsadm -a -r 88.4.38.76:15004 -t 88.4.38.86:15004 -w 10000 -i
ipvsadm -a -r 88.4.38.77:15004 -t 88.4.38.86:15004 -w 10000
ipvsadm -a -r 88.4.38.78:15004 -t 88.4.38.86:15004 -w 10000

ipvsadm -a -r 88.4.38.78:15003 -t 88.4.38.86:15003

删除
ipvsadm -d -r 88.4.38.76:15004 -t 88.4.38.86:15004
ipvsadm -d -r 88.4.38.77:15004 -t 88.4.38.86:15004
ipvsadm -d -r 88.4.38.78:15004 -t 88.4.38.86:15004
ipvsadm -D -t 88.4.38.86:15004

ipvsadm -A -t 88.4.38.86:15003 -s sed
ipvsadm -a -r 88.4.38.76:15003 -t 88.4.38.86:15003 -w 10000
ipvsadm -a -r 88.4.38.77:15003 -t 88.4.38.86:15003 -w 10000
ipvsadm -a -r 88.4.38.78:15003 -t 88.4.38.86:15003 -w 10000

ipvsadm -d -r 88.4.38.76:15003 -t 88.4.38.86:15003
ipvsadm -d -r 88.4.38.77:15003 -t 88.4.38.86:15003
ipvsadm -d -r 88.4.38.78:15003 -t 88.4.38.86:15003

ipvsadm -D -t 88.4.38.86:15002
```
----------------------------------------------------------------------------
# 硬件时间
```sh
利用系统时间设置硬件时间来
hwclock --systohc
```
----------------------------------------------------------------------------
# 拆掉raid
```sh
umount /data1
mdadm -S /dev/md0
mdadm --zero-superblock /dev/sda
mdadm --zero-superblock /dev/sdb
```
----------------------------------------------------------------------------
# 查看是否机械硬盘
```sh
#是否机械硬盘
egrep -Hi '' /sys/block/*/queue/rotational
lsblk -d -o name,rota
lsblk -a -o NAME,KNAME,MOUNTPOINT,ROTA,SIZE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,RA,RO,RM

fdisk -l
#"heads"（磁头），"track"（磁道）和"cylinders"（柱面）
smartctl --all /dev/sda
smartctl -A /dev/sda
```
----------------------------------------------------------------------------
# 查找对应线程所占的 cpu核
```sh
taskset -pc  PID

首先 可以通过  top  -H   -d  1  -p  PID 查看具体 进程的 cpu ，内存 等等 占据大小 比例
再 按下 1
可以查看到 cpu的占用比例，多少个核在使用 就可以看到多少个 %Cpu
```
----------------------------------------------------------------------------
# 文件句柄
```sh
man 5 proc 然后查找 关键字

fs.file-max   系统所有句柄数
fs.nr_open     单进程句柄数
DefaultLimitNOFIL    用户总句柄数
```
----------------------------------------------------------------------------
# 卷
- 物理盘 raid 设置,划分 partition,在LVM上是PV
- 多个PV组成VG
- 从VG分割出LV
- LV格式化后mount到目录

# cgroup
## 查看cgroups的挂载信息
```sh
# mount -t cgroup
cgroup on /sys/fs/cgroup/systemd type cgroup (rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/usr/lib/systemd/systemd-cgroups-agent,name=systemd)
cgroup on /sys/fs/cgroup/cpu,cpuacct type cgroup (rw,nosuid,nodev,noexec,relatime,cpu,cpuacct)
cgroup on /sys/fs/cgroup/hugetlb type cgroup (rw,nosuid,nodev,noexec,relatime,hugetlb)
cgroup on /sys/fs/cgroup/net_cls,net_prio type cgroup (rw,nosuid,nodev,noexec,relatime,net_cls,net_prio)
cgroup on /sys/fs/cgroup/perf_event type cgroup (rw,nosuid,nodev,noexec,relatime,perf_event)
cgroup on /sys/fs/cgroup/pids type cgroup (rw,nosuid,nodev,noexec,relatime,pids)
cgroup on /sys/fs/cgroup/freezer type cgroup (rw,nosuid,nodev,noexec,relatime,freezer)
cgroup on /sys/fs/cgroup/rdma type cgroup (rw,nosuid,nodev,noexec,relatime,rdma)
cgroup on /sys/fs/cgroup/memory type cgroup (rw,nosuid,nodev,noexec,relatime,memory)
cgroup on /sys/fs/cgroup/devices type cgroup (rw,nosuid,nodev,noexec,relatime,devices)
cgroup on /sys/fs/cgroup/cpuset type cgroup (rw,nosuid,nodev,noexec,relatime,cpuset)
cgroup on /sys/fs/cgroup/blkio type cgroup (rw,nosuid,nodev,noexec,relatime,blkio)

如果没有的话，也可以通过以下命令来把想要的subsystem mount 到系统中：
# mount -t cgroup -o cpu,cpuset,memory cpu_and_mem /cgroup/cpu_and_mem
这个命令就创建一个名为cpu_and_mem的层级，这个层级上附加了cpu,cpuset,memory三个子系统，并把层级挂载到了/cgroup/cpu_and_mem.

什么是子系统？
cgroups支持的所有可配置的资源称为subsystem。例如cpu是一种subsystem，memory也是一种subsystem。linux内核在演进过程中subsystem是不断增加的。
```
## 创建group
```sh
# mkdir /sys/fs/cgroup/cpu/mycgroup
# ls /sys/fs/cgroup/cpu/mycgroup
# 该目录中会自动创建一些文件
-rw-r--r-- 1 root root 0 Mar 23 15:40 cgroup.clone_children
-rw-r--r-- 1 root root 0 Mar 23 15:40 cgroup.procs
-r--r--r-- 1 root root 0 Mar 23 15:40 cpuacct.stat
-rw-r--r-- 1 root root 0 Mar 23 15:40 cpuacct.usage
-r--r--r-- 1 root root 0 Mar 23 15:40 cpuacct.usage_all
-r--r--r-- 1 root root 0 Mar 23 15:40 cpuacct.usage_percpu
-r--r--r-- 1 root root 0 Mar 23 15:40 cpuacct.usage_percpu_sys
-r--r--r-- 1 root root 0 Mar 23 15:40 cpuacct.usage_percpu_user
-r--r--r-- 1 root root 0 Mar 23 15:40 cpuacct.usage_sys
-r--r--r-- 1 root root 0 Mar 23 15:40 cpuacct.usage_user
-rw-r--r-- 1 root root 0 Mar 23 15:40 cpu.cfs_period_us
-rw-r--r-- 1 root root 0 Mar 23 15:40 cpu.cfs_quota_us
-rw-r--r-- 1 root root 0 Mar 23 15:40 cpu.rt_period_us
-rw-r--r-- 1 root root 0 Mar 23 15:40 cpu.rt_runtime_us
-rw-r--r-- 1 root root 0 Mar 23 15:40 cpu.shares
-r--r--r-- 1 root root 0 Mar 23 15:40 cpu.stat
-rw-r--r-- 1 root root 0 Mar 23 15:40 notify_on_release
-rw-r--r-- 1 root root 0 Mar 23 15:40 tasks
```
除了每个cgroup独特的资源控制文件，还有一些通用的文件。

- tasks：当前 cgroup 包含的任务（task）pid 列表，把某个进程的 pid 添加到这个文件中就等于把进程交由到该cgroup控制。
- cgroup.procs：使用逻辑和tasks相同。
- notify_on_release：0或者1，该文件的内容为1时，当cgroup退出时（不再包含任何进程和子cgroup），将调用release_agent里面配置的命令。
- release_agent：需要执行的命令。
## 添加任务进程到cgroup
```sh
echo PID > tasks
```
一次只能添加一个任务进程ID。如果有多个任务ID，需分多次添加。  

cgroup各个子系统初始化时，默认把系统中所有进程都纳管了，将一个进程的pid添加到新建的cgroup tasks文件的操作，实际是从一个cgroup移入到另一个cgroup的操作。所以要将进程从某个cgroup中删除，只能通过将其移出到另一个cgroup来实现，或者将进程终止。

## 删除 cgroup
删除子资源，就是删除对应的目录：
```sh
rmdir /sys/fs/cgroup/cpu/mycgroup
```
## 限制cpu使用
跟cpu相关的子系统有cpu、cpuacct和cpuset。其中：
- cpuset主要用于设置cpu的亲和性，可以限制cgroup中的进程只能在指定的cpu上运行。
- cpuacct包含当前cgroup所使用的CPU的统计信息。
- cpu：限制cgroup的cpu使用上限。  

此篇，我们主要看下cpu子系统的使用。  
### cpu子系统

1. 限制进程可使用的CPU百分比。

设置 CPU 数字的单位都是微秒，用us表示。
```
cpu.cfs_period_us:时间周期长度，取值范围为1毫秒到1秒。
cfs_quota_us：当前cgroup在设置的周期长度内所能使用的CPU时间。
```
两个文件配合起来设置CPU的使用上限。  
示例：
```sh
限制使用2个CPU（内核）（每500ms能使用1000ms的CPU时间，即使用两个内核）
# echo 1000000 > cpu.cfs_quota_us
# echo 500000 > cpu.cfs_period_us
```
### cpu.shares
用来设置CPU的相对值，并且是针对所有的CPU（内核），默认值是1024，假如系统中有两个cgroup，分别是A和B，A的shares值是1024，B的shares值是512，那么A将获得1024/(1204+512)=66%的CPU资源，而B将获得33%的CPU资源。  

shares有两个特点:
- 如果A不忙，没有使用到66%的CPU时间，那么剩余的CPU时间将会被系统分配给B，即B的CPU使用率可以超过33%
- 如果添加了一个新的cgroup C，且它的shares值是1024，那么A的限额变成了1024/(1204+512+1024)=40%，B的变成了20%。  

综上，我们看到shares是一个绝对值，需要和其他cgroup的值进行比较才能得到自己的相对限额。

# 查看文件编码
```
vi 文件
然后
:set fileencoding
```

# 查看带宽、流量
1. 查看网络带宽  
ethtool eth0 | grep Speed

2. 查看流量   
Iftop

3. 查看多网卡绑定  
cat /proc/net/bonding/bond0

# man使用
yum install -y man   
yum install -y man-pages  
man命令是Linux下的帮助指令，通过man指令可以查看Linux中的指令帮助、配置文件帮助和编程帮助等信息。  

man(选项)(参数)  
选项   
-a：在所有的man帮助手册中搜索；   
-f：等价于whatis指令，显示给定关键字的简短描述信息；   
-P：指定内容时使用分页程序；   
-M：指定man手册搜索的路径。   
参数   
数字：指定从哪本man手册中搜索帮助；   
关键字：指定要搜索帮助的关键字。  


# free 详解
在介绍Cached与Buffers区别之前，我们先来看看Linux下的内存信息。
```sh
# free
              total        used        free      shared  buff/cache   available
Mem:       16400176     5846976     3617776      723728     6935424     9212468
Swap:             0           0
```
```
　　首先我们来看看上述都表示什么意思：
　　Mem：表示物理内存统计 
　　-/+ buffers/cached：表示物理内存的缓存统计 
　　Swap：表示硬盘上交换分区的使用情况，这里我们不去关心。
　　系统的总物理内存：255988Kb（256M），但系统当前真正可用的内存并不是第一行free 标记的 24284Kb，它仅代表未被分配的内存。

　　我们使用total1、used1、free1、used2、free2 等名称来代表上面统计数据的各值，1、2 分别代表第一行和第二行的数据。

　　total1：表示物理内存总量。 
　　used1：表示总计分配给缓存（包含buffers 与cache ）使用的数量，但其中可能部分缓存并未实际使用。 
　　free1：未被分配的内存。 
　　shared1：共享内存，一般系统不会用到，这里也不讨论。 
　　buffers1：系统分配但未被使用的buffers 数量。 
　　cached1：系统分配但未被使用的cache 数量。buffer 与cache 的区别见后面。 
　　used2：实际使用的buffers 与cache 总量，也是实际使用的内存总量。 
　　free2：未被使用的buffers 与cache 和未被分配的内存之和，这就是系统当前实际可用内存。
　　可以整理出如下等式：

　　　　total1 = used1 + free1
　　　　total1 = used2 + free2
　　　　used1 = buffers1 + cached1 + used2
　　　　free2 = buffers1 + cached1 + free1
　　　　内存利用率 = used2 / total1
```
buffer 与cache 的区别
```
	A buffer is something that has yet to be "written" to disk.
	A cache is something that has been "read" from the disk and stored for later use.
	两者都是RAM中的数据。
```
## 手工释放内存
```
第一步，使用free命令查看内存，这其实没有什么实际作用，就是做个前后对比；
第二步，执行sync命令，是为了确保文件系统的完整性（sync命令将所有未写的系统缓存写到磁盘中）；
第三步，执行echo 3 > /proc/sys/vm/drop_caches就开始释放内存了。

这里说明一下/proc/sys/vm/drop_caches的作用：当写入1时，释放页面缓存；写入2时，释放目录文件和inodes；写入3时，释放页面缓存、目录文件和inodes。可见，整个操作过程就是释放磁盘缓存。
```
## 查看内存硬件
```
find /sys -name meminfo
cat /sys/devices/system/node/node*/meminfo

MemTotal:          45964 kB    //所有可用的内存大小，物理内存减去预留位和内核使用。系统从加电开始到引导完成，firmware/BIOS要预留一些内存，内核本身要占用一些内存，最后剩下可供内核支配的内存就是MemTotal。这个值在系统运行期间一般是固定不变的，重启会改变。
MemFree:            1636 kB    //表示系统尚未使用的内存。
MemAvailable:       8496 kB    //真正的系统可用内存，系统中有些内存虽然已被使用但是可以回收的，比如cache/buffer、slab都有一部分可以回收，所以这部分可回收的内存加上MemFree才是系统可用的内存
Buffers:               0 kB    //用来给块设备做缓存的内存，(文件系统的 metadata、pages)
Cached:             7828 kB    //分配给文件缓冲区的内存,例如vi一个文件，就会将未保存的内容写到该缓冲区
SwapCached:            0 kB    //被高速缓冲存储用的交换空间（硬盘的swap）的大小
Active:            19772 kB    //经常使用的高速缓冲存储器页面文件大小
Inactive:           3128 kB    //不经常使用的高速缓冲存储器文件大小
Active(anon):      15124 kB    //活跃的匿名内存
Inactive(anon):       52 kB    //不活跃的匿名内存
Active(file):       4648 kB    //活跃的文件使用内存
Inactive(file):     3076 kB    //不活跃的文件使用内存
Unevictable:           0 kB    //不能被释放的内存页
Mlocked:               0 kB    //系统调用 mlock 家族允许程序在物理内存上锁住它的部分或全部地址空间。这将阻止Linux 将这个内存页调度到交换空间（swap space），即使该程序已有一段时间没有访问这段空间
SwapTotal:             0 kB    //交换空间总内存
SwapFree:              0 kB    //交换空间空闲内存
Dirty:                 4 kB    //等待被写回到磁盘的
Writeback:             0 kB    //正在被写回的
AnonPages:         15100 kB    //未映射页的内存/映射到用户空间的非文件页表大小
Mapped:             7160 kB    //映射文件内存
Shmem:               100 kB    //已经被分配的共享内存
Slab:               9236 kB    //内核数据结构缓存
SReclaimable:       2316 kB    //可收回slab内存
SUnreclaim:         6920 kB    //不可收回slab内存
KernelStack:        2408 kB    //内核消耗的内存
PageTables:         1268 kB    //管理内存分页的索引表的大小
NFS_Unstable:          0 kB    //不稳定页表的大小
Bounce:                0 kB    //在低端内存中分配一个临时buffer作为跳转，把位于高端内存的缓存数据复制到此处消耗的内存
WritebackTmp:          0 kB    //FUSE用于临时写回缓冲区的内存
CommitLimit:       22980 kB    //系统实际可分配内存
Committed_AS:     536244 kB    //系统当前已分配的内存
VmallocTotal:     892928 kB    //预留的虚拟内存总量
VmallocUsed:       29064 kB    //已经被使用的虚拟内存
VmallocChunk:     860156 kB    //可分配的最大的逻辑连续的虚拟内存
```



# systemctl
查看 systemctl enable 哪些组件
```sh
# systemctl list-unit-files
UNIT FILE                                     STATE   
proc-sys-fs-binfmt_misc.automount             static  
dev-hugepages.mount                           static  
dev-mqueue.mount                              static  
proc-sys-fs-binfmt_misc.mount                 static  
sys-fs-fuse-connections.mount                 static  
sys-kernel-config.mount                       static  
sys-kernel-debug.mount                        static  
tmp.mount                                     disabled
brandbot.path                                 disabled
systemd-ask-password-console.path             static  
systemd-ask-password-plymouth.path            static  
systemd-ask-password-wall.path                static  
session-19716.scope                           static  
session-22053.scope                           static  
session-22372.scope                           static  
session-23364.scope                           static  
session-23977.scope                           static  
session-24260.scope                           static  
session-25275.scope                           static  
session-25445.scope                           static  
session-26637.scope                           static  
session-26646.scope                           static  
session-6089.scope                            static  
arp-ethers.service                            disabled
auditd.service                                enabled 
autovt@.service                               enabled 
blk-availability.service                      disabled
……
```
```
systemctl list-unit-files --state=enabled
```
其它
- 列出所有已经加载的systemd units：`systemctl`
- 列出所有service：`systemctl list-units --type=service`
- 列出所有active状态（运行或退出）的服务：`systemctl list-units --type=service --state=active`
- 列出所有正在运行的服务：`systemctl list-units --type=service --state=running`
- 列出所有正在运行或failed状态的服务：`systemctl list-units --type service --state running,failed`
- 列出所有enabled状态的服务：`systemctl list-unit-files --state=enabled`

# 查看磁盘是否机械盘
```
lsblk -d -o name,rota

NAME    ROTA
nvme0n1    0
sda        1
```
ROTA 为 1 代表是机械盘