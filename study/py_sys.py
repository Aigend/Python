# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_sys.py
# @Date    : 2022/05/12:0:09
# @Author  : jinwenlong@oppo.com
import sys
"""
sys.maxsize
sys.argv
"""


def local_sys_001():
    print(sys.maxsize)  # 9223372036854775807
    print(sys.argv)  # ['F:/code/py/py_study/py_sys.py']
    print(sys.prefix) # E:\Python37
    # print(sys.base_prefix)
    # print(sys.base_exec_prefix)
    # print(sys.)

def local_sys_002():
    print(sys.maxsize)


if __name__ == '__main__':
    local_sys_001()
