# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/7/20 9:26
# @File:constant.py
import os
import psutil
import platform

__all__ = ["PROJECT_DIR", "UTILS_DIR", "COMMON_DIR", "MAIN_DIR", "CGW_DIR", "SERIAL_NODE"]

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UTILS_DIR = os.path.join(PROJECT_DIR, "utils")
COMMON_DIR = os.path.join(PROJECT_DIR, "common")
MAIN_DIR = os.path.join(PROJECT_DIR, "kylin")
CGW_DIR = os.path.join(PROJECT_DIR, "cgw")

CAN_INSTANCE = {}

CAN_NODE_44 = {
    "bms0": "can16",  # C1仓
    "bms1": "can17",  # C2仓
    "bms2": "can18",  # C3仓
    "bms3": "can19",  # C4仓
    "bms4": "can20",  # C5仓
    "bms5": "can21",  # C6仓
    # "bms5": "can19",  # C6仓
    "bms6": "can22",  # C7仓
    "bms7": "can23",  # C8仓
    "bms8": "can24",  # C9仓
    "bms9": "can25",  # C10仓
    "bms10": "can0",  # A1仓
    "bms11": "can1",  # A2仓
    "bms12": "can2",  # A3仓
    "bms13": "can3",  # A4仓
    "bms14": "can4",  # A5仓
    "bms15": "can5",  # A6仓
    "bms16": "can6",  # A7仓
    "bms17": "can7",  # A8仓
    "bms18": "can8",  # A9仓
    "bms19": "can9",  # A10仓
    "bms20": "can10",  # A11仓
}

CAN_NODE_72 = {
    "bms0": "can16",  # C1仓
    "bms1": "can17",  # C2仓
    "bms2": "can18",  # C3仓
    "bms3": "can19",  # C4仓
    "bms4": "can20",  # C5仓
    "bms5": "can21",  # C6仓
    "bms6": "can22",  # C7仓
    "bms7": "can23",  # C8仓
    "bms8": "can24",  # C9仓
    "bms9": "can25",  # C10仓
    # A仓 L4 对应can0，发现无法接收数据，供应商排查
    "bms10": "can1",  # A1仓 L5
    "bms11": "can2",  # A2仓 L6
    "bms12": "can3",  # A3仓 L7
    "bms13": "can4",  # A4仓 L0
    "bms14": "can5",  # A5仓 L1
    "bms15": "can6",  # A6仓 L2
    "bms16": "can7",  # A7仓 L3
    "bms17": "can8",  # A8仓
    "bms18": "can9",  # A9仓
    "bms19": "can10",  # A10仓
    "bms20": "can11",  # A11仓
}

CAN_NODE_HF = {
    "bms0": "can16",  # C1仓
    "bms1": "can17",  # C2仓
    "bms2": "can18",  # C3仓
    "bms3": "can19",  # C4仓
    "bms4": "can20",  # C5仓
    "bms5": "can21",  # C6仓
    "bms6": "can22",  # C7仓
    "bms7": "can23",  # C8仓
    "bms8": "can24",  # C9仓
    "bms9": "can25",  # C10仓
    # A仓 L4 对应can0，发现无法接收数据，供应商排查
    "bms10": "can0",  # A1仓 L5
    "bms11": "can1",  # A2仓 L6
    "bms12": "can2",  # A3仓 L7
    "bms13": "can3",  # A4仓 L0
    "bms14": "can4",  # A5仓 L1
    "bms15": "can5",  # A6仓 L2
    "bms16": "can6",  # A7仓 L3
    "bms17": "can7",  # A8仓
    "bms18": "can8",  # A9仓
    "bms19": "can9",  # A10仓
    "bms20": "can10",  # A11仓
}

u_name = platform.node()
if u_name == "zoo-Default-string":  # 百安
    BMS_CAN_NODE = CAN_NODE_44
    ACDC_CAN_NODE = "can26"
    CDC_CAN_NODE = "can27"
elif u_name == "zoo-AIMB-705G2":  # CHJ
    BMS_CAN_NODE = CAN_NODE_72
    ACDC_CAN_NODE = "can26"
    CDC_CAN_NODE = "can27"
elif u_name == "zoo-AIMB-705G3":  # HF
    BMS_CAN_NODE = CAN_NODE_HF
    ACDC_CAN_NODE = "can11"
    CDC_CAN_NODE = "can12"
else:
    BMS_CAN_NODE = CAN_NODE_72
    ACDC_CAN_NODE = "can26"
    CDC_CAN_NODE = "can27"

SCT_CAN_NODE = "can23"

# meter 接通信板的485串口A1, B1
# sensor 接通信板的485串口A2, B2
# pcu_meter 接PCU板的485串口A1, B1
# pcu_sensor 接PCU板的485串口A2, B2
SERIAL_NODE = {
    "sensor": "/dev/ttyUSB0",
    "meter": "/dev/ttyUSB1",
    "pcu_sensor": "/dev/ttyUSB2",
    "pcu_meter": "/dev/ttyUSB3",
    "detect_1": "/dev/ttyUSB4",
}

PLC_NODE = {
    "ip": "192.168.1.15",
    "port": 8000
}

# Matrix 部署在主控环境下，通过localhost:5003访问，需要让matrix_utils.py在主控linux下启动
MATRIX_NODE = {}

if __name__ == '__main__':
    print(PROJECT_DIR)
