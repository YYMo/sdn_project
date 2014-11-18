#!/bin/bash
sudo ovs-vsctl show | grep 'Controller' | sed -n "1,1p" | awk '{print $2}' | tr -d '"' 