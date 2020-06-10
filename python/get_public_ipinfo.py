#!/usr/bin/env python
#coding:utf-8

import sys
import urllib2
import socket

def get_ip_info(ip):
    """
    获取公网IP所在的国家和ISP[互联网服务提供商]
    """
    try:
        socket.setdefaulttimeout(10)
        apiurl = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
        content = urllib2.urlopen(apiurl).read()
        data = eval(content)['data']
        code = eval(content)['code']
        if code == 0:
            return data['country_id'],data['isp_id']
        else:
            return data
    except:
        return "Usage:%s IP" % ip

if __name__ == '__main__':
    print get_ip_info(sys.argv[1])
