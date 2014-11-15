#!/bin/bash

file_name='hit_miss.out'
ovs-dpctl show | \
sed -n -e '2{p;q}' | \
awk -F":" '{print $1","$2","$3","$4","$5}' | \
awk -F" " '{print $2","$3","$4}' > "$file_name"
