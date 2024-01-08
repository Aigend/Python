#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/4/12 18:51

import json
"""写入数据到json文件中"""
numbers = [1,2,3,4,5,6,7]
filename = "numbers.json"
with open(filename,"w") as f_obj:
    json.dump(numbers,f_obj)

"""从json文件中读取数据"""
file_read_name = "numbers.json"
with open(file_read_name) as f_obj:
    num = json.load(f_obj)
print(num)