#!/bin/bash
#
# svnserve        Startup script for the Subversion svnserve
#
# chkconfig: - 85 15
# description: The svnserve daemon allows access to Subversion repositories \
#              using the svn network protocol.

# Modify exe, prog, option
exe=/usr/bin/svnserve
[ -x $exe ] || exit 5
prog=svnserve
option="-d -r /data/svndata/"

delay_restart=5
lockfile=/var/lock/subsys/$prog

############################################################################################
start() {
    if check_status &> /dev/null; then
        echo "$prog is running... " && echo -e "Starting $prog: \t\t\e[31m[ failed ]\e[0m" && return 1
    else
        $exe $option && echo -e "Starting $prog: \t\t\e[32m[  OK  ]\e[0m" && touch $lockfile && return 0
    fi
}

stop() {
    if check_status &> /dev/null; then
        pid
        kill $pid && rm -f $lockfile && echo -e "Stopping $prog: \t\t\e[32m[  OK  ]\e[0m" && return 0
    else
        echo "$prog is stopped." && echo -e "Stopping $prog: \t\t\e[31m[ failed ]\e[0m" && return 1
    fi
}

pid() {
    pid=`netstat -tlnp | grep $prog | awk '{ print $NF }' | cut -d / -f1`
}

check_status() {
    netstat -tlnp | grep $prog
}

status() {
    echo "Proto Recv-Q Send-Q Local Address               Foreign Address             State       PID/Program name"
    check_status 2> /dev/null
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop && sleep $delay_restart && start
        ;;
    status)
        status
        ;;
    *)
        echo $"Usage: $0 {start|stop|status|restart}"
esac
