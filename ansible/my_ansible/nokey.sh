#! /bin/bash

curdir=$(cd `dirname $0`; pwd)
cd $curdir

#bash install_sshpass.sh

rm -rf /root/.ssh/id_rsa /root/.ssh/id_rsa.pub /root/.ssh/known_hosts

expect -c "
spawn ssh-keygen

expect {
\"Enter file in which to save the key (/root/.ssh/id_rsa):\" {send \"\r\"; exp_continue}
\"Enter passphrase (empty for no passphrase):\" {send \"\r\"; exp_continue}
\"Enter same passphrase again:\" {send \"\r\"; exp_continue}
}"  #免交互执行ssh-keygen


ipcount=`cat ip_passwd_list|wc -l`

i=1
#for ((i=1;i<=$ipcount;i++));
while [ $i -le $ipcount ]
do

ip="cat ip_passwd_list |awk '{print \$1}'|head -n $i|tail -n 1"
passwd="cat ip_passwd_list |awk '{print \$2}'|head -n $i|tail -n 1"

ip_eval=$(eval $ip)
passwd_eval=$(eval $passwd)
#echo $ip_eval
#echo $passwd_eval

expect -c "
spawn ssh $ip_eval -o StrictHostKeyChecking=no 

expect {
\"(yes/no)\" {send \"yes\r\"; exp_continue}
\"password:\" {send \"$passwd_eval\r\"; exit}
}"


echo $passwd_eval > /tmp/.nokey_pass
#shpass -p$ ssh 10.20.0.17 'cat >> ~/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub  示例
cp_pub_key="sshpass -f /tmp/.nokey_pass ssh $ip_eval 'mkdir -p .ssh && cat >> ~/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub"
#echo $cp_pub_key
eval $cp_pub_key
i=$((i+1))
done
rm -rf /tmp/.nokey_pass
