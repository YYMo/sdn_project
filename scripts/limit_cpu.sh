#!/bin/bash
ps -ax | grep python | grep forwarding.l2_learning | awk '{print $1}' | xargs -i cpulimit -p {} -l 1 -v
