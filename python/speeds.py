#!/usr/bin/python
#coding: utf8

# 获取实时网速

import time
import sys
import os

from misc import KMG

kmg = KMG(1024)

def get_speed():
    info = {}
    with open('/proc/net/dev') as fd:
        for line in fd:
            if line.startswith('Inter') or line.startswith(' face'):
                pass
            else:
                line = line.split()
                info[line[0].strip(":")] = [line[1], line[3], line[9], line[11]]
    return info

def speed_readable(speed):
    if speed < kmg.k:
        speed = "%s B/s" % speed
    elif kmg.k <= speed < kmg.m:
        speed = "%s KB/s" % (speed/kmg.k)
    elif kmg.m <= speed < kmg.g:
        speed = "%s MB/s" % (speed/kmg.m)
    elif kmg.g <= speed < kmg.t:
        speed = "%s MB/s" % (speed/kmg.g)
    return speed

while True:
    pre_info = get_speed()
    time.sleep(1)
    post_info = get_speed()
    os.system( 'clear' )
    print "%-10s %15s %15s %15s %15s" % ('Interface', "Receives", "R-errors", "Transmits", "T-errors")
    try:
        for key in pre_info:
            rx = int(post_info[key][0]) - int(pre_info[key][0])
            rx = speed_readable(rx)

            re = int(post_info[key][1]) - int(pre_info[key][1])
            re = speed_readable(re)

            tx = int(post_info[key][2]) - int(pre_info[key][2])
            tx = speed_readable(tx)

            te = int(post_info[key][3]) - int(pre_info[key][3])
            te = speed_readable(te)
            print("%-10s %15s %15s %15s %15s" % (key, rx, re, tx, te))
    except Exception as e:
        print(e)
        sys.exit()
