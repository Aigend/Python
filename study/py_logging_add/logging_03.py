# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : logging_03.py
# @Date    : 2022/05/13:19:23
# @Author  : jinwenlong@oppo.com
import logging
import logging.handlers
import os
import time


class logs(object):
    def __init__(self):
        # 获取模块名称，测试的时候直接控模块即可，但是在实际使用的情况下需要针对不同需要进行日志撰写的模块进行命名
        # 列如：通讯协议模块，测试模块，数据库模块，业务层模块，API调用模块
        # 可以考虑 __init__(self,model_name) 这样传入，然后再用一个list规定一下模块名称
        self.logger = logging.getLogger("")
        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET,
                  'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        # 创建文件目录
        logs_dir = "logs"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = '%s.txt' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath,
                                                                   maxBytes=1024 * 1024 * 50,
                                                                   backupCount=5)
        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        rotatingFileHandler.setFormatter(formatter)
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.NOTSET)
        console.setFormatter(formatter)
        # 添加内容到日志句柄中
        self.logger.addHandler(rotatingFileHandler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.NOTSET)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)


"""其他模块可以直接调用输出，在实际情况中最好结合try-catch返回的excepte的值将其输出出来，
而在实际使用中，可以try-catch中的except需要发生了错误需要进行logger.error()输出，也不要吝啬代码量，
在需要进行一些提示信息的地方logger.info()，此外有一些操作可能引发错误也可以logger.warning()，总之不要吝啬，也不要画蛇添足。
最后是其他模块如何调用此模块的代码，封装好的logging模块我命名为loguil2，注意调用它的同时也需要引入logging，重复引用注意留意打包问题。"""

import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger = logs()

    a = [1, 2, 3]
    logger.info("list a only have 1,2,3")
    logger.warning("操作不当可能导致错误发生")
    try:
        print(a[3])
        logger.debug("this is debug")
    except Exception as e:
        logger.error(e)
    finally:
        logger.info("无论如何需要执行此")
