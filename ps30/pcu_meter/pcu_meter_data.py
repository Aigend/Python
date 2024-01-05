# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/9/6 15:32
# @File:pcu_meter_data.py
PCU_METER_MAP = {
    '104500': 'meter1_A_line_voltage',  # 进线1路A线电压
    '104501': 'meter1_B_line_voltage',  # 进线1路B线电压
    '104502': 'meter1_C_line_voltage',  # 进线1路C线电压
    '104503': 'meter1_A_phase_current',  # 进线1路A相电流
    '104504': 'meter1_B_phase_current',  # 进线1路B相电流
    '104505': 'meter1_C_phase_current',  # 进线1路C相电流
    '104506': 'meter1_A_phase_voltage',  # 进线1路A相电压
    '104507': 'meter1_B_phase_voltage',  # 进线1路B相电压
    '104508': 'meter1_C_phase_voltage',  # 进线1路C相电压
    '104509': 'meter1_total_power',  # 进线1路总有功功率
    '104510': 'meter1_power_factor',  # 进线1路总功率因素
    '104511': 'meter1_energy',  # 进线1路总电能
    '104512': 'meter1_sharp_secondary_energy',  # 进线1路总尖电能
    '104513': 'meter1_peak_secondary_energy',  # 进线1路总峰电能
    '104514': 'meter1_flat_secondary_energy',  # 进线1路总平电能
    '104515': 'meter1_valley_secondary_energy',  # 进线1路总谷电能

    '104516': 'meter2_A_line_voltage',  # 进线2路A线电压
    '104517': 'meter2_B_line_voltage',  # 进线2路B线电压
    '104518': 'meter2_C_line_voltage',  # 进线2路C线电压
    '104519': 'meter2_A_phase_current',  # 进线2路A相电流
    '104520': 'meter2_B_phase_current',  # 进线2路B相电流
    '104521': 'meter2_C_phase_current',  # 进线2路C相电流
    '104522': 'meter2_A_phase_voltage',  # 进线2路A相电压
    '104523': 'meter2_B_phase_voltage',  # 进线2路B相电压
    '104524': 'meter2_C_phase_voltage',  # 进线2路C相电压
    '104525': 'meter2_total_power',  # 进线2路总有功功率
    '104526': 'meter2_power_factor',  # 进线2路总功率因素
    '104527': 'meter2_energy',  # 进线2路总电能
    '104528': 'meter2_sharp_secondary_energy',  # 进线2路总尖电能
    '104529': 'meter2_peak_secondary_energy',  # 进线2路总峰电能
    '104530': 'meter2_flat_secondary_energy',  # 进线2路总平电能
    '104531': 'meter2_valley_secondary_energy',  # 进线2路总谷电能

    '104532': 'meter3_A_line_voltage',  # PCU换电站进线A线电压
    '104533': 'meter3_B_line_voltage',  # PCU换电站进线B线电压
    '104534': 'meter3_C_line_voltage',  # PCU换电站进线C线电压
    '104535': 'meter3_A_phase_current',  # PCU换电站进线表A相电流
    '104536': 'meter3_B_phase_current',  # PCU换电站进线表B相电流
    '104537': 'meter3_C_phase_current',  # PCU换电站进线表C相电流
    '104538': 'meter3_A_phase_voltage',  # PCU换电站进线表A相电压
    '104539': 'meter3_B_phase_voltage',  # PCU换电站进线表B相电压
    '104540': 'meter3_C_phase_voltage',  # PCU换电站进线表C相电压
    '104541': 'meter3_total_power',  # PCU换电站进线表总有功功率
    '104542': 'meter3_power_factor',  # PCU换电站进线表总功率因素
    '104543': 'meter3_energy',  # PCU换电站进线表总电能
    '104544': 'meter3_sharp_secondary_energy',  # PCU换电站进线总尖电能
    '104545': 'meter3_peak_secondary_energy',  # PCU换电站进线总峰电能
    '104546': 'meter3_flat_secondary_energy',  # PCU换电站进线总平电能
    '104547': 'meter3_valley_secondary_energy',  # PCU换电站进线总谷电能

    '104548': 'meter4_A_line_voltage',  # PCU液冷进线A线电压
    '104549': 'meter4_B_line_voltage',  # PCU液冷进线B线电压
    '104550': 'meter4_C_line_voltage',  # PCU液冷进线C线电压
    '104551': 'meter4_A_phase_current',  # PCU液冷进线表A相电流
    '104552': 'meter4_B_phase_current',  # PCU液冷进线表B相电流
    '104553': 'meter4_C_phase_current',  # PCU液冷进线表C相电流
    '104554': 'meter4_A_phase_voltage',  # PCU液冷进线表A相电压
    '104555': 'meter4_B_phase_voltage',  # PCU液冷进线表B相电压
    '104556': 'meter4_C_phase_voltage',  # PCU液冷进线表C相电压
    '104557': 'meter4_total_power',  # PCU液冷进线表总有功功率
    '104558': 'meter4_power_factor',  # PCU液冷进线表总功率因素
    '104559': 'meter4_energy',  # PCU液冷进线表总电能
    '104560': 'meter4_sharp_secondary_energy',  # PCU液冷进线总尖电能
    '104561': 'meter4_peak_secondary_energy',  # PCU液冷进线总峰电能
    '104562': 'meter4_flat_secondary_energy',  # PCU液冷进线总平电能
    '104563': 'meter4_valley_secondary_energy',  # PCU液冷进线总谷电能
}