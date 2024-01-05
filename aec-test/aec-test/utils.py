"""
@Author: wenlong.jin
@File: utils.py
@Project: aec-test
@Time: 2023/7/7 11:26
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import os
import socket
from datetime import datetime
from logging.handlers import RotatingFileHandler

import colorlog

# from concurrent_log_handler import ConcurrentRotatingFileHandler


_log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}


class Logger:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, path=os.path.join(os.getcwd(), "logs"), filename="all.log"):
        if hasattr(self, "logger"):
            return
        if not os.path.exists(path):
            os.makedirs(path)
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(filename)s] [line:%(lineno)d] %(message)s',
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
        self.logger.info("#" * 50)

    def get_logger(self):
        return self.logger


log = Logger().get_logger()


def check_ip_address_available():
    """

    :return:
    """
    # ip_address = psutil.net_if_addrs()
    # try:
    #     for eth_name, eth_info in ip_address.items():
    #         for address in eth_info:
    #             if address.family.name == 'AF_INET' and address.address == "192.168.1.10":
    #                 return True
    # except Exception as e:
    #     return False
    host = "192.168.1.10"
    port = "8800"
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, int(port)))
        return True
    except socket.error:
        return False
    finally:
        if s:
            s.close()


def generate_report_data(data):
    """

    :param data:
    :return:
    """
    path = os.path.join(os.getcwd(), "report")
    if not os.path.exists(path):
        os.makedirs(path)
    name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(path, f"{name}.json")
    with open(path, 'w') as fs:
        json.dump(data, fs)


if __name__ == '__main__':
    print(check_ip_address_available())
