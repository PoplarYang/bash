#!/usr/bin/env python
# encoding: utf-8
# python3

from socket import *
from time import ctime

HOST = ''
PORT = 1000
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 创建套接字
tcpSerSock = socket(AF_INET, SOCK_STREAM)
#tcpSerSock.settimeout(5)
# 绑定套接字
tcpSerSock.bind(ADDR)
# 监听套接字
tcpSerSock.listen(5)

try:
    print 'TCP server litenning on port %s now.' % PORT
    while True:
        print 'waiting for connection ...'
        # 等待接收客户端建立连接连接
        tcpCliSock, addr = tcpSerSock.accept()
        print 'client connected from:', addr
        while True:
            print 'waiting for data'
            # 等待接收客户端数据
            data = tcpCliSock.recv(BUFSIZE)
            # 如果客户端发送的数据为空，结束本次连接
            if not data:
                print 'There is no data.'
                tcpCliSock.close()
                break

            print 'recieve data "%s"' % data
            tcpCliSock.send('[%s] %s' % (data, ctime()))
except (EOFError, KeyboardInterrupt):
    pass
finally:
    tcpSerSock.close()
    print 'Server is stopped...'
