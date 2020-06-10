#!/usr/bin/env python
# coding: utf-8

# 2017-05-26

"""
脚本用于指定的代码服务器拉取代码, 主要有以下特点
    1 apache认证功能
    2 应用版本控制
    3 记录更新日志
    4 记录上一个稳定版本
    5 脚本锁定，一次只能运行一个脚本
    6 部分文件权限控制
"""

import os
import sys
import urllib2
import tarfile
from subprocess import Popen, PIPE
from shlex import shlex
import datetime
# 目录删除模块
import shutil
# 脚本退出时执行模块
from atexit import register

# 开启调试模式
debug = True
# debug = False

# 应用名称
app_name = "wordpress"
# 远程代码服务器，这里是httpd
remote_host = "http://112.124.102.8:94"
# 远程live版本号
remote_live_version_url = os.path.join(remote_host, app_name, "live_version.txt")
# 保存的版本数
versions_to_keep = 3
# 下载文件和解压后文件存放目录
depoly_dir = "/alidata/www/web"
# 应用根目录
doc_root = os.path.join(depoly_dir, "live")
# 应用正在运行的版本
local_live_version_file = os.path.join(depoly_dir, "live_version.txt")
# 上一个稳定版本
last_stable_version_file = os.path.join(depoly_dir, "last_stable_version.txt")
# 应用白名单，正在运行的版本和上个稳定版本保留不删除
app_white_version_list = []
# 进程锁
lock_file = "/tmp/deploy.pid"
# 更改权限
# 相对于web_root的路径
# file_to_change_owner = [ 'wp-admin', 'wp-includes']
file_to_change_owner = []
USER = '' # USER = 'apache'
update_log = os.path.join(depoly_dir, 'update_log')
error_log = os.path.join(depoly_dir, 'error_log')


# 帐号认证
def login(func):
    def wrapper(*args):
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='Secrete Aera',
                                  uri=remote_host,
                                  user='jenkins',
                                  passwd='jenkins')
        opener = urllib2.build_opener(auth_handler)
        # ...and install it globally so it can be used with urlopen.
        urllib2.install_opener(opener)
        return func(*args)
    return wrapper


# 获取远程发布的live版本号
@login
def getRemoteLiveVersion():
    # 代码服务器正在运行的版本
    remote_live_version = urllib2.urlopen(remote_live_version_url).read().rstrip()
    return remote_live_version


# 获取远程的md5值
@login
def getRemoteMd5(version):
    remote_md5_url = os.path.join(remote_host, app_name, "%s-%s.md5" % (app_name, version))
    remote_md5 = urllib2.urlopen(remote_md5_url).read().rstrip()
    return remote_md5


# 直接追加的下载有问题，当下载失败，再次下载会直接追加，导致文件不一致
# @login
# def downloadFile(version):
#    remote_file_url = os.path.join(remote_host, app_name, "%s-%s.tar.gz" % (app_name, version))
#    data = urllib2.urlopen(remote_file_url)
#    download_file = os.path.join(depoly_dir,"%s-%s.tar.gz" % (app_name, version))
#    with open(download_file, "ab") as fd:
#        for item in data:
#            fd.write(item)
#    updateLocalLiveVersion(version)


#下载文件
@login
def downloadFile(version):
   download_file = os.path.join(depoly_dir, "%s-%s.tar.gz" % (app_name, version))
   remote_file_url = os.path.join(remote_host, app_name, "%s-%s.tar.gz" % (app_name, version))
   request = urllib2.urlopen(remote_file_url)
   first = True # 首次写入标志
   while True:
       data = request.read(8192)
       if not data: break
       if first:
           with open(download_file, "wb") as fd:
               fd.write(data)
           first = False
       else:
           with open(download_file, "ab") as fd:
               fd.write(data)
   return True

# @login
# def downloadFile(version):
#     download_file = os.path.join(depoly_dir, "%s-%s.tar.gz" % (app_name, version))
#     remote_file_url = os.path.join(remote_host, app_name, "%s-%s.tar.gz" % (app_name, version))
#     request = urllib2.urlopen(remote_file_url)
#     for k, data in enumerate(request):
#         if k == 0:
#             with open(download_file, "wb") as fd:
#                 fd.write(data)
#         else:
#             with open(download_file, "ab") as fd:
#                 fd.write(data)
#     else:
#         return True


# 计算本地的md5值
def getLocalMd5(version):
    download_file = os.path.join(depoly_dir, "%s-%s.tar.gz" % (app_name, version))
    if os.path.exists(download_file):
        data = Popen(["md5sum", download_file], stdout=PIPE, stderr=PIPE)
        local_md5 = data.stdout.read().split()[0]
        return local_md5
    else:
        if debug: print 'file %s is not exists' % download_file


# 更新本地live版本号
def updateLocalLiveVersion(version):
    with open(local_live_version_file, 'wb') as fd:
        fd.write(version)


# 更新本地stable版本号
def updateLastStableVersion(last_stable_file):
    if last_stable_file:
        last_stable_version = last_stable_file.split('-')[-1]
    else:
        last_stable_version = "unkown"
    with open(last_stable_version_file, 'wb') as fd:
        fd.write(last_stable_version)


# 获取本地live版本号
def getLocalLiveVersion():
    if os.path.exists(local_live_version_file):
        with open(local_live_version_file) as fd:
            local_live_version = fd.read().strip()
    else:
        local_live_version = "0"
    return local_live_version


# 获取本地stable版本号
def getLastStableVersion():
    if os.path.exists(last_stable_version_file):
        with open(last_stable_version_file) as fd:
            last_stable_version = fd.read().strip()
    else:
        last_stable_version = "0"
    return last_stable_version


# 解压并创建连接，发布新版本，
def extractAndLink(version):
    download_file = os.path.join(depoly_dir, "%s-%s.tar.gz" % (app_name, version))
    to_be_live = os.path.join(depoly_dir, "%s-%s" % (app_name, version))
    tar = tarfile.open(download_file)
    tar.extractall(path=depoly_dir)
    if os.path.exists(doc_root):
        last_stable_file = os.readlink(doc_root)
        if last_stable_file != to_be_live:
            os.unlink(doc_root)
    else:
        last_stable_file = False
    os.symlink(to_be_live, doc_root)
    # 更新上个稳定版本记录
    updateLastStableVersion(last_stable_file)
    return True


# 版本排序
def versionSort(l):
    from distutils.version import LooseVersion
    vs = [LooseVersion(i) for i in l]
    vs.sort()
    return [i.vstring for i in vs]


# 退出时，进行版本控制，保留一定数量的版本，不清理白名单中的版本
@register
def keepRightVersion():
    from glob import glob
    globbing = r"%s/%s*" % (depoly_dir, app_name)
    file_list = glob(globbing)
    tar_file_list = [i for i in file_list if i.endswith('tar.gz')]
    if debug: print 'tarfile list %s' % tar_file_list
    tar_to_remove = versionSort(tar_file_list)[:-versions_to_keep]
    if debug: print 'tarfile list to remove %s' % tar_to_remove
    com_file_list = [i for i in file_list if not i.endswith('tar.gz')]
    com_to_remove = versionSort(com_file_list)[:-versions_to_keep]
    getWhiteVersionList()
    if tar_to_remove:
        for item in tar_to_remove:
            if item not in app_white_version_list:
                os.remove(item)
        del item
    if com_to_remove:
        for item in com_to_remove:
            if item not in app_white_version_list:
                shutil.rmtree(item)
        del item


# 程序锁
def lockFile():
    cmd = 'pidof python'
    cmd = list(shlex(cmd))
    ret = Popen(cmd, stdout=PIPE, stderr=PIPE)
    pids_list = ret.stdout.read().strip().split()
    # err = ret.stderr.read()
    if os.path.exists(lock_file):
        with open(lock_file) as fd:
            pid = fd.read().strip()
        if pid:
            if pid in pids_list:
                if debug: print "The %s is running" % __file__
                sys.exit()
            else:
                if debug: print "pidfile %s exists, but process %s has been dead." % (lock_file, __file__)
                os.remove(lock_file)
                sys.exit()
        else:
            os.remove(lock_file)
            sys.exit()
    else:
        with open(lock_file, 'w') as fd:
            fd.write(str(os.getpid()))
        if debug: print "process is start ok with pid %s" % os.getpid()


# 退出时候清理锁
@register
def unLockFile():
    if os.path.exists(lock_file):
        os.remove(lock_file)
        if debug: print "lockfile %s has been removed at end of process." % lock_file


# 更改部分文件权限
@register
def changeFileOwner():
    if file_to_change_owner and USER:
        files = [os.path.join(depoly_dir, 'live', file) for file in file_to_change_owner]
        for item in files:
            if os.path.exists(item):
                cmd = 'chown -R %s:%s %s' % (USER, USER, item)
                os.system(cmd)


# 生成白名单
def getWhiteVersionList():
    version_list = []
    local_version = getLocalLiveVersion()
    if local_version not in version_list:
        version_list.append(local_version)
    last_stable_version = getLastStableVersion()
    if last_stable_version not in version_list:
        version_list.append(last_stable_version)

    for version in version_list:
        targz = os.path.join(depoly_dir, "%s-%s.tar.gz" % (app_name, version))
        app_white_version_list.append(targz)
        dir = os.path.join(depoly_dir, "%s-%s" % (app_name, version))
        app_white_version_list.append(dir)
    if debug: print "white version list: %s" % app_white_version_list


def enlog(message, log_file=update_log):
    remessage = '%s  [ %s ] "%s"\n' % (datetime.datetime.now(), __file__, message)
    with open(log_file, 'ab') as fd:
        fd.write(remessage)


def init():
    # 通过lockfile和pid判断程序是否在执行
    lockFile()
    if not os.path.exists(depoly_dir):
        os.makedirs(depoly_dir)


if __name__ == "__main__":
    init()
    # 版本检查
    remote_live_version = getRemoteLiveVersion()
    local_version = getLocalLiveVersion()
    if remote_live_version != local_version:
        # 下载
        if downloadFile(remote_live_version):
            if debug: print "download version: %s ok" % remote_live_version
            remote_md5 = getRemoteMd5(remote_live_version)
            local_md5 = getLocalMd5(remote_live_version)
            # 检查md5
            if remote_md5 == local_md5:
                if debug: print "check md5 on version: %s ok" % remote_live_version
                # print extractAndLink(remote_live_version)
                if extractAndLink(remote_live_version):
                    updateLocalLiveVersion(remote_live_version)
                    message = 'version update to %s.' % remote_live_version
                    enlog(message)
                    if debug: print "update to version: %s" % remote_live_version
                else:
                    if debug: print "update to version: %s failed" % remote_live_version
            else:
                if debug: print "check md5 on version: %s faild" % remote_live_version
                if debug: print "remote_md5 %s" % remote_md5
                if debug: print "local_md5 %s" % local_md5
        else:
            if debug: print "download version: %s failed, maybe owing to network..." % remote_live_version
    else:
        if debug: print "local server has the same version: %s with remote code server." % remote_live_version
