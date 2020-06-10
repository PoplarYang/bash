#!/usr/bin/expect

set user root
set host 192.168.101.191
set password root

spawn ssh $user@$host
expect {
    "yes/no" { send "yes\r"; exp_continue }
    "password" { send "$password\r" }
}

interact