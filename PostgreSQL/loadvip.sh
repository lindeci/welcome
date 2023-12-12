#!/bin/bash
 
VIP=172.1.1.20
GATEWAY=172.1.1.254
DEV=eth0

action=$1
role=$2
cluster=$3
 
 
load_vip()
{
    #ip a|grep -w ${DEV}|grep -w ${VIP} >/dev/null
    ping -c3 -w3 $vip &>/dev/null
    if [ $? eq 0 ] ;then
        echo "vip exists, skip load vip" >> /data/pgsql/loadvip.log 
    else
        sudo ip addr add ${VIP}/24 dev ${DEV} >/dev/null
        rc=$?
        if [ $rc -ne 0 ] ;then
            echo "fail to add vip ${VIP} at dev ${DEV} rc=$rc"
            exit 1
        fi
        echo "added vip ${VIP} at dev ${DEV}" >> /data/pgsql/loadvip.log
        arping -q -A -c 3 -I ${DEV}  ${VIP} >/dev/null
        rc=$?
        if [ $rc -ne 0 ] ;then
            echo "fail to call arping to gateway rc=$rc" >> /data/pgsql/loadvip.log
            exit 1
        fi
        echo "called arping" >> /data/pgsql/loadvip.log
    fi
}

unload_vip()
{
    ip a|grep -w ${DEV}|grep -w ${VIP} >/dev/null
    if [ $? -eq 0 ] ;then
        sudo ip addr del ${VIP}/24 dev ${DEV} >/dev/null
        rc=$?
        if [ $rc -ne 0 ] ;then
            echo "fail to delete vip ${VIP} at dev ${DEV} rc=$rc" >> /data/pgsql/loadvip.log
            exit 1
        fi
        echo "deleted vip ${VIP} at dev ${DEV}" >> /data/pgsql/loadvip.log
    else
        echo "vip not exists, skip delete vip" >> /data/pgsql/loadvip.log
    fi
}
 
case $action in
    on_start|on_restart|on_role_change)
        case $role in
            master)
                load_vip
                ;;
            replica)
                unload_vip
                ;;
            *)
                echo "wrong role '$role'" >> /data/pgsql/loadvip.log
                exit 1
                ;;
        esac
    ;;
    *)
        echo "wrong action '$action'" >> /data/pgsql/loadvip.log
        exit 1
        ;;
esac