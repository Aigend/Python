# !/user/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/17 21:46
# @File: py_type.py
class MyMeta(type):

    def __new__(cls, *args, **kwargs):
        print("mymeta __new__ ...")
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, class_name, class_bases, class_dic):
        print("mymeta __init__ ...")
        print(self)
        print(class_bases)
        print(self.__bases__)
        print(class_dic)
        if '__doc__' not in class_dic or len(class_dic['__doc__'].strip(' \n')) == 0:
            raise TypeError('类中必须有文档注释，并且文档注释不能为空')


    # def __call__(self, *args, **kwargs):
    #     print("mymeta __call__ ...")


class People(metaclass=MyMeta):
    """

    """
    def __new__(cls, *args, **kwargs):
        print("people __new__ ...")
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        print("people __init__ ...")

    def __call__(self, *args, **kwargs):
        print("people __call__ ...")