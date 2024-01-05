#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: wenlong.jin
@File: __init__.py.py
@Project: ps30
@Time: 2023/7/3 09:58
"""
from multiprocessing import Queue

icc_process_pool = {}
icc_q = {f"icc{i}": Queue() for i in range(4)}  # 保存不同进程的队列对象