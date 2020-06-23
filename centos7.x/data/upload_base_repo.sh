#!/bin/bash

OS_VERSION=7

yum install wget -y
wget http://pkzxwcntr.bkt.clouddn.com/up -O /usr/bin/uploadfile
chmod +x /usr/bin/uploadfile

[ -e "centos_${OS_VERSION}_repo.tar.gz" ] && rm -rf centos_${OS_VERSION}_repo.tar.gz
tar zcf centos_${OS_VERSION}_repo.tar.gz centos_repo
uploadfile -f centos_${OS_VERSION}_repo.tar.gz -b kodoe
