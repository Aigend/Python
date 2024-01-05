# !/user/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/17 20:33
# @File: py_gevent.py
import time

import gevent
from gevent import monkey
monkey.patch_all()


def f1(n):
    for i in range(n):
        print(gevent.getcurrent(), i)
        gevent.sleep(1)

def f2(n):
    for i in range(n):
        print(gevent.getcurrent(), i)


def f3(n):
    for i in range(n):
        print(gevent.getcurrent(), i)

print("********")
g1 = gevent.spawn(f1, 5)
print("------")
g2 = gevent.spawn(f2, 5)
print("#####")
g3 = gevent.spawn(f3, 5)
print("&&&")
print("^^^^^")
g1.join()
gevent.sleep(10)
print("@@@")
g2.join()
print("%%%")
g3.join()

# gevent.joinall([g1,g2, g3])