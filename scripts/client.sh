#!/bin/bash
sudo python server.py &
./commander.sh &
./monitor.sh 192.168.44.129 &