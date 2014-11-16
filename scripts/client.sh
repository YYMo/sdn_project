#!/bin/bash
rm -rf command.txt
rm -rf hit_miss.out
rm -rf setController.time
sudo python server.py &
./commander.sh &
./monitor.sh 192.168.44.129 &
