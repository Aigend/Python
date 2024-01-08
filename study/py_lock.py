#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2022/5/8 23:58
# -*- coding:utf8  -*-
import random
import threading
import time
num = 100
threading_list = []


def fun():
    global num
    time.sleep(random.random())
    lock.acquire() # 加锁
    print(threading.current_thread().name)
    print("get num:", num, threading.current_thread())
    num += 1
    lock.release()  # 释放锁


# 实例化锁对象
lock = threading.Lock()
for x in range(200):
    t = threading.Thread(target=fun)
    t.start()
    threading_list.append(t)

for x in threading_list:
    x.join()

print("num:", num)