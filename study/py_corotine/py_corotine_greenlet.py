# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_corotine_greenlet.py
# @Date    : 2022/07/16:21:34
# @Author  : jinwenlong@oppo.com
from greenlet import greenlet
import time


def task_1():
    print("###")
    while True:
        print("--This is task 1!--")
        g2.switch()
        print("￥￥￥￥")# 切换到g2中运行
        time.sleep(0.5)


def task_2():
    print("***")
    while True:
        print("--This is task 2!--")
        g1.switch()  # 切换到g1中运行
        print("$$$")
        time.sleep(0.5)


if __name__ == "__main__":
    g1 = greenlet(task_1)  # 定义greenlet对象
    print(type(g1))
    from typing import Coroutine
    print(isinstance(g1, Coroutine))
    g2 = greenlet(task_2)
    print("@@@")
    g1.switch()  # 切换到g1中运行
