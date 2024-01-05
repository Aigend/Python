# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/8/15 10:59
# @File:acdc_process.py
import sys
import time
import can

from utils.log import log


def run(q, pt_q, node):
    # bus = can.Bus(bustype="socketcan", channel=node, receive_own_messages=True, )
    bus = can.interface.Bus(bustype="socketcan", channel=node, bitrate=125000)
    acdc_instance = {}
    while True:
        while not q.empty():
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


def analyze(ac_q, pt_q):
    while True:
        _group = ""
        if not pt_q.empty():
            msg, acdc_instance = pt_q.get()
            if _group == msg.data[1]:
                continue
            _group = msg.data[1]
            _num = 0x20 + (msg.data[1] - 1) * 3
            flag = False  # 用于判断是否有修改对应的数据，修改则传输，否则不处理
            for i in range(3):
                addr = _num + i
                if addr in acdc_instance:
                    acdc_msg = acdc_instance[addr]
                    flag = acdc_msg.update_pf2a_msg(msg.data)
            if flag:
                ac_q.put(acdc_instance)
        time.sleep(0.002)


def _recv(bus):
    try:
        return bus.recv()
    except can.CanError:
        _, exc_value, _ = sys.exc_info()
        log.error(f"<ACDC>:ACDC Recv Message happen error: {str(exc_value)}")
        time.sleep(1)


def _send(bus, msg):
    try:
        bus.send(msg)
        time.sleep(0.002)
    except can.CanError:
        _, exc_value, _ = sys.exc_info()
        log.error(f"<ACDC>:: ACDC Message NOT sent, happen error: {str(exc_value)}")
        time.sleep(1)
