"""
@Author: wenlong.jin
@File: settings.py
@Project: full
@Time: 2023/10/25 15:33
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CHARGE_DIR = os.sep.join([BASE_DIR, "data", "charge"])

# BASE_URL = r"http://127.0.0.1:8080/kylin/"
# BASE_URL = r"http://10.160.102.21:8888/kylin/"
# BASE_URL = r"http://10.170.198.4:8888/kylin/"
BASE_URL = r"http://10.143.16.71:8888/kylin/"

PLC_URL = BASE_URL + r"plc/allinfo/set"
PLC_KILL_URL = BASE_URL + r"plc/kill_process/set"

BMS_URL = BASE_URL + r"bms/allinfo/set"
BMS_CLOSE_URL = BASE_URL + r"bms/kill_process/set?kill=bms{0}"

ACDC_URL = BASE_URL + r"acdc/allinfo/set"
ACDC_CLOSE_URL = BASE_URL + r"acdc/kill_process/set?kill=module{0}"
ACDC_KILL_URL = BASE_URL + r"acdc/kill_process/set?kill=all"

PDU_URL = BASE_URL + r"pdu/allinfo/set"
PDU_KILL_URL = BASE_URL + r"pdu/kill_process/set"

DETECT_URL = BASE_URL + r"detect/allinfo/set"

MPC_URL = BASE_URL + r"mpc/allinfo/set"

CLOUD_EVENT_URL = BASE_URL + r"cloud/event/set"
CLOUD_REALTIME_URL = BASE_URL + r"cloud/realtime/set"

AEC_KILL_URL = BASE_URL + r"aec/kill_process/set"

DEBUG_URL = r"http://10.143.16.71:8888/info"

PROXIES = {"http": None, "https": None}

if __name__ == '__main__':
    print(BMS_CLOSE_URL.format(3))
