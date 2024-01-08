# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_abc_1.py
# @Date    : 2022/07/17:0:38
# @Author  : jinwenlong@oppo.com
from abc import ABCMeta, abstractmethod


# 生成实现类
class Foo:
    def __getitem__(self, index):
        ...

    def __len__(self):
        ...

    def get_iterator(self):
        return iter(self)


# 生成基类，
class MyIterable(metaclass=ABCMeta):
    # 我是一个虚拟方法
    @abstractmethod
    def __iter__(self):
        while False:
            yield None

    def get_iterator(self):
        return self.__iter__()

    @classmethod
    def __subclasshook__(cls, C):
        if cls is MyIterable:
            if any("__iter__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented


# 将实现类注册到虚拟类中
MyIterable.register(Foo)
