# ***dev_3.0分支为三代站自动化仿真工具开发分支***
***
### 描述:
    1. 基于python3.6.9 Django 3.2 模板开发，推荐相同版本部署
    2. 部署环境依赖于硬件：如485串口，网口，can口，在docker环境中部署需要解决硬件环境和docker容器的映射
### 环境安装
1. 拉取最新代码
    ```
    git clone -b dev_3.0 git@git.nevint.com:PERD/pangu/simulator/ps20.git ps30
    ```
2. 安装python库
    ```
   推荐pyenv:git clone https://github.com/pyenv/pyenv.git ~/.pyenv
   配置pyenv环境：vim ~/.bashrc
      export PYENV_ROOT="${HOME}/.pyenv"
      if [ -d "${PYENV_ROOT}" ]; then
        export PATH="${PYENV_ROOT}/bin:${PATH}"
        eval "$(pyenv init -)"
      fi
   安装python版本：pyenv install 3.6.9 # 安装版本
   安装插件：git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
   配置环境：
        echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
        source ~/.bashrc
   创建虚拟环境：pyenv virtualenv 3.6.9 py3.6.9 
   安装三方库:python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirement.txt
    ```
3. 启动程序
   ```
   python3 manage.py runserver 0.0.0.0:8080
   ```
4. pp-battery-fe前端代码（暂不操作）
   ```
   属于submodule, 目前部署环境未联网，不支持实时编译前端文件的方式，直接把前端编译的包集成到django的templates下访问
   git clone -b dev_wen git@git.nevint.com:PERD/Cloud/frontend/pp-battery-fe.git
   
   git submodule add -b dev_wen git@git.nevint.com:PERD/Cloud/frontend/pp-battery-fe.git
   git submodule foreach git pull
   
   git submodule update --init --recursive
   ```
5. py_swap 属于消费云端kafka数据的代码，存入mongodb，Django提供接口供脚本侧访问数据库数据
   ```
   消费为stg环境的站的数据，代码在本地无法消费，必须要在luban环境下运行才能成功消费
   git clone -b dev_3.0 git@git.nevint.com:PERD/pangu/simulator/py_swap.git py_swap
   ```
6. uWSGI部署（不推荐，下面描述暂不操作）
   ```
   * pip install -r requirements.txt
   * pip install uwsgi
   * uwsgi --http :8080 --wsgi-file ./kylin/wsgi.py 
   * uwsgi --http :8090 --module kylin.wsgi
   * uwsgi --ini uwsgi.ini 
   * uwsgi --ini /etc/uwsgi9090.ini & /usr/local/nginx/sbin/nginx
   * uwsgi -d --ini uwsgi.ini
   * uwsgi --stop /root/ps20/uwsgi.pid
   * uwsgi restart /root/ps20/uwsgi.pid
   * uwsgi --http :9090 --wsgi-file foobar.py
   * uwsgi --http :9090 --wsgi-file foobar.py --master --processes 4 --threads 2
   * uwsgi --http :9090 --wsgi-file foobar.py --master --processes 4 --threads 2 --stats 127.0.0.1:9191
   * uwsgi --socket 127.0.0.1:3031 --chdir /home/foobar/myproject/ --wsgi-file myproject/wsgi.py --master --processes 4 --threads 2 --stats 127.0.0.1:9191
   ```
7. 调试运行不依赖硬件的模块，可在docker容器中运行（暂不操作）
   ```
    sudo docker build -q -f ./Dockerfile -t "kylin:latest" .
    sudo docker commit --author "wenlong.jin@nio.com" --message "创建kylin容器" 容器ID hrb.nioint.com/ps-cicd/kylin:latest
    sudo docker tag kylin:latest hrb.nioint.com/ps-cicd/kylin:latest
    sudo docker login hrb.nioint.com
    sudo docker push hrb.nioint.com/ps-cicd/kylin:latest
    sudo docker run -it --rm --net="host" --name="kylin" --cpus=2 -v $PWD:/tmp -w /home/build hrb.nioint.com/ps-cicd/kylin:latest /bin/bash ./runServer.sh $1 $2
   ```
### 调试命令
1. 调试常用linux命令：
    ```
    根据端口查询进程：lsof -i :端口
    查看8080端口是否被占用:netstat -anp | grep 8080
   ```
2. 更新proto文件：
    ```
    protoc --python_out=./ ./SCT.proto 
   ```
### SonaType Nexus服务器搭建（用于无法连接外网的的公司内网环境）
```
  1. docker pull sonatype/nexus3
  2. mkdir /mnt/data/nexus/data -p
  3. chown -R 200  /mnt/data/nexus/data
  4. docker run -d -p 8001:8081 --name nexus -v /mnt/data/nexus/data:/nexus-data --restart=always sonatype/nexus3
  5. 步骤4之后，可以通过http:ip:8001访问nexus仓库
  6. docker exec -it 容器ID /bin/bash 
  7. cat /nexus-data/admin.password
     cat /mnt/data/nexus/data/admin.password
  8. 修改配置参数：vim /mnt/data/nexus/data/etc/nexus.properties
  9. 在容器中修改：/opt/sonatype/nexus/bin/nexus.vmoptions
  10. python3 -m pip install -r requirement.txt --index-url=http://10.10.208.121:8001/repository/pypi-proxy/simple --trusted-host=10.10.208.121  
  ```
### Redis 缓存服务器搭建
```angular2html
    sudo apt-get install redis-server
    sudo vim /etc/redis/redis.conf
        # bind 127.0.0.1
        requirepass your_pwd #设置新的密码
    /etc/init.d/redis-server restart

```
