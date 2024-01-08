# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_test_package.py
# @Date    : 2022/07/06:23:55
# @Author  : jinwenlong@oppo.com
from py_package import *
from py_package.order import *
# from py_package.delivery import *
order.create_sales_order()
delivery.create_delivery()
# create_delivery()
import os
print(type(os))
print(type(os.path))