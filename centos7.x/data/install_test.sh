#!/bin/bash

rm -rf /etc/yum.repos.d/*

cat >> /etc/yum.repos.d/centos.repo << EOF
[centos]
name=base Packages for centos$releasever
baseurl=file:///mnt/centos_repo/
gpgcheck=0
enabled=1
EOF

yum makecache
yum remove -y fakesystemd

pkgs=(
python-pymongo
numactl
openresty
htop
iotop
lrzsz
lsof
lsscsi
nmap
ntpdate
parted
screen
tree
telnet
python-setuptools
python-requests
python-chardet
python-urllib3
python-pymongo
net-tools
supervisor
python-pip
python-devel
httpd
libcurl
openssl
)

for pkg in ${pkgs[@]}; do
        yum install -y $pkg &> /dev/null
	if [[ $? -eq 0 ]]; then
		echo "install $pkg ok."
	else
		echo "install $pkg failed.."
	fi
done
#subversion-devel
#systemd
#libselinux
#sysstat
#perl
