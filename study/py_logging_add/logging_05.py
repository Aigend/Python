# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : logging_05.py
# @Date    : 2022/05/13:18:35
# @Author  : jinwenlong@oppo.com

import logging
import logging_05_help_01


def main():
    logging.basicConfig(filename='logging_05_help_temp_01.log', level=logging.DEBUG)
    logging.info('Started')
    logging_05_help_01.do_something()
    logging.info('Finished')


if __name__ == '__main__':
    main()
