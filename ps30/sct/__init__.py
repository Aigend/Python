# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/17 15:17
# @File: __init__.py.py
from multiprocessing import Queue

sct_process_pool = {}
sct_q = {f"sct{i}": Queue() for i in range(4)}  # 保存不同进程的队列对象
