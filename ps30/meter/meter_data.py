# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/12 16:50
# @File: meter_data.py
METER_MAP = {
    '194014': 'meter1_com_state',  # 1# CMC与电表1通信状态
    '190084': 'meter1_A_line_voltage',  # 进线1路A线电压
    '190085': 'meter1_B_line_voltage',  # 进线1路B线电压
    '190086': 'meter1_C_line_voltage',  # 进线1路C线电压
    '190087': 'meter1_A_phase_current',  # 进线1路A相电流
    '190088': 'meter1_B_phase_current',  # 进线1路B相电流
    '190089': 'meter1_C_phase_current',  # 进线1路C相电流
    '190090': 'meter1_A_phase_voltage',  # 进线1路A相电压
    '190091': 'meter1_B_phase_voltage',  # 进线1路B相电压
    '190092': 'meter1_C_phase_voltage',  # 进线1路C相电压
    '190093': 'meter1_total_power',  # 进线1路总有功功率
    '190094': 'meter1_power_factor',  # 进线1路总功率因素
    '190095': 'meter1_energy',  # 进线1路总电能
    '190096': 'meter1_sharp_secondary_energy',  # 进线1路总尖电能
    '190097': 'meter1_peak_secondary_energy',  # 进线1路总峰电能
    '190098': 'meter1_flat_secondary_energy',  # 进线1路总平电能
    '190099': 'meter1_valley_secondary_energy',  # 进线1路总谷电能
    '700601': 'meter1_com_fault',  # 1#CMC与电表1通信故障
    
    '194015': 'meter2_com_state',  # 1# CMC与电表2通信状态
    '190100': 'meter2_A_line_voltage',  # 进线2路A线电压
    '190101': 'meter2_B_line_voltage',  # 进线2路B线电压
    '190102': 'meter2_C_line_voltage',  # 进线2路C线电压
    '190103': 'meter2_A_phase_current',  # 进线2路A相电流
    '190104': 'meter2_B_phase_current',  # 进线2路B相电流
    '190105': 'meter2_C_phase_current',  # 进线2路C相电流
    '190106': 'meter2_A_phase_voltage',  # 进线2路A相电压
    '190107': 'meter2_B_phase_voltage',  # 进线2路B相电压
    '190108': 'meter2_C_phase_voltage',  # 进线2路C相电压
    '190109': 'meter2_total_power',  # 进线2路总有功功率
    '190110': 'meter2_power_factor',  # 进线2路总功率因素
    '190111': 'meter2_energy',  # 进线2路总电能
    '190112': 'meter2_sharp_secondary_energy',  # 进线2路总尖电能
    '190113': 'meter2_peak_secondary_energy',  # 进线2路总峰电能
    '190114': 'meter2_flat_secondary_energy',  # 进线2路总平电能
    '190115': 'meter2_valley_secondary_energy',  # 进线2路总谷电能
    '700602': 'meter2_com_fault',  # 1#CMC与电表2通信故障
}