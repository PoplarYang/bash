#!/bin/bash
#
# first step to add alias
#add_alias(){
#	echo "#Alias defined by Hiyang @ `date +"%F %T"`" >>  ~/.bashrc
#	ech >> ~/.bashrc
#	cat ./mybashrc.sh >> ~/.bashrc
#	ech >> ~/.bashrc
#	. ~/.bashrc
#}

add_ali_repo(){
	cd /etc/yum.repos.d/
	ls * && tar zc ./* -f bak.tar.gz && rm -rf *.repo
	cd -
	egrep "5\." /etc/issue && linux_version=5
	egrep "6\." /etc/issue && linux_version=6

	cp ./repo/Centos-$linux_version.repo /etc/yum.repos.d/
	cp ./repo/epel-$linux_version.repo /etc/yum.repos.d/
}

add_vimrc(){
#	echo "#Vimrc defined by Hiyang @ `date +"%F %T"`" >>  ~/.vimrc
        cat ./vimrc >> ~/.vimrc
	. ~/.vimrc
}

# Formate
ech-(){
	echo -e "--------------------------------------------------------------------\n"
}
ech(){
	echo -e "####################################################################\n"
}

# Step 1
echo -e "\e[31m Step 1 Alias Setup\n\t\t\t\tListed on this bashrc\e[0m"
ech-
cat ~/.bashrc
ech-
echo -e "\t\t\t\t\e[31mListed on this mybashrc\e[0m"
cat ./mybashrc.sh
read -p "Do you want to source?(y/n) " addalias
test $addalias = "y" && source ./mybashrc.sh && echo -e "\e[32m Source Alias OK.\e[0m"
ech

# Step 2
echo -e "\e[31m Step 2 Ali Repo Setup\n            Listed on this yum.repo.d.\e[0m"
ech-
ls /etc/yum.repos.d/
ech-
read -p "Do you want to add and backup?(y/n) " addrepo
test $addrepo = "y" && add_ali_repo && echo -e "\e[32m Add Repo OK.\e[0m"
ech

# Step 3
echo -e "\e[31m Step 3 Vimrc Setup\n            Listed on this vimrc\e[0m"
ech-
test -e ~/.vimrc && cat ~/.vimrc || echo ".vimrc is not existed." && touch ~/.vimrc
ech-
read -p "Do you want to add?(y/n) " addvimrc
test $addvimrc = "y" && add_vimrc && echo -e "\e[32m Add Vimrc OK.\e[0m"
