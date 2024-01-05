FROM ubuntu:20.04
LABEL authors="wenlong.jin@nio.com"
WORKDIR /tmp
RUN chmod 777 /tmp

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

COPY ./requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn