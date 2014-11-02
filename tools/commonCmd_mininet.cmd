sudo ovs-vsctl add-port br0 ethX

sudo ovs-vsctl list-ports br0

sudo ovs-vsctl show

sudo ovs-vsctl set-controller br0 tcp:<controller_ip>:6633

sudo ovs-vsctl set-fail-mode br0 secure

sudo ovs-ofctl dump-flows br0

