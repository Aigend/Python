# !/user/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/29 20:15
# @File: py_base64.py
import base64

print(base64.b64encode(b'binary\x00string'))

base64.b64decode(b'YmluYXJ5AHN0cmluZw==')
