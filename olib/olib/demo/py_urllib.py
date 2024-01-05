# !/user/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/17 21:00
# @File: py_urllib.py
import gevent
from gevent import monkey
import urllib.request
monkey.patch_all()


def downloader(file_name, url_address):
    req = urllib.request.urlopen(url_address)
    content = req.read()
    with open(file_name, "wb") as f:
        f.write(content)


def main():
    gevent.joinall([
        gevent.spawn(downloader, "绝地求生女解说Corrine宅个人Vlog视频.mp4",
                                 "https://img.dongyoutu.com/20210423/841dd2e192db6c70630ba12112c386f8.mp4"),
        gevent.spawn(downloader, "《跑跑卡丁车：RUSH+》与《绝地求生Mobile》一起联手推出搞笑视频.mp4", "https://img.dongyoutu.com/20210402/1111.mp4")
                    ])


if __name__ == '__main__':
    main()
