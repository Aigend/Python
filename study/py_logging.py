# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : py_logging.py
# @Date    : 2022/05/13:18:06
# @Author  : jinwenlong@oppo.com

import logging
import threading
"""
日志级别等级排序：critical > error > warning > info > debug

级别越高打印的日志越少，反之亦然，即

debug : 打印全部的日志( notset 等同于 debug )
info : 打印 info, warning, error, critical 级别的日志
warning : 打印 warning, error, critical 级别的日志
error : 打印 error, critical 级别的日志
critical : 打印 critical 级别

一、 Logging 模块日志记录方式
Logging 模块提供了两种日志记录方式：

一种方式是使用 Logging 提供的模块级别的函数
另一种方式是使用 Logging 日志系统的四大组件记录

"""


# 1、Logging 定义的模块级别函数
# 打印日志级别
def local_logging_001():
    logging.debug('Python debug')
    logging.info('Python info')
    logging.warning('Python warning')
    logging.error('Python Error')
    logging.critical('Python critical')


def local_logging_002():
    logging.basicConfig(level=logging.ERROR)  # 注意：Logging.basicConfig() 需要在开头就设置，在中间设置并无作用
    logging.debug('Python debug')
    logging.info('Python info')
    logging.warning('Python warning')
    logging.error('Python Error')
    logging.critical('Python critical')
    logging.log(logging.ERROR, 'test')


def local_logging_003():
    # 1.2 将日志信息记录到文件
    import os
    if not os.path.exists(r'.\temp'):
        os.mkdir(r'.\temp')
    logging.basicConfig(filename=r'.\temp\example.log', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')


def local_logging_004():
    logger = local_logging_004_help_001()
    thread_names = ['Mike', 'George', 'Wanda', 'Dingbat', 'Nina']
    for i in range(5):
        my_thread = threading.Thread(
            target=local_logging_004_help_002, name=thread_names[i], args=(i, logger))
        my_thread.start()


def local_logging_004_help_001():
    logger = logging.getLogger("threading_example")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(r".\temp\threading.log")
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def local_logging_004_help_002(number, logger):
    """
    可以被线程使用的一个函数
    """
    logger.debug(f'{threading.current_thread().getName()} doubler function executing')
    result = number * 2
    logger.debug('doubler function ended with: {}'.format(
        result))


if __name__ == '__main__':
    pass
    # local_logging_001()
    # local_logging_002()
    # local_logging_003()
    local_logging_004()
