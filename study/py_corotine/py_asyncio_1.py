# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_asyncio_1.py
# @Date    : 2022/07/16:23:49
# @Author  : jinwenlong@oppo.com
import asyncio

@asyncio.coroutine
def hello():
    print("Hello, World!")
    # 异步调用asyncio.sleep(1)
    r = yield from asyncio.sleep(5)
    print("Hello again")

# 获取EventLoop
loop = asyncio.get_event_loop()
# 执行coroutine
print("***")
loop.run_until_complete(hello())
print("###")
loop.close()
