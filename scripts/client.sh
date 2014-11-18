#!/bin/bash
rm -rf command.txt
rm -rf hit_miss.out

#$1 : ip 

#$2 : sleep time in monitor

##1 : check_timeout

rm -rf setController.time
sudo python server.py &
sudo ./commander.sh &
sudo ./monitor.sh $1 $2 $3&
