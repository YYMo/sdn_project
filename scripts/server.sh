#!/bin/bash
#$1 serverPort
rm -rf command.txt
sudo python server.py $1 &
sudo ./commander.sh &