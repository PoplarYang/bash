#!/bin/sh
. /etc/init.d/functions
# chkconfig: - 85 15 
# description:  Tomcat

# tomcat安装目录
export CATALINA_HOME="/usr/local/tomcat"
case "$1" in
start)
	if [ -f $CATALINA_HOME/bin/startup.sh ];then
		echo $"Start Tomcat"
		$CATALINA_HOME/bin/startup.sh
	fi
	;;
stop)
	if [ -f $CATALINA_HOME/bin/shutdown.sh ];then
		echo $"Stop Tomcat"
		$CATALINA_HOME/bin/shutdown.sh
	fi
	;;
*)
	echo $"Usage: $0 {start|stop}"
	exit 1
	;;
esac




