#!/bin/bash

printf "
    Some Attention !!!
1) To ensure lsync and rsync work properly, make sure lsync work in local network area.
2) reconfig before you start lsync"
echo
# 资源服务器配置lsync
. ./include/CheckRpm.sh
CheckRpm rsync
CheckRpm lsyncd

# 确保目录
[ -d /var/log/lsyncd ] || mkdir -p /var/log/lsyncd

cat ./conf/lsyncd.conf > /etc/lsyncd.conf

# 密码文件
RSYNC_PASSWD=$(cat tmp.password)
echo "$RSYNC_PASSWD" > /etc/rsyncd.password
chmod 600 /etc/rsyncd.password
rm -rf tmp.password

# 开机自启
echo "/usr/bin/lsyncd -log Exec /etc/lsyncd.conf" >> /etc/rc.local

# 服务脚本
cp conf/lsyncd.sh /etc/init.d/lsyncd
chmod +x /etc/init.d/rsyncd

echo "lsyncd install OK"
