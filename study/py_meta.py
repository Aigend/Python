# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_meta.py
# @Date    : 2022/05/19:22:47
# @Author  : jinwenlong@oppo.com
"""
参考：
    https://baijiahao.baidu.com/s?id=1714968279510507597&wfr=spider&for=pc
"""
class Meta(type):
    def __call__(cls, *args, **kwargs):
        print(f"cls in Meta.__call__ is  {cls}")
        return type.__call__(cls, *args, **kwargs)

class Painter(metaclass=Meta):

    def __new__(cls, *args, **kwargs):
        print("Paint __new__")

    def __int__(self):
        print("Paint __init__")

p1 = Painter()
p2 = Painter()

print(p1 is p2) # True