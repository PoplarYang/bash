#!/usr/bin/env python
#coding: utf-8 

import os
import sys

#########################################################
# kmgt模块
Kbyte = 1024.0 ** 1
Mbyte = 1024.0 ** 2
Gbyte = 1024.0 ** 3
Tbyte = 1024.0 ** 5
Pbyte = 1024.0 ** 6

def kmgt(item):
    """
    可视化显示文件字节
    """
    try:
        item = int(item)
    except Exception:
        return item
    if item <= 0:
        return item
    elif 0 < item < Kbyte:
        return "{0}".format(item)
    elif Kbyte <= item < Mbyte:
        return "{0:.2f}{1}".format(item/Kbyte, 'k')
    elif Mbyte <= item < Gbyte:
        return "{0:.2f}{1}".format(item/Mbyte, 'M')
    elif Gbyte <= item < Tbyte:
        return "{0:.2f}{1}".format(item/Gbyte, 'G')
    elif Tbyte <= item < Pbyte:
        return "{0:.2f}{1}".format(item/Tbyte, 'T')
    elif Pbyte <= item:
        return "{0:.2f}{1}".format(item/Pbyte, 'P')
#########################################################


def search_bigfile(path='.', max_num=10):
    """
    查找大文件，默认是查找当前目录下的钱10条
    """
    li = list()
    if os.path.exists(path):
        for paths, dirs, files in os.walk(path):
            if not paths.startswith('/dev') and not paths.startswith('/proc') and not paths.startswith('/sys'):
                for fl in files:
                    abs_path = os.path.join(paths,fl)
                    try:
                        size = os.path.getsize(abs_path)
                    except Exception:
                        continue
                    li.append((abs_path, size))
    return sorted(li, key=lambda x: x[1], reverse=True)[:max_num]

if __name__ == '__main__':
    try:
        for item, size in search_bigfile(sys.argv[1], int(sys.argv[2])):
            print item, kmgt(size)
    except Exception:
        for item, size in search_bigfile():
            print item, kmgt(size)

