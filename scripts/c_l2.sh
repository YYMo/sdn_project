#!/bin/bash

sudo ../pox.py log --file=pox.log,w openflow.of_01 --port=$1 forwarding.l2_learning
