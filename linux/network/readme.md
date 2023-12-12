- [查看链路](#查看链路)
- [查看流量](#查看流量)
- [查看连接数](#查看连接数)
- [查看每个IP地址连接数](#查看每个ip地址连接数)
- [查看防火墙](#查看防火墙)
- [查看iptables](#查看iptables)
- [查看dns](#查看dns)
- [查看hosts](#查看hosts)

# 查看链路
traceroute xx.xx.xx.xx

# 查看流量
iftop -B -i eth0

# 查看连接数
cat /proc/sys/fs/file-nr
# 查看每个IP地址连接数
netstat -na | grep ESTABLISHED | awk '{print$5}' | awk -F : '{print$1}' |sort |uniq -c | sort -r

# 查看防火墙
getenforce

# 查看iptables
iptables -L

# 查看dns
cat /etc/resolv.conf

# 查看hosts
cat /etc/hosts