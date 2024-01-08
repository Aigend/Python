#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/4/3 23:49
"""
os.path.join() 函数来做这件事很简单。
如果将单个文件和路径上的文件夹名称的字符串传递给它，os.path.join() 就会返回一个文件路径的字符串，包含正确的路径分隔符。
"""
import os
myFiles = ['accounts.txt', 'details.csv', 'invite.docx']
for filename in myFiles:
    print(os.path.join('F:\\demo\\exercise', filename))

# os.getcwd() 函数可以取得当前工作路径的字符串
#os.chdir() 改变它.如果使用 os.chdir() 修改的工作目录不存在，Python 解释器会报错
"""
当前工作目录为 "C:\Windows\System32"，
若文件 demo.txt 就位于这个 System32 文件夹下，
则 demo.txt 的相对路径表示为 ".\demo.txt"（其中 .\ 就表示当前所在目录）
使用相对路径表示某文件所在的位置时，除了经常使用 .\ 表示当前所在目录之外，还会用到 ..\ 表示当前所在目录的父目录
"""

