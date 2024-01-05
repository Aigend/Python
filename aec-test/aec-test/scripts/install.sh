#!/usr/bin/sh
#--------------------------------------------
# author:wenlong.jin
# date: 2023.7.18
#--------------------------------------------
##### 用户配置区 开始 #####
#
##### 用户配置区 结束  #####
echo "******install.sh******"
find ./ -maxdepth 1 -name "02[2-3]012" | xargs rm -rf
echo $1
if [[ $1 == *023012* ]]
then
    unzip $1
    find ./ -maxdepth 1 -name "02[2-3]012*.zip" | xargs rm -rf
else
    tar zxvf $1 ./
    find ./ -maxdepth 1 -name "02[2-3]012*.tar.gz" | xargs rm -rf
fi
dir=`find ./ -maxdepth 1 -name "02[2-3]012"`
cd $dir
echo 'NIOpower68!@#$' | sudo -S bash ./install.sh