#!/bin/bash
#Description: A shell script to copy parameter1 to parameter2 and Display a progress bar

# Read the parameter for copy,$1 is source dir and $2 is destination dir
dir=$1/*
des=$2
# Test the destination dirctory whether exists
[ -d $des ] && echo "Dir Exist" && exit 1
# Create the destination dirctory
mkdir $des
# Set counter, it will auto increase to the number of source file
i=0
# Count the number of source file
n=$(echo $1/* |wc -w)

for file in $(echo $dir); do
# Calculate progress
    percent=$((100*(++i)/n))
    cat <<EOF
XXX
$percent
Copying file $file ...
XXX
EOF
    /bin/cp -r $file $des &>/dev/null
done | dialog --title "Copy" --gauge "files" 10 70
clear

