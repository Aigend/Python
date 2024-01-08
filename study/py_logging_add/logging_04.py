# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : logging_04.py
# @Date    : 2022/05/13:18:37
# @Author  : jinwenlong@oppo.com

import logging

# 显示消息时间
# logging.basicConfig(format='%(asctime)s %(message)s')
# logging.warning('is when this event was logged.')

# 多次重复定义无效
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# logging.warning('is when this event was logged.')

# # 更改显示消息的格式
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
# logging.debug('Python message format Debug')
# logging.info('Python message format Info')
# logging.warning('Python message format Warning')
