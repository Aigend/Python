"""
@Author: wenlong.jin
@File: demo.py
@Project: aec-test
@Time: 2023/7/19 14:53
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
import shutil


# files = ["BBSA.json", "BSA.json", "PiP.json", "PPP.json", "RSDS.json", "RSDV_PiP.json", "ViP.json", "WL.json",
#          "WPV.json", "VOR.json", "PiP_Unattended.json"]
# for file in files:
#     file = os.path.join("/usr/local/NIO/config/ai", file)
#     if not os.path.exists(file):
#         continue
#     with open(file, 'rb') as fr:
#         data = json.load(fr)
#         if not ("simulate_mode" in data and not data["simulate_mode"]):
#             continue
#         print(f"modify {file}, set `simulate_mode` true")
#         data["simulate_mode"] = True
#     with open(file, 'w') as fw:
#         json.dump(data, fw)

def copy_task_scheduler(ver):
    if "023012" not in ver:
        return
    source_file = r"/home/nio/task_scheduler.json"
    destination_file = r"/usr/local/NIO/config/ai/task_scheduler.json"
    if os.path.exists(source_file):
        if os.path.exists(destination_file):
            print(f"{destination_file} file exist...")
        shutil.copyfile(source_file, destination_file)
        print(f"{destination_file} copy success")
    else:
        print(f"{source_file} file not exist...")


def check_version(ver):
    ver, ver_ext = os.path.splitext(os.path.basename(ver))
    path = r"/usr/local/NIO/config/ai/aec_info_sender.json"
    if not os.path.exists(path):
        print(f"file {path} not exist")
        sys.exit(1)
    with open(path) as f:
        aec = json.load(f)
        if aec.get("version") in ver:
            print(f"check success, aec version match target {ver}")
            copy_task_scheduler(ver)
            sys.exit(0)
        print(f"AEC version {aec.get('version')} not match target {ver}")
        sys.exit(2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("check aec version")
    parser.add_argument('--ver', default='', help='target version')
    args = parser.parse_args()
    check_version(args.ver)
