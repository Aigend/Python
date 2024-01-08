# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/4/10 18:44
# @File: py_mul.py
from multiprocessing import Process, Lock, Value

import time


def add_one(lock, num):
    for i in range(3):
        lock.acquire()
        num.value += 1
        print(num.value)
        time.sleep(1)
        lock.release()


if __name__ == '__main__':
    num = Value('i', 0)
    lock = Lock()
    p1 = Process(target=add_one, args=(lock, num))
    p2 = Process(target=add_one, args=(lock, num))
    p1.start()
    p2.start()
