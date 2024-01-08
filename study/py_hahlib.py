# !/user/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/3/17 13:09
# @File: py_hahlib.py
import hashlib
import json

passwd = {
    "bms": "",
    "acdc": "",
    "plc": ""
}
md5 = hashlib.md5()
md5.update(json.dumps(passwd).encode("utf-8"))
md5.update(json.dumps(passwd).encode("utf-8"))
print(md5.digest())
print(md5.digest_size)