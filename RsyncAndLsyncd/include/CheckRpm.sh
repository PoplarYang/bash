#!/bin/bash
#
# Check whether rpm is installed or not.
# status: 0 for install
#         1 for not install

CheckRpm(){
    PARA="$*"
    if echo "$PARA" | grep -w "quiet" &> /dev/null; then
        PKG=$(echo "$PARA" | cut -d' ' -f2)
        if rpm -q $PKG &> /dev/null; then
            return 0
        elif yum install -y $PKG &> /dev/null; then
            return 0
        else
            return 1
        fi
    else
        PKG="$PARA"
        if rpm -q $PKG &> /dev/null; then
            echo "$PKG is install"
            return 0
        elif yum install -y $PKG &> /dev/null; then
            echo "$PKG was not install, but now installed."
            return 0
        else
            echo "$PKG install failed."
            return 1
        fi
    fi
}
