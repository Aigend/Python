# !/user/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/22 18:29
# @File: py_request.py
from pprint import pprint

import requests

url = 'http://httpbin.org/post'
data = {'a_test': 112233, 'b_test': 223344}
r = requests.post(url=url, data=data).json()
pprint(r)

url = 'http://httpbin.org/post'
data = {'a_test': 112233, 'b_test': 223344}
r = requests.post(url=url, json=data).json()
pprint(r)