#!/usr/bin/sh
#--------------------------------------------
# author:wenlong.jin
# date: 2023.7.18
#--------------------------------------------
##### 用户配置区 开始 #####
#
##### 用户配置区 结束  #####
echo "###########"
rm -rf ./resource.json
rm -rf ./report/*
rm -rf ./logs/*
find ./ -maxdepth 1 -name "02[2-3]012*" | xargs rm -rf
echo "Jenkins post data: ${data}"
echo "Jenkins post version: ${version}"
#echo "${data}" > ./resource.json
url=`python3 ./scripts/analyze.py`
echo "download url ${url}"
#wget -q "http://10.110.168.160:9000/pus3.0/P0309823 AT/AEC-APP/023012.1.11.0/023012.1.11.0.zip"
wget -q "${url}"
ver=`find ./ -maxdepth 1 -name "02[2-3]012*"`
if [ ! -f "$ver" ]; then
  echo "##### version download fail"
  python3 ./scripts/analyze.py --func send_pangea_result
  exit 1
fi
sshpass -p 'NIOpower68!@#$' scp $ver nio@192.168.1.13:/home/nio/
sshpass -p 'NIOpower68!@#$' scp ./scripts/install.sh nio@192.168.1.13:/home/nio/
sshpass -p 'NIOpower68!@#$' ssh nio@192.168.1.13 "bash ./install.sh $ver"
sleep 60
if [[ $ver == *023012* ]]
then
    echo "version is 023012, scp task_scheduler_3.json file to AEC"
    sshpass -p 'NIOpower68!@#$' scp ./scripts/task_scheduler_3.json nio@192.168.1.13:/home/nio/task_scheduler.json
else
    echo "version is 022012, scp task_scheduler_2.json file to AEC"
    sshpass -p 'NIOpower68!@#$' scp ./scripts/task_scheduler_2.json nio@192.168.1.13:/home/nio/task_scheduler.json
fi
sshpass -p 'NIOpower68!@#$' scp ./scripts/version.py nio@192.168.1.13:/home/nio/
sshpass -p 'NIOpower68!@#$' ssh nio@192.168.1.13 "sudo python3 ./version.py --ver $ver"
if [ $? -ne 0 ]; then
    echo "##### fail upgrade $ver"
    python3 ./scripts/analyze.py --func send_pangea_result
    exit 1
else
    echo "##### success upgrade $ver"
fi
sleep 20
echo "begin to execute rtsp push stream"
bash rtsp.sh $ver
echo "###########"