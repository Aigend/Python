# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/12 15:42
# @File: pcu_sensor_msg.py
import modbus_tk.defines as cst
import serial
from modbus_tk import modbus_rtu

from utils.log import log

"""
4、读可读写模拟量寄存器(保持寄存器)：
计算机发送命令：[设备地址] [命令号03] [起始寄存器地址高8位] [低8位] [读取的寄存器数高8位] [低8位] [CRC校验的低8位] [CRC校验的高8位]

例：[11][03][00][6B][00][03][CRC低][CRC高]
意义如下：
（1）设备地址和上面的相同。
（2）命令号:读模拟量的命令号固定为03。
（3）起始地址高8位、低8位：表示想读取的模拟量的起始地址(起始地址为0)。比如例子中的起始地址为107。
（4）寄存器数高8位、低8位：表示从起始地址开始读多少个模拟量。例子中为3个模拟量。注意，在返回的信息中一个模拟量需要返回两个字节。

设备响应：[设备地址] [命令号03] [返回的字节个数][数据1][数据2]...[数据n][CRC校验的低8位] [CRC校验的高8位]

例：[11][03][06][02][2B][00][00][00][64][CRC低][CRC高]
意义如下：
（1）设备地址和命令号和上面的相同。
（2）返回的字节个数：表示数据的字节个数，也就是数据1，2...n中的n的值。例子中返回了3个模拟量的数据，因为一个模拟量需要2个字节所以共6个字节。
（3）数据1...n：其中[数据1][数据2]分别是第1个模拟量的高8位和低8位，[数据3][数据4]是第2个模拟量的高8位和低8位，以此类推。例子中返回的值分别是555，0，100。
（4）CRC校验同上。


"""


class PcuSensorMsg:

    def __init__(self):
        self.port = ''
        self.slave1 = ''
        self.start_server_flag = False
        self.server = ""

    def start_sensor_server(self):
        self.server = modbus_rtu.RtuServer(serial.Serial(port=self.port),
                                           baudrate=9600, bytesize=8, parity='N', stopbits=1)
        self.server.start()
        log.info("<PCU_Sensor>:pcu sensor server running success...")
        self.slave1 = self.server.add_slave(1)
        self.slave1.add_block('B', cst.HOLDING_REGISTERS, 0, 5)
        # self.sensor_data_init()

    def stop_sensor_server(self):
        if isinstance(self.server, modbus_rtu.RtuServer):
            self.server.stop()

    def set_meter_RegParam(self, Reg_address=0, Reg_Value=0):
        self.slave1.set_values('B', Reg_address, Reg_Value)

    # def sensor_data_init(self):
    #     self.set_meter_RegParam(0x0004, 60)  # 温度上限报警值
    #     self.set_meter_RegParam(0x0005, 0)  # 温度上限报警使能
    #     self.set_meter_RegParam(0x0006, 0)  # 温度下限报警值
    #     self.set_meter_RegParam(0x0007, 0)  # 温度下限报警使能
    #     self.set_meter_RegParam(0x0008, 95)  # 湿度上限报警值
    #     self.set_meter_RegParam(0x0009, 0)  # 湿度上限报警使能
    #     self.set_meter_RegParam(0x000A, 0)  # 湿度下限报警值
    #     self.set_meter_RegParam(0x000B, 0)  # 湿度下限报警使能


if __name__ == '__main__':
    sensor = PcuSensorMsg()
    # sensor.port = 'com1'
    sensor.port = 'com4'
    # sensor.port = '/dev/ttyUSB0'
    sensor.start_sensor_server()
    sensor.slave1.set_values('B', 0x0001, 28)  # channel1 湿度
    sensor.slave1.set_values('B', 0x0002, 29)  # channel1 温度
    sensor.slave1.set_values('B', 0x0003, 28)  # channel2 湿度
    sensor.slave1.set_values('B', 0x0004, 29)  # channel2 温度
