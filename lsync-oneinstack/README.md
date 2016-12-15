第1步 资源端部署rsync，注意在rsyncd.password文件重新生成密码，默认为root:123456;
修改配置文件；
若防火墙有限制，则需要授权；
rsyncd-daemon start 启动

第2步 被同步端部署lsync，注意在rsyncd.password文件重新生成密码，默认为root:123456;
配置文件中修改src和dest
lsyncd-daemon start 启动；

第3步 测试

注意：
    被同步端的目录因为涉及上传，所以启动httpd的用户需要有读写权限.