#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2022/5/9 0:00
from threading import BoundedSemaphore
# -*- coding:GBK -*-
import threading
import time

sum_1 = 0


def run(i):
    global sum_1
    time.sleep(1)
    # lock.acquire()
    semaphore.acquire()
    sum_1 += 1
    print("线程%s来了,并修改了sum_1的值为：%s" % (i, sum_1))
    semaphore.release()
    # lock.release()


# lock = threading.Lock()
semaphore = threading.BoundedSemaphore(5)

for x in range(10):
    t = threading.Thread(target=run, args=(x,))
    t.start()

while threading.active_count() != 1:
    pass

print("程序结束")
