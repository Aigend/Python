FROM ubuntu:20.04
LABEL authors="wenlong.jin@nio.com"
WORKDIR /tmp
RUN chmod 777 /tmp

RUN apt-get -qq update && DEBIAN_FRONTEND="noninteractive" apt-get -qq install -y \
    apt-utils \
    cmake \
    golang \
    wget \
    curl \
    doxygen \
    unzip \
    vim \
    git \
    can-utils \
    iputils-ping \
    net-tools \
    htop \
    axel \
    lzma \
    liblzma-dev \
    libbz2-dev \
    libffi-dev \
    libncurses-dev \
    libreadline-dev \
    libssl-dev \
    libsqlite3-dev \
    build-essential \
    zlib1g-dev \
    libdbus-1-3 \
    libfreetype6 \
    libfontconfig \
    libx11-6 \
    libgl1-mesa-dev \
    libsm6 \
    libice6 \
    libc6-dev \
    libxext6 \
    libxrender1 \
    libxcomposite1 \
    libxkbcommon-x11-0 \
    libwayland-cursor0 \
    libclang-dev  \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ARG PYENV_TAG=v2.3.13
RUN git clone https://github.com/pyenv/pyenv.git /usr/local/.pyenv \
    && cd /usr/local/.pyenv \
    && git checkout -b local v2.3.13

ENV TZ=Asia/Shanghai
ENV PYENV_ROOT=/usr/local/.pyenv
ENV PATH=$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

ARG PYTHON_VERSION=3.6.9
RUN mkdir -p /usr/local/.pyenv/cache \
    && wget https://npm.taobao.org/mirrors/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz -P /usr/local/.pyenv/cache/ \
    && pyenv install $PYTHON_VERSION \
    && pyenv global $PYTHON_VERSION

COPY ./requirement.txt requirement.txt
COPY ./runServer.sh runServer.sh

# 通过sonatype安装
# RUN python3 -m pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

RUN python3 -m pip install -r requirement.txt --index-url=http://10.10.208.121:8001/repository/pypi-proxy/simple --trusted-host=10.10.208.121