#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/11/4 10:48
import os
print(os.path.join("c:\\","log.txt"))
print(os.getcwd())
print(os.chdir("C:\\"))
print(os.getcwd())
print(os.chdir("F:\python_test\lect_1104"))
print(os.getcwd())
try:
    os.chdir('C:\\error')
except Exception as e:
    print(os.getcwd())
print("-----------------------")
print(os.path.abspath("..\\"))
print(os.path.isabs(os.path.abspath(".")))
print(os.path.relpath('C:\\Windows', 'C:\\'))
print(os.path.relpath('C:\\Windows', 'C:\\360Safe\\SoftMgr'))