# !/user/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/29 20:46
# @File: py_yield.py
# 子生成器
def ttes6t(n):
    i = 5
    while i < n + 5:
        yield i
        i += 1


# 委派生成器
def ttest_yield_from(n):
    print("test_yield_from start")
    yield from ttes6t(n)
    print("test_yield_from end")


for i in ttest_yield_from(3):
    print(i)
