# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_asyncio_2.py
# @Date    : 2022/07/16:23:51
# @Author  : jinwenlong@oppo.com
import threading
import asyncio
num = 1
@asyncio.coroutine
def hello(name):
    global num
    if num == 1:
        num += 1
        print("@@@")
    else:
        print("$$$")
    print('Hello, World! (%s) (%s)' % (threading.currentThread(), name))
    yield from asyncio.sleep(5)
    print('Hello, again! (%s) (%s)' % (threading.currentThread(), name))

loop = asyncio.get_event_loop()
tasks = [hello("###"), hello("***")]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

# 第二行和第三行中间暂停1秒
'''
Hello, World! (<_MainThread(MainThread, started 4749815296)>)
Hello, World! (<_MainThread(MainThread, started 4749815296)>)
Hello, again! (<_MainThread(MainThread, started 4749815296)>)
Hello, again! (<_MainThread(MainThread, started 4749815296)>)
'''
