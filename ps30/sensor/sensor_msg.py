# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/9/7 9:14
# @File:sensor_msg.py
import modbus_tk.defines as cst
import serial
from modbus_tk import modbus_rtu

from utils.log import log


class SensorMsg:

    def __init__(self):
        self.port = ''
        self.slave1 = ''
        self.start_server_flag = False
        self.server = ""

    def start_sensor_server(self):
        self.server = modbus_rtu.RtuServer(serial.Serial(port=self.port),
                                           baudrate=9600, bytesize=8, parity='N', stopbits=1)
        self.server.start()
        log.info("<Sensor>:sensor server running success...")
        self.slave1 = self.server.add_slave(1)
        self.slave1.add_block('B', cst.HOLDING_REGISTERS, 0, 50)
        self.sensor_data_init()

    def stop_sensor_server(self):
        if isinstance(self.server, modbus_rtu.RtuServer):
            self.server.stop()

    def set_meter_RegParam(self, Reg_address=0, Reg_Value=0):
        self.slave1.set_values('B', Reg_address, Reg_Value)

    def sensor_data_init(self):
        self.set_meter_RegParam(0x0004, 60)  # 温度上限报警值
        self.set_meter_RegParam(0x0005, 0)  # 温度上限报警使能
        self.set_meter_RegParam(0x0006, 0)  # 温度下限报警值
        self.set_meter_RegParam(0x0007, 0)  # 温度下限报警使能
        self.set_meter_RegParam(0x0008, 95)  # 湿度上限报警值
        self.set_meter_RegParam(0x0009, 0)  # 湿度上限报警使能
        self.set_meter_RegParam(0x000A, 0)  # 湿度下限报警值
        self.set_meter_RegParam(0x000B, 0)  # 湿度下限报警使能


if __name__ == '__main__':
    sensor = SensorMsg()
    # sensor.port = 'com1'
    sensor.port = 'com4'
    # sensor.port = '/dev/ttyUSB0'
    sensor.start_sensor_server()
    sensor.slave1.set_values('B', 0x0000, 28)  # 湿度 530011
    sensor.slave1.set_values('B', 0x0001, 29)  # 温度 530010
