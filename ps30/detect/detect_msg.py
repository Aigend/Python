#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 11:34
# @Author  : wenlong.jin@nio.com
# @File    : detect_msg.py
# @Software: ps20
import modbus_tk.defines as cst
import serial
from modbus_tk import modbus_rtu

from utils.log import log


class DetectMsg:

    def __init__(self, ):
        self.port = ''
        self.slave1 = ''
        self.start_server_flag = False
        self.server = ""

    def start_detect_server(self):
        self.server = modbus_rtu.RtuServer(serial.Serial(port=self.port),
                                           baudrate=9600, bytesize=8, parity='N', stopbits=1)
        self.server.start()
        log.info("<Detect>:detect charge board server running success...")
        self.slave1 = self.server.add_slave(0x6E)
        self.slave1.add_block('B', cst.HOLDING_REGISTERS, 0, 257)

    def stop_detect_server(self):
        if isinstance(self.server, modbus_rtu.RtuServer):
            self.server.stop()

    def set_detect_RegParam(self, Reg_address=0, Reg_Value=0):
        self.slave1.set_values('B', Reg_address, Reg_Value)

    def init_data(self, data):
        value_pos = int(data.get('value_pos', 65539))  # 正端绝缘电阻值
        value_pos_h = (value_pos >> 16) & 0xFF
        value_pos_l = value_pos & 0xFF
        self.set_detect_RegParam(0x0000, value_pos_h)
        self.set_detect_RegParam(0x0001, value_pos_l)

        value_nev = int(data.get('value_nev', 65538))  # 负端绝缘电阻值
        value_nev_h = (value_nev >> 16) & 0xFF
        value_nev_l = value_nev & 0xFF
        self.set_detect_RegParam(0x0002, value_nev_h)
        self.set_detect_RegParam(0x0003, value_nev_l)

        read_volt = int(data.get('read_volt', 120))  # 绝缘检测端电压
        read_volt = read_volt & 0xFF
        self.set_detect_RegParam(0x0004, read_volt)

        self.set_detect_RegParam(0x0005, 9999)  # 电压采集端电压

        self.set_detect_RegParam(0x0006, 121)  # 电流采集端电流

        self.set_detect_RegParam(0x0007, 0)  # 系统状态/报警位

        self.set_detect_RegParam(0x0008, 0)  # 充电电量
        self.set_detect_RegParam(0x0009, 0)

        self.set_detect_RegParam(0x000A, 50)  # 分流器标称电流值

        self.set_detect_RegParam(0x000B, 75)  # 分流器标称电压值

        self.set_detect_RegParam(0x000C, 0)  # 绝缘报警类型

        self.set_detect_RegParam(0x000D, 10)  # 绝缘报警阈值

        self.set_detect_RegParam(0x000E, 121)  # 硬件版本

        self.set_detect_RegParam(0x000F, 121)  # 软件版本

        self.set_detect_RegParam(0x0100, 1)  # 充电桩/换电站
