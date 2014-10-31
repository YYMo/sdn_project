//install cgroup
sudo apt-get install cgroup-bin
//Make a cgroup for user mininet:
sudo cgcreate -a mininet:mininet -t mininet:mininet -g memory:mininet
#This should have created a group (a directory) at /sys/fs/cgroup/memory/mininet
//set the MAX memory to use
echo 100 > /sys/fs/cgroup/memory/mininet/memory.limit_by_bytes

//use it to run your program:
sudo cgexec -g memory:mininet mn 
