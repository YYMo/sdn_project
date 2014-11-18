#!/bin/bash
rm -rf command.txt
rm -rf hit_miss.out

#$1 : ip 

#$2 : sleep time in monitor

##1 : check_timeout

#4: server port

rm -rf setController.time
sudo python server.py $4 &
sudo ./commander.sh &
sudo ./monitor.sh $1 $2 $3&
