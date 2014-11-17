#!/bin/bash
#./monitor 192.168.44.32 6789 5(s)
$fail_number
$controller_ip
$interval

echo $#
if [ $# -gt 1 ]
then
    controller_ip=$1
fi

if [ $# -gt 2 ]
then
    interval=$2
fi

prev_setController_time='setController.time'
while ((1<10))
do
    sleep 10
    ./check_fail.sh > fail_nodes.txt
    bDisCon=`./compare_hit_value.sh`
    #1 ping timeout 
    if [ ${bDisCon} -eq 0 ] #legal
    then
       echo 'no fails'
    else
        echo '#1 fail'
        #python send.py $1 50006 "newCon"
        #./reconnect_fail.sh localhost ${startPort}
        #startPort=`expr $startPort + 1`
        $(date +'%m/%d/%Y %H:%M:%S') > $prev_setController_time
        
    fi
    
    #2 connection loss
    fail_number=` wc -l fail_nodes.txt | awk '{print $1}'`
    if [ ${fail_number} -eq 0 ] #legal
    then
        echo 'no fails'
    else 
        echo '#2 fail'
        python send.py $1 50006 "newCon"

    fi

    #3 packets per min or avg_time
    avg_time=`cat avg_time10000X`
    if [ ${avg_time} -lt 20000 ]
    then
        echo 'good responce time'
    else
        echo '#3 fail'
        #python send.py $1 50006 "newCon ${startPort}"
        #./disconnect_all.sh
        #./reconnect_all.sh $1 ${startPort}
        #startPort=`expr $startPort + 1`
    fi

done
