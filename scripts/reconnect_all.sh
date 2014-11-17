#!/bin/bash
sudo ./disconnect_all.sh

sudo ovs-vsctl show | \
awk '/Bridge/ {print; getline; print; getline; print;}' | \
awk '{if (NR%3==0){print $0} else {printf"%s ",$0}}' | \
awk '$0 !~ /true/' | awk '{print $2}' | tr -d '"'  | \
xargs -i sudo ovs-vsctl set-controller {} tcp:$1:$2