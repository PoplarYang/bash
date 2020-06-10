#!/bin/bash

##################################################################
# Function: switch golang version
# Usage:  bash genv.sh
# Author: echohelloyang@foxmail.com 
# Github: https://github.com/PoplarYang
# Create Day: 2020-06-10
# Modify Time: 
# Version: v1
# For: linux, darwin
##################################################################


INSTALL_DIR=/usr/local
VERSIONS=(
go1.13.11
go1.14.2
go1.14.4
)

function support() {
    echo "Suport versions:"
    for version in ${VERSIONS[@]}; do
        echo -e "\t$version"
    done
}
support
echo "select the number:"
select version in ${VERSIONS[@]}; do
    rm -rf /usr/local/go
    ln -sv /usr/local/${version} /usr/local/go
    if [[ $? -eq 0 ]]; then
        exit 0
    else
        echo "Wrong select, enter number."
    fi
done
