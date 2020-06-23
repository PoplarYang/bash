#FROM centos:7.1.1503
#FROM centos:7.2.1511
#FROM centos:7.3.1611
#FROM centos:7.4.1708
#FROM centos:7.5.1804
#FROM centos:7.6.1810
#FROM centos:7.7.1908
FROM centos:7.8.2003
MAINTAINER hiyang echohiyang@foxmail.com
RUN rm -rf /etc/yum.repos.d/*
ADD Centos-7.repo /etc/yum.repos.d/
ADD epel-7.repo /etc/yum.repos.d/
ADD openresty.repo /etc/yum.repos.d/
RUN sed -i 's/keepcache=0/keepcache=1/g' /etc/yum.conf 
RUN echo "nameserver 114.114.114.114" > /etc/resolv.conf
RUN yum install -y yum-utils createrepo epel-release screen
WORKDIR /mnt/
