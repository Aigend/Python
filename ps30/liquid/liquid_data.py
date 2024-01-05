# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author:wenlong.jin
# @Time:2022/8/30 13:40
# @File:liquid_data.py
liquid_real_time_key = {
    # 状态数据
    # "300000": "**",  # 1# 水冷通信状态
    "300001": "power_protection_switch",  # 1#水冷 电源保护器
    "300002": "big_tank_low_level_switch",  # 1#水冷 大水箱低液位保护开关
    "300003": "big_tank_high_level_switch",  # 1#水冷 大水箱高液位保护开关
    "300004": "drain_valve_switch",  # 1#水冷 大水箱日常排液阀反馈
    "300005": "inner_loop_flow_switch",  # 1#水冷 内循环回水流量开关
    "300006": "heating_stage_started",  # 1#水冷 加热棒运行状态反馈
    "300007": "heating_stage_fault",  # 1#水冷 加热棒故障状态反馈
    "300008": "compressor_1_started",  # 1#水冷 压缩机1状态反馈
    "300009": "compressor_2_started",  # 1#水冷 压缩机2状态反馈
    "300010": "compressor_1_power_protection",  # 1#水冷 压缩机1空开保护反馈
    "300011": "compressor_2_power_protection",  # 1#水冷 压缩机2空开保护反馈
    "300012": "pump_1_frequency_fault",  # 1#水冷 前仓外循环泵变频器故障反馈
    "300013": "pump_1_frequency_feedback",  # 1#水冷 前仓外循环泵频率反馈
    "300014": "pump_1_started",  # 1#水冷 前仓外循环泵变频器运行反馈
    "300015": "pump_2_frequency_feedback",  # 1#水冷 后仓外循环泵频率反馈
    "300016": "pump_2_frequency_fault",  # 1#水冷 后仓外循环泵变频器故障反馈
    "300017": "pump_2_started",  # 1#水冷 后仓外循环泵变频器运行反馈
    "300018": "pump_3_frequency_fault",  # 1#水冷 大水箱内循环泵变频器故障反馈
    "300019": "pump_3_frequency_feedback",  # 1#水冷 大水箱内循环泵频率反馈
    "300020": "pump_3_started",  # 1#水冷 大水箱内循环泵变频器运行反馈
    "300021": "fan_1_frequency_fault",  # 1#水冷 排风机1变频器故障反馈
    "300022": "fan_1_frequency_feedback",  # 1#水冷 排风机1频率反馈
    "300023": "fan_1_started",  # 1#水冷 排风机1变频器运行反馈
    "300024": "fan_2_frequency_fault",  # 1#水冷 排风机2变频器故障反馈
    "300025": "fan_2_frequency_feedback",  # 1#水冷 排风机2频率反馈
    "300026": "fan_2_started",  # 1#水冷 排风机2变频器运行反馈

    # 实时数据
    "300500": "press_meter_1",  # 1#水冷 前仓压力计
    "300501": "press_meter_2",  # 1#水冷 后仓压力计
    "300502": "tank_temp",  # 1#水冷 大水箱温度
    "300503": "tank_level",  # 1#水冷 大水箱液位
    "300504": "front_backwater_temp",  # 1#水冷 前仓回水温度
    "300505": "back_backwater_temp",  # 1#水冷 后仓回水温度
    "300506": "flow_meter_1",  # 1#水冷 前仓回水流量
    "300507": "flow_meter_2",  # 1#水冷 后仓回水流量
    "300508": "electric_cabinet_temp",  # 1#水冷 电控箱温度
    "300509": "exhaust_1_temp",  # 1#水冷 蒸发器温度1
    "300510": "exhaust_2_temp",  # 1#水冷 蒸发器温度2
    "300511": "compressor_1_pressure_low",  # 1#水冷 压缩机低压1
    "300512": "compressor_2_pressure_low",  # 1#水冷 压缩机低压2
    "300513": "compressor_1_pressure_high",  # 1#水冷 压缩机高压1
    "300514": "compressor_2_pressure_high",  # 1#水冷 压缩机高压2
    "300515": "exchanger_temp",  # 1#水冷 板换出水温度
    "30": "software_version",  # 1# 水冷设备软件版本号
    "31": "manufacturer",  # 1# 水冷厂家编号
    "hardware_version": "hardware_version",	 # 水冷 硬件版本

    "frequency_of_1_fan": "frequency_of_1_fan",
    "frequency_of_1_pump": "frequency_of_1_pump",
    "frequency_of_2_fan": "frequency_of_2_fan",
    "frequency_of_2_pump": "frequency_of_2_pump",
    "frequency_of_3_pump": "frequency_of_3_pump",
    "higher_limit_setting_temp_of_tank": "higher_limit_setting_temp_of_tank",
    "lower_limit_setting_temp_of_tank": "lower_limit_setting_temp_of_tank",
    "middle_limit_setting_temp_of_tank": "middle_limit_setting_temp_of_tank",
    "remote_reset": "remote_reset",
    "remote_start_cooling_system": "remote_start_cooling_system",
    "set_cooling_system_in_manual_mode": "set_cooling_system_in_manual_mode",
    "set_cooling_system_in_remote_mode": "set_cooling_system_in_remote_mode",
    "start_1_fan": "start_1_fan",
    "start_1_pump": "start_1_pump",
    "start_2_fan": "start_2_fan",
    "start_2_pump": "start_2_pump",
    "start_3_pump": "start_3_pump",
}

liquid_alarm_key = {
    "700400": "low_level_protection_of_tank_trigger",  # 1水冷 大水箱低液位开关保护（LS01)
    "700401": "high_level_protection_of_tank_trigger",  # 1水冷 大水箱高液位开关保护（LS03)
    "700402": "tank_level_is_low",  # 1水冷 大水箱液位过低 (LT01)
    "700403": "tank_level_is_high",  # 1水冷 大水箱液位高度较高 (LT01)
    "700404": "temp_of_tank_is_too_high_to_stop_pump",  # 1水冷 大水箱水温过高停外循环水泵 （TT03)
    "700405": "temp_sensor_of_tank_fault",  # 1水冷 大水箱水温传感器故障 （TT03)
    "700406": "level_sensor_of_tank_fault",  # 1水冷 大水箱液位传感器故障 (LT01)
    "700407": "low_level_swtich_mismatching_level_meter",  # 1水冷 大水箱低液位开关（LS01)与液位计不匹配（LT01)
    "700408": "high_level_swtich_mismatching_level_meter",  # 1水冷 大水箱高液位开关（LS03)与液位计不匹配（LT01)
    "700409": "flow_meter_1_fault",  # 1水冷 前仓#1水泵水流量传感器故障 （FT01)
    "700410": "flow_meter_2_fault",  # 1水冷 后仓#2水泵水流量传感器故障 （FT02)
    "700411": "press_meter_1_fault",  # 1水冷 前仓#1水泵水压力传感器故障 （PT03)
    "700412": "press_meter_2_fault",  # 1水冷 后仓#2水泵水压力传感器故障 (PT04)
    "700413": "backwater_temp_sensor_1_fault",  # 1水冷 前仓#1回水温度传感器故障 （TT01)
    "700414": "backwater_temp_sensor_2_fault",  # 1水冷 后仓#2回水温度传感器故障 （TT02)
    "700415": "solenoid_valve_1_open_failed",  # 1水冷 前仓#1电磁阀未打开（EV01)
    "700416": "solenoid_valve_1_close_failed",  # 1水冷 前仓#1电磁阀未关闭（EV01)
    "700417": "solenoid_valve_2_open_failed",  # 1水冷 后仓#2电磁阀未打开（EV02)
    "700418": "solenoid_valve_2_close_failed",  # 1水冷 后仓#2电磁阀未关闭（EV02)
    "700419": "drain_valve_switch_is_opened",  # 1水冷 日常排液阀未关闭（LM01)
    "700420": "heating_stage_is_abnormal",  # 1水冷 加热棒状态异常（HT)
    "700421": "heating_stage_contactor_is_abnormal",  # 1水冷 加热棒接触器异常（HTS)
    "700422": "flow_protection_of_inner_loop_trigger",  # 1水冷 内循环水流量开关保护 （FS13)
    "700423": "high_press_of_1_compressor_trigger",  # 1水冷 压缩机1高压保护 （PT-H01)
    "700424": "low_press_of_1_compressor_trigger",  # 1水冷 压缩机1低压保护 （PT-L01)
    "700425": "high_press_of_2_compressor_trigger",  # 1水冷 压缩机2高压保护 （PT-H02)
    "700426": "low_press_of_2_compressor_trigger",  # 1水冷 压缩机2低压保护 （PT-L02)
    "700427": "compressor_1_cocontactor_trigger",  # 1水冷 压缩机1接触器异常（CP01-S)
    "700428": "compressor_2_cocontactor_trigger",  # 1水冷 压缩机2接触器异常（CP02-S)
    "700429": "temp_of_water_outlet_is_low",  # 1水冷 蒸发器出水温度过低 (TT08)
    "700430": "exhaust_1_temp_high",  # 1水冷 压缩机1排气温度过高 (TT06)
    "700431": "exhaust_2_temp_high",  # 1水冷 压缩机2排气温度过高 (TT07)
    "700432": "high_press_senor_of_1compressor_fault",  # 1水冷 压缩机高压传感器1故障 （PT-H01)
    "700433": "high_press_senor_of_2compressor_fault",  # 1水冷 压缩机高压传感器2故障 （PT-H02)
    "700434": "low_press_senor_of_1compressor_fault",  # 1水冷 压缩机低压传感器1故障 （PT-L01)
    "700435": "low_press_senor_of_2compressor_fault",  # 1水冷 压缩机低压传感器2故障 （PT-L02)
    "700436": "temp_of_water_outlet_fault",  # 1水冷 蒸发器出水温度传感器故障 (TT08)
    "700437": "temp_of_1_compressor_fault",  # 1水冷 压缩机1排气温度传感器故障 (TT06)
    "700438": "temp_of_2_compressor_fault",  # 1水冷 压缩机2排气温度传感器故障 (TT07)
    "700439": "maintenance_cycle_of_3_pump_reach",  # 1水冷 内循环泵已到维护时间 （PM03)
    "700440": "maintenance_cycle_of_1_pump_reach",  # 1水冷 外循环泵1#已到维护时间 （PM01）
    "700441": "maintenance_cycle_of_2_pump_reach",  # 1水冷 外循环泵2#已到维护时间 （PM02)
    "700442": "maintenance_cycle_of_1_compressor_reach",  # 1水冷 压缩机1已到维护时间 （CP01)
    "700443": "maintenance_cycle_of_1_fan_reach",  # 1水冷 冷凝风机1已到维护时间 (F01)
    "700444": "maintenance_cycle_of_2_compressor_reach",  # 1水冷 压缩机2已到维护时间 （CP02)
    "700445": "maintenance_cycle_of_2_fan_reach",  # 1水冷 冷凝风机2已到维护时间 (F02)
    "700446": "maintenance_cycle_of_heating_reach",  # 1水冷 加热器已到维护时间 (HT)
    "700447": "frozen_start_3_pump",  # 1水冷 防冻保护开内循环水泵 （PM03)
    "700448": "frozen_start_heating",  # 1水冷 防冻保护开加热器 （HT)
    "700449": "temp_of_electric_cabinet_is_high",  # 1水冷 电控箱温度超高停机（ET)
    "700450": "temp_of_electric_cabinet_fault",  # 1水冷 电控箱温度传感器故障 （ET)
    "700451": "power_protection_trigger",  # 1水冷 电源故障（缺相或错相)（EJ)
    "700452": "compressor_1_overload",  # 1水冷 压缩机1过载 （CP01-P)
    "700453": "compressor_2_overload",  # 1水冷 压缩机2过载 （CP02-P)
    "700454": "converter_fault_of_1_pump",  # 1水冷 前仓#1水泵变频器故障 （PM01-A)
    "700455": "converter_fault_of_2_pump",  # 1水冷 后仓#2水泵变频器故障 （PM02-A)
    "700456": "converter_fault_of_3_pump",  # 1水冷 内循环#3水泵变频器故障 （PM03-A)
    "700457": "converter_fault_of_1_fan",  # 1水冷 #1风机变频器故障 （F01-A)
    "700458": "converter_fault_of_2_fan",  # 1水冷 #2风机变频器故障 （F02-A)
    # "Compressor_1_pk_protection": "Compressor_1_pk_protection",  # #1风机变频器故障
    "communication_lost": "communication_lost",  # 一般通讯故障
    # "Compressor_2_pk_protection": "Compressor_2_pk_protection"  # #2风机变频器故障
}
