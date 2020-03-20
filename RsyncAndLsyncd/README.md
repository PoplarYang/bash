### This script is used to install rsync and lsyncd, so that files between server can be synchronised.
#### Server A serves as resource server, and rsync works as a daemon, ensure port 873 is open to web server.
#### Server B serves as web server, and lsyncd is use to check file, ensure lsyncd log directory is existed.

##### Step 1: bash SyncdInstall.sh, modify /etc/rsyncd.conf according to "#";  --> resource server
##### Step 2: bash LsyncdInstall.sh, modify /etc/lsyncd.conf according to "--". ---> web server