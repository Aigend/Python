#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2022/4/28 15:02

print(">>>>>>  1   <<<<<<<")
# print(filter(lambda x:x%2==1, [3,5,6,8,9,7,1,0]))
# it = filter(lambda x:x%2==1, [3,5,6,8,9,7,1,0])
# for i in it:
#     print(i)

print(">>>>>>  2   <<<<<<<")
# class func_demo(object):
#     def __init__(self):
#         print("super func_demo")
#     name = "zhangsan"
#     def run(self):
#         return "hello func_demo"
# obj = func_demo()
#
# print(hasattr(obj, "name"))
# print(hasattr(obj, "age")) #False
# print(hasattr(func_demo, "name"))
#
# print(setattr(obj, "age", 18)) # 返回None
# print(hasattr(obj, "age"))

print(">>>>>>  3   <<<<<<<")
# rmb_str_value = input("请输入人民币金额： ")
# rmb_value = eval(rmb_str_value)
# usb_vs_rmb = 6.77
# #字符串需要转成数字：eval()方法
# # usd_value = rmb_str_value / usb_vs_rmb
# usd_value = rmb_value / usb_vs_rmb
# print(usd_value)

print(">>>>>>  4   <<<<<<<")
# name = "Are you OK"
# print(name.upper())
# print(name.title())
# print(name.lower())
# print(name.count("y"))

print(">>>>>>  5   <<<<<<<")
# class func_demo2(func_demo):
#
#     def __init__(self, name, age):
#         # super(func_demo2, self).__init__()
#         func_demo.__init__(self)
#         self.__name = name
#         self.__age = age
#         self.address = "shenzhen"
#
#     def run(self):
#         return "hello func_demo2"
#
# print(func_demo2.__mro__) #(<class '__main__.func_demo2'>, <class '__main__.func_demo'>, <class 'object'>)
# func_demo2("lisi", 20)

print(">>>>>>  6   <<<<<<<")
# class Foo(object):
#     def __init__(self, func):
#         self._func = func
#
#     def __call__(self):
#         print ('class decorator runing')
#         self._func()
#         print ('class decorator ending')
#
# @Foo
# def bar():
#     print ('bar')
#
# bar()

# import logging
# def use_logging(level):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             if level == "warn":
#                 logging.warning("%s is running" % func.__name__)
#             elif level == "info":
#                 logging.info("%s is running" % func.__name__)
#             return func(*args)
#         return wrapper
#
#     return decorator
#
# @use_logging(level="warn")
# def foo(name='foo'):
#     print("i am %s" % name)
#
# foo()
#
print(">>>>>>  7   <<<<<<<")
# import unittest.TesCase
# class demo(unittest.TestCase):
#     def __init__(self):
#         pass



# try:
#     divide_num = int(input("请输入被除数： "))
#     answer = 8/divide_num
#     print(answer)
# except ZeroDivisionError:
#     print("you can't divide by zero")
# else:
#     print(answer)
#
#
# import json
# """写入数据到json文件中"""
# numbers = [1,2,3,4,5,6,7]
# filename = "numbers.json"
# with open(filename,"w") as f_obj:
#     json.dump(numbers,f_obj)
#
# """从json文件中读取数据"""
# file_read_name = "numbers.json"
# with open(file_read_name) as f_obj:
#     num = json.load(f_obj)
# print(num)


print(">>>>>>  8   <<<<<<<")
# a = 1
# class ReturnExistObj:
#     def __new__(cls, *args, **kwargs):
#         print("enter __new__ function")
#         if a == 1:
#             # return object.__new__(cls)
#             return super(ReturnExistObj, cls).__new__(cls)
#     def __init__(self):
#         print("enter __init__ function")
#
# ReturnExistObj()

print(">>>>>>  9   <<<<<<<")
# a = 1
# b = 1
# print(id(a))#140735951262752
# print(id(b))#140735951262752
# a = 3
# print(id(a))#140735951262816
# print(id(b))#140735951262752

print(">>>>>>  10   <<<<<<<")
s = "safaejqggrbqrblqefqlgvekfvasdasa"
from collections import Counter
d = dict(Counter(s))
print(d)
#{'s': 3, 'a': 5, 'f': 3, 'e': 3, 'j': 1, 'q': 4, 'g': 3, 'r': 2, 'b': 2, 'l': 2, 'v': 2, 'k': 1, 'd': 1}
list = sorted(d.items(), key = lambda x:x[1],reverse=False)
print(list)
new_d = {}
for lt in list:
    new_d[lt[0]] = lt[1]
print(new_d)

print(">>>>>>  11   <<<<<<<")
a = 11
b = 12
c = [a,13]
print(c) # [11, 13]
a = 10
print(c) # [11, 13]
a = [1,2,3,]
print(c)

d = [1,4]
e = [d]
print(e)
d[0] = 3
print(e)
d = "333"
print(e)


class Demo:

    def __init__(self, a):
        self.a = a
        self.next = None

head = Demo(1)
head2 = Demo(2)
head.next = head2
head2.next = None

dummy = Demo(0)
dummy.next = head
pre = dummy
pre = pre.next
print(pre.a)
print(dummy.a)

print("-------")
from collections import deque
q = deque([3, 4, 5])
for i in range(len(q)):
    q.pop()
    q.appendleft(f"#{i}")

print(q)