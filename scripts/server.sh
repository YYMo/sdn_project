#!/bin/bash
rm -rf command.txt
sudo python server.py &
sudo ./commander.sh &