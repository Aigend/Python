"""
@Author: wenlong.jin
@File: aw.py
@Project: aec-test
@Time: 2023/7/19 11:32
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from executor import mcs_init_process

from utils import log
with open("resource.json") as f:
    resource = json.load(f)
    log.info(resource)
mcs_init_process(resource)
