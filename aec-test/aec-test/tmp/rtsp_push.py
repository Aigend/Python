"""
@Author: wenlong.jin
@File: rtsp.py
@Project: aec-test
@Time: 2023/8/8 10:36
"""
import multiprocessing
import os.path
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import subprocess as sp

# 自行设置,url为推送的服务器地址
camera_urls = ['rtsp://192.168.1.10:8554/Streaming/Channels/102',
               'rtsp://192.168.1.10:8554/Streaming/Channels/103',
               'rtsp://192.168.1.10:8554/Streaming/Channels/104',
               'rtsp://192.168.1.10:8554/Streaming/Channels/105']


def rtsp_popen(name, url, resource):
    command = ["ping", "www.baidu.com"]
    command = ['ffmpeg',
               '-re',
               '-stream_loop',
               '-1',
               '-i', resource,
               '-c', 'copy',
               '-f', 'rtsp',
               url]
    if os.path.exists(f"logs/{name}.log"):
        os.remove(f"logs/{name}.log")
    with open(f"logs/{name}.log", "ab") as log:
        proc = sp.Popen(command, stdout=log, stderr=log, close_fds=True)
        proc.wait()
    while True:
        time.sleep(5)


if __name__ == '__main__':

    pros = []
    for i in range(len(camera_urls)):
        print("###")
        pro = multiprocessing.Process(target=rtsp_popen,
                                      args=(f"camera_{i + 2}", camera_urls[i], f'out_put.mp4'))
        pro.daemon = True
        pros.append(pro)
        pro.start()

    for pro in pros:
        pro.join()
