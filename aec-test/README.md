# aec-test



# Description
脚本模拟MCS和真实的AEC程序进行通信，软件环境依赖python，硬件环境依赖192.168.1.10:8800地址

脚本日志保存在logs文件夹下all.log

结果数据保存在report文件夹下.json文件

install.sh 修改配置文件操作需要添加 nio ALL = NOPASSWD: ALL 到/etc/sudoers

## Getting started
### 1. 本地脚本或docker方式执行
```
方式1:
安装依赖库：
python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
指定测试的换电次数，并启动脚本
python3 executor.py --num number --case Test_Normal_SwapBattery_001 # Test_Normal_SwapBattery_001 为自己要测试的用例名称
```

```
方式2:
下载Docker镜像
sudo docker pull hrb.nioint.com/ps-cicd/aec-test:latest
启动Docker容器
sudo docker run -it --rm --net="host" --name="aec-test" -v $PWD:/tmp hrb.nioint.com/ps-cicd/aec-test:latest python3 executor.py --num number --case Test_Normal_SwapBattery_001
```
### 2. 流水线方式触发
任务已配置运行节点，tag为aec， job链接：
```angular2html
http://pangea-jenkins.nioint.com/job/pangea-PUS3.0-AEC-TEST/
```