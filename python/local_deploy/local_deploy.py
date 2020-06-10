#!/usr/bin/env python
#coding: utf8
#python2
# v0.1

#from distutils.version import LooseVersion
import os
import sys
from shutil import copytree, rmtree

last_versions_file = "last_versions"
white_versions_file = "white_versions"
version_to_keep = 3
file_to_change_owner = ['Runtime',]
file_to_clear = ['Runtime',]
app_user = 'www'
app_root = "app_root"
update_type = "delta"


def get_versions_from_file(fp):
    """
    从文件读取版本列表
    :param fp: 文件路径
    :return: 版本列表s
    """
    try:
        ret = []
        with open(fp) as fd:
            for line in fd:
                ret.append(line.strip())
        return ret
    except Exception as e:
        print e
        sys.exit()


def get_last_versions_list():
    last_versions_list = get_versions_from_file(last_versions_file)
    return last_versions_list

def get_live_version():
    # 获取上一个版本
    last_versions_list = get_last_versions_list()
    if last_versions_list:
        live_version_file = last_versions_list[-1]
    else:
        live_version_file = None
    return live_version_file


def backup_live_version(live_version_file, new_version_file):
    """
    备份版本
    :param live_version: 当前版本
    :param new_version: 最新版本(将要更新的版本)
    :return: True or False
    """
    try:
        new_version = version_file_to_version(new_version_file)
        live_version = version_file_to_version(live_version_file)
        if not new_version:
            print "file name is invalid!!!"
            return False
        if os.path.exists(new_version):
            rmtree(new_version)
        if update_type == "delta":
            copytree(live_version, new_version)
        try:
            if os.path.exists(app_root):
                os.unlink(app_root)
        except Exception:
            pass
    except Exception as e:
        print e
        return False
    else:
        return True


def get_new_version_file():
    """
    用户输入版本信息
    :return: new_version_file
    """
    while True:
        new_version_file = raw_input("Plaese input new version file >> ")
        if os.path.exists(new_version_file):
            return new_version_file
        else:
            print "invalid input!!!"
            user_input = raw_input("r for retry or q for quit >> ")
            if user_input == 'r':
                pass
            elif user_input == 'q':
                sys.exit()
            else:
                print "invalid input!!!"


def version_file_to_version(version_file):
    if version_file.endswith('.tar.gz'):
        return version_file.rsplit('.', 2)[0]
    elif version_file.endswith('.zip'):
        return version_file.rsplit('.', 1)[0]
    else:
        return False


def restore_from_last_versions(version_to_restore):
    """
    从以前的版本恢复
    :param last_versions_list: 可以恢复的版本列表
    :return: True or False
    """
    for version in version_to_restore:
        print version
    try:
        while True:
            user_input = raw_input("choose which version to restore , q for quit >> ")
            if user_input in version_to_restore:
                if os.path.exists(user_input):
                    os.unlink(app_root)
                    os.symlink(user_input, app_root)
                    break
                else:
                    print "the version %s doesn‘t exist" % user_input
            elif user_input == 'q':
                return False
            else:
                print "invalid input!!!"
    except Exception as e:
        print e
        return False
    else:
        return True


def update_to_new_version(new_version_file):
    """
    更新到新版本
    :param new_version_file: 新版本文件
    :return:
    """
    try:
        if os.path.isfile(new_version_file):
            new_version = version_file_to_version(new_version_file)
            if new_version_file.endswith('.tar.gz'):
                import tarfile
                tar = tarfile.open(new_version_file)
                tar.extractall()
            elif new_version_file.endswith('.zip'):
                if os.system('unzip -o %s' % new_version_file) != 0:
                    return False
            else:
                print "file %s is invalid" % new_version_file
                return False
            with open(last_versions_file, mode='a') as fd:
                fd.write("%s%s" % (new_version_file, '\n'))
                os.symlink(new_version, app_root)
                return True
        else:
            return False
    except Exception  as e:
        return False


def remove_expired_versions(versions_to_remove):
    """
    删除过期的版本
    :param versions_to_remove:
    :return: None
    """
    try:
        for file in versions_to_remove:
            print file.rsplit('.', 1)[0]
            if os.path.exists(file.rsplit('.', 1)[0]):
                rmtree(file.rsplit('.', 1)[0])
            if os.path.exists(file):
                print file
                os.remove(file)
    except Exception as e:
        print e
        return False
    else:
        return True


def keep_right_version():
    """
    版本检查，保留若干个版本
    :param last_versions_list:
    :param white_versions_list:
    :return: None
    """
    last_versions_list = get_last_versions_list()
    if last_versions_list and len(last_versions_list) > version_to_keep:
        versions_to_remove = last_versions_list[:-version_to_keep]
        white_versions_list = get_versions_from_file(white_versions_file)
        if white_versions_list:
            versions_to_remove = set(versions_to_remove) - set(white_versions_list)

        if remove_expired_versions(versions_to_remove):
            print "remove expired versions successfully..."
        else:
            print "remove expired versions failed..."

        versions_to_keep = last_versions_list[-version_to_keep:]
        with open(last_versions_file, mode='w') as fd:
            for line in versions_to_keep:
                #fd.write("{}{}".format(line, '\n'))
                fd.write("%s%s" % (line, '\n'))


def change_file_owner():
    """
    改变某些文件的属主
    :return:
    """
    if file_to_change_owner and app_user:
        files = [ os.path.join(app_root, file) for file in file_to_change_owner ]
        for item in files:
            if os.path.exists(item):
                cmd = 'chown -R %s:%s %s' % (app_user, app_user, item)
                os.system(cmd)
            else:
                print "the file %s doesn't exist..." % item
    else:
        print "file_to_change_owner or app_user is None"


def clear_file():
    """
    clear current appa cache,such as Runtime in php
    :return:
    """
    if file_to_clear:
        for file in file_to_clear:
            file_to_cleared = os.path.join(app_root, file)
            if os.path.exists(file_to_cleared):
                if os.system("rm -rf %s/*" % file_to_cleared) == 0:
                    print "the file %s has been cleared..." % file_to_cleared
                else:
                    print "the file %s clear failed, need to claer manually..." % file_to_cleared
            else:
                print "the file %s doesn't exist..." % file_to_cleared
    else:
        print "file_to_clear list is None..."


if __name__ == "__main__":

    # 确保版本文件存在
    if not os.path.exists(last_versions_file):
        os.system("touch %s" % last_versions_file)

    # 确保白名单文件存在
    if not os.path.exists(white_versions_file):
        os.system("touch %s" % white_versions_file)

    while True:
        user_input = raw_input("you can choose u for update, r for restore, c for clear cache, q for quit the script >> ")
        if user_input == "u":
            # 获取存在的版本列表
            last_versions_list = get_last_versions_list()

            # 获取上一个版本
            live_version_file = get_live_version()

            # 获取新版本
            new_version_file = get_new_version_file()

            # 上一个版本存在
            if live_version_file:
                if live_version_file != new_version_file:
                    if backup_live_version(live_version_file, new_version_file):
                        print "backup sucessfully..."
                        if update_to_new_version(new_version_file):
                            last_versions_list.append(new_version_file)
                            print "update sucessfully..."
                        else:
                            print "update failed..."
                    else:
                        print "backup failed..."
                else:
                    print "new version file already has been update"

            # 首次更新
            else:
                if os.path.islink(app_root):
                    os.remove(app_root)

                if update_to_new_version(new_version_file):
                    print "update sucessfully..."
                else:
                    print "update failed..."

        elif user_input == "r":
            last_versions_list = get_last_versions_list()
            white_versions_list = get_versions_from_file(white_versions_file)
            if white_versions_list:
                version_to_restore = set(last_versions_list) | set(white_versions_list)
            else:
                version_to_restore = last_versions_list
            if version_to_restore:
                version_to_restore = [version.rsplit('.', 1)[0] for version in version_to_restore]
                if restore_from_last_versions(version_to_restore):
                    print "restore sucessfully..."
                else:
                    print "restore failed..."
            else:
                print "you don’t have files that can be restored..."

        elif user_input == "c":
            clear_file()

        elif user_input == "q":
            break
        else:
            print "invalid input!!!"
    change_file_owner()
    keep_right_version()