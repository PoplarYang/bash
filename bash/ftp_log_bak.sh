#!/bin/bash
#scripts for dirbakup and upload to ftp server.
#author by haojiu 
#create by 
bakdir=mylog
date=`date +%F`

cd /var
tar zcf ${bakdir}_${date}.tar.gz ${bakdir}

sleep 1

ftp -n <<- EOF
open 192.168.142.129    #远程ftp服务器IP
user aaa bbb
put mylog_*.tar.gz
bye
EOF  
rm -rf  mylog_*.tar.gz