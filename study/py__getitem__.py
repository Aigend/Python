# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py__getitem__.py
# @Date    : 2022/07/16:22:50
# @Author  : jinwenlong@oppo.com
"""
   黄哥Python 联系方式，自己搜
"""


class DataBase:
    """Python 3 中的类"""

    a = 1

    def __init__(self, id, address):
        """初始化方法"""
        self.id = id
        self.address = address
        self.d = {self.id: 1,
                  self.address: "192.168.1.1",
                  }

    def __getitem__(self, key):
        # return self.__dict__.get(key, "100")
        return self.d.get(key, "default")


data = DataBase(1, "192.168.2.11")
print(data.__dict__)
print(DataBase.__dict__)
print(dir(data))
print(dir(DataBase))
print(vars(DataBase))
print(vars(data))
print(data["hi"])
print(data[data.id])
