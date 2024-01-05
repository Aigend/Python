#!/usr/bin/sh
#--------------------------------------------
# author:wenlong.jin
# date: 2023.8.25
#--------------------------------------------
##### 用户配置区 开始 #####
#
##### 用户配置区 结束  #####

#检查5000端口是否被占用，如果占用输出1，如果没有被占用输入0
pIDa=`lsof -i :5000|grep -v "PID" | awk '{print $2}'`
if [ "$pIDa" != "" ];
then
   echo "flask 5000 process has start"
else
   echo "start flask 5000 process"
   python3 app.py &
fi

#NUM=$(ps -ef |grep mediamtx | grep -v grep |wc -l)
#if [ $NUM -ne 0 ]; then
echo "kill -9 mediamtx process"
ps -ef | grep mediamtx | grep -v grep | awk '{print $2}' | xargs kill -9
sleep 10
echo "mediamtx not run, execute runServer.sh"
bash /root/mediamtx/runServer.sh
#fi

COUNT=$(ps -ef |grep ffmpeg | grep -v grep |wc -l)
if [ $COUNT -ne 0 ]; then
    echo "kill -9 ffmpeg rtsp process"
    ps -ef | grep ffmpeg | grep -v grep | awk '{print $2}' | xargs kill -9
    sleep 10
fi
echo "begin ffmpeg rtsp process"
#ffmpeg -re -stream_loop -1 -i ./source/camera_2.mp4  -c copy -f rtsp rtsp://192.168.1.10:8554/Streaming/Channels/102 &
#ffmpeg -re -stream_loop -1 -i ./source/camera_3.mp4  -c copy -f rtsp rtsp://192.168.1.10:8554/Streaming/Channels/103 &
ffmpeg -re -stream_loop -1 -i ./source/camera_4.mp4  -c copy -f rtsp rtsp://192.168.1.10:8554/Streaming/Channels/104 &
#ffmpeg -re -stream_loop -1 -i ./source/camera_5.mp4  -c copy -f rtsp rtsp://192.168.1.10:8554/Streaming/Channels/105 &
echo $1
if [[ $1 == *022012* ]]
then
    ffmpeg -re -stream_loop -1 -i ./source/camera_2_1.mp4  -c copy -f rtsp rtsp://192.168.1.10:8554/Streaming/Channels/106 &
    ffmpeg -re -stream_loop -1 -i ./source/camera_2_8.mp4  -c copy -f rtsp rtsp://192.168.1.10:8554/Streaming/Channels/107 &
fi
sleep 120
echo "rtsp script end ..."