# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2022/11/24 18:40
# @File: pcu_meter_utils.py
import sys
import time
import traceback

import serial

from pcu_meter.pcu_meter_msg import PcuMeterMsg
from utils.log import log


def start_meter_modbus_process(pcu_meter_q, port):
    """

    :param pcu_meter_q:
    :param port:
    :return:
    """
    meter_obj = PcuMeterMsg()
    meter_obj.meter_data_init()
    ser = serial.Serial(port=port, baudrate=9600, timeout=0.5)
    ser.flushInput()  # 清空缓冲区
    while True:
        try:
            if not pcu_meter_q.empty():
                temp = pcu_meter_q.get()
                meter_obj.slave_1_data = temp[0]
                meter_obj.slave_2_data = temp[1]
                meter_obj.slave_3_data = temp[2]
                meter_obj.slave_4_data = temp[3]
            count = ser.inWaiting()
            if count != 0:
                recv = ser.read(8)
                if recv and len(recv) > 1 and recv[0] == 1:
                    ser.write(meter_obj.slave_1_data)
                    # print("slave1 data response")
                    # print("111", meter_obj.slave_1_data[80], meter_obj.slave_1_data[81])
                elif recv and len(recv) > 1 and recv[0] == 2:
                    ser.write(meter_obj.slave_2_data)
                    # print("slave2 data response")
                    # print("222", meter_obj.slave_2_data[80], meter_obj.slave_2_data[81])
                elif recv and len(recv) > 1 and recv[0] == 3:
                    ser.write(meter_obj.slave_3_data)
                    # print("slave3 data response")
                    # print("333", meter_obj.slave_3_data[80], meter_obj.slave_3_data[81])
                elif recv and len(recv) > 1 and recv[0] == 4:
                    ser.write(meter_obj.slave_4_data)
                    # print("slave4 data response")
                    # print("444", meter_obj.slave_4_data[80], meter_obj.slave_4_data[81])
        except Exception as e:
            log.error(traceback.format_exc())
            _, exc_value, _ = sys.exc_info()
            log.error(f"<PCU_Meter>:start pcu meter server happen error, {str(exc_value)}")
            time.sleep(1)
