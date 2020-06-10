#!/usr/bin/env python
#coding:utf-8

import re, urllib2


class Get_public_ip:
    """
    获取本机的公网地址
    """
    def getip(self):
        try:
            # 获取公网ip和归属地
            public_ip = self.visit("http://ip.chinaz.com/getip.aspx")
        except:
            try:
                # 获取公网ip
                public_ip = self.visit("http://ipv4.icanhazip.com/")
            except:
                public_ip = "So sorry!!!"
        return public_ip

    def visit(self, url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+', str).group(0)


if __name__ == "__main__":
    getmyip = Get_public_ip()
    print getmyip.getip()
