# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/4/27 16:35
# @File: pdu_demo.py
import time
from multiprocessing import Process, Pipe


def demo1(out_pipe, in_pipe):
    out_pipe.close()
    while True:
        in_pipe.send({3: 4})
        time.sleep(1)
        in_pipe.send([3, 4, 5])


def demo2(out_pipe, in_pipe):
    in_pipe.close()
    while True:
        data = out_pipe.recv()
        print(type(data))
        print(data)


if __name__ == '__main__':
    out_pipe, in_pipe = Pipe()
    th1 = Process(target=demo1, args=(out_pipe, in_pipe))
    th2 = Process(target=demo2, args=(out_pipe, in_pipe))
    th1.daemon = True
    th2.daemon = True
    th1.start()
    th2.start()
    th1.join()
    th2.join()
