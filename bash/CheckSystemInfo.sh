#!/bin/bash
#
# The script is used to catch server and sofrware information.
# Version: 1.2

# time
TIME=$(date +"%F %T")

# Check OS
if [ -n "$(grep 'Aliyun Linux release' /etc/issue)" -o -e /etc/redhat-release ]; then
  OS=CentOS
  [ -n "$(grep ' 7\.' /etc/redhat-release)" ] && CentOS_RHEL_version=7
  [ -n "$(grep ' 6\.' /etc/redhat-release)" -o -n "$(grep 'Aliyun Linux release6 15' /etc/issue)" ] && CentOS_RHEL_version=6
  [ -n "$(grep ' 5\.' /etc/redhat-release)" -o -n "$(grep 'Aliyun Linux release5' /etc/issue)" ] && CentOS_RHEL_version=5
fi

# System Bit
if [ "$(getconf WORD_BIT)" == "32" ] && [ "$(getconf LONG_BIT)" == "64" ]; then
  OS_BIT=64
else
  OS_BIT=32
fi

# network
if [ $CentOS_RHEL_version == '7' ]; then
    ETH0=$(ifconfig | egrep -A 1 eth0 | awk '/inet/ { print $2 }')
    ETH1=$(ifconfig | egrep -A 1 eth1 | awk '/inet/{ print $2 }')
else
    ETH0=$(ifconfig | egrep -A 1 eth0 | awk '/inet/ { print $2 }' | cut -d':' -f2)
    ETH1=$(ifconfig | egrep -A 1 eth1 | awk '/inet/ { print $2 }' | cut -d':' -f2)
fi
# sshd port
SSHD_PORT=$(netstat -tlnp | awk '/sshd/ { print $4 }' | cut -d":" -f 2)

# iptabels version
iptables -nvL | grep multiport /dev/null && IPTABLES_VERSION=6 || IPTABLES_VERSION="Not modify"

# httpd
HTTPD_PID=$(ps -eo comm,user,pid | awk '/httpd/ {if ($2!="root") print $3}' | head -n1)
if [ -z $HTTPD_PID ]; then
    HTTPD_VERSION=$(echo null)
    HTTPD_INSTALL=$(echo null)
    MPM=$(echo null)
    ServerRoot=$(echo null)
    APACHE_USER=$(echo null)
else
    HTTPD=$(lsof -p $HTTPD_PID | awk '/httpd$/{ print $NF }')
    [ -e $HTTPD -a $HTTPD == "/usr/sbin/httpd" ] && HTTPD_INSTALL=yum || HTTPD_INSTALL=compile

    if [ $HTTPD_INSTALL == "yum" ]; then
        ServerRoot=/etc/httpd
        APACHE_USER=$(ps aux | grep httpd | head -n2 | tail -n1 | awk '{ print $1 }')
    else
        ServerRoot=$(dirname $(dirname $HTTPD))
        APACHE_USER=$(ps -eo comm,user,pid | awk '/httpd/ {if ($2!="root") print $2}' | head -n1)
    fi

    HTTPD_VERSION=$($HTTPD -v | awk '/version/{ print $3 }' | cut -d'/' -f2)
    MPM=$($HTTPD -l | egrep 'prefork|work|event')
    [ -z $HTTPD ] && MPM=$(basename $(lsof -p $HTTPD_PID | awk -F'_' '/mod_mpm/ { print $NF }'))
# vritual host
    VIRTUALHOST=$($HTTPD -S | awk '/^\*/ { print " ",$0 }' )
fi

# nginx
NGINX_VERSION=$(nginx -v 2>&1 | awk -F'/' '{ print $2 }')
[ -z $NGINX_VERSION ] && NGINX_VERSION="null"
# php
if php -v &> /dev/null; then
    PHP_ROOT=$(php -i | awk 'BEGIN {RS=" "} /--prefix=/' | cut -d "=" -f2 | cut -d "'" -f1)
    PHP_VERSION=$(php -v | awk '/^PHP/ { print $2 }')
    ZEND_ENGINE=$(php -v | awk '/^Zend/ { print $3 }' | cut -b 2-6)
    ZEND_EXTENSION=$(php -v | awk -F',' '/with/ { print $1 }' | grep -v 'the' | awk -F"with" '{ print $2}')
#ZEND_EXTENSION=${ZEND_EXTENSION-null}
    [ -z "$ZEND_EXTENSION" ] && ZEND_EXTENSION=null
else
    PHP_ROOT=null
    PHP_VERSION=null
    ZEND_ENGINE=null
    ZEND_EXTENSION=null
fi

# mysql
if mysql -h127.0.0.1 -p123456 2>&1 | grep ERROR  &> /dev/null; then
    MYSQL_VERSION=$(mysql -V | cut -d' ' -f 6 | cut -d',' -f 1)
else
    MYSQL_VERSION=null
fi

# Mem
MemTotal=$(awk '/^MemTotal/ { print $2 }' /proc/meminfo)
MemTotal=$(expr $MemTotal / 1024)

MemFree=$(awk '/^MemFree/ { print $2 }' /proc/meminfo)
MemFree=$(expr $MemFree / 1024)

MemCached=$(awk '/^Cached/ { print $2 }' /proc/meminfo)
MemCached=$(expr $MemCached / 1024)

MemAvailable=$(expr $MemFree + $MemCached)
MemAvailablel=$(expr $MemAvailable \* 100 / $MemTotal)

SwapTotal=$(awk '/^SwapTotal/ { print $2 }' /proc/meminfo)
SwapTotal=$(expr $SwapTotal / 1024)
SwapFree=$(awk '/^SwapFree/ { print $2 }' /proc/meminfo)
SwapFree=$(expr $SwapFree / 1024)

# DISK
DiskTitle=$(df -h | head -n1)
DiskInfo=$(df -h | awk '/^\/dev\// { print $0 }')

# CPU
CPUCores=$(grep pro /proc/cpuinfo | wc -l)
CPUInfo=$(cat /proc/cpuinfo | grep 'model name' | sort -u | cut -d':' -f 2)
UpTime=$(uptime)

# java
if java -version &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | awk '/version/ { print $0}')
else
    JAVA_VERSION=null
fi

clear
printf "                               System Information Summary\n"
echo "---------------------------------------------------------------------------------------------"
printf "%-25s%-25s%-25s\n" "  OS: CentOS $CentOS_RHEL_version" "OS_BIT: $OS_BIT" "Check Time: $TIME"
printf "%-25s%-25s%-25s\n" "  Eth0: $ETH0" "Eth1: $ETH1" "SSHD_PORT: $SSHD_PORT"
printf "%-20s%-20s\n" "  CPU Cores: $CPUCores" "$CPUInfo"
printf " Uptime: $UpTime\n"
printf "%-10s%-10s%-10s%-10s%-10s%-10s\n" " " "Total" "Free" "Cached" "Available" "AvailablePercentage"
printf "%-10s%-10s%-10s%-10s%-10s%s" "Mem(M)"  "${MemTotal}" "${MemFree}" "${MemCached}" "${MemAvailable}" "${MemAvailablel}"
echo -e "%"
printf "%-10s%-10s%-10s\n" "Swap(M)"  "${SwapTotal}" "${SwapFree}"
echo "---------------------------------------------------------------------------------------------"
echo "$DiskTitle"
echo "$DiskInfo"
echo "---------------------------------------------------------------------------------------------"
echo "- Apache"
printf "%-20s%-25s%-20s\n" "  Version: $HTTPD_VERSION" "Install_type: $HTTPD_INSTALL" "MPM: $MPM"
printf "%-20s%-25s\n" "  User: $APACHE_USER" "ServerRoot: $ServerRoot"
echo "- Virtual Host"
printf "  $VIRTUALHOST\n"
echo "---------------------------------------------------------------------------------------------"
printf "%-10s%-20s\n" "- Nginx" "Version: ${NGINX_VERSION}"
printf "%-10s%-20s\n" "- Java" "Version: ${JAVA_VERSION}"
echo "- PHP"
printf "%-20s%-20s%-30s\n" "  Version: $PHP_VERSION"  "Zend_engine: $ZEND_ENGINE" "php_root: $PHP_ROOT"
echo "- Zend_extension"
printf " $ZEND_EXTENSION\n"
echo "---------------------------------------------------------------------------------------------"
echo "- MySQL"
printf "%-20s\n" "  Version: $MYSQL_VERSION"
echo "---------------------------------------------------------------------------------------------"
