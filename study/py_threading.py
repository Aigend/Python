#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2022/5/8 23:57

import threading


def local_threading_001():
    for i in range(5):
        my_thread = threading.Thread(target=local_threading_001_help_01, args=(i,))
        my_thread.start()


def local_threading_001_help_01(number):
    """
    可以被线程使用的一个函数
    """
    print(threading.currentThread().getName())  # "\n"换行符
    print(number * 2)


if __name__ == '__main__':
    local_threading_001()
