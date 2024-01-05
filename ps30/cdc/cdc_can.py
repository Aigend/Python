"""
@Project: ps30
@File: cdc_can.py
@Author: wenlong.jin
@Time: 2023/11/29 10:50
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time

import can

from utils.log import log


def cdc_run(out_pipe, in_pipe, can_node):
    """
    目前只是读取主控下发给CDC的限制功率值
    """
    bus = can.interface.Bus(bustype="socketcan", channel=can_node, bitrate=125000)
    cdc_instance = {}
    while True:
        while not cdc_q.empty():
            acdc_instance = q.get()
        msg = _recv(bus)
        if not msg:
            continue
        reply_addr = msg.arbitration_id >> 8 & 0xFF
        msg_type = msg.arbitration_id >> 16 & 0xFF
        if msg_type == 0x05:
            pt_q.put((msg, acdc_instance))
        elif msg_type == 0x40:  # 功率控制模块向充电模块发送心跳帧：优先级6，PF：0x40
            acdc_msg = acdc_instance.get(reply_addr)
            if acdc_msg:
                for msg in acdc_msg.pf2a:
                    _send(bus, msg)
        elif msg_type == 0x82:  # 功率控制模块向充电模块发送定值查询命令帧：优先级6，PF：0x82
            if msg.data[0] == 0x01:
                param_num = msg.data[-1]
                _recv(bus)
                acdc_msg = acdc_instance.get(reply_addr)
                if acdc_msg:
                    for msg in acdc_msg.pf83[param_num]:
                        _send(bus, msg)

def _recv(bus):
    """

    """
    try:
        return bus.recv()
    except can.CanError:
        _, exc_value, _ = sys.exc_info()
        log.error(f"<ACDC>:ACDC Recv Message happen error: {str(exc_value)}")
        time.sleep(1)
