#!/usr/bin/env python
#coding: utf8
import sys
import os
import socket

def IsOpen(ip,port):
    """
    检测ip的端口是否开放
    """
    socket.setdefaulttimeout(5)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        print True
    except:
        print False

if __name__ == '__main__':
    IsOpen(sys.argv[1],int(sys.argv[2]))
