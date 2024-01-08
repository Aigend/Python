# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_corotine_gevent.py
# @Date    : 2022/07/16:22:09
# @Author  : jinwenlong@oppo.com
from gevent import monkey;

monkey.patch_all()
import gevent
import time


def eat(name):
    print('%s eat 1' % name)
    gevent.sleep(2)
    print('%s eat 2' % name)


def play(name):
    print('%s play 1' % name)
    gevent.sleep(1)
    print('%s play 2' % name)


ctime = time.time()
g1 = gevent.spawn(eat, 'frank')
g2 = gevent.spawn(play, name='frank')
gevent.joinall([g1, g2])

print('主线程执行结束')
print(time.time() - ctime)  # 2.0050058364868164
