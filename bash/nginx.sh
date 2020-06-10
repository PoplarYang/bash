#!/bin/sh
#
# nginx - this script starts and stops the nginx daemin
#
# chkconfig:   - 85 15 
# description:  Nginx is an HTTP(S) server, HTTP(S) reverse \
#               proxy and IMAP/POP3 proxy server
# processname: nginx
# config:      /usr/local/nginx/conf/nginx.conf
# pidfile:     /usr/local/nginx/logs/nginx.pid

# Source function library.
. /etc/rc.d/init.d/functions

# Source networking configuration.
. /etc/sysconfig/network

# Check that networking is up.
[ "$NETWORKING" = "no" ] && exit 0

EXE="/usr/sbin/nginx"
PROG=$(basename $EXE)

CONF_FILE="/etc/nginx/conf/nginx.conf"

LOCKFILE=/var/lock/subsys/nginx

start() {
    [ -x $EXE ] || exit 5
    [ -f $CONF_FILE ] || exit 6
    echo -n $"Starting $PROG: "
    daemon $EXE -c $CONF_FILE
    retval=$?
    echo
    [ $retval -eq 0 ] && touch $LOCKFILE
    return $retval
}

stop() {
    echo -n $"Stopping $PROG: "
    killproc $PROG -QUIT
    retval=$?
    echo
    [ $retval -eq 0 ] && rm -f $LOCKFILE
    return $retval
}

restart() {
    configtest || return $?
    stop
    start
}

reload() {
    configtest || return $?
    echo -n $"Reloading $PROG: "
    killproc $EXE -HUP
    RETVAL=$?
    echo
}

force_reload() {
    restart
}

configtest() {
  $EXE -t -c $CONF_FILE
}

rh_status() {
    status $PROG
}

rh_status_q() {
    rh_status >/dev/null 2>&1
}

case "$1" in
    start)
        rh_status_q && exit 0
        $1
        ;;
    stop)
        rh_status_q || exit 0
        $1
        ;;
    restart|configtest)
        $1
        ;;
    reload)
        rh_status_q || exit 7
        $1
        ;;
    force-reload)
        force_reload
        ;;
    status)
        rh_status
        ;;
    condrestart|try-restart)
        rh_status_q || exit 0
            ;;
    *)
        echo $"Usage: $0 {start|stop|status|restart|condrestart|try-restart|reload|force-reload|configtest}"
        exit 2
esac
