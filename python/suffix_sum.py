#!/usr/bin/env python

import os
import sys

def cal_suffix(path='.'):
    ret = {}
    if os.path.exists(path):
        for paths, dirs, files in os.walk(path):
            for file in files:
                if '.' in file:
                    suffix = file.rsplit('.')[-1]
                    if suffix in ret:
                        ret[suffix] += 1
                    else:
                        ret[suffix] = 1
    return ret

if __name__ == '__main__':
    try:
        print cal_suffix(sys.argv[1])
    except Exception:
        print cal_suffix()