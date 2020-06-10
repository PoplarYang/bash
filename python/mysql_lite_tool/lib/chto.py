#!/usr/bin/env python
# encoding: utf-8

""""""
# 1~1024
# kbytes 1024
kbytes = 1024
# mbytes  1024 ** 2
mbytes = 1024 ** 2
# gbytes  1024 ** 3
gbytes = 1024 ** 3
# gbytes  1024 ** 3
tbytes = 1024 ** 4


def is_legal_check(item):
    if item:
        for value in str(item):
            if value in [str(x) for x in xrange(0, 10)]:
                pass
            else:
                return False
        else:
            return True

def chto(item):
    if is_legal_check(item):
        new_item = int(item)
        if new_item < 1024:
            return '%s' % new_item
        elif kbytes <= new_item < mbytes:
            return '%sK' % (new_item/kbytes)
        elif mbytes <= new_item < gbytes:
            return '%sM' % (new_item/mbytes)
        elif gbytes <= new_item < tbytes:
            return '%sG' % (new_item/gbytes)
        elif tbytes <= new_item:
            return '%sT' % (new_item/tbytes)
    else:
        # print 'illegal %s' % (item)
        return item

if __name__ == '__main__':
    l = [1, 1024, 2048, 's' ,10240000]
    print [chto(i) for i in l]
