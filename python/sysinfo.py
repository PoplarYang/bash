#!/usr/bin/env python
#coding: utf-8

from subprocess import Popen, PIPE

def getDimSysInfoList():
    """获取System Information部分内容列表
    输入：无
    输出：dmi列表"""
    dmi_sysinfo_list = []
    p = Popen(['dmidecode'], stdout=PIPE)
    dmi_info = p.stdout
    # 使用文件迭代器按行进行遍历
    for line in dmi_info:
        if line.startswith('System Information'):
            # 检测到System Information后，接着上面的for循环继续遍历文件
            for line in dmi_info:
                # 重点：可迭代对象dmi_info，接着外层循环的位置继续迭代
                # 在这个for循环中，检测到'\n'，说明System Information结束，跳出此层for循环
                if line == '\n':
                    break
                else:
                    dmi_sysinfo_list.append(line.strip())
            # 内层的for循环结束，函数返回结果
            return dmi_sysinfo_list

def getInfo():
    """获取System Information并重新组织为字典"""
    dmi_sysinfo_list = getDimSysInfoList()
    # 列表解析和字典解析的结合
    dmidict = {k: v.strip() for k,v in [item.split(':') for item in dmi_sysinfo_list]}
    # 获取指定部分信息字典
    dmidict = {item: dmidict[item] for item in ['Manufacturer','Product Name', 'Version']}
    return dmidict

if __name__ == '__main__':
    dmidict = getInfo()
    for k, v in dmidict.iteritems():
        print '%s: %s' % (k, v)

