#! /bin/bash

curdir=$(cd `dirname $0`; pwd)
cd $curdir

echo 'install sshpass and expect...'
yum install -y sshpass > /dev/null 2>&1
yum install -y expect > /dev/null 2>&1


rpm -qa | grep sshpass || (uname -i | grep aarch64 && test -e ../../group_files/tdsql_common/sshpass-1.06-2.el7.aarch64.rpm && rpm -ivh ../../group_files/tdsql_common/sshpass-1.06-2.el7.aarch64.rpm)
rpm -qa | grep sshpass || (uname -i | grep x86_64  && test -e ../../group_files/tdsql_common/sshpass-1.06-1.el7.x86_64.rpm && rpm -ivh ../../group_files/tdsql_common/sshpass-1.06-1.el7.x86_64.rpm)
