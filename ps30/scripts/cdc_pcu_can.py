"""
@Project: ps30
@File: cdc_pcu_can.py
@Author: wenlong.jin
@Time: 2023/11/30 14:43
@version: 1.0.0
@Description:
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    保伦pcu和cdc之间的过程数据
"""
import sys
import time

import can

from log import log


def run(node):
    bus = can.interface.Bus(bustype="socketcan", channel=node, bitrate=125000)
    while True:
        msg = _recv(bus)
        SA = msg.arbitration_id & 0xFF
        PS = msg.arbitration_id >> 8 & 0xFF
        msg_type = msg.arbitration_id >> 16 & 0xFF
        log.info(f"SA: {hex(SA)}, PS {hex(PS)} msg_type: {msg_type}, data: {[hex(msg.data[i]) for i in range(8)]}")


def _recv(bus):
    try:
        return bus.recv()
    except can.CanError:
        _, exc_value, _ = sys.exc_info()
        log.error(f"<ACDC>:ACDC Recv Message happen error: {str(exc_value)}")
        time.sleep(1)


if __name__ == '__main__':
    run("can27")
