#!/usr/bin/env python
#coding: utf8

import socket
def GetLocalIp():
    """
    获取本机的网络出口IP，并非公网IP
    """
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"

if __name__ == "__main__":
    IPADDR = GetLocalIp()
    print IPADDR
