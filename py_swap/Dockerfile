# 设置基础镜像
FROM artifactory.nioint.com/dd-venus-docker-virtual/base/centos7.9python3.8:1.3
# 设置代码文件夹工作目录 /app
WORKDIR /app
# 复制当前代码文件到容器中 /app
ADD . /app
# 设置时间
# RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
# 安装所需的包，这里的requirements文件名需和项目生成的一致
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/ --trusted-host mirrors.tuna.tsinghua.edu.cn
# 执行入口文件
CMD ["python3", "main.py"]
