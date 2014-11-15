#!/bin/bash
sudo ovs-vsctl show | \
awk '/Bridge/ {print; getline; print; getline; print;}' | \
awk '{if (NR%3==0){print $0} else {printf"%s ",$0}}' | \
awk '{print $2 " " $5}' | tr -d '"' | grep -E 'fail|Port' | awk '{print $1}' | \
xargs -i sudo ovs-vsctl set-controller {} tcp:$1:$2
