# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/9/7 9:18
# @File:sensor_data.py
key_map = {
    '194016': 'com_state',  # 1# CMC与转接柜温湿度通信状态
    '190080': 'ch1_sensor_temperature',  # 充电区域温度
    '190081': 'ch1_sensor_humidity',  # 充电区域湿度
    '190082': 'ch2_sensor_temperature',  # CMC 电池仓温度
    '190083': 'ch2_sensor_humidity',  # CMC 电池仓湿度
    '764022': 'temp_upper_alarm',  # 充电仓温度上限报警
    '764023': 'temp_lower_alarm',  # 充电仓温度下限报警
    '764024': 'humidity_upper_alarm',  # 充电仓湿度上限报警
    '764025': 'humidity_lower_alarm',  # 充电仓湿度下限报警
    '700603': 'com_state_fault',  # 1#CMC与温湿度传感器通信故障
}
