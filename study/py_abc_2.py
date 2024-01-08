# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_abc_2.py
# @Date    : 2022/07/17:11:53
# @Author  : jinwenlong@oppo.com
from abc import ABCMeta, abstractmethod

"""
    工厂模式：
    不直接向客户端暴露创建对象的细节，而是通过一个工厂类来负责
    创建产品类的实例。
"""


# 抽象产品角色
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def pay(self, money):
        pass

    def test(self, name):
        print("###")


# 具体产品角色
class AliPay(Payment):
    def pay(self, money):
        print("支付宝支付%d元" % money)


class WechatPay(Payment):
    def pay(self, money):
        print("微信支付%d元" % money)


# 工厂角色
class CreatePayment:
    @classmethod
    def create_payment(cls, name):
        if name == "ali":
            return AliPay()
        elif name == "wechat":
            return WechatPay()
        else:
            raise TypeError("No such payment named %s." % name)


# 抽象类是否可以实例化
# pay = Payment() # 不可以进行实例化

# 客户端调用
p = CreatePayment()
payment = p.create_payment('wechat')
payment.pay(100)
