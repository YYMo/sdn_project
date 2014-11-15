#!/bin/bash
#./monitor 192.168.44.32 6789
$fail_number
$controller_ip
$controller_port

echo $#
if [ $# -gt 1 ]
then
    $controller_ip=$1
fi

if [ $# -gt 2 ]
then
    $controller_port=$2
fi

while ((1<10))
do
    sleep 2
    fail_number=` wc -l fail_nodes.txt | awk '{print $1}'`
    if [ ${fail_number} -eq 0 ]
    then
        echo 'no fails'
    else 
    	./reconnect_fail.sh $1 $2
    fi
done