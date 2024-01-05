"""
@Author: wenlong.jin
@File: command.py
@Project: aec-test
@Time: 2023/7/7 11:38
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-


class ExecutorException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.message}"