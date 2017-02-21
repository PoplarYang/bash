#!/bin/bash
#

python2=2.7.13
python2_url=https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tar.xz
python3=3.6.0
python3_url=https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz

pyenv_cache=~/.pyenv/cache

yum install -y readline readline-devel readline-static openssl openssl-devel openssl-static sqlite-devel bzip2-devel bzip2-libs

git clone https://github.com/yyuu/pyenv.git ~/.pyenv

echo 'export PYENV_ROOT=$HOME/.pyenv' >> ~/.bash_profile
echo 'export PATH=$PYENV_ROOT/bin:$PATH' >> ~/.bash_profile
echo "eval $(pyenv init -)" >> ~/.bash_profile
exec $SHELL -l

if ! -d $pyenv_cache; then
	mkdir -p $pyenv_cache
fi
cd $pyenv_cache

if ! ls Python-2.7.13.tar.xz; then
	wget $python2_url
fi
pyenv install $python2 -v
pyenv virtualenv $python2 py27

#if ls Python-3.6.0.tar.xz; then
#	wget $python3_url
#fi
#pyenv install $python3 -v
#pyenv virtualenv $python3 py35

git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
echo "eval $(pyenv virtualenv-init -)" >> ~/.bash_profile
echo 'alias py27="pyenv activate py27"' >> ~/.bash_profile
echo 'alias pyenv py35="pyenv activate py35"' >> ~/.bash_profile
echo 'alias pyenv pyd="pyenv deactivate"' >> ~/.bash_profile
source ~/.bash_profile
