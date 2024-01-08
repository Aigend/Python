# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_threadingpool.py
# @Date    : 2022/07/16:0:04
# @Author  : jinwenlong@oppo.com
import time
from concurrent.futures import ThreadPoolExecutor  # 并行期货，线程池执行者
"""
pool = ThreadPoolExecutor(100)
pool.submit(函数名,参数1，参数2，参数...)
"""


def task(video_url):
    i = 1
    while True:
        print("开始执行任务", video_url)     # 开始执行任务 www.xxxx-299.com 3
        time.sleep(1)
        i += 1
        if i > 5:
            break


# 创建线程池，最多维护10个线程
threadpool = ThreadPoolExecutor(2)
# 生成300网址，并放入列表
url_list = ["www.xxxx-{}.com".format(i) for i in range(10)]
for url in url_list:
    """
    在线程池中提交一个任务，线程池如果有空闲线程，则分配一个线程去执行，执行完毕后在将线程交还给线程池，
    如果没有空闲线程，则等待。注意在等待时，与主线程无关，主线程依然在继续执行。
    """
    print(url)
    print(threadpool.submit(task, url))

print("等待线程池中的任务执行完毕中······")
threadpool.shutdown(True)   # 等待线程池中的任务执行完毕后，在继续执行
print("END")