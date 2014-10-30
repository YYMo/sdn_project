#!/bin/bash

sudo ovs-vsctl show | \
awk '/Bridge/' | \
awk '{print $2}' | \
tr -d '"' | \
xargs -i sudo ovs-vsctl del-controller {}
