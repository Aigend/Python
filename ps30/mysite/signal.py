#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: wenlong.jin
@File: signal.py.py
@Project: ps30
@Time: 2023/7/3 15:13
"""
import django.dispatch
from django.dispatch import receiver
# 创建一个信号
register_signal = django.dispatch.Signal(providing_args=["request", "user"])  # 触发的时候需要传递的参数


# 定义回调函数(即信号接收者)并使用装饰器进行注册
@receiver(register_signal, dispatch_uid="register_callback")
def register_callback(sender, **kwargs):
    print("客户端地址：%s，邮件接收者：%s" % (kwargs['request'], kwargs['user']))
