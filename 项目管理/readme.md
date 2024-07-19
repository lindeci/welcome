
XX环境地址：
管理端  https://xxx.com
用户端  https://xxx.com

项目负责人：       联系方式：
技术负责人：       联系方式：
项目管理：         联系方式：
需求负责人：       联系方式：
UI负责人：         联系方式：
后端：             联系方式：
前端：             联系方式：
运维：             联系方式：
数据库：           联系方式：
测试：             联系方式：


项目干系人
角色	部门	人员	职责	电话	企业微信	微信	邮箱
项目经理	行业n部		统筹项目计划、人员…				
售前架构师	行业n部		项目前期信息传递...				
销售/商务	拓展中心	黄凯	项目的销售，负责汇款验收…				
产品交付工程师	南区-区技	林德赐	负责项目中产品交付实施…				
产品交付项目经理	南区-区技		负责项目中产品交付计划和人员的管理…				
客户A-运维							
客户B-业务							
                            
-------------------------------------------------------------------------

0-2项目就绪检查清单（必看）
序号	名称	状态	负责人	对接人	备注
项目基本信息					
1.1	是否完成下单流程走到区域生态交付中心				
1.2	项目相关干系人是否全部收集完毕，相关人员是否获悉项目启动				
1.3	是否召开项目启动会议，交付内容是否清晰	是			
1.4	项目小组人员是否已经明确	是			
1.5	项目主体计划是否已经具备	是			
1.6	实施方案与LLD是否落实到人	是	林德赐		
1.7	硬件上架配置等集成工作是否落实到人	是	胡亚威		
硬件环境					
2.1	机房机柜环境是否准备就绪，DB节点之间以及PROXY节点之间跨交换机（最起码跨机柜）				
2.2	本期涉及的设备（网络设备、服务器、存储等）是否到达安装现场（物理机双网卡绑定+网络通畅）				
2.3	CPU优化建议使用cpupower设置CPU Performance模式：在BIOS(cpu 选项，或者电源管理选项)直接配置为max performance。				
2.4	服务器硬件环境是否已按照产品推荐方案准备完毕（服务器硬件状态正常）				
2.5	涉及的第三方应用服务器是否已安装调试好				
2.6	实施人员在现场的实施条件（工作台、远程网络等）是否已准备好				
2.7	培训资源（场地、设备、设施等）是否已按实施计划准备好				
软件环境					
3.1	操作系统或其他依赖软件是否准备就绪		林德赐		
3.2	是否已经准备好实施所需要的物料（软件包、数据等）		林德赐		
3.3	客户端软件是否安装齐备（浏览器、专用客户端等）				
3.4	交付软件是否符合客户需求（软件版本、功能列表等）				
3.5	用户手册、安装手册、安装盘是否已按合同要求准备齐全	是	林德赐		
3.6	合同中约定的成果物是否已按要求准备就绪				
3.7	实施所需工具是否已准备齐全（各种工具软件及实施的表格、模版等工具）	是	林德赐		
3.8	客户是否已确认实施计划、培训计划和验收测试计划				

-------------------------------------------------------------------------
0-3交付部署步骤（必看+工时填写）
领域	子领域	编号	具体事项	依赖	开始时间	结束时间	部署责任人	验收责任人	状态	升级领导	问题跟进
产品研发	物料包输出	1	"TDSQL已接入腾讯微云，请到微云取物料，微云地址：
https://share.weiyun.com/bwFCEnLe
2020年12月28日后，除非是扩容，以及老中心灾备，不然请使用TDSQL最新版V10.3.16.2.0"
    授权获取	2	"license获取流程：http://km.oa.com/group/tdsql/articles/show/376703
提醒FT行业架构师走申请流程。"
环境准备	信息收集	3	收集服务器数量和服务器配置（填写《1-1服务器配置》）
    部署方案	4	确定集群规模，输出完整的软件部署方案及计划（见《1-3组件混布方案》）
    硬件准备	5	"1.确定服务器数量及硬件配置（CPU优化建议：BIOS使用cpupower设置Performance模式）
2.注意跨机柜上架服务器，至少DB机器要跨机柜。"
    网络配置	6	"准备网络环境，包括、线路连接、交换机配置等工作，保证所有服务器的网络需互通；
服务器建议双网卡bonding；
网络细节规划请咨询相关的网络工程师。
LVS的几台机器要在同一网段，其它资源无同一网段要求。"
    硬盘配置	7	"1、所有机器上的/data分区大小要求200G以上（非DB机器的/data路径大小可以100G）。
2、DB服务器日志磁盘建议(/data1)：如果是sata盘至少硬raid5，不建议raid0。
3、DB服务器数据磁盘建议(/data2)：如果是sata盘做硬raid10，不建议raid0或raid5；如存在多个3T以上nvme盘，建议使用多数据磁盘部署规划。"
    操作系统	8	"1、必须是CentOS7.4以上版本(centos/redhat/kylin建议7.5/7.6/7.7，其他版本未经过充分测试；如手动安装OS,请勾选“ComputerNode/DevelopmentTools组件”)
2、ARM版单独确认。
3、这次使用的是CentOS7.6"
    yum源	9	所有服务器需配置好对应系统的yum源（必要）
    NTP服务	10	部署NTP服务器，所有服务器连接NTP服务器，且必须使用Asia/Shanghai 东八区（UTC+08:00），保证服务器间的时间误差不超过3秒。
    部署规划	11	详细IP及部署模块规划列表。
部署阶段	操作系统与信息确认	12	"1.到现场进行服务器、网络环境和操作系统核对，所有服务器需提前安装好操作系统。
2.主机名(hostname)要改好，不用用缺省的localhost；且/etc/hosts解析也要统一。
3.如每个服务器存在多网卡多网段（例如：一个用于业务流，一个用于管理的情况），请确保多台服务器的网卡devicename与IP网络一一对应，且默认路由出口也要一致。"
    准备数据目录路径	13	"1、DB机器的数据磁盘和日志磁盘，需要单独挂载磁盘；数据磁盘和日志磁盘的大小比例建议6:1~ 3:1 之间（至少6:1，但超过3:1有点浪费，常规业务5:1即可）
2、数据磁盘和日志磁盘文件系统建议用xfs（删除大文件不会带来大IO阻塞）。"
    ansible主控机准备工作	14	"1.把一键部署包上传到主控机上
2.设置主控机到所有机器（包括自己）的ssh免密登录
3.解压一键部署包
4.安装ansible"
    安装TDSQL核心模块	15	"1.修改hosts文件
2.设置系统账号tdsql的密码
3.修改ansible变量
4.执行安装"
    初始化和使用	16	"1.初始化chitu
2.新建集群"
    安装HDFS	17	安装hdfs高可用架构
    安装LVS（可选）	18	LVS的几台机器要在同一网段
    其他可选模块安装	19	多源同步/网关SQL审计
部署后期	基本功能验证	20	创建网关组
        21	创建分布式实例
        22	水平扩容
        23	账号授权
        24	手工备份
        25	慢查询
        26	onlineddl
"验收准备
（交付件）"	功能测试	27	输出功能测试报告（部署文档中的“集群验收 ”章节完成后，再进行测试用例：https://lexiangla.com/teams/k100044/docs/9421aad4222611eab8ba0a58ac131593?company_from=gdc）
    性能测试1	28	"1、输出性能测试报告1（针对非分布式实例，压测模板参见：https://lexiangla.com/teams/k100044/docs/a2d1b4d4f0f211eaafb50a58ac131146?company_from=gdc）
2、请连续压测2~4小时，OS及硬件稳定无故障。"
    性能测试2	29	"输出性能测试报告2（针对分布式实例，压测模板参见：
https://lexiangla.com/teams/k100044/docs/f62c8b6cf0f311eabfec0a58ac135f40?company_from=gdc）"
    高可用测试	30	高可用测试文档（模板参见：https://lexiangla.com/teams/k100044/docs/d2395fb27fb711eaa9c20a58ac1306bb?company_from=gdc）
    POC测试（可选）	31	只针对POC项目需要做此测试（模板参见：https://lexiangla.com/teams/k100044/docs/184cc180222811eaaa6a0a58ac130a12?company_from=gdc）
    数据同步测试	32	"多源同步测试（模板参见：）
https://lexiangla.com/teams/k100044/docs/b8a5e920a65011eab4d90a58ac13260d?company_from=gdc"
    培训	33	客户培训（半天基础培训）
平台试运行	平台试运行（可选）	34	业务上线试运行（可选）
离场巡检	赤兔监控巡检	35	"确保环境正常，离场前，输出赤兔监控巡检报告。
（模板参见：https://docs.qq.com/doc/DTWhLRkJncUlncVJj）"
交付验收	验收离场（必须）	36	"《TDSQL项目离场申请》请客户签字或与客户（行业）邮件确认方可离场。
（模板参见：
https://docs.qq.com/sheet/DTWRUbWNQWEZTaVJM?tab=BB08J2&c=A1A0A0 ）
"
项目转维	产品转维（必须）	37	"产品转维流程：https://lexiangla.com/teams/k100017/docs/2cc33582dba911ea85fc0a58ac132a70?company_from=gdc
区技PM发起转维流程：
发起转维评审会议：区技交付一线+区技PM+行业+交付中心售后"

-------------------------------------------------------------------------
0-4出包记录（必须）
序号	所属产品	物料包分类	操作系统版本	物料包说明	出包时间	变更人	变更时间	当前状态	变更结果
0	TDSQL	全量介质包	CentOS7.6 X64(X86)	V10.3.16.2	2021年5月18日			未更新	成功/失败后回滚/失败待解决
1									

-------------------------------------------------------------------------
服务器配置
各组件的服务器配置要求：									
No.	配置	DB & proxy	ZK	Scheduler/OSS	赤兔/扁鹊	监控 & 采集	LVS	HDFS	KAFKA/ES
1	高性能服务器	Y							
    SSD盘，CPU和内存性能高								
2	普通服务器		Y	Y	Y	Y	Y		
    SAS盘，CPU和内存性能普通								
3	大磁盘容量服务器							Y	


高配物理服务器：适用于DB/PROXY								
项目	描述			数量	RAID及分区设计			
主机	裸金属物理机（华为2288HV5）			3台				
处理器	英特尔至强金牌5218(2.3GHz/16-Core）			2				
内存	32G DDR4			8				
阵列卡	SR150			1				
硬盘1	"960G SSD硬盘
RAID卡：配置2G缓存RAID卡*1，支持RAID 0、1、5、6、50、60、10等，2GB 缓存，含超级电容，含掉电保护。"			2	2块960GB的SSD盘做raid1做系统盘，系统根分区/ 100G，剩下的给/data			
硬盘2	4T-NVMe PCIe SSD硬盘			2	按数据盘：日志盘=4：1的比例划分，将/data1 划分1600G(日志盘，上报时再按照90%），/data2 划分 6400G（数据盘）（上报时再按照90%）			
万兆网卡	1GE电口（X722）*2，10GE光口（X722）*2（满配光模块）			1	业务网双万兆网卡，做bond4			

-------------------------------------------------------------------------
1-3组件混布方案（必须）
集群1：9台服务器部署的规划样例：3个控制节点+3个数据库节点+2个lvs+1个hdfs节点+1个vip。									
集群名：cluster01	虚拟机1	虚拟机2	虚拟机3	虚拟机4	虚拟机5	19.19.8.1	19.19.8.2	19.19.8.3	19.19.8.4
zk	Y	Y	Y						
"chituDB（监控库）
建议规格：2C/4G/100G，最小1C/2G/50G"						Y	Y	Y	
scheduler	Y	Y							
oss		Y	Y						
chitu	Y	Y							
monitor（采集监控）		Y	Y						
db						Y	Y	Y	
proxy						Y	Y	Y	
hdfs									Y
lvs(vip:待补充)				Y	Y				
ansible	Y								
-------------------------------------------------------------------------
部署过程问题记录
序号	所属产品	问题分类	发现时间	反馈人	问题现象	问题定位	解决方案	问题跟进人	进展	出包确认结论
                                        
1										
2										
3										
4										
5										

-------------------------------------------------------------------------
1-5综合布线表
设备名称	主机名	机柜	设备位置	网卡接口	光/电	对应网络	交换机位置	端口	交换机名称	允许VLAN	备注
DB节点01	J5_29U_TDSQL_DB_01	J5	29-30	Eth3	电口	管理网	J5机柜41U		J5-CE5855-MGMT-01		lacp-mode4
    J5_29U_TDSQL_DB_01	J5	29-30	Eth4	电口	管理网	J7机柜41U		J7-CE5855-MGMT-01		
    J5_29U_TDSQL_DB_01	J5	29-30	slot2-1	光口	业务网络	J5机柜45U		J5-CE6820-DATA-01		lacp-mode4
    J5_29U_TDSQL_DB_01	J5	29-30	3eth-1	光口	业务网络	J7机柜45U		J7-CE6820-DATA-01		
    J5_29U_TDSQL_DB_01	J5	29-30	IPMI	电口	带外管理	J6机柜45U		J6-CE5855-BMC-01	vlan 100	
DB节点02	J6_26U_TDSQL_DB_02	J6	26-29	Eth3	电口	管理网	J5机柜41U		J5-CE5855-MGMT-01		lacp-mode4
    J6_26U_TDSQL_DB_02	J6	26-29	Eth4	电口	管理网	J7机柜41U		J7-CE5855-MGMT-01		
    J6_26U_TDSQL_DB_02	J6	26-29	slot2-1	光口	业务网络	J5机柜45U		J5-CE6820-DATA-01		lacp-mode4
    J6_26U_TDSQL_DB_02	J6	26-29	3eth-1	光口	业务网络	J7机柜45U		J7-CE6820-DATA-01		
    J6_26U_TDSQL_DB_02	J6	26-29	IPMI	电口	带外管理	J6机柜45U		J6-CE5855-BMC-01	vlan 100	
DB节点03	J7_26U_TDSQL_DB_03	J7	26-27	Eth3	电口	管理网	J5机柜41U		J5-CE5855-MGMT-01		lacp-mode4
    J7_26U_TDSQL_DB_03	J7	26-27	Eth4	电口	管理网	J7机柜41U		J7-CE5855-MGMT-01		
    J7_26U_TDSQL_DB_03	J7	26-27	slot2-1	光口	业务网络	J5机柜45U		J5-CE6820-DATA-01		lacp-mode4
    J7_26U_TDSQL_DB_03	J7	26-27	3eth-1	光口	业务网络	J7机柜45U		J7-CE6820-DATA-01		
    J7_26U_TDSQL_DB_03	J7	26-27	IPMI	电口	带外管理	J6机柜45U		J6-CE5855-BMC-01	vlan 100	
DB冷备节点	J7_29U_TDSQL_BK_01	J7	29-30	Eth3	电口	管理网	J5机柜41U		J5-CE5855-MGMT-01		lacp-mode4
    J7_29U_TDSQL_BK_01	J7	29-30	Eth4	电口	管理网	J7机柜41U		J7-CE5855-MGMT-01		
    J7_29U_TDSQL_BK_01	J7	29-30	slot2-1	光口	业务网络	J5机柜45U		J5-CE6820-DATA-01		lacp-mode4
    J7_29U_TDSQL_BK_01	J7	29-30	3eth-1	光口	业务网络	J7机柜45U		J7-CE6820-DATA-01		
    J7_29U_TDSQL_BK_01	J7	29-30	IPMI	电口	带外管理	J6机柜45U		J6-CE5855-BMC-01	vlan 100	

-------------------------------------------------------------------------
2-1交付环境信息（组件版本登记）
 TDSQL： v10.3.16.2.0版本										
服务器组件	DB / Proxy	ZK	SCH/OSS	赤兔/扁鹊	监控/采集	LVS	ansible	HDFS	kafka	Consumer
各组件版本登记	"DB：
MySQL5.7：5.7.33-V2.0R681D005-v17-20210125-2105-log"	Zookeeper：3.4.14	"Scheduler：1.16.0-TDSQL-KEEPER-V2.0R710D003MERGE16.1
"	"赤兔管理台：V1.8.6-bcac6d2d
赤兔-Web：nginx/1.19.0
赤兔-PHP：7.2.33
扁鹊：1.4"	Monitor：分离版本V16	LVS：				
    "Proxy： 1.16.7-M-V2.0R703D0038112120
"		Manager：1.16.0-TDSQL-KEEPER-V2.0R710D003MERGE16.1							
    Agent：AGENT-V3.0R012D0038110959		OSS：OSS-V2.0-V10 0R030D004B111209-YUN&MIG@16.0.4-compable							
机型	安装包目录	数据目录	日志目录	数据库程序目录						
TS85(例)	/data/home/tdsql/tdsqlinstall	/data2/tdengine/dat	/data1/tdengine/log	/data/tdsql_run						

-------------------------------------------------------------------------
2-2模块启停手册

                            
    agent	MySQL	网关	LVS			
目录	/data/tdsql_run/4001/mysqlagent/bin	"MySQL5.7：/data/tdsql_run/4001/percona-5.7.17/install
MySQL8.0：/data/tdsql_run/4001/mysql-server-8.0.18/install/"	/data/tdsql_run/15001/gateway/bin	/data/application/lvsmanager/bin			
启动	./startreport_cgroup.sh ../conf/mysqlagent_4001.xml	./startmysql_cgroup.sh 4001	./start_cgroup.sh instance_15001	./startlvsmanager.sh ../conf/lvsmanager.xml			
停止	./stoptreport_cgroup.sh ../conf/mysqlagent_4001.xml	./stopmysql_cgroup.sh 4001	./stop.sh instance_15001	./stoplvsmanager.sh ../conf/lvsmanager.xml			
重启	./restartreport_cgroup.sh ../conf/mysqlagent_4001.xml	./restartmysql_cgroup.sh 4001	./restart_cgroup.sh instance_15001	./restartlvsmanager.sh ../conf/lvsmanager.xml			
        连接MySQL ./jmysql.sh 4001					
                            
                            
                            
    Scheduler	OSS	ZK	赤兔	采集	监控	扁鹊
目录	/data/application/scheduler/bin	/data/application/oss/boot/	/data/application/zookeeper/bin/		/data/application/tdsql_collector/bin	/data/application/tdsql_analysis/bin	/data/application/clouddba/bin
启动	/start_manager.sh	./start.sh	./zkServer.sh start	"/usr/local/php/sbin/php-fpm -y /usr/local/php/etc/php-fpm.conf -c /usr/local/php/lib/php.ini
;  /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf"	./start.sh	./start.sh	./start.sh ../conf/diagnosis.conf
停止	./stop_manager.sh	./stop.sh	./zkServer.sh stop	"pkill nginx;
pkill php-fpm"	./stop.sh	./stop.sh	./stop.sh ../conf/diagnosis.conf
重启			./zkServer.sh restart		./restart.sh	./restart.sh	./restart.sh ../conf/diagnosis.conf
                            
                            
                            
    kafka	OnlineDDL	producter	consumer			
目录	/data/application/kafka/bin	/data/application/onlineddl/bin/	 /data/tdsql_run/4001/mysqlagent/bin	 /data/application/consumer/bin/			
启动	"./kafka-server-start.sh -daemon 
../config/server.properties"	"./ddlperformermng
--zklist={{ hostvars.zk1.ansible_ssh_host }}:2118
 --zkrootpath={{ zk_rootdir }} --dev={{ netif_name }}"	./startbinlogproduct.sh ../conf/mysqlagent_4001.xml	"./binlogconsumermgn --zklist 10.240.139.35:2118 
--zkrootpath /noshard1 --kafkazklist 10.240.139.35:2118 
--kafkazkrootpath /kafka --dev eth1"			
停止	"./kafka-server-stop.sh -daemon 
../config/server.properties"	kill -9 进程号	./stopbinlogproduct.sh ../conf/mysqlagent_4001.xml	kill -9 进程号			
重启			./restartbinlogproduct.sh ../conf/mysqlagent_4001.xml				
                            

-------------------------------------------------------------------------

比如mysql环境信息

生产环境
编号  数据中心 机柜 U位 IP 机器账号  机器密码 数据库账号 数据库密码 库名.表名 应用连接串 部署目录 客户端命令 启动命令 关闭命令 备注 项目-库 项目负责人 库负责人 对应同步链路 对应高可用组件