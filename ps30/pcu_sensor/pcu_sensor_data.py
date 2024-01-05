# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/12 15:19
# @File: pcu_sensor_data.py
PCU_SENSOR_MAP = {
    # '104804': 'com_state_distribution_box',  # 1# PCU与配电柜温湿度通信状态
    '104805': 'com_state_charging_box',  # 1# PCU与充电柜温湿度通信状态
    # '104700': 'd_chan11_hum_value',  # 1#PCU配电柜温湿度通道1湿度
    # '104701': 'd_chan11_tem_value',  # 1#PCU配电柜温湿度通道1温度
    # '104702': 'd_chan12_hum_value',  # 1#PCU配电柜温湿度通道2湿度
    # '104703': 'd_chan13_tem_value',  # 1#PCU配电柜温湿度通道2温度
    '104704': 'c_chan11_hum_value',  # 1#PCU充电柜温湿度通道1湿度
    '104705': 'c_chan11_tem_value',  # 1#PCU充电柜温湿度通道1温度
    '104706': 'c_chan12_hum_value',  # 1#PCU充电柜温湿度通道2湿度
    '104707': 'c_chan12_tem_value',  # 1#PCU充电柜温湿度通道2温度
    # '720206': 'd_com_state_fault',  # 1#PCU与配电柜温湿度控制器通信故障
    '720207': 'c_com_state_fault',  # 1#PCU与充电柜温湿度控制器通信故障
}
