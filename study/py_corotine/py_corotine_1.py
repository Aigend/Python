# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_corotine_1.py
# @Date    : 2022/07/16:21:18
# @Author  : jinwenlong@oppo.com
from inspect import getgeneratorstate
from time import sleep


def corotine():
    for i in range(3):
        sleep(0.5)
        x = yield i + 1
        print('-> corotine x=', x)


coro = corotine()
while True:
    try:
        print(f'corotine status:{getgeneratorstate(coro)}')
        coro.send(100)
        next(coro)
        print(f'corotine status:{getgeneratorstate(coro)}')
        next(coro)
        print("**")
        print(f'corotine status:{getgeneratorstate(coro)}')
    except TypeError as e:
        print(e)
        coro = corotine()
        print(next(coro))  # 激活生成器
        continue
    except StopIteration:
        print('coroutine is finished.')
        print(f'corotine status:{getgeneratorstate(coro)}')
        break
