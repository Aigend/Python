# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/12 16:51
# @File: meter_utils.py
import sys
import time
import traceback

import serial

from meter.meter_msg import MeterMsg
from utils.log import log


def start_meter_modbus_process(Meter_q, port):
    """

    :param Meter_q:
    :param port:
    :return:
    """
    meter_obj = MeterMsg()
    meter_obj.meter_data_init()
    ser = serial.Serial(port=port, baudrate=9600, timeout=0.5)
    ser.flushInput()  # 清空缓冲区
    while True:
        try:
            if not Meter_q.empty():
                temp = Meter_q.get()
                meter_obj.slave_1_data = temp[0]
                meter_obj.slave_2_data = temp[1]
            count = ser.inWaiting()
            if count != 0:
                recv = ser.read(8)
                if recv and len(recv) > 1 and recv[1] == 17:
                    log.info(f"<Meter>:recv:{[hex(recv[i]) for i in range(len(recv))]}")
                    ser.read(4)
                    if recv[0] == 1:
                        data = [0x01, 0x11, 0x0A, 0x00, 0x00, 0x02, 0x2D, 0x00, 0x73, 0x00, 0x0C, 0x8B, 0x5C, 0xC3,
                                0x54]
                        s = bytearray(data)
                        ser.write(s)
                        log.info(f"<Meter>:addr 01 res:{[hex(data[i]) for i in range(len(data))]}")
                    elif recv[0] == 2:
                        data = [0x02, 0x11, 0x0A, 0x00, 0x00, 0x02, 0x2D, 0x00, 0x73, 0x00, 0x0C, 0x8B, 0x5C, 0xC6,
                                0x97]
                        s = bytearray(data)
                        ser.write(s)
                        log.info(f"<Meter>:addr 02 res:{[hex(data[i]) for i in range(len(data))]}")
                elif recv and len(recv) > 1 and recv[0] == 1:
                    ser.write(meter_obj.slave_1_data)
                elif recv and len(recv) > 1 and recv[0] == 2:
                    ser.write(meter_obj.slave_2_data)
        except Exception as e:
            log.error(traceback.format_exc())
            _, exc_value, _ = sys.exc_info()
            log.error(f"<Meter>:start meter server happen error, {str(exc_value)}")
            time.sleep(1)