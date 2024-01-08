#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/4/2 20:30
import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
"""
str.format(args)
str 用于指定字符串的显示样式；args 用于指定要进行格式转换的项，如果有多项，之间有逗号进行分割
在创建显示样式模板时，需要使用{}和：来指定占位符，其完整的语法格式为：
{ [index][ : [ [fill] align] [sign] [#] [width] [.precision] [type] ] }
"""
#以货币形式显示
print("货币形式：{:,d}".format(1000000))
#科学计数法表示
print("科学计数法：{:E}".format(1200.12))

str1 = "人生苦短，我用Python"
a1=len(str1.encode('gbk'))
a2=len(str1.encode())
print(a1)
print(a2)