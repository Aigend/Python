# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_corotine_2.py
# @Date    : 2022/07/16:21:24
# @Author  : jinwenlong@oppo.com
from inspect import getgeneratorstate


def sample_coro2(a):
    print('-> Started: a=', a)
    b = yield a
    print('-> Received: b=', b)
    c = yield a + b
    print('-> Received: c=', c)


coro = sample_coro2(2)
try:
    print(getgeneratorstate(coro))
    print('调用方:', next(coro))
    print(getgeneratorstate(coro))
    # print('调用方:', next(coro))
    print('调用方:', coro.send(4))
    print('调用方:', coro.send(8))
except StopIteration:
    print(getgeneratorstate(coro))