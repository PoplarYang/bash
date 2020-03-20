#!/bin/bash

# 资源服务器配置rsync，启用daemon模式
printf "
    Some Attention !!!
1) To ensure rsync daemon work properly, check that port 873 is open to web server and make sure lsync work in local network area.
2) reconfig before you start rsync"
echo
. ./include/CheckRpm.sh
CheckRpm rsync
cat ./conf/rsyncd.conf > /etc/rsyncd.conf

# 密码文件
CheckRpm quiet mkpasswd
RSYNC_PASSWD=$(mkpasswd -l 16)
echo $RSYNC_PASSWD > tmp.password
echo "root:$RSYNC_PASSWD" > /etc/rsyncd.password
chmod 600 /etc/rsyncd.password

# 开机自启
echo "/usr/bin/rsync --daemon --config=/etc/rsyncd.conf" >> /etc/rc.local

# 服务脚本
cp conf/rsyncd.sh /etc/init.d/rsync
chmod +x /etc/init.d/lsyncd

echo "rsyncd install OK"
