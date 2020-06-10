#!/bin/bash

# chkconfig: - 10 90
# description: Tomcat Service

# Value About Prog
ProgName="Tomcat"
ProgBaseDir="/usr/local/tomcat"
ProgStart="${ProgBaseDir}/bin/catalina.sh start"
ProgStop="${ProgBaseDir}/bin/catalina.sh stop"

# Check Prog Status
# 1:running
# 2:stoped
chk_status()
{
	local ProgID=$(ps -ef | grep ${ProgName} | grep -w ${ProgBaseDir} | grep -v 'grep' |awk '{print $2}')  
	if [ -n ${ProgID} ]; then
		return 0
	else
		return 1
	fi
}

# Check Web Status
# Return HttpCode
chk_web_status()
{
	local WebUrl='http://112.124.102.8:8080'
	local WebStatusCode=$(curl -s -o /dev/null -m 10 --connect-timeout 10 $WebUrl -w %{http_code})
	echo -e "Curl test WebStatusCode is \e[32m${WebStatusCode}.\e[0m"
}

start()
{	
	${ProgStart} 
	if [ $? -eq 0 ]; then
		sleep 8
		echo -e "Start ${ProgName} \e[32mOK.\e[0m"
	else
		echo -e "Start ${ProgName} \e[31mfailed.\e[0m"
	fi
}

stop()
{
	${ProgStop}
	if [ $? -eq 0 ]; then
		sleep 8
		echo -e "Stop ${ProgName} \e[32mOK.\e[0m"
	else
		echo -e "Stop ${ProgName} \e[31mfailed.\e[0m"
	fi
}

case $1 in
start)
	if ! chk_status; then
		start
		chk_web_status
		exit 0
	else
		echo -e "${ProgName} is \e[32mRunning.\e[0m"
		exit 1
	fi
	;;
stop)
	if chk_status; then
		stop
		chk_web_status
		exit 0
	else
		echo "${ProgName} is \e[31mnot Running.\e[0m"
		exit 1
	fi
	;;
restart)
	if chk_status; then
		stop
		start
		chk_web_status
		exit 0
	else
		echo "${ProgName} is \e[31mnot Running.\e[0m"
		exit 1
	fi
	;;
status)
	if chk_status; then
		echo -e "${ProgName} is \e[32mRunning.\e[0m"
	else
		echo "${ProgName} is \e[31mnot Running.\e[0m"
	fi
	;;
webstatus)
	chk_web_status
	;;
*)
	echo "basename $0:[start|stop|restart]"
	exit 1
	;;
esac