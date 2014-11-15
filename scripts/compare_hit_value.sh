#!/bin/bash

prev_hit_file='hit_miss.out'
prev_setController_time='setController.time'

# check if the previous hit number has been recorded
if [ ! -e $prev_hit_file ]
then
    
    ovs-dpctl show | \
    sed -n -e '2{p;q}' | \
    awk -F":" '{print $1","$2","$3","$4","$5}' | \
    awk -F" " '{print $2","$3","$4}' > "$prev_hit_file"

    echo "$prev_hit_file has been created for the first time"
    exit 1

fi

# if exist: get the previous hit number
prev_hit=`awk -F"," '{print $2}' $prev_hit_file`
#echo $prev_hit

# get the current hit number 
cur_hit=`ovs-dpctl show | \
         sed -n -e '2{p;q}' | \
	 awk -F":" '{print $1","$2","$3","$4","$5}' | \
	 awk -F" " '{print $2","$3","$4}' | awk -F"," '{print $2}'`
#echo $cur_hit

# check if the previous set controller time exists, if not, default to '01/01/1973 00:00:00'
if [ ! -e $prev_setController_time ]
then
   echo "no previous set time..." 
   prev_set=$(date -d '01/01/1973 00:00:00' +'%m:%d:%Y:%H:%M:%S')
   prev_set_output=$(date -d '01/01/1973 00:00:00' +'%m/%d/%Y %H:%M:%S')
else
   prev_setTime=`awk -F"|" '{print $1}' $prev_setController_time`
   #echo $prev_setTime
   prev_set=`date -d "$prev_setTime" +'%m:%d:%Y:%H:%M:%S'`
   prev_set_output=`date -d "$prev_setTime" +'%m/%d/%Y %H:%M:%S'`
fi
#echo "Prev time : $prev_set"

# get the current timestamp
now=$(date +'%m:%d:%Y:%H:%M:%S')
#echo "Current time : $now"

# def a function to convert time to seconds (for now: assume only comparing without date difference... needs further improvements)
t2s()
{
  local T=$1;shift
  #echo $((10#${T:0:2} * 3600 * 24 * 30 + 10#${T:3:2} * 3600 * 24 + 10#${T:6:4} * 3600 * 24 * 30 * 360 + 10#${T:11:2} * 3600 + 10#${T:14:2} * 60 + 10#${T:17:2})) 
  echo $((10#${T:11:2} * 3600 + 10#${T:14:2} * 60 + 10#${T:17:2}))
}

# calculate the time difference in seconds
diff_time=$(( $(t2s $now) - $(t2s $prev_set) ))
#echo $(t2s $now)
#echo $(t2s $prev_set)
#echo $diff_time

# check if the current hit number is greater than previous hit number && time difference from the previous set controller time is greater than 30s
if [[ $prev_hit -lt $cur_hit && $diff_time -gt 30 ]]
then
    #echo "cur_hit $cur_hit is bigger than prev_hit $prev_hit"
    #echo "time difference from the prev set controller time is $diff_time"
    echo "1"
else 
    echo "0"
fi

# output the current hit number to a $prev_hit_file file for the next run
ovs-dpctl show | \
sed -n -e '2{p;q}' | \
awk -F":" '{print $1","$2","$3","$4","$5}' | \
awk -F" " '{print $2","$3","$4}' > "$prev_hit_file"
