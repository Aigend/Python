"""
@Author: wenlong.jin
@File: log.py
@Project: full
@Time: 2023/10/25 14:28
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from logging.handlers import RotatingFileHandler

import colorlog

from config.settings import BASE_DIR

__all__ = ["log", ]


_log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}


class Logger:

    def __init__(self, path=os.path.join(BASE_DIR, "log"), filename="test.log"):
        if hasattr(self, "logger"):
            return
        if not os.path.exists(path):
            os.makedirs(path)
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(filename)s] [line:%(lineno)d] %(message)s',
                                '%Y-%m-%d %H:%M:%S')
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(filename)s] [line:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=_log_colors_config
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)

        file_handler = RotatingFileHandler(filename=os.path.join(path, filename), mode="a",
                                           maxBytes=1024 * 1024 * 1024, backupCount=1, encoding='utf-8')
        file_handler.setFormatter(fmt)
        file_handler.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


log = Logger().get_logger()