FROM artifactory.nioint.com/dd-venus-docker-virtual/base/centos7.9python3.9:1.0
LABEL authors="wenlong.jin@nio.com"
WORKDIR /app
ADD . /app
RUN python3 -m pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/ --trusted-host mirrors.tuna.tsinghua.edu.cn