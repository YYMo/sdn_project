#!/bin/bash

start_line=1

while ((1<10))
do
    sleep 5
    line_num=`awk 'END{print NR}' pox.log`
    echo 'start: '$start_line
    echo 'end: '$line_num
    ((deal_num=$line_num-$start_line))
    echo 'deal with: '$deal_num

    awk "NR=="${start_line},"NR=="${line_num} pox.log | \
    awk '/print_time/'  | awk '{print $3}' | \
    awk '{a=$1;getline;printf("%f\n",$1-a)}' > temp_result.txt

    ((total_line=$line_num-$start_line+1))
    num_packets=`awk 'END{print NR}' temp_result.txt`
    echo 'Total packet_in: '$num_packets
    ((start_line=$line_num+1)) 

    if [ $num_packets -eq 0 ]
    then
       continue
    fi
    avg_time=`awk '{a+=$1}END{print a/NR}' temp_result.txt`
    echo 'avg time: '$avg_time
done