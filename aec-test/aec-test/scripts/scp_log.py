"""
@Author: wenlong.jin
@File: scp_log.py
@Project: aec-test
@Time: 2023/8/28 14:47
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import os
import re
import json


def copy_log():
    for file in os.listdir("."):
        if re.match(r"(\d{4}-\d{1,2}-\d{1,2}_\d{1,2}-\d{1,2}-\d{1,2}\.json)", file):
            print("file:", file)
            with open(file) as f:
                res = json.load(f)
                ts = res.get("start", 0)
                break
    else:
        return
    source_dir = r"/usr/local/NIO/TR"
    destination_dir = r"/home/nio"
    for file in os.listdir(source_dir):
        if file.startswith("ec_ai_app.localhost.root.log.INFO") or file.startswith("mcs_info_processor.localhost.root.log.INFO"):
            source = os.path.join(source_dir, file)
            destination = os.path.join(destination_dir, file)
            mid = int(os.path.getmtime(source) * 1000)
            if mid > ts:
                shutil.copyfile(source, destination)
                print(f"{destination} copy success")


if __name__ == '__main__':
    copy_log()