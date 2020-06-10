#!/bin/bash

##################################################################
# Description: 在pyenv环境中安装指定版本的 python
#              为了解决直接从python官网安装缓慢
# Create Day: 2020-06-10
# Modify Time:
# Author: echohelloyang@foxmail.com
# Github: https://github.com/PoplarYang
##################################################################


# $1 python 版本

version=$1
if [ ! -e /.pyenv/cache/Python-$version.tar.xz ]; then
    wget http://mirrors.sohu.com/python/$version/Python-$version.tar.xz -P ~/.pyenv/cache/
fi
pyenv install $version
