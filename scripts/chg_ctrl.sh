#!/bin/bash

ovs-vsctl set-fail-mode $1 secure
ovs-vsctl del-controller $1
ovs-vsctl set-controller $1 tcp:$2:$3
echo "change switch: $1's controller to $2:$3"
