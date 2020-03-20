#!/bin/bash

# start and stop lsyncd

start(){
    LSYNC_PID=$(ps aux | awk '$NF~/lsyncd.conf$/ {print $2}')
    if [ -z "$LSYNC_PID" ]; then
        lsyncd -log Exec /etc/lsyncd.conf && echo -e "start lsyncd OK\c"
        LSYNC_PID=$(ps aux | awk '$NF~/lsyncd.conf$/ {print $2}')
        echo "[ PID $LSYNC_PID ]"
    else
        echo "lsync is running...[ PID $LSYNC_PID ]"
    fi
}

stop(){
    LSYNC_PID=$(ps aux | awk '$NF~/lsyncd.conf$/ {print $2}')
    if [ -n "$LSYNC_PID" ]; then
        kill $LSYNC_PID && echo "stop lsyncd OK [ PID $LSYNC_PID ]"
    else
        echo "lsyncd is not running..."
    fi
}

status(){
    LSYNC_PID=$(ps aux | awk '$NF~/lsyncd.conf$/ {print $2}')
    if [ -n "$LSYNC_PID" ]; then
        echo "lsync [ PID $LSYNC_PID ] is running"
    else
        echo "lsync is not running..."
    fi
}

case $1 in
    start)
        start;;
    stop)
        stop;;
    status)
        status;;
    *)
    echo "Error Input!![ lsyncd-daemon start | stop | status ]";;
esac