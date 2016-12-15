#!/bin/bash
#
# rsync oneinstack shell

# read -t -p "Whether to add iptables! (default n press ENTER) [y/n]" iptables_yn
# if [ $iptables_yn = "y" ]; then
#	iptables -I INPUT $number -p tcp -m state --state NEW -s $src_ip -d $dest_ip -j ACCEPT && echo "add iptables"
# fi

# check rsync
echo "check rsync"
rpm -q rsync && echo "rsync is installed" || yum install -y rsync

echo "root:123456" > /etc/rsyncd.password
chmod 600 /etc/rsyncd.password

# rsyncd configuration
cat rsyncd.conf > /etc/rsyncd.conf

## 开机自启
echo "/usr/bin/rsync --daemon --config=/etc/rsyncd.conf" >> /etc/rc.local

## start shell
cat rsync-daemon > /usr/bin/rsync-daemon
chmod 755 /usr/bin/rsync-daemon

# check install
if [ -s /usr/bin/rsync-daemon -a -s /etc/rsyncd.conf ]; then
	printf "
lsyncd install successful!
/etc/rsyncd.conf        configuration
/usr/bin/rsync-daemon 	start
/etc/rsyncd.password 	password"
fi
