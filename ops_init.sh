#!/bin/bash

##################################################################
# Description: 系统初始化时sshd需要修改的参数脚本
# Create Day: 2020-06-10
# Modify Time: 
# Author: echohelloyang@foxmail.com 
# Github: https://github.com/PoplarYang
##################################################################

echo abc123 | passwd root --stdin
sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication no//g' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sed -i 's/^.*UseDNS yes$/UseDNS no/g' /etc/ssh/sshd_config
service sshd restart
