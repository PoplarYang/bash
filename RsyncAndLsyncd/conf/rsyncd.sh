#!/bin/bash

# start and stop lsync daemon

start(){
    local RSYNC_PID=$(ps aux | awk '$NF~/rsyncd.conf$/ {print $2}')
    if [ -z "$RSYNC_PID" ]; then
        /usr/bin/rsync --daemon --config=/etc/rsyncd.conf && echo -e  "start rsync OK\c"
        RSYNC_PID=$(ps aux | awk '$NF~/rsyncd.conf$/ {print $2}')
        echo "[ PID $RSYNC_PID ]"
    else
        echo "rsync is running... [ PID $RSYNC_PID ]"
    fi
}

stop(){
    local RSYNC_PID=$(ps aux | awk '$NF~/rsyncd.conf$/ {print $2}')
    if [ -n "$RSYNC_PID" ]; then
        kill $RSYNC_PID && echo "stop rsync [ PID $RSYNC_PID ] OK"
    else
        echo "rsync is not running..."
    fi
}

status(){
    local RSYNC_PID=$(ps aux | awk '$NF~/rsyncd.conf$/ {print $2}')
    if [ -n "$RSYNC_PID" ]; then
        echo "rsync [ PID $RSYNC_PID ] is running"
    else
        echo "rsync is not running..."
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
    echo "Error Input!![ rsync-daemon start | stop | status ]";;
esac