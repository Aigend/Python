# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_adapter_2.py
# @Date    : 2022/07/17:0:34
# @Author  : jinwenlong@oppo.com
from abc import ABC, abstractmethod


class Target(ABC):
    @abstractmethod
    def operation1(self):
        pass

    @abstractmethod
    def operation2(self):
        pass


class Adaptee:
    def operation1(self):
        str(self)
        print('adaptee.operation1')


class Adapter(Target):
    def __init__(self):
        self.adaptee = Adaptee()

    def operation1(self):
        self.adaptee.operation1()

    def operation2(self):
        print('adaptee.operation2')


if __name__ == '__main__':
    adapter = Adapter()
    adapter.operation1()
    adapter.operation2()