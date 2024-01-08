#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2022/5/9 0:13
from collections import Counter
s = "safaejqggrbqrblqefqlgvekfvasdasa"
print(Counter(s))
print(type(Counter(s)))#<class 'collections.Counter'>
for key, val in Counter(s).items():
    print(key, ">>>", val) #s >>> 3