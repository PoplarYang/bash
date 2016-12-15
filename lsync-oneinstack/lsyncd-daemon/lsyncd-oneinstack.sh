#!/bin/bash
#
# lsyncd oneinstack shell

configure(){
    [ -e /var/log/lsyncd ] || mkdir -p /var/log/lsyncd
    echo '123456' > /etc/rsyncd.password
    chmod 600 /etc/rsyncd.password

    ## start lsyncd at starting up
    echo "/usr/bin/lsyncd -log Exec /etc/lsyncd.conf" >> /etc/rc.local

    cat lsyncd.conf > /etc/lsyncd.conf

    # start script
    cat lsyncd-daemon > /usr/bin/lsyncd-daemon
    chmod +x /usr/bin/lsyncd-daemon

    # check install
    if [ -s /usr/bin/lsyncd-daemon -a -s /etc/rsyncd.password -a -s /etc/lsyncd.conf -a -d /var/log/lsyncd ]; then
        printf "
    lsyncd install successful!
    /usr/bin/lsyncd-daemon  start
    /etc/lsyncd.conf        configuration
    /var/log/lsyncd         logs
    /etc/rsyncd.password    password"
    fi
    echo
}

# check rsync and lryncd
echo "check rsync and lryncd"
rpm -q rsync && echo -e "rsync is installed.\n" || yum install -y rsync
rpm -q lsyncd && echo -e "lsyncd is installed.\n" && lsyncd_install=0 || yum install -y lsyncd

# lsyncd configuration
## make sure some file and dir
if [ -n $lsyncd_install ]; then
    read -t 15 -p "Do you want to reconfigure it?(default n) [y/n] " lsyncd_yn
else
    configure
fi

if [[ ! $lsyncd_yn =~ ^[y|n]$ ]]; then
    echo "Wrong input, please input y or n."
else
    if [ $lsyncd_yn = 'y' ]; then
        configure
    else
        echo "Don't install or configure."
    fi
fi


