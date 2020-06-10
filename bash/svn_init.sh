#!/bin/bash
#
# chkconfig:   - 85 15
# description: The Script for SVN service
server_name=svnserve

# only need to modify this.
svnrepo=/data/svnrepo
start_server="svnserve -d -r $svnrepo"
stop_server="killall $server_name"

function check_status(){
    netstat -tlnp | grep -q "$server_name"
    if [ $? = 0 ];then
        return 0  # running
    else 
        return 1  # stopped
    fi
}

function status(){
    check_status
    if [ $? = 0 ];then
        echo "SVN $svnrepo is running..."
    else 
        echo "SVN $svnrepo is stpped"
    fi
}

function start(){
    check_status && echo "SVN $svnrepo is running..." || $start_server && echo "start SVN $svnrepo OK"
}

function stop(){
    check_status && $stop_server  && echo "stop SVN $svnrepo OK" || echo "SVN $svnrepo is stpped"
}

function restart(){
    check_status
    if [ $? == 0 ];then
        $stop_server  && echo "stop SVN $svnrepo OK"
        $start_server && echo "start SVN $svnrepo OK"
    else
        echo "SVN $svnrepo is not running..."
    fi
}

case $1 in
    start)
        start;;
    stop)
        stop;;
    restart)
        restart;;
    status)
        status;;
    *)
        echo "sytax error"
    esac