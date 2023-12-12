- [iostat](#iostat)
- [iostat 的来源](#iostat-的来源)
- [iotop](#iotop)
- [df](#df)
- [fio](#fio)
  - [测试随机写](#测试随机写)
  - [测试顺序写](#测试顺序写)
- [查看io调度策略](#查看io调度策略)
- [查看磁盘自动挂载](#查看磁盘自动挂载)
- [Linux下查看Raid磁盘阵列信息的方法](#linux下查看raid磁盘阵列信息的方法)
- [linux字符集相关：](#linux字符集相关)
- [服务器重启如何判断](#服务器重启如何判断)
- [查看OS对进程资源限制](#查看os对进程资源限制)
- [查看端口被谁占用](#查看端口被谁占用)
- [OOM](#oom)
- [瓶颈排查](#瓶颈排查)

# iostat
`iostat -dxmct 1 -p vda`
```sh
04/16/2022 02:55:35 AM
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.00    0.00    0.25    0.00    0.00   99.75

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
vda              0.00    2.00      0.00     56.00     0.00    12.00   0.00  85.71    0.00    1.00   0.00     0.00    28.00   1.50   0.30
vda1             0.00    2.00      0.00     56.00     0.00    12.00   0.00  85.71    0.00    1.00   0.00     0.00    28.00   1.50   0.30

其中 wareq-sz:28.00 * w/s:2.00=wkB/s:56.00
```
# iostat 的来源
`cat /proc/diskstats`

# iotop
`iotop -oP -d 1`  
可以接着按键盘的<-或者->方向键控制排序字段

`pidstat -d 1 -H -h -l -p 69554 -r -s -w -v -u -t`
```sh
# Time        UID      TGID       TID    %usr %system  %guest   %wait    %CPU   CPU  minflt/s  majflt/s     VSZ     RSS   %MEM StkSize  StkRef   kB_rd/s   kB_wr/s kB_ccwr/s iodelay   cswch/s nvcswch/s threads   fd-nr  Command
1650053639     27     69554         -    0.00    0.00    0.00    0.00    0.00     3      0.00      0.00 3584124  522684   6.57     132      60      0.00      0.00      0.00       0      0.00      0.00      41      41  /usr/libexec/mysqld --basedir=/usr 
1650053639     27         -     69554    0.00    0.00    0.00    0.00    0.00     3      0.00      0.00 3584124  522684   6.57     132      60      0.00      0.00      0.00       0      0.00      0.00      41      41  |__/usr/libexec/mysqld --basedir=/usr 
1650053639     27         -     69564    0.00    0.00    0.00    1.00    0.00     0      0.00      0.00 3584124  522684   6.57     132      60      0.00      0.00      0.00       0      2.00      0.00      41      41  |__/usr/libexec/mysqld --basedir=/usr 
1650053639     27         -     69565    0.00    0.00    0.00    0.00    0.00     3      0.00      0.00 3584124  522684   6.57     132      60      0.00      0.00      0.00       0      2.00      0.00      41      41  |__/usr/libexec/mysqld --basedir=/usr 
1650053639     27         -     69566    0.00    0.00    0.00    0.00    0.00     0      0.00      0.00 3584124  522684   6.57     132      60      0.00      0.00      0.00       0      2.00      0.00      41      41  |__/usr/libexec/mysqld --basedir=/usr 
1650053639     27         -     69567    0.00    0.00    0.00    0.00    0.00     2      0.00      0.00 3584124  522684   6.57     132      60      0.00      0.00      0.00       0      2.00      0.00      41      41  |__/usr/libexec/mysqld --basedir=/usr 
1650053639     27         -     69568    0.00    0.00    0.00    0.00    0.00     2      0.00      0.00 3584124  522684   6.57     132      60      0.00      0.00      0.00       0      2.00      0.00      41      41  |__/usr/libexec/mysqld --basedir=/usr 
1650053639     27         -   1932682    0.00    0.00    0.00    0.00    0.00     3      0.00      0.00 3584124  522684   6.57     132      60      0.00      0.00      0.00       0      0.00      0.00      41      41  |__/usr/libexec/mysqld --basedir=/usr 
```
# df
`df -hT`
# fio
## 测试随机写
`fio --name=randwrite --runtime=1200 --group_reporting --allow_mounted_write=1 --ioengine=libaio --iodepth=64 --numjobs=1 --rate_iops=5000 --direct=1  --rw=randwrite --bs=16k --size=2G --filename=/tmp/fio`
```sh
randwrite: (g=0): rw=randwrite, bs=(R) 16.0KiB-16.0KiB, (W) 16.0KiB-16.0KiB, (T) 16.0KiB-16.0KiB, ioengine=libaio, iodepth=64
fio-3.19
Starting 1 process
Jobs: 1 (f=1), 0-5000 IOPS: [w(1)][41.4%][w=33.9MiB/s][w=2169 IOPS][eta 00m:34s]
Jobs: 1 (f=1), 0-5000 IOPS: [w(1)][100.0%][w=34.4MiB/s][w=2199 IOPS][eta 00m:00s]
randwrite: (groupid=0, jobs=1): err= 0: pid=3374302: Sat Apr 16 04:39:11 2022
  write: IOPS=2225, BW=34.8MiB/s (36.5MB/s)(2048MiB/58904msec); 0 zone resets
    slat (usec): min=2, max=34102, avg=16.69, stdev=290.13
    clat (usec): min=561, max=113234, avg=28449.81, stdev=5166.25
     lat (usec): min=571, max=113247, avg=28466.65, stdev=5161.78
    clat percentiles (usec):
     |  1.00th=[  955],  5.00th=[27132], 10.00th=[27919], 20.00th=[28181],
     | 30.00th=[28705], 40.00th=[28705], 50.00th=[28967], 60.00th=[28967],
     | 70.00th=[29230], 80.00th=[29492], 90.00th=[30278], 95.00th=[31851],
     | 99.00th=[36439], 99.50th=[46924], 99.90th=[60031], 99.95th=[61604],
     | 99.99th=[66323]
   bw (  KiB/s): min=33088, max=79309, per=99.83%, avg=35539.80, stdev=4108.71, samples=117
   iops        : min= 2068, max= 4956, avg=2221.23, stdev=256.72, samples=117
  lat (usec)   : 750=0.19%, 1000=0.99%
  lat (msec)   : 2=1.07%, 4=0.28%, 10=0.23%, 20=0.25%, 50=96.58%
  lat (msec)   : 100=0.42%, 250=0.01%
  cpu          : usr=1.68%, sys=4.69%, ctx=116103, majf=0, minf=11
  IO depths    : 1=0.2%, 2=0.3%, 4=0.6%, 8=0.7%, 16=0.7%, 32=0.2%, >=64=97.4%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.1%, >=64=0.0%
     issued rwts: total=0,131072,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=64

Run status group 0 (all jobs):
  WRITE: bw=34.8MiB/s (36.5MB/s), 34.8MiB/s-34.8MiB/s (36.5MB/s-36.5MB/s), io=2048MiB (2147MB), run=58904-58904msec

Disk stats (read/write):
  vda: ios=6/130980, merge=0/5534, ticks=0/3709315, in_queue=3709315, util=99.93%
```  
## 测试顺序写

`fio --filename=/tmp/test.big -iodepth=32 -ioengine=libaio -direct=1 -rw=write -bs=256k -size=2g -numjobs=4 -runtime=60 -group_reporting -name=test-write  -time_based`
```sh
test-write: (g=0): rw=write, bs=(R) 256KiB-256KiB, (W) 256KiB-256KiB, (T) 256KiB-256KiB, ioengine=libaio, iodepth=32
...
fio-3.19
Starting 4 processes
test-write: Laying out IO file (1 file / 2048MiB)
Jobs: 4 (f=4): [W(4)][100.0%][w=107MiB/s][w=429 IOPS][eta 00m:00s]
test-write: (groupid=0, jobs=4): err= 0: pid=3375109: Sat Apr 16 04:44:59 2022
  write: IOPS=437, BW=109MiB/s (115MB/s)(6599MiB/60298msec); 0 zone resets
    slat (usec): min=9, max=297767, avg=180.75, stdev=6594.87
    clat (msec): min=2, max=596, avg=291.97, stdev=69.39
     lat (msec): min=2, max=596, avg=292.15, stdev=69.11
    clat percentiles (msec):
     |  1.00th=[   15],  5.00th=[  159], 10.00th=[  296], 20.00th=[  296],
     | 30.00th=[  296], 40.00th=[  296], 50.00th=[  296], 60.00th=[  300],
     | 70.00th=[  300], 80.00th=[  300], 90.00th=[  300], 95.00th=[  334],
     | 99.00th=[  542], 99.50th=[  567], 99.90th=[  592], 99.95th=[  592],
     | 99.99th=[  592]
   bw (  KiB/s): min=22528, max=260371, per=99.55%, avg=111557.20, stdev=7412.04, samples=479
   iops        : min=   88, max= 1015, avg=435.75, stdev=28.93, samples=479
  lat (msec)   : 4=0.09%, 10=0.22%, 20=1.56%, 50=1.02%, 100=0.99%
  lat (msec)   : 250=2.93%, 500=91.44%, 750=1.76%
  cpu          : usr=0.17%, sys=0.30%, ctx=24577, majf=0, minf=63
  IO depths    : 1=0.1%, 2=0.1%, 4=0.1%, 8=0.1%, 16=0.2%, 32=99.5%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.1%, 64=0.0%, >=64=0.0%
     issued rwts: total=0,26395,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=32

Run status group 0 (all jobs):
  WRITE: bw=109MiB/s (115MB/s), 109MiB/s-109MiB/s (115MB/s-115MB/s), io=6599MiB (6919MB), run=60298-60298msec

Disk stats (read/write):
  vda: ios=6/26400, merge=0/166, ticks=0/7486590, in_queue=7486591, util=99.92%
```
# 查看io调度策略
`cat /sys/block/vda/queue/scheduler`  
[mq-deadline] kyber bfq none
# 查看磁盘自动挂载
```sh
cat /etc/fstab 
/dev/mapper/centos-home /data                   xfs     defaults        0 0
/dev/mapper/centos-swap swap                    swap    defaults        0 0
```

# Linux下查看Raid磁盘阵列信息的方法
以下是组建服务器raid时查到的资料，做下笔记，没兴趣的朋友请无视。  
Linux下查看软、硬raid信息的方法。  
软件raid：只能通过Linux系统本身来查看

`cat /proc/mdstat`

可以看到raid级别，状态等信息。 
硬件raid： 最佳的办法是通过已安装的raid厂商的管理工具来查看，有cmdline，也有图形界面。如Adaptec公司的硬件卡就可以通过下面的命令进行查看：

`/usr/dpt/raidutil -L all`

可以看到非常详细的信息。  
当然更多情况是没有安装相应的管理工具，只能依靠Linux本身的话一般我知道的是两种方式：  
`dmesg |grep -i raid`和`cat /proc/scsi/scsi`

显示的信息差不多，raid的厂商，型号，级别，但无法查看各块硬盘的信息。  
另外经过实际测试，Dell的服务器可以通过命令来显示，而HP、IBM等的服务器通过上面的命令是显示不出的。只能够通过装硬件厂商的管理工具来查看DELL的BMC可以查看。  

`cat /proc/scsi/scsi`

可以看到是SCSI上的设备。一般情况可以看到RAID级别。lspci可以看到RAID卡的型号。
```sh
rpm -ivh MegaCli-1.01.09-0.i386.rpm

命令使用：
MegaCli -LDInfo -Lall -aALL 查raid级别
MegaCli -AdpAllInfo -aALL 查raid卡信息
MegaCli -PDList -aALL 查看硬盘信息
MegaCli -AdpBbuCmd -aAll 查看电池信息
MegaCli -FwTermLog -Dsply -aALL 查看raid卡日志

MegaCli常用参数介绍
MegaCli -adpCount 【显示适配器个数】
MegaCli -AdpGetTime –aALL 【显示适配器时间】
MegaCli -AdpAllInfo -aAll 【显示所有适配器信息】
MegaCli -LDInfo -LALL -aAll 【显示所有逻辑磁盘组信息】
MegaCli -PDList -aAll 【显示所有的物理信息】
MegaCli -AdpBbuCmd -GetBbuStatus -aALL |grep ‘Charger Status‘【查看充电状态】
MegaCli -AdpBbuCmd -GetBbuStatus -aALL【显示BBU状态信息】
MegaCli -AdpBbuCmd -GetBbuCapacityInfo -aALL【显示BBU容量信息】
MegaCli -AdpBbuCmd -GetBbuDesignInfo -aALL 【显示BBU设计参数】
MegaCli -AdpBbuCmd -GetBbuProperties -aALL 【显示当前BBU属性】
MegaCli -cfgdsply -aALL 【显示Raid卡型号，Raid设置，Disk相关信息】
```
磁带状态的变化，从拔盘，到插盘的过程中。
```sh
Device |Normal|Damage|Rebuild|Normal
Virtual Drive |Optimal|Degraded|Degraded|Optimal
Physical Drive |Online|Failed –> Unconfigured|Rebuild|Online
```

# linux字符集相关：
```sh
vim
:set ff  查看当前文本的模式类型，一般为dos,unix
:set ff=dos  设置为dos模式， 也可以用 sed -i 's/$/\r/' 
:set ff=unix  设置为unix模式，也可以用一下方式转换为unix模式:sed -i 's/.$//g'
 
 
:set fileencoding查看现在文本的编码
:set fenc=编码  转换当前文本的编码为指定的编码
:set enc=编码  以指定的编码显示文本，但不保存到文件中。
```

# 服务器重启如何判断
除了看日志和 vmcore，还要考虑硬件的问题。  
我遇到过两次硬件问题，一次是机柜送风口被遮住了导致温度过高，一次是内存条有问题。  
温度监控可以提前添加到 zabbix 之类的监控平台，也可以看 IPMI。  
内存检测可以用 memtest 做个可启动优盘。也可以往 /dev/shm 里写数据，同时查看内存错误计数。  
查看内存错误计数： `grep "[0-9]" /sys/devices/system/edac/mc/mc*/csrow*/ch*ce_count`​

# 查看OS对进程资源限制
`prlimit --pid=3945138`
```sh
RESOURCE   DESCRIPTION                             SOFT      HARD UNITS
AS         address space limit                unlimited unlimited bytes
CORE       max core file size                 unlimited unlimited bytes
CPU        CPU time                           unlimited unlimited seconds
DATA       max data size                      unlimited unlimited bytes
FSIZE      max file size                      unlimited unlimited bytes
LOCKS      max number of file locks held      unlimited unlimited locks
MEMLOCK    max locked-in-memory address space     65536     65536 bytes
MSGQUEUE   max bytes in POSIX mqueues            819200    819200 bytes
NICE       max nice prio allowed to raise             0         0 
NOFILE     max number of open files               10000     10000 files
NPROC      max number of processes                30945     30945 processes
RSS        max resident set size              unlimited unlimited bytes
RTPRIO     max real-time priority                     0         0 
RTTIME     timeout for real-time tasks        unlimited unlimited microsecs
SIGPENDING max number of pending signals          30945     30945 signals
STACK      max stack size                       8388608 unlimited bytes
```
==============================================================================================================================================================================
# 查看端口被谁占用
`lsof -i tcp:3306`

# OOM
对照一个OOM实例并解析如下：
```sh
1. [19174.926798] copy invoked oom-killer: gfp_mask=0x24200c8(GFP_USER|__GFP_MOVABLE), nodemask=0, order=0, oom_score_adj=0--------参考dump_header()，输出OOM产生现场线程信息，包括分配掩码、OOM信息。 
2. [19174.937586] CPU: 0 PID: 163 Comm: copy Not tainted 4.9.56 #1---------参考show_stack()，显示栈信息。可以看出OOM现场的调用信息，这里可以看出是CMA分配出发了OOM。 
[19174.943274]  
Call Trace: 
[<802f63c2>] dump_stack+0x1e/0x3c 
[<80132224>] dump_header.isra.6+0x84/0x1a0 
[<800f2d68>] oom_kill_process+0x23c/0x49c 
[<800f32fc>] out_of_memory+0xb0/0x3a0 
[<800f7834>] __alloc_pages_nodemask+0xa84/0xb5c 
[<801306b8>] alloc_migrate_target+0x34/0x6c 
[<8012f30c>] migrate_pages+0x108/0xbe4 
[<800f8a0c>] alloc_contig_range+0x188/0x378 
[<80130c54>] cma_alloc+0x100/0x220 
[<80388fe2>] dma_alloc_from_contiguous+0x2e/0x48 
[<8037bb30>] xxxxx_dma_alloc_coherent+0x48/0xdc 
[<8037be8c>] mem_zone_ioctl+0xf0/0x198 
[<80148cec>] do_vfs_ioctl+0x84/0x70c 
[<80149408>] SyS_ioctl+0x94/0xb8 
[<8004a246>] csky_systemcall+0x96/0xe0 
3. [19175.001223] Mem-Info:------------参考show_mem()，输出系统内存详细使用情况。这里可以看出free=592很少，active_anon和shmem非常大。 
[19175.003535] active_anon:99682 inactive_anon:12 isolated_anon:1----------显示当前系统所有node不同类型页面的统计信息，单位是页面。 
[19175.003535]  active_file:55 inactive_file:75 isolated_file:0 
[19175.003535]  unevictable:0 dirty:0 writeback:0 unstable:0 
[19175.003535]  slab_reclaimable:886 slab_unreclaimable:652 
[19175.003535]  mapped:2 shmem:91862 pagetables:118 bounce:0 
[19175.003535]  free:592 free_pcp:61 free_cma:0 
[19175.035394] Node 0 active_anon:398728kB inactive_anon:48kB active_file:220kB inactive_file:300kB unevictable:0kB isolated(anon):4kB isolated(file):0kB mapped:8kB dirty:0kB writeback:0kB shmem:367448kB writeback_tmp:0kB unstable:0kB pages_scanned:2515 all_unreclaimable? yes
#NAME?
[19175.059602] Normal free:2368kB min:2444kB low:3052kB high:3660kB active_anon:398728kB inactive_anon:48kB active_file:220kB inactive_file:300kB unevictable:0kB writepending:0kB present:1048572kB managed:734584kB mlocked:0kB slab_reclaimable:3544kB slab_unreclaimable:2608kB kernel_stack:624kB pagetables:472kB bounce:0kB free_pcp:244kB local_pcp:244kB free_cma:0kB
#NAME?
[19175.091602] lowmem_reserve[]: 0 0 0 
[19175.095144] Normal: 21*4kB (MHI) 14*8kB (MHI) 13*16kB (HI) 2*32kB (HI) 4*64kB (MI) 2*128kB (MH) 0*256kB 2*512kB (HI) 1*1024kB (H) 1*2048kB (I) 0*4096kB = 5076kB
#NAME?
91996 total pagecache pages 
[19175.112370] 262143 pages RAM 
[19175.115254] 0 pages HighMem/MovableOnly 
[19175.119106] 78497 pages reserved 
[19175.122350] 90112 pages cma reserved 
4. [19175.125942] [ pid ]   uid  tgid total_vm      rss nr_ptes nr_pmds swapents oom_score_adj name-----------参考dump_tasks(),输出系统可被kill的进程内存使用情况。 
[19175.134514] [  135]     0   135     1042       75       4       0        0         -1000 sshd 
[19175.143070] [  146]     0   146      597      141       3       0        0             0 autologin 
[19175.152057] [  147]     0   147      608      152       4       0        0             0 sh 
[19175.160434] [  161]     0   161   109778     7328     104       0        0             0 xxxxx 
5. [19175.169068] Out of memory: Kill process 161 (xxxxx) score 39 or sacrifice child---------------因为OOM待kill的进程信息。 
6. [19175.176439] Killed process 161 (xxxxx) total-vm:439112kB, anon-rss:29304kB, file-rss:8kB, shmem-rss:0kB----------已经发送信号SIGKILL强制退出的进程信息。
通过上面的信息可以知道是哪个进程、OOM现场、哪些内存消耗太多。

这里需要重点查看系统的active_anon和shmem为什么如此大，造成了OOM。
```
===============
# 瓶颈排查
```sh
网络带宽、延时、堆积丢包重传；
cpu单核单线程； sys比例；
磁盘iops、带宽、iowait；
内存swap；

系统基本信息；
```