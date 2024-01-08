# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_asyncio_add_done_callback.py
# @Date    : 2022/07/17:0:01
# @Author  : jinwenlong@oppo.com
from time import time
import asyncio


async def f():
    print("i'm coroutine")
    return "return i'm coroutine"


def callback(future):
    print('result is {}'.format(future.result()))


start = time()
coroutine = f()
# 获取当前主线程的事件轮循队列
loop = asyncio.get_event_loop()
# 创建任务
task = loop.create_task(coroutine)
# 绑定回调函数
task.add_done_callback(callback)
# 执行任务
loop.run_until_complete(task)
print(task)

end = time()
print('it takes %d seconds' % (end-start))

