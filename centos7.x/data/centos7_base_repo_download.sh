#!/bin/bash

which wget &> /dev/null || yum install wget -y
which yumdownloader || yum install yum-utils -y

rm -rf /etc/yum.repos.d/*

wget http://mirrors.aliyun.com/repo/epel-7.repo -O /etc/yum.repos.d/epel-7.repo
sed -i '/^.*aliyuncs.*$/d' /etc/yum.repos.d/epel-7.repo
wget http://mirrors.aliyun.com/repo/Centos-7.repo -O /etc/yum.repos.d/Centos-7.repo
sed -i '/^.*aliyuncs.*$/d' /etc/yum.repos.d/Centos-7.repo

yum-config-manager --add-repo https://openresty.org/package/rhel/openresty.repo

yum makecache
yum update -y

targz_dir=/mnt/centos_repo
[ -d $targz_dir ] || mkdir $targz_dir
rm -rf $targz_dir/*

# python
py_group=(
python-chardet
python-devel
python-netaddr
python-pip
python-pymongo
python-requests
python-six
python-setuptools
python-urllib3
)

# 安装小工具
utils_group=(
createrepo
yum-utils
wget
curl
tree
lrzsz 
telnet
net-tools
iproute 
lsof
nmap
screen
numactl
parted
lsscsi
htop
iftop
iotop
ntp
ntpdate 
rpm-build
iptables
iptables-services 
sysstat
dstat
iperf
perf
smartmontools
ipmitool
vim-enhanced
git
openssl
)

lib_group=(
gcc
cmake
perl
libcurl 
libcurl-devel
apr-devel 
subversion-devel
cyrus-sasl-devel
libselinux-python
)

# 安装常用软件
app_group=(
keepalived
pacemaker
docker
openresty
nginx
chrony
memcached
redis
supervisor
httpd
httpd-utils
unbound
rpcbind
dnsmasq
nfs-utils
nfs-common
samba
samba-winbind-clients
samba-winbind 
ctdb
ftp
vsftp
)

function download_pkg() {
    for pkg in $@; do
	echo "downloading $pkg ..."
        yumdownloader --resolve --destdir=$targz_dir -y ${pkg} > /dev/null
    done
}

download_pkg ${py_group[@]}
download_pkg ${utils_group[@]}
download_pkg ${lib_group[@]}
download_pkg ${app_group[@]}

# ansible
yumdownloader --resolve --destdir=$targz_dir -y ansible > /dev/null

find /var/cache/yum/x86_64/7/ -name "*.rpm" -exec mv {} $targz_dir \;

find $targz_dir -name "*686.rpm" -exec rm -f {} \;
find $targz_dir -name "*586.rpm" -exec rm -f {} \;

createrepo --update $targz_dir

