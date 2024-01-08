#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/4/11 23:10
"""
说明：计时装饰器
版本：V1.0
"""
import time
def say_hello():
    start_time=time.time()
    time.sleep(5)
    print("say hello")
    end_time=time.time()
    print(end_time-start_time)
def say_goodbye():
    start_time=time.time()
    time.sleep(5)
    print("say goodbye")
    end_time=time.time()
    print(end_time-start_time)
def decorator(func):
    """
    这是个计时装饰器
    :param func:
    :return:
    """
    def wrapper(*args,**kwargs):
        pass


if __name__ == '__main__':
    say_hello()
    say_goodbye()