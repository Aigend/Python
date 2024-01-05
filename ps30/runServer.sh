#!/usr/bin/sh
#--------------------------------------------
# author:wenlong.jin
# date: 2023.5.17
#--------------------------------------------
##### 用户配置区 开始 #####
#
##### 用户配置区 结束  #####
git pull origin dev_3.0
nohup python3 manage.py runserver 0.0.0.0:8080 &