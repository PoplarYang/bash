#!/bin/bash
# 计时进度条
i=0
while [ $i -lt 20 ]; do
    for j in '-' '\' '|' '/'; do
        printf "intel testing : %s\r" $j
        sleep 0.1
        #((i++))
        let i++
    done
done
