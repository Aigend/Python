# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : logging_01.py
# @Date    : 2022/05/13:18:43
# @Author  : jinwenlong@oppo.com
import logging
logger = logging.getLogger("endlesscode")
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler(stream=None)
sh.setLevel(logging.ERROR)
ft = logging.Formatter(r"%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(ft)

logger.addHandler(sh)

logger.error("1111111111")