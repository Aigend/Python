#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/16 15:46
# @Author  : wenlong.jin@nio.com
# @File    : log.py
# @Software: ps20
import os
import logging
from logging.handlers import RotatingFileHandler


class _Logger:

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, "_instance"):
    #         cls._instance = super(_Logger, cls).__new__(cls, *args, **kwargs)
    #     return cls._instance


    def __init__(self, path=os.path.join(os.getcwd(), "logs")):
        if not os.path.exists(path):
            os.makedirs(path)
        if not hasattr(self, "logger"):
            self.logger = logging.getLogger(path)
            self.logger.setLevel(logging.DEBUG)
            fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s] [line:%(lineno)d] %(message)s',
                                    '%Y-%m-%d %H:%M:%S')
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(fmt)
            console_handler.setLevel(logging.INFO)

            all_handler = RotatingFileHandler(filename=os.path.join(path, "test.log"), maxBytes=50 * 1024 * 1024,
                                              backupCount=3, encoding='utf-8')
            all_handler.setFormatter(fmt)
            all_handler.setLevel(logging.DEBUG)

            if not self.logger.handlers:
                self.logger.addHandler(console_handler)
                self.logger.addHandler(all_handler)

    def get_logger(self):
        return self.logger


log = _Logger().get_logger()
