#!/bin/bash
start_line=1
line_N
touch command.txt
while ((1<10))
do
    line_num=`awk 'END{print NR}' 'command.txt'`
    #echo 'start: '$start_line
    #echo 'end: '$line_num

    ((line_N=$line_num-$start_line)) 
    ((testN=$line_N+1))
    #echo $line_N
    if [ ${testN} -eq 0 ]
    then
    	sleep 1
    	continue
    fi

    sed -n "${start_line},${line_num}p" 'command.txt' > temp_run.sh
    chmod +x temp_run.sh
    cp temp_run.sh  t_run.sh
    ./t_run.sh
    
    ((start_line=$line_num+1)) 

    sleep 1
done