- [ansible脚本](#ansible脚本)
- [tdsql\_beginning/tasks/main.yml内容](#tdsql_beginningtasksmainyml内容)
- [tdsql\_filebeat\_helper](#tdsql_filebeat_helper)
- [install\_filebeat\_helper.sh内容](#install_filebeat_helpersh内容)
- [tdsql\_es7内容](#tdsql_es7内容)
- [install\_es7.sh内容](#install_es7sh内容)
- [初始化机器脚本](#初始化机器脚本)

# ansible脚本
ansible-playbook -i tdsql_hosts playbooks/tdsql_es7.yml

tdsql_install/playbooks/tdsql_es7.yml内容
```sh
---
- name: install es beginning
  hosts: tdsql_es
  remote_user: root
  gather_facts: false
  roles:
    - tdsql_beginning

- name: install filebeat_helper on proxy
  hosts: tdsql_proxy
  remote_user: root
  gather_facts: false
  roles:
    - tdsql_filebeat_helper

- name: install filebeat_helper on es
  hosts: tdsql_es
  remote_user: root
  gather_facts: false
  roles:
    - tdsql_filebeat_helper

- name: install es7 server
  hosts: tdsql_es
  remote_user: root
  gather_facts: false
  roles:
    - tdsql_es7

- name: update conf on clouddba
  hosts: tdsql_chitu1
  remote_user: root
  gather_facts: false
  roles:
    - tdsql_update_clouddba


- name: init filebeat_helper on proxy
  hosts: tdsql_proxy
  remote_user: root
  gather_facts: false
  vars:
    tdsql_need_import_ndjson_var: true
  roles:
    - tdsql_filebeat_init
```

# tdsql_beginning/tasks/main.yml内容 
tdsql_install/playbooks/roles/tdsql_beginning/tasks/main.yml内容
```sh
---
- name: set umask 0022 on /etc/profile
  shell: " grep 'umask 0022 # TDSQL UMASK SET' /etc/profile || echo 'umask 0022 # TDSQL UMASK SET' >> /etc/profile ; cd / "

- name: set umask 0022 on /etc/bashrc
  shell: " grep 'umask 0022 # TDSQL UMASK SET' /etc/bashrc || echo 'umask 0022 # TDSQL UMASK SET' >> /etc/bashrc ; cd / "

- name: create the directory
  shell: "test -e /data/tools/.beginning_finished && exit 0; umask 0022; mkdir -p /data/tools /data/application /data/application/pycrond /data/home/tdsql /data/hadoop/tmp/journal ; chmod 755 /data/tools /data/application /data/application/pycrond /data/home /data/home/tdsql /data/hadoop /data/hadoop/tmp /data/hadoop/tmp/journal; cd /"

- name: ansible local create the directory
  shell: "mkdir -p /data/tools "
  connection: local
  run_once: true

- name: set tdsql_uid=6666 when not defined
  set_fact:
    tdsql_uid: '6666'
  when: tdsql_uid is not defined

- name: set 1 node tdsql_zk_list
  set_fact:
    tdsql_zk_list: "{{ tdsql_zk_domain_name }}1:{{ tdsql_zk_clientport }}"
  when: groups['tdsql_zk'] | length | int == 1

- name: set 3 nodes tdsql_zk_list
  set_fact:
    tdsql_zk_list: "{{ tdsql_zk_domain_name }}1:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}2:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}3:{{ tdsql_zk_clientport }}"
  when: groups['tdsql_zk'] | length | int == 3

- name: set 5 nodes tdsql_zk_list
  set_fact:
    tdsql_zk_list: "{{ tdsql_zk_domain_name }}1:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}2:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}3:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}4:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}5:{{ tdsql_zk_clientport }}"
  when: groups['tdsql_zk'] | length | int == 5

################# 安装依赖包 #####################
- name: copy the tdsql_common
  synchronize:
    src: "{{ playbook_dir }}/../../group_files/tdsql_common/"
    dest: /data/tools/

- name: copy the tdsql_lib
  synchronize:
    src: "{{ playbook_dir }}/../../group_files/tdsql_lib/"
    dest: /data/tools/

- name: copy the init_env_packet.sh and init_env_make.sh to dest host
  template:
    backup: no
    force: yes
    src: "../files/shell_scripts/{{ item }}"
    dest: /data/tools/
  with_items: ['init_env_make.sh', 'init_env_packet.sh']

- name: do init_env_packet.sh
  shell: "/bin/bash /data/tools/init_env_packet.sh"

- name: do init_env_make.sh
  shell: "/bin/bash /data/tools/init_env_make.sh"

- name: copy the fiotest.sh to the dst host
  synchronize:
    src: "../files/shell_scripts/fiotest.sh"
    dest: /data/tools/
################# 安装依赖包 #####################


######## install python3 & python tools ########
- name: copy the tdsql_python to the dst host
  synchronize:
    src: "{{ playbook_dir }}/../../group_files/tdsql_python/"
    dest: /data/tools/

- name: copy the install_python3.sh to the dst host
  synchronize:
    src: "../files/shell_scripts/install_python.sh"
    dest: /data/tools/

- name: install python3
  shell: "/bin/bash /data/tools/install_python.sh"
######## install python3 & python tools ########



##### set os param and create tdsql user #######
- name: generate the init_os_para.sh on dest host
  template:
    backup: no
    force: yes
    src: "../files/shell_scripts/init_os_para.j2"
    dest: /data/tools/init_os_para.sh

- name: do init_os_para.sh
  shell: "/bin/bash /data/tools/init_os_para.sh"
##### set os param and create tdsql user #######



######## install jdk ###############

# 设置jdk环境变量
- name: local read profile_add
  shell: "cat {{ role_path }}/files/profile_jdk"
  connection: local
  register: info
  run_once: true

- name: write /etc/profile
  blockinfile: path=/etc/profile block="{{ info['stdout'] }}" create=yes marker="# {mark} jdk_env"

# 拷贝安装jdk
- name: copy the jdk.zip file to the dst host
  synchronize:
    src: "{{ playbook_dir }}/../../group_files/tdsql_jdk/jdk.zip"
    dest: /data/home/tdsql/

- name: copy the install_jdk.sh to the dst host
  synchronize:
    src: "../files/shell_scripts/install_jdk.sh"
    dest: /data/tools/install_jdk.sh

- name: do install_jdk.sh
  shell: "/bin/bash /data/tools/install_jdk.sh"
######## install jdk ###############


######## install hadoop ############
# 设置hadoop环境变量
- name: local read profile_add
  shell: "cat {{ role_path }}/files/profile_hadoop"
  connection: local
  register: info
  run_once: true

- name: write /etc/profile
  blockinfile: path=/etc/profile block="{{ info['stdout'] }}" create=yes marker="# {mark} hadoop_env"

# 拷贝hadoop并安装
- name: copy the hdfsinstall packets to the dst host
  synchronize: src="{{ playbook_dir }}/../../group_files/tdsql_hdfs/" dest=/data/home/tdsql/

- name: upload the scripts file to the dest host
  synchronize: src=../files/shell_scripts/install_hdfs.sh dest=/data/tools/

- name: install the hdfsinstall packet
  shell: "/bin/bash /data/tools/install_hdfs.sh"
######## install hadoop ############


######## install monitortop ########
- name: copy the tdsql_monitorcmd to the dst host
  synchronize:
    src: "{{ playbook_dir }}/../../group_files/tdsql_monitorcmd/"
    dest: /data/tools/

- name: copy the install_monitor.sh to the dst host
  synchronize:
    src: "../files/shell_scripts/install_monitor.sh"
    dest: /data/tools/

- name: install monitortop packet
  shell: "/bin/bash /data/tools/install_monitor.sh; cd /data"

# 定时任务配置放到后面一起...
######## install monitortop ########



######## install oc_agent ########
- name: copy the oc_agent file to the dst host
  synchronize:
    src: "{{ playbook_dir }}/../../tdsql_packet/tdsql_oc/oc_agent.tgz"
    dest: /data/tools/

- name: copy the oc_agent script to the dst host
  synchronize:
    src: "../files/shell_scripts/install_oc_agent.sh"
    dest: /data/tools/

- name: install oc_agent packet
  shell: "/bin/bash /data/tools/install_oc_agent.sh"

- name: set 1 node tdsql_zk_list
  set_fact:
    tdsql_zk_list: "{{ tdsql_zk_domain_name }}1:{{ tdsql_zk_clientport }}"
  when: groups['tdsql_zk'] | length | int == 1

- name: set 3 nodes tdsql_zk_list
  set_fact:
    tdsql_zk_list: "{{ tdsql_zk_domain_name }}1:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}2:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}3:{{ tdsql_zk_clientport }}"
  when: groups['tdsql_zk'] | length | int == 3

- name: set 5 nodes tdsql_zk_list
  set_fact:
    tdsql_zk_list: "{{ tdsql_zk_domain_name }}1:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}2:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}3:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}4:{{ tdsql_zk_clientport }},{{ tdsql_zk_domain_name }}5:{{ tdsql_zk_clientport }}"
  when: groups['tdsql_zk'] | length | int == 5

- name: generate oc server password
  shell: "/data/oc_agent/bin/oc_encrypt -s {{ tdsql_os_pass }} "
  run_once: true
  register: info

- name: generate oc client password
  shell: "/data/oc_agent/bin/oc_encrypt -c {{ tdsql_os_pass }} "
  run_once: true
  register: info2

- name: copy the oc_agent config file
  synchronize:
    src: ../templates/oc_agent.j2
    dest: /data/tools/oc_agent.xml

- name: replace the oc_agent wait_for_change_tdsql_secret_pass
  replace:
    dest: /data/tools/oc_agent.xml
    regexp: 'wait_for_change_tdsql_secret_pass'
    replace: "{{ info['stdout'] }}"

- name: replace the oc_agent wait_for_change_zklist
  replace:
    dest: /data/tools/oc_agent.xml
    regexp: 'wait_for_change_zklist'
    replace: "{{ tdsql_zk_list }}"

- name: replace the oc_agent wait_for_change_zk_rootdir
  replace:
    dest: /data/tools/oc_agent.xml
    regexp: 'wait_for_change_zk_rootdir'
    replace: "{{ tdsql_zk_rootdir }}"

- name: replace the oc_agent wait_for_change_local_ip
  replace:
    dest: /data/tools/oc_agent.xml
    regexp: 'wait_for_change_local_ip'
    replace: "{{ hostvars[inventory_hostname]['ansible_ssh_host'] }}"

- name: replace oc_agent.xml
  shell: "/bin/cp -a /data/tools/oc_agent.xml /data/oc_agent/conf/oc_agent.xml"

- name: start oc_agent
  shell: "source /etc/profile ; cd /data/oc_agent/bin ; ./restart.sh; sleep 5"
######## install oc_agent ########



#### 配置定时任务
- name: upload the checkalive file to the dest host
  synchronize:
    src: "{{ playbook_dir }}/../../group_files/tdsql_checkalive/"
    dest: /data/tools/

- name: local read tdsql_crontab
  shell: "cat {{ role_path }}/files/tdsql_crontab"
  connection: local
  register: tdsql_cron
  run_once: true

- name: write /etc/crontab
  blockinfile: path=/etc/crontab block="{{ tdsql_cron['stdout'] }}" create=yes marker="# {mark} tdsql_begining"


#### 配置zk的host映射
- name: generate the zk_hosts.j2 on dest host
  template: backup=no force=yes src=../templates/zk_hosts.j2 dest=/data/tools/zk_hosts.txt
  connection: local
  run_once: true

- name: local read zk_hosts
  shell: "cat /data/tools/zk_hosts.txt"
  connection: local
  register: zk_hosts
  run_once: true

- name: write /etc/hosts
  blockinfile: path=/etc/hosts block="{{ zk_hosts['stdout'] }}" create=yes marker="# {mark} tdsql_zk_hosts"

#### 标记beginning安装完成, 后续不需要重复安装
- name: touch and mark file /data/tools/.beginning_finished
  shell: "touch /data/tools/.beginning_finished"

```

# tdsql_filebeat_helper
tdsql_install/playbooks/roles/tdsql_filebeat_helper/tasks/main.yml内容
```sh
---

- name: copy the filebeat_helper file to the dst host
  synchronize:
    src: "{{ playbook_dir }}/../../group_files/tdsql_filebeat/filebeat_helper.tgz"
    dest: /data/tools/

- name: copy the filebeat_helper script to the dst host
  synchronize:
    src: "../files/shell_scripts/install_filebeat_helper.sh"
    dest: /data/tools/


- name: install filebeat_helper packet
  shell: "/bin/bash /data/tools/install_filebeat_helper.sh"


- name: copy config file
  template:
    backup: no
    force: yes
    src: ../templates/filebeat_helper_config.json.j2
    dest: /data/filebeat_helper/config/filebeat_helper_config.json

- name: replace filebeat_helper_config.json esip
  replace:
    dest: /data/filebeat_helper/config/filebeat_helper_config.json
    regexp: 'wait_for_change_esip'
    replace: "{{ hostvars.tdsql_es1.ansible_ssh_host }}"


- name: chown filebeat_helper dir
  shell: "chown -R tdsql.users /data/filebeat_helper && chmod 777 -R /data/filebeat_helper"
```
# install_filebeat_helper.sh内容
tdsql_install/playbooks/roles/tdsql_filebeat_helper/files/shell_scripts/install_filebeat_helper.sh内容
```sh
#!/bin/bash


test -e /data/filebeat_helper && exit 0

cd /data/tools

tar xf filebeat_helper.tgz -C /data/ && chmod 777 -R /data/filebeat_helper && chown -R tdsql:users /data/filebeat_helper


/bin/cp -a /data/filebeat_helper/elastic-stack /data/application

cd /data/application/elastic-stack &&  tar xf filebeat.tar.gz


mkdir -p /data/filebeat_helper/user_config

chmod 777 -R /data/application/elastic-stack && chown -R tdsql.users /data/application/elastic-stack

chmod 777 -R /data/filebeat_helper && chown -R tdsql.users /data/filebeat_helper
```

# tdsql_es7内容

```sh
---

- name: copy the es7 script to the dst host
  synchronize:
    src: "../files/shell_scripts/install_es7.sh"
    dest: /data/tools/

- name: install es7 packet
  shell: "/bin/bash /data/tools/install_es7.sh"

- name: copy the es7 config file
  synchronize:
    src: ../templates/elasticsearch.yml.j2
    dest: /data/application/elastic-stack/elasticsearch/config/elasticsearch.yml

- name: copy the kibana7 config file
  synchronize:
    src: ../templates/kibana.yml.j2
    dest: /data/application/elastic-stack/kibana/config/kibana.yml

- name: replace kibana.yml esip
  replace:
    dest: /data/application/elastic-stack/kibana/config/kibana.yml
    regexp: 'wait_for_change_esip'
    replace: "{{ hostvars.tdsql_es1.ansible_ssh_host }}"

- name: replace elasticsearch.yml esip
  replace:
    dest: /data/application/elastic-stack/elasticsearch/config/elasticsearch.yml
    regexp: 'wait_for_change_esip'
    replace: "{{ hostvars.tdsql_es1.ansible_ssh_host }}"

- name: replace elasticsearch.yml esdir
  replace:
    dest: /data/application/elastic-stack/elasticsearch/config/elasticsearch.yml
    regexp: 'wait_for_change_esdir'
    replace: "{{ tdsql_es7_base_path }}"

- name: set es jvm.options
  shell: "sed -i 's/^-Xms1g/-Xms{{ tdsql_es7_mem }}g/g' /data/application/elastic-stack/elasticsearch/config/jvm.options && sed -i 's/^-Xms4g/-Xms{{ tdsql_es7_mem }}g/g' /data/application/elastic-stack/elasticsearch/config/jvm.options && sed -i 's/^-Xmx1g/-Xmx{{ tdsql_es7_mem }}g/g' /data/application/elastic-stack/elasticsearch/config/jvm.options && sed -i 's/^-Xmx4g/-Xmx{{ tdsql_es7_mem }}g/g' /data/application/elastic-stack/elasticsearch/config/jvm.options"

- name: chown es7 dir
  shell: "chown -R tdsql:users /data/application/elastic-stack && chmod 777 -R /data/application/elastic-stack"

- name: local read profile_add
  shell: "cat {{ role_path }}/files/profile_add"
  connection: local
  register: info
  run_once: true

- name: write /etc/profile
  blockinfile: path=/etc/profile block="{{ info['stdout'] }}" create=yes marker="# {mark} jdk_es_env"


- name: copy the check_es_alive.sh to the dst host
  synchronize:
    src: "../files/shell_scripts/check_es_alive.sh"
    dest: /data/tools/

- name: local read tdsql_crontab
  shell: "cat {{ role_path }}/files/tdsql_crontab"
  connection: local
  register: tdsql_cron
  run_once: true

- name: write /etc/crontab
  blockinfile: path=/etc/crontab block="{{ tdsql_cron['stdout'] }}" create=yes marker="# {mark} tdsql_es"

- name: wait es start, estimated 100s
  shell: "for i in $(seq 1 50); do ps -ef | grep 'data/application/elastic-stack/elasticsearch' | grep 'org.elasticsearch.bootstrap.Elasticsearch' | grep -v grep && exit 0; sleep 2; done; echo 'es not started.'; exit 1"

- name: wait kibana start, estimated 100s
  shell: "for i in $(seq 1 50); do netstat -nalp | grep LISTEN | grep ':5601' && exit 0; sleep 2; done; echo 'kibana port 5601 not started.'; exit 1"

- name: wait 10s and check es is work
  shell: "sleep 10; ps -ef | grep 'data/application/elastic-stack/elasticsearch' | grep 'org.elasticsearch.bootstrap.Elasticsearch' | grep -v grep && exit 0; echo 'es not work.'; exit 1"

- name: check kibana is work
  shell: "netstat -nalp | grep LISTEN | grep ':5601' && exit 0; echo 'kibana port 5601 not work.'; exit 1"

- name: import component_template
  shell: "cd /data/filebeat_helper/bin; ./dump_tool -esHost='{{ hostvars.tdsql_es1.ansible_ssh_host }}:9200' -dumpType=component_template -op=import -filePath=../dump_files/component_template.json | grep Success || exit 1"
  delegate_to: tdsql_es1
  become_user: tdsql
  become: true
  run_once: true

- name: import index_template
  shell: "cd /data/filebeat_helper/bin; ./dump_tool -esHost='{{ hostvars.tdsql_es1.ansible_ssh_host }}:9200' -dumpType=index_template -op=import -filePath=../dump_files/index_template.json | grep Success || exit 1 "
  delegate_to: tdsql_es1
  become_user: tdsql
  become: true
  run_once: true


- name: import pipeline
  shell: "cd /data/filebeat_helper/bin; ./dump_tool -esHost='{{ hostvars.tdsql_es1.ansible_ssh_host }}:9200' -dumpType=pipeline -op=import -filePath=../dump_files/pipeline.json | grep Success || exit 1"
  delegate_to: tdsql_es1
  become_user: tdsql
  become: true
  run_once: true
```

# install_es7.sh内容
tdsql_install/playbooks/roles/tdsql_es7/files/shell_scripts/install_es7.sh
```
#!/bin/bash

test -e /data/application/elastic-stack/elasticsearch && exit 0


#cd /data/filebeat_helper

#/bin/cp -a elastic-stack /data/application


cd /data/application/elastic-stack

tar xf elasticsearch.tar.gz  && tar xf kibana.tar.gz


chmod 777 -R /data/application/elastic-stack && chown tdsql:users -R /data/application/elastic-stack
```

# 初始化机器脚本
tdsql_install/roles/tdsql_beginning/files/shell_scripts/init_os_para.j2内容
```sh
#!/usr/bin/env bash

# 如果该文件存在，则表示该机器的beginning已经执行过，不需要重复执行
test -e /data/tools/.beginning_finished && exit 0

# 关闭透明大页
test -e /sys/kernel/mm/transparent_hugepage/enabled && cat /sys/kernel/mm/transparent_hugepage/enabled | grep never && echo never > /sys/kernel/mm/transparent_hugepage/enabled && (grep '# TDSQL TRANSPARENT_HUGEPAGE SET' /etc/rc.local || echo 'echo never > /sys/kernel/mm/transparent_hugepage/enabled # TDSQL TRANSPARENT_HUGEPAGE SET' >> /etc/rc.local)

echo 6553500 > /proc/sys/fs/file-max
grep "file-max" /etc/sysctl.conf || echo "fs.file-max=6553500" >> /etc/sysctl.conf
grep "max_map_count" /etc/sysctl.conf || echo "vm.max_map_count=655360" >> /etc/sysctl.conf

tdsql_uid="{{ tdsql_uid }}"
grep  -w tdsql  /etc/passwd || grep -E ":${tdsql_uid}:[0-9]+:" /etc/passwd || ( useradd -d /home/tdsql -u ${tdsql_uid} -g users tdsql  &&  echo "tdsql:{{ tdsql_os_pass }}"|chpasswd )
grep  -w tdsql  /etc/passwd || (useradd -d /home/tdsql -g users tdsql  &&  echo "tdsql:{{ tdsql_os_pass }}"|chpasswd)
chage -M -1 tdsql
test -e /etc/cron.allow || touch /etc/cron.allow
grep -w 'tdsql' /etc/cron.allow || echo 'tdsql' >> /etc/cron.allow
chown -R tdsql:users /data/home/tdsql

chattr = /etc/sudoers
grep "^\s*tdsql\s\+ALL\s*=\s*NOPASSWD:ALL" /etc/sudoers || echo "tdsql ALL =NOPASSWD:ALL" >> /etc/sudoers
sed  -i 's/^Defaults\s*requiretty$/#Defaults    requiretty/g' /etc/sudoers
chmod 0440 /etc/sudoers

grep '# BEGIN TDSQL SET' /etc/profile || echo -e "
# BEGIN TDSQL SET
ulimit -HSn 600000
export HISTSIZE=5000
umask 0022
# END TDSQL SET
" >> /etc/profile

# 麒麟V10 HISTTIMEFORMAT是只读变量
test -e /etc/profile.d/zzz_kylin_history.sh && sed -i 's/^kylin_variable_readonly HISTTIMEFORMAT .*/kylin_variable_readonly HISTTIMEFORMAT \"%F %T \`whoami\` \" # TDSQL HISTTIMEFORMAT SET/g' /etc/profile.d/zzz_kylin_history.sh

test -e /etc/profile.d/zzz_kylin_history.sh || ( grep '# TDSQL HISTTIMEFORMAT SET' /etc/profile || echo -e "export HISTTIMEFORMAT=\"%F %T \`who am i\` \" # TDSQL HISTTIMEFORMAT SET" >> /etc/profile )


grep '# TDSQL UMASK SET' /home/tdsql/.bashrc || echo "umask 0022 # TDSQL UMASK SET" >> /home/tdsql/.bashrc
grep '# TDSQL UMASK SET' /etc/bashrc || echo "umask 0022 # TDSQL UMASK SET" >> /etc/bashrc
source /etc/bashrc

test -f /proc/sys/fs/nr_open && nr_open=`cat /proc/sys/fs/nr_open` && echo $nr_open | grep -E "[0-9]+" && [ $nr_open -lt 1000000 ] && echo '1048576' > /proc/sys/fs/nr_open
test -e /etc/security/limits.conf && (grep '# BEGIN TDSQL SET' /etc/security/limits.conf || echo -e "
# BEGIN TDSQL SET
*          -    nofile     1000000
# END TDSQL SET
" >> /etc/security/limits.conf )

test -e /etc/security/limits.d/80-nofile.conf && (grep '# BEGIN TDSQL SET' /etc/security/limits.d/80-nofile.conf || echo -e "
# BEGIN TDSQL SET
*          -    nofile     1000000
# END TDSQL SET
" >> /etc/security/limits.d/80-nofile.conf )

sed -i 's/.*RemoveIPC.*/RemoveIPC=no/' /etc/systemd/logind.conf
grep 'RemoveIPC' /etc/systemd/logind.conf || echo 'RemoveIPC=no' >> /etc/systemd/logind.conf
systemctl restart systemd-logind.service

sed -i 's/^#\s*StrictHostKeyChecking\s*ask$/StrictHostKeyChecking no/g' /etc/ssh/ssh_config
sed -i 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/sshd_config


#添加ssh新监听36000端口
#grep "Port 36000"  /etc/ssh/sshd_config  || (echo "" >> /etc/ssh/sshd_config && echo "Port 36000" >> /etc/ssh/sshd_config)
#egrep "^Port 22"  /etc/ssh/sshd_config  ||  (echo "" >> /etc/ssh/sshd_config && echo "Port 22" >> /etc/ssh/sshd_config)

if [ -f /usr/bin/systemctl ]
then
  systemctl restart sshd
else
  /etc/init.d/sshd restart
fi



sysctl -p|grep "ip_local_port_range"|grep 32768 || echo "net.ipv4.ip_local_port_range=32768 61000" >> /etc/sysctl.conf
echo "32768 61000" > /proc/sys/net/ipv4/ip_local_port_range
grep -q pid_max /etc/sysctl.conf || echo "kernel.pid_max=98304" >> /etc/sysctl.conf
echo "98304"> /proc/sys/kernel/pid_max
grep -q threads-max /etc/sysctl.conf || echo "kernel.threads-max=8241675" >> /etc/sysctl.conf
echo "8241675"> /proc/sys/kernel/threads-max

grep -q tcp_tw_reuse /etc/sysctl.conf || echo "net.ipv4.tcp_tw_reuse=1" >> /etc/sysctl.conf
echo "1" > /proc/sys/net/ipv4/tcp_tw_reuse

grep -q tcp_window_scaling /etc/sysctl.conf || echo "net.ipv4.tcp_window_scaling=1" >> /etc/sysctl.conf
echo "1" > /proc/sys/net/ipv4/tcp_window_scaling

grep -q tcp_max_syn_backlog /etc/sysctl.conf || echo "net.ipv4.tcp_max_syn_backlog=4096" >> /etc/sysctl.conf
echo "4096" > /proc/sys/net/ipv4/tcp_max_syn_backlog

grep -q somaxconn /etc/sysctl.conf || echo "net.core.somaxconn=4096" >> /etc/sysctl.conf
echo "4096" > /proc/sys/net/core/somaxconn

grep -q netdev_max_backlog /etc/sysctl.conf || echo "net.core.netdev_max_backlog=2000" >> /etc/sysctl.conf
echo "2000" > /proc/sys/net/core/netdev_max_backlog

grep -q vm.swappiness /etc/sysctl.conf || echo "vm.swappiness=0">> /etc/sysctl.conf
nohup swapoff -a &
grep -q swapoff /etc/rc.local || echo "swapoff -a">> /etc/rc.local

grep -E '^[ ]{0,}net.ipv4.tcp_keepalive_time' /etc/sysctl.conf || echo "net.ipv4.tcp_keepalive_time=5" >> /etc/sysctl.conf
echo "5" > /proc/sys/net/ipv4/tcp_keepalive_time
sed -i 's/^\s*net.ipv4.tcp_keepalive_time\s*=.*/net.ipv4.tcp_keepalive_time=5/g' /etc/sysctl.conf

grep -E '^[ ]{0,}net.ipv4.tcp_keepalive_intvl' /etc/sysctl.conf || echo "net.ipv4.tcp_keepalive_intvl=2" >> /etc/sysctl.conf
echo "2" > /proc/sys/net/ipv4/tcp_keepalive_intvl
sed -i 's/^\s*net.ipv4.tcp_keepalive_intvl\s*=.*/net.ipv4.tcp_keepalive_intvl=2/g' /etc/sysctl.conf

grep -E '^[ ]{0,}net.ipv4.tcp_keepalive_probes' /etc/sysctl.conf || echo "net.ipv4.tcp_keepalive_probes=5" >> /etc/sysctl.conf
echo "5" > /proc/sys/net/ipv4/tcp_keepalive_probes
sed -i 's/^\s*net.ipv4.tcp_keepalive_probes\s*=.*/net.ipv4.tcp_keepalive_probes=5/g' /etc/sysctl.conf


grep -E '^[ ]{0,}net.ipv4.tcp_retries2' /etc/sysctl.conf || echo "net.ipv4.tcp_retries2=6" >> /etc/sysctl.conf
echo "6" > /proc/sys/net/ipv4/tcp_retries2
sed -i 's/^\s*net.ipv4.tcp_retries2\s*=.*/net.ipv4.tcp_retries2=6/g' /etc/sysctl.conf

chmod +x /etc/rc.local /etc/rc.d/rc.local


sed -i 's/^SELINUX=.*$/SELINUX=disabled/' /etc/selinux/config
setenforce 0


#core file config
ulimit -c unlimited
sed -i "s/^\s*ulimit\s\+-c.*/ulimit -c unlimited/g" /etc/profile
grep "^\s*ulimit\s\+-c\s\+unlimited" /etc/profile || echo "ulimit -c unlimited" >> /etc/profile
mkdir -p /data/coredump/ && chmod 777 /data/coredump/
echo "/data/coredump/core-%e-%p-%t" > /proc/sys/kernel/core_pattern
grep "kernel.core_pattern=/data/coredump/core-%e-%p-%t" /etc/sysctl.conf || echo "kernel.core_pattern=/data/coredump/core-%e-%p-%t" >> /etc/sysctl.conf




#优化每个用户创建最大进程数
echo "*    soft   nproc     60000" > /etc/security/limits.d/20-nproc.conf
echo "root  soft  nproc  unlimited" >> /etc/security/limits.d/20-nproc.conf


# 磁盘IO调度算法设置
# NVME默认设置为none，SATA接口的SSD默认设置为deadline
for BID in `cd /sys/block && ls -l  |grep -v virtual |awk '{print $9}' `
do
  BTYPE=''
  BROTAT=`cat /sys/block/${BID}/queue/rotational`
  if [ ${BROTAT} -eq 0 ]
  then
    if echo ${BID} | grep nvme
    then
      cat /sys/block/${BID}/queue/scheduler | grep noop && BTYPE='noop'
      cat /sys/block/${BID}/queue/scheduler | grep none && BTYPE='none'
    elif hdparm -I /dev/${BID} | grep 'Transport:' | grep SATA
    then
      cat /sys/block/${BID}/queue/scheduler | grep 'mq-deadline' && BTYPE='mq-deadline'
      cat /sys/block/${BID}/queue/scheduler | grep deadline | grep -v 'mq-deadline' && BTYPE='deadline'
    fi
  fi
  if [ -n "${BTYPE}" ]
  then
    echo ${BTYPE} > /sys/block/${BID}/queue/scheduler
    cat /etc/rc.local | grep "# TDSQL DEV ${BID} SET" || echo "echo ${BTYPE} > /sys/block/${BID}/queue/scheduler # TDSQL DEV ${BID} SET" >> /etc/rc.local
  fi
done

#关闭防火墙
iptables -F

if [ -f /usr/bin/systemctl ]
then
  systemctl disable firewalld
  systemctl stop firewalld
else
  /etc/init.d/iptables stop
  chkconfig iptables off
fi


#重新加载生效
sysctl -p


grep '# TDSQL PATH SET'  /etc/profile || echo 'export PATH=/usr/local/bin:$PATH # TDSQL PATH SET' >>/etc/profile

cd /data


# add lib
test -e /usr/lib64/libcrypto.so.1.0.2k || /bin/cp -a /data/tools/libcrypto.so.1.0.2k /usr/lib64/
test -e /usr/lib64/libssl.so.1.0.2k || /bin/cp -a /data/tools/libssl.so.1.0.2k /usr/lib64/

cd /usr/lib64
test -e libreadline.so.6 || ln -s libreadline.so.7.0 libreadline.so.6
test -e libncurses.so.5 || ln -s libncurses.so.6.1 libncurses.so.5
test -e libtinfo.so.5 || ln -s libtinfo.so.6.1 libtinfo.so.5
test -e libssl.so.10 || ln -s libssl.so.1.0.2k libssl.so.10
test -e libcrypto.so.10 || ln -s libcrypto.so.1.0.2k libcrypto.so.10
test -e libidn.so.11 || ln -s libidn.so.12 libidn.so.11
test -e libnsl.so.1 || ( test -e libnsl.so.2.0.0 && ln -s libnsl.so.2.0.0 libnsl.so.1 )

cd /


uname -i | grep aarch64 && uname -r | grep ky10 && test -L /usr/bin/dstat && [ ! -L /usr/bin/dstat_rename_by_tdsql ] && [ ! -e /usr/share/dstat ] && test -e /data/tools/dstat.bak && test -e /data/tools/dstat.tgz && {
  mv /usr/bin/dstat /usr/bin/dstat_rename_by_tdsql
  cp -a /data/tools/dstat.bak /usr/bin/dstat
  tar xf /data/tools/dstat.tgz -C /usr/share/
  chmod 755 /usr/bin/dstat
  chmod 644 -R /usr/share/dstat
  chmod 755 /usr/share/dstat
}

mkdir -p /data /data1 /tmp
chmod 777 /tmp
chmod 755 /data /data1
chown tdsql:users /data /data1

cd /tmp
ls -a | grep -E '^agent_config\.lock$|^agent_cgroup\.lock$|^hsperf|^\.filebeat_help_lock$|^dcagent_daemon$|^dcagent$|^ddlperformermng_daemon\.lock$|^ddlperformermng\.lock$|^install_proxy\.lock$|^install_tdsql\.lock$|^jetty-|^percona-version-check$|^proxy_[0-9]+\.lock$|^install_mysql_[0-9]+|tdsql_[0-9]+\.lock$|^agent_gtidlist\.lock$|^uninstall|^analyze|^reinstall|^supervisor\.sock$|^supervisord\.pid$|^elasticsearch-' | xargs -r chown -R tdsql:users

cd /
```