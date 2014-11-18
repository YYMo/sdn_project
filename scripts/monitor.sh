#!/bin/bash
#./monitor 192.168.44.32 sleep_time check_timeout serverport
$fail_number
$controller_ip
$interval
sleep_time=30
start_line=1
check_timeout=0

echo $#
if [ $# -gt 1 ]
then
    controller_ip=$1
fi

if [ $# -gt 2 ]
then
    sleep_time=$2
fi


if [ $# -gt 3 ]
then
    check_timeout=$3
fi
touch avg_time10000X
echo 0 > avg_time10000X
prev_setController_time='setController.time'
while ((1<10))
do
    bDisCon=`./compare_hit_value.sh`
    #1 ping timeout 
    if [ ${bDisCon} -eq 0 ] && [ $check_timeout ] #legal
    then
        echo 'no fails' > t.txt
    else
        echo '#1 fail'
        python send.py $1 $4 "newCon2"
        #./reconnect_fail.sh localhost ${startPort}
        #startPort=`expr $startPort + 1`
        $(date +'%m/%d/%Y %H:%M:%S') > $prev_setController_time
        sleep ${sleep_time}
        continue
        
    fi
    
    #2 connection loss
    ./check_fail.sh > fail_nodes.txt
    fail_number=` wc -l fail_nodes.txt | awk '{print $1}'`
    if [ ${fail_number} -eq 0 ] #legal
    then
        echo 'no fails' > t.txt
    else 
        echo 'Connection Loss, request for a controllers'
        python send.py $1 $4 "newCon"
        sleep ${sleep_time}
        continue

    fi

    #3 packets per min or avg_time
    avg_time=`cat avg_time10000X`
    if [ ${avg_time} -lt 20000 ]
    then
        echo 'no fails' > t.txt
    else
        echo 'no fails' > t.txt
        #echo '#3 fail'
        #python send.py $1 50006 "newCon ${startPort}"
        #./disconnect_all.sh
        #./reconnect_all.sh $1 ${startPort}
        #startPort=`expr $startPort + 1`
        sleep ${sleep_time}
    fi
    


done
