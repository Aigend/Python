# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py__getattribute__.py
# @Date    : 2022/07/16:21:06
# @Author  : jinwenlong@oppo.com
class Attribute(object):
    def __init__(self, name):
        self.name = name

    def __getattribute__(self, key):
        try:
            print('calling __getattribute__.{key}'.format(key=key))
            # 调用超类
            return super(Attribute, self).__getattribute__(key)
            # return object.__getattribute__(self, key)
        except KeyError:
            return 'default'
        # except AttributeError as ex:  # 捕获了该异常就不用调用__getattr__
        #     print(ex)

    def __getattr__(self, key):
        # 什么时候被调用:
        # 1.当属性不在实例以及基类和祖先类的__dict__
        # 2. 当触发AtrributeError异常时(不仅仅是__getattribute__()引发的 AttributeError),porperty中定义的get()方法也会抛出异常
        print('calling __getattr__.{key}'.format(key=key))
        # return 'default'


if __name__ == '__main__':
    print(Attribute("###").address)
