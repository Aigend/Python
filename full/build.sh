#!/usr/bin/sh
#--------------------------------------------
# author:wenlong.jin
# date: 2023.10.26
#--------------------------------------------
##### 用户配置区 开始 #####
#
##### 用户配置区 结束  #####
echo "##### build.sh #####"

SCRIPT_PATH=$(
  cd $(dirname $0)
  pwd -P
)

PREFIX="[BUILD]"

echo "$PREFIX Script path: $SCRIPT_PATH"

python3 -m pip install -r /app/requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/ --trusted-host mirrors.tuna.tsinghua.edu.cn

python3 -m pylint --rcfile=/app/pylint.conf /app

