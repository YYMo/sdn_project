#!/bin/bash
#$1: port
#$2: logname
sudo ../pox.py log --file=$2,w openflow.of_01 --port=$1 forwarding.l2_learning
