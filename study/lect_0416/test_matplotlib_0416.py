#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/4/16 23:10

# class Dog(object):
#     food = "gutou"
#     age = "1"
#     def __init__(self, name):
#         self.NAME = name
#         print(self.NAME)
#     # @classmethod
#     # def eat(self,age): #只能是类中的变量
#     #     print(self.NAME)
#     #     print(age)
#     #     print(self.food)
#
#     # @classmethod
#     # def eat1(self, age):  # 只能是类中的变量
#     #     # print(self.NAME)
#     #     age = "2"
#     #     self.food = "tang"
#     @staticmethod
#     def print_1():
#         print(Dog.food, Dog.age)
#         # print(self.NAME)

# d = Dog("labuladuo")
# # d.eat(Dog.age)    #通过对象调用
# # Dog.eat(Dog.age)  #通过类调用
# # print("-----1-----")
# # d.eat1(Dog.age)
# # Dog.print_1()
# # print("--------2-------")
# # Dog.eat1(Dog.age)
# d.print_1()

class Dog(object):
    food = "gutou"
    age = "1"
    def __init__(self, name):
        self.NAME = name
        print(self.NAME)

    def pr(self):
        print(Dog.food,Dog.age)
        print(self.food,self.age)
        print("2222222222")
    @staticmethod
    def print_1():
        print(Dog.food, Dog.age)
        print("1111")
        # print(self.NAME)

d = Dog("labuladuo")
d.print_1()
d.pr()
