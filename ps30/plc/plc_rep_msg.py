# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2022/11/3 20:04
# @File: plc_rep_msg.py
from utils.log import log
import ctypes


class PLC_MSG_SIZE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_msg_size", ctypes.c_int16),
    ]


def generate_PLC_MSG_SIZE_STRUCT(obj, data):
    obj.c_msg_size = data.get("c_msg_size")[0]


class PLC_MODE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_work_mode", ctypes.c_int16),
    ]


def generate_PLC_MODE_STRUCT(obj, data):
    # print("*" * 30)
    obj.c_work_mode = data.get("c_work_mode")[0]
    # print("obj.c_work_mode", obj.c_work_mode)


class PLC_AXIS_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_moving", ctypes.c_bool),
        ("c_stand_still", ctypes.c_bool),
        ("c_syn_mode", ctypes.c_bool),
        ("c_stopping", ctypes.c_bool),
        ("c_fault", ctypes.c_bool),
        ("c_warning", ctypes.c_bool),
        ("c_id", ctypes.c_int16),
        ("c_fault_id", ctypes.c_int32),
        ("c_warning_id", ctypes.c_int16),
        ("c_servo_mode", ctypes.c_int16),
        ("c_torque_actual_value", ctypes.c_int16),
        ("c_pos_actual_value", ctypes.c_int64),
        ("c_velocity_actual_value", ctypes.c_int32),
    ]


def generate_PLC_AXIS_STRUCT(obj, data):
    obj.c_moving = data.get("c_moving")[0]
    obj.c_stand_still = data.get("c_stand_still")[0]
    obj.c_syn_mode = data.get("c_syn_mode")[0]
    obj.c_stopping = data.get("c_stopping")[0]
    obj.c_fault = data.get("c_fault")[0]
    obj.c_warning = data.get("c_warning")[0]
    obj.c_id = data.get("c_id")[0]
    obj.c_fault_id = data.get("c_fault_id")[0]
    obj.c_warning_id = data.get("c_warning_id")[0]
    obj.c_servo_mode = data.get("c_servo_mode")[0]
    obj.c_torque_actual_value = data.get("c_torque_actual_value")[0]
    obj.c_pos_actual_value = data.get("c_pos_actual_value")[0]
    obj.c_velocity_actual_value = data.get("c_velocity_actual_value")[0]


class PLC_LR_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_axis", PLC_AXIS_STRUCT * 25),
        ("c_battery_exist", ctypes.c_bool),
    ]


def generate_PLC_LR_STRUCT(obj, data):
    for i in range(25):
        generate_PLC_AXIS_STRUCT(obj.c_axis[i], data.get("c_axis")[i])
    obj.c_battery_exist = data.get("c_battery_exist")[0]


class PLC_BC_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_axis", PLC_AXIS_STRUCT * 4),
        ("c_battery_exist", ctypes.c_bool * 24),
    ]


def generate_PLC_BC_STRUCT(obj, data):
    for i in range(4):
        generate_PLC_AXIS_STRUCT(obj.c_axis[i], data.get("c_axis")[i])
    # print("data", data)
    # print("data>>>", data.get("c_battery_exist"))
    for i in range(24):
        obj.c_battery_exist[i] = data.get("c_battery_exist")[i][0]


class PLC_VP_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_axis", PLC_AXIS_STRUCT * 9),
        ("c_vehicle_exist", ctypes.c_bool),
    ]


def generate_PLC_VP_STRUCT(obj, data):
    for i in range(9):
        generate_PLC_AXIS_STRUCT(obj.c_axis[i], data.get("c_axis")[i])
    obj.c_vehicle_exist = data.get("c_vehicle_exist")[0]


class PLC_SENSOR_STRUCT(ctypes.Structure):
    # 传感器数据结构定义 500个
    _fields_ = [
        ("c_roller_door_01_up_limt", ctypes.c_bool),  # // 前卷帘门上到位
        ("c_roller_door_01_down_limt", ctypes.c_bool),  # // 前卷帘门下到位
        ("c_roller_door_02_up_limt", ctypes.c_bool),  # // 后卷帘门上到位
        ("c_roller_door_02_down_limt", ctypes.c_bool),  # // 后卷帘门下到位
        ("c_front_roller_door_safety_01", ctypes.c_bool),  # // 前卷帘门安全保护1
        ("c_front_roller_door_safety_02", ctypes.c_bool),  # // 前卷帘门安全保护2
        ("c_rear_roller_door_safety_01", ctypes.c_bool),  # // 后卷帘门安全保护1
        ("c_rear_roller_door_safety_02", ctypes.c_bool),  # // 后卷帘门安全保护2
        ("c_maintain_area_safety_01", ctypes.c_bool),  # // 维护区安全保护1
        ("c_maintain_area_safety_02", ctypes.c_bool),  # // 维护区安全保护2
        ("c_pl_buffer_dece_sensor_1", ctypes.c_bool),  # // 左缓存区电池减速
        ("c_pl_buffer_sensor_f_1", ctypes.c_bool),  # // 左缓存区前电池到位
        ("c_pl_buffer_sensor_r_1", ctypes.c_bool),  # // 左缓存区后电池到位
        ("c_pl_lf_clamp_home_sensor", ctypes.c_bool),  # // 左前轮推杆原点
        ("c_pl_lf_V_check_sensor", ctypes.c_bool),  # // 左前轮进槽
        ("c_pl_l_V_lock_extend_sensor", ctypes.c_bool),  # // V槽左锁止上到位
        ("c_pl_l_V_lock_retract_sensor", ctypes.c_bool),  # // V槽左锁止下到位
        ("c_pl_rf_clamp_home_sensor", ctypes.c_bool),  # // 右前轮推杆原点
        ("c_pl_rf_V_check_sensor", ctypes.c_bool),  # // 右前轮进槽
        ("c_pl_r_V_lock_extend_sensor", ctypes.c_bool),  # // V槽右锁止上到位
        ("c_pl_r_V_lock_retract_sensor", ctypes.c_bool),  # // V槽右锁止下到位
        ("c_pl_f_guide_work_sensor", ctypes.c_bool),  # // 前导向条前到位
        ("c_pl_f_guide_home_sensor", ctypes.c_bool),  # // 前导向条后到位
        ("c_pl_r_guide_work_sensor", ctypes.c_bool),  # // 后导向条前到位
        ("c_pl_r_guide_home_sensor", ctypes.c_bool),  # // 后导向条后到位
        ("c_pl_lr_clamp_home_sensor", ctypes.c_bool),  # // 左后轮推杆原点
        ("c_pl_rr_clamp_home_sensor", ctypes.c_bool),  # // 右后轮推杆原点
        ("c_pl_door_01_open_sensor", ctypes.c_bool),  # // 左开合门开到位
        ("c_pl_door_01_close_sensor", ctypes.c_bool),  # // 左开合门关到位
        ("c_pl_door_02_open_sensor", ctypes.c_bool),  # // 右开合门开到位
        ("c_pl_door_02_close_sensor", ctypes.c_bool),  # // 右开合门关到位
        ("c_pl_door_close_safe_sensor", ctypes.c_bool),  # // 开合门闭合安全
        ("c_bc_lift_dece_sensor", ctypes.c_bool),  # // 接驳位减速
        ("c_bc_lift_reach_sensor_f", ctypes.c_bool),  # // 接驳位前到位
        ("c_bc_lift_reach_sensor_r", ctypes.c_bool),  # // 接驳位后到位
        ("c_bc_lift_work_sensor", ctypes.c_bool),  # // 接驳位举升工作位
        ("c_pl_buffer_dece_sensor_2", ctypes.c_bool),  # // 右缓存区电池减速
        ("c_pl_buffer_sensor_f_2", ctypes.c_bool),  # // 右缓存区前电池到位
        ("c_pl_buffer_sensor_r_2", ctypes.c_bool),  # // 右缓存区后电池到位
        ("c_buffer_stopper_01_extend_sensor_02", ctypes.c_bool),  # // 右缓存区前电池阻挡工作位
        ("c_buffer_stopper_01_retract_sensor_02", ctypes.c_bool),  # // 右缓存区前电池阻挡原点位
        ("c_buffer_stopper_02_extend_sensor_02", ctypes.c_bool),  # // 右缓存区后电池阻挡工作位
        ("c_buffer_stopper_02_retract_sensor_02", ctypes.c_bool),  # // 右缓存区后电池阻挡原点位
        ("c_RGV_bc_reach_sensor_01", ctypes.c_bool),  # // 电池平整1
        ("c_RGV_bc_reach_sensor_02", ctypes.c_bool),  # // 电池平整2
        ("c_RGV_bc_reach_sensor_03", ctypes.c_bool),  # // 电池平整3
        ("c_RGV_bc_reach_sensor_04", ctypes.c_bool),  # // 电池平整4
        ("c_RGV_bc_reach_sensor_05", ctypes.c_bool),  # // 电池平整5
        ("c_RGV_bc_reach_sensor_06", ctypes.c_bool),  # // 电池平整6
        ("c_lf_pin_extend_sensor", ctypes.c_bool),  # // 左前车身定位销上到位
        ("c_lf_pin_retract_sensor", ctypes.c_bool),  # // 左前车身定位销下到位
        ("c_lf_pin_touch_sensor", ctypes.c_bool),  # // 左前车身定位销接触车身
        ("c_rr_pin_extend_sensor", ctypes.c_bool),  # // 右后车身定位销上到位
        ("c_rr_pin_retract_sensor", ctypes.c_bool),  # // 右后车身定位销下到位
        ("c_rr_pin_touch_sensor", ctypes.c_bool),  # // 右后车身定位销接触车身
        ("c_lr_pin_extend_sensor", ctypes.c_bool),  # // 左后车身定位销上到位
        ("c_lr_pin_retract_sensor", ctypes.c_bool),  # // 左后车身定位销下到位
        ("c_lr_pin_touch_sensor", ctypes.c_bool),  # // 左后车身定位销接触车身
        ("c_gun1_lift_work_sensor", ctypes.c_bool),  # // 1#升降上到位
        ("c_gun1_lift_home_sensor", ctypes.c_bool),  # // 1#升降下到位
        ("c_gun2_lift_work_sensor", ctypes.c_bool),  # // 2#升降上到位
        ("c_gun2_lift_home_sensor", ctypes.c_bool),  # // 2#升降下到位
        ("c_gun9_move_home_sensor", ctypes.c_bool),  # // 9#平移位置1
        ("c_gun9_move_work_sensor", ctypes.c_bool),  # // 9#平移位置2
        ("c_gun9_lift_work_sensor", ctypes.c_bool),  # // 9#升降上到位
        ("c_gun9_lift_home_sensor", ctypes.c_bool),  # // 9#升降下到位
        ("c_gun10_move_home_sensor", ctypes.c_bool),  # // 10#平移位置1
        ("c_gun10_move_work_sensor", ctypes.c_bool),  # // 10#平移位置2
        ("c_gun10_lift_work_sensor", ctypes.c_bool),  # // 10#升降上到位
        ("c_gun10_lift_home_sensor", ctypes.c_bool),  # // 10#升降下到位
        ("c_gun11_lift_work_sensor", ctypes.c_bool),  # // 11#升降上到位
        ("c_gun11_lift_home_sensor", ctypes.c_bool),  # // 11#升降下到位
        ("c_gun12_lift_work_sensor", ctypes.c_bool),  # // 12#升降上到位
        ("c_gun12_lift_home_sensor", ctypes.c_bool),  # // 12#升降下到位
        ("c_RGV_work_sensor", ctypes.c_bool),  # // RGV举升工作位
        ("c_RGV_maintain_sensor", ctypes.c_bool),  # // RGV举升维护位
        ("c_pl_stopper_01_home_sensor", ctypes.c_bool),  # // 前电池阻挡升降原点位
        ("c_pl_stopper_01_work_sensor", ctypes.c_bool),  # // 前电池阻挡升降工作位
        ("c_pl_stopper_01_reach_sensor", ctypes.c_bool),  # // 前电池阻挡电池到位
        ("c_pl_stopper_02_home_sensor", ctypes.c_bool),  # // 后电池阻挡升降原点位
        ("c_pl_stopper_02_work_sensor", ctypes.c_bool),  # // 后电池阻挡升降工作位
        ("c_pl_stopper_02_reach_sensor", ctypes.c_bool),  # // 后电池阻挡电池到位
        ("c_pl_move_work_sensor_1", ctypes.c_bool),  # // RGV平移 传送位
        ("c_pl_move_work_sensor_2", ctypes.c_bool),  # // RGV平移 NPA位
        ("c_pl_move_work_sensor_3", ctypes.c_bool),  # // RGV平移 NPD位
        ("c_pl_move_work_sensor_4", ctypes.c_bool),  # // RGV平移备用1
        ("c_pl_move_work_sensor_5", ctypes.c_bool),  # // RGV平移备用2
        ("c_pl_stopper_01_dece_sensor", ctypes.c_bool),  # // 前电池阻挡电池减速
        ("c_bc_slot1_ec_retract_sensor_1", ctypes.c_bool),  # // 1仓NPA电插头上到位
        ("c_bc_slot1_ec_extend_sensor_1", ctypes.c_bool),  # // 1仓NPA电插头下到位
        ("c_bc_slot1_lc_retract_sensor_1", ctypes.c_bool),  # // 1仓NPA水插头上到位
        ("c_bc_slot1_lc_extend_sensor_1", ctypes.c_bool),  # // 1仓NPA水插头下到位
        ("c_bc_slot1_ec_retract_sensor_2", ctypes.c_bool),  # // 1仓NPD电插头上到位
        ("c_bc_slot1_ec_extend_sensor_2", ctypes.c_bool),  # // 1仓NPD电插头下到位
        ("c_bc_slot1_lc_retract_sensor_2", ctypes.c_bool),  # // 1仓NPD水插头上到位
        ("c_bc_slot1_lc_extend_sensor_2", ctypes.c_bool),  # // 1仓NPD水插头下到位
        ("c_bc_slot1_check_sensor_1", ctypes.c_bool),  # // 1仓电池区分NPA
        ("c_bc_slot1_check_sensor_2", ctypes.c_bool),  # // 1仓电池区分NPD
        ("c_bc_slot1_reached_sensor", ctypes.c_bool),  # // 1仓电池落到位
        ("c_bc_slot1_smoke_sensor", ctypes.c_bool),  # // 1仓烟雾报警
        ("c_bc_slot1_liq_flow_switch_st", ctypes.c_bool),  # // 1仓水冷流量开关
        ("c_bc_sum_smoke_sensor", ctypes.c_bool),  # // 电池仓整体烟雾
        ("c_bc_slot2_ec_retract_sensor_1", ctypes.c_bool),  # // 2仓NPA电插头上到位
        ("c_bc_slot2_ec_extend_sensor_1", ctypes.c_bool),  # // 2仓NPA电插头下到位
        ("c_bc_slot2_lc_retract_sensor_1", ctypes.c_bool),  # // 2仓NPA水插头上到位
        ("c_bc_slot2_lc_extend_sensor_1", ctypes.c_bool),  # // 2仓NPA水插头下到位
        ("c_bc_slot2_ec_retract_sensor_2", ctypes.c_bool),  # // 2仓NPD电插头上到位
        ("c_bc_slot2_ec_extend_sensor_2", ctypes.c_bool),  # // 2仓NPD电插头下到位
        ("c_bc_slot2_lc_retract_sensor_2", ctypes.c_bool),  # // 2仓NPD水插头上到位
        ("c_bc_slot2_lc_extend_sensor_2", ctypes.c_bool),  # // 2仓NPD水插头下到位
        ("c_bc_slot2_check_sensor_1", ctypes.c_bool),  # // 2仓电池区分NPA
        ("c_bc_slot2_check_sensor_2", ctypes.c_bool),  # // 2仓电池区分NPD
        ("c_bc_slot2_reached_sensor", ctypes.c_bool),  # // 2仓电池落到位
        ("c_bc_slot2_smoke_sensor", ctypes.c_bool),  # // 2仓烟雾报警
        ("c_bc_slot2_liq_flow_switch_st", ctypes.c_bool),  # // 2仓水冷流量开关
        ("c_bc_slot3_ec_retract_sensor_1", ctypes.c_bool),  # // 3仓NPA电插头上到位
        ("c_bc_slot3_ec_extend_sensor_1", ctypes.c_bool),  # // 3仓NPA电插头下到位
        ("c_bc_slot3_lc_retract_sensor_1", ctypes.c_bool),  # // 3仓NPA水插头上到位
        ("c_bc_slot3_lc_extend_sensor_1", ctypes.c_bool),  # // 3仓NPA水插头下到位
        ("c_bc_slot3_ec_retract_sensor_2", ctypes.c_bool),  # // 3仓NPD电插头上到位
        ("c_bc_slot3_ec_extend_sensor_2", ctypes.c_bool),  # // 3仓NPD电插头下到位
        ("c_bc_slot3_lc_retract_sensor_2", ctypes.c_bool),  # // 3仓NPD水插头上到位
        ("c_bc_slot3_lc_extend_sensor_2", ctypes.c_bool),  # // 3仓NPD水插头下到位
        ("c_bc_slot3_check_sensor_1", ctypes.c_bool),  # // 3仓电池区分NPA
        ("c_bc_slot3_check_sensor_2", ctypes.c_bool),  # // 3仓电池区分NPD
        ("c_bc_slot3_reached_sensor", ctypes.c_bool),  # // 3仓电池落到位
        ("c_bc_slot3_smoke_sensor", ctypes.c_bool),  # // 3仓烟雾报警
        ("c_bc_slot3_liq_flow_switch_st", ctypes.c_bool),  # // 3仓水冷流量开关
        ("c_bc_slot4_ec_retract_sensor_1", ctypes.c_bool),  # // 4仓NPA电插头上到位
        ("c_bc_slot4_ec_extend_sensor_1", ctypes.c_bool),  # // 4仓NPA电插头下到位
        ("c_bc_slot4_lc_retract_sensor_1", ctypes.c_bool),  # // 4仓NPA水插头上到位
        ("c_bc_slot4_lc_extend_sensor_1", ctypes.c_bool),  # // 4仓NPA水插头下到位
        ("c_bc_slot4_ec_retract_sensor_2", ctypes.c_bool),  # // 4仓NPD电插头上到位
        ("c_bc_slot4_ec_extend_sensor_2", ctypes.c_bool),  # // 4仓NPD电插头下到位
        ("c_bc_slot4_lc_retract_sensor_2", ctypes.c_bool),  # // 4仓NPD水插头上到位
        ("c_bc_slot4_lc_extend_sensor_2", ctypes.c_bool),  # // 4仓NPD水插头下到位
        ("c_bc_slot4_check_sensor_1", ctypes.c_bool),  # // 4仓电池区分NPA
        ("c_bc_slot4_check_sensor_2", ctypes.c_bool),  # // 4仓电池区分NPD
        ("c_bc_slot4_reached_sensor", ctypes.c_bool),  # // 4仓电池落到位
        ("c_bc_slot4_smoke_sensor", ctypes.c_bool),  # // 4仓烟雾报警
        ("c_bc_slot4_liq_flow_switch_st", ctypes.c_bool),  # // 4仓水冷流量开关
        ("c_bc_slot5_ec_retract_sensor_1", ctypes.c_bool),  # // 5仓NPA电插头上到位
        ("c_bc_slot5_ec_extend_sensor_1", ctypes.c_bool),  # // 5仓NPA电插头下到位
        ("c_bc_slot5_lc_retract_sensor_1", ctypes.c_bool),  # // 5仓NPA水插头上到位
        ("c_bc_slot5_lc_extend_sensor_1", ctypes.c_bool),  # // 5仓NPA水插头下到位
        ("c_bc_slot5_ec_retract_sensor_2", ctypes.c_bool),  # // 5仓NPD电插头上到位
        ("c_bc_slot5_ec_extend_sensor_2", ctypes.c_bool),  # // 5仓NPD电插头下到位
        ("c_bc_slot5_lc_retract_sensor_2", ctypes.c_bool),  # // 5仓NPD水插头上到位
        ("c_bc_slot5_lc_extend_sensor_2", ctypes.c_bool),  # // 5仓NPD水插头下到位
        ("c_bc_slot5_check_sensor_1", ctypes.c_bool),  # // 5仓电池区分NPA
        ("c_bc_slot5_check_sensor_2", ctypes.c_bool),  # // 5仓电池区分NPD
        ("c_bc_slot5_reached_sensor", ctypes.c_bool),  # // 5仓电池落到位
        ("c_bc_slot5_smoke_sensor", ctypes.c_bool),  # // 5仓烟雾报警
        ("c_bc_slot5_liq_flow_switch_st", ctypes.c_bool),  # // 5仓水冷流量开关
        ("c_bc_slot1_5_pressure_switch_st", ctypes.c_bool),  # // 1~5仓水冷压力开关
        ("c_bc_slot6_ec_retract_sensor_1", ctypes.c_bool),  # // 6仓NPA电插头上到位
        ("c_bc_slot6_ec_extend_sensor_1", ctypes.c_bool),  # // 6仓NPA电插头下到位
        ("c_bc_slot6_lc_retract_sensor_1", ctypes.c_bool),  # // 6仓NPA水插头上到位
        ("c_bc_slot6_lc_extend_sensor_1", ctypes.c_bool),  # // 6仓NPA水插头下到位
        ("c_bc_slot6_ec_retract_sensor_2", ctypes.c_bool),  # // 6仓NPD电插头上到位
        ("c_bc_slot6_ec_extend_sensor_2", ctypes.c_bool),  # // 6仓NPD电插头下到位
        ("c_bc_slot6_lc_retract_sensor_2", ctypes.c_bool),  # // 6仓NPD水插头上到位
        ("c_bc_slot6_lc_extend_sensor_2", ctypes.c_bool),  # // 6仓NPD水插头下到位
        ("c_bc_slot6_check_sensor_1", ctypes.c_bool),  # // 6仓电池区分NPA
        ("c_bc_slot6_check_sensor_2", ctypes.c_bool),  # // 6仓电池区分NPD
        ("c_bc_slot6_reached_sensor", ctypes.c_bool),  # // 6仓电池落到位
        ("c_bc_slot6_smoke_sensor", ctypes.c_bool),  # // 6仓烟雾报警
        ("c_bc_slot6_liq_flow_switch_st", ctypes.c_bool),  # // 6仓水冷流量开关
        ("c_bc_slot7_ec_retract_sensor_1", ctypes.c_bool),  # // 7仓NPA电插头上到位
        ("c_bc_slot7_ec_extend_sensor_1", ctypes.c_bool),  # // 7仓NPA电插头下到位
        ("c_bc_slot7_lc_retract_sensor_1", ctypes.c_bool),  # // 7仓NPA水插头上到位
        ("c_bc_slot7_lc_extend_sensor_1", ctypes.c_bool),  # // 7仓NPA水插头下到位
        ("c_bc_slot7_ec_retract_sensor_2", ctypes.c_bool),  # // 7仓NPD电插头上到位
        ("c_bc_slot7_ec_extend_sensor_2", ctypes.c_bool),  # // 7仓NPD电插头下到位
        ("c_bc_slot7_lc_retract_sensor_2", ctypes.c_bool),  # // 7仓NPD水插头上到位
        ("c_bc_slot7_lc_extend_sensor_2", ctypes.c_bool),  # // 7仓NPD水插头下到位
        ("c_bc_slot7_check_sensor_1", ctypes.c_bool),  # // 7仓电池区分NPA
        ("c_bc_slot7_check_sensor_2", ctypes.c_bool),  # // 7仓电池区分NPD
        ("c_bc_slot7_reached_sensor", ctypes.c_bool),  # // 7仓电池落到位
        ("c_bc_slot7_smoke_sensor", ctypes.c_bool),  # // 7仓烟雾报警
        ("c_bc_slot7_liq_flow_switch_st", ctypes.c_bool),  # // 7仓水冷流量开关
        ("c_bc_slot8_ec_retract_sensor_1", ctypes.c_bool),  # // 8仓NPA电插头上到位
        ("c_bc_slot8_ec_extend_sensor_1", ctypes.c_bool),  # // 8仓NPA电插头下到位
        ("c_bc_slot8_lc_retract_sensor_1", ctypes.c_bool),  # // 8仓NPA水插头上到位
        ("c_bc_slot8_lc_extend_sensor_1", ctypes.c_bool),  # // 8仓NPA水插头下到位
        ("c_bc_slot8_ec_retract_sensor_2", ctypes.c_bool),  # // 8仓NPD电插头上到位
        ("c_bc_slot8_ec_extend_sensor_2", ctypes.c_bool),  # // 8仓NPD电插头下到位
        ("c_bc_slot8_lc_retract_sensor_2", ctypes.c_bool),  # // 8仓NPD水插头上到位
        ("c_bc_slot8_lc_extend_sensor_2", ctypes.c_bool),  # // 8仓NPD水插头下到位
        ("c_bc_slot8_check_sensor_1", ctypes.c_bool),  # // 8仓电池区分NPA
        ("c_bc_slot8_check_sensor_2", ctypes.c_bool),  # // 8仓电池区分NPD
        ("c_bc_slot8_reached_sensor", ctypes.c_bool),  # // 8仓电池落到位
        ("c_bc_slot8_smoke_sensor", ctypes.c_bool),  # // 8仓烟雾报警
        ("c_bc_slot8_liq_flow_switch_st", ctypes.c_bool),  # // 8仓水冷流量开关
        ("c_bc_slot9_ec_retract_sensor_1", ctypes.c_bool),  # // 9仓NPA电插头上到位
        ("c_bc_slot9_ec_extend_sensor_1", ctypes.c_bool),  # // 9仓NPA电插头下到位
        ("c_bc_slot9_lc_retract_sensor_1", ctypes.c_bool),  # // 9仓NPA水插头上到位
        ("c_bc_slot9_lc_extend_sensor_1", ctypes.c_bool),  # // 9仓NPA水插头下到位
        ("c_bc_slot9_ec_retract_sensor_2", ctypes.c_bool),  # // 9仓NPD电插头上到位
        ("c_bc_slot9_ec_extend_sensor_2", ctypes.c_bool),  # // 9仓NPD电插头下到位
        ("c_bc_slot9_lc_retract_sensor_2", ctypes.c_bool),  # // 9仓NPD水插头上到位
        ("c_bc_slot9_lc_extend_sensor_2", ctypes.c_bool),  # // 9仓NPD水插头下到位
        ("c_bc_slot9_check_sensor_1", ctypes.c_bool),  # // 9仓电池区分NPA
        ("c_bc_slot9_check_sensor_2", ctypes.c_bool),  # // 9仓电池区分NPD
        ("c_bc_slot9_reached_sensor", ctypes.c_bool),  # // 9仓电池落到位
        ("c_bc_slot9_smoke_sensor", ctypes.c_bool),  # // 9仓烟雾报警
        ("c_bc_slot9_liq_flow_switch_st", ctypes.c_bool),  # // 9仓水冷流量开关
        ("c_bc_slot10_ec_retract_sensor_1", ctypes.c_bool),  # // 10仓NPA电插头上到位
        ("c_bc_slot10_ec_extend_sensor_1", ctypes.c_bool),  # // 10仓NPA电插头下到位
        ("c_bc_slot10_lc_retract_sensor_1", ctypes.c_bool),  # // 10仓NPA水插头上到位
        ("c_bc_slot10_lc_extend_sensor_1", ctypes.c_bool),  # // 10仓NPA水插头下到位
        ("c_bc_slot10_ec_retract_sensor_2", ctypes.c_bool),  # // 10仓NPD电插头上到位
        ("c_bc_slot10_ec_extend_sensor_2", ctypes.c_bool),  # // 10仓NPD电插头下到位
        ("c_bc_slot10_lc_retract_sensor_2", ctypes.c_bool),  # // 10仓NPD水插头上到位
        ("c_bc_slot10_lc_extend_sensor_2", ctypes.c_bool),  # // 10仓NPD水插头下到位
        ("c_bc_slot10_check_sensor_1", ctypes.c_bool),  # // 10仓电池区分NPA
        ("c_bc_slot10_check_sensor_2", ctypes.c_bool),  # // 10仓电池区分NPD
        ("c_bc_slot10_reached_sensor", ctypes.c_bool),  # // 10仓电池落到位
        ("c_bc_slot10_smoke_sensor", ctypes.c_bool),  # // 10仓烟雾报警
        ("c_bc_slot10_liq_flow_switch_st", ctypes.c_bool),  # // 10仓水冷流量开关
        ("c_bc_slot6_10_pressure_switch_st", ctypes.c_bool),  # // 6~10仓水冷压力开关
        ("c_stacker_low_sensor_1", ctypes.c_bool),  # // 堆垛机仓位对接1层
        ("c_stacker_low_sensor_2", ctypes.c_bool),  # // 堆垛机仓位对接2层
        ("c_stacker_low_sensor_3", ctypes.c_bool),  # // 堆垛机仓位对接3层
        ("c_stacker_low_sensor_4", ctypes.c_bool),  # // 堆垛机仓位对接4层
        ("c_stacker_low_sensor_5", ctypes.c_bool),  # // 堆垛机仓位对接5层
        ("c_stacker_low_sensor_6", ctypes.c_bool),  # // 堆垛机仓位对接6层
        ("c_stacker_low_sensor_0", ctypes.c_bool),  # // 堆垛机接驳位对接位
        ("c_stacker_move_f_sensor", ctypes.c_bool),  # // 堆垛机行走前仓位
        ("c_stacker_move_r_sensor", ctypes.c_bool),  # // 堆垛机行走后仓位
        ("c_stacker_move_RGV_sensor", ctypes.c_bool),  # // 堆垛机行走RGV对接位
        ("c_stacker_left_safe_sensor_1", ctypes.c_bool),  # // 货叉上层左超程
        ("c_stacker_right_safe_sensor_1", ctypes.c_bool),  # // 货叉上层右超程
        ("c_stacker_left_safe_sensor_2", ctypes.c_bool),  # // 货叉下层左超程
        ("c_stacker_right_safe_sensor_2", ctypes.c_bool),  # // 货叉下层右超程
        ("c_fork_retract_sensor_1", ctypes.c_bool),  # // 货叉主叉臂中点
        ("c_fork_retract_sensor_2", ctypes.c_bool),  # // 货叉辅叉臂中点
        ("c_fork_left_extend_sensor_1", ctypes.c_bool),  # // 货叉叉臂左到位1
        ("c_fork_left_extend_sensor_2", ctypes.c_bool),  # // 货叉叉臂左到位2
        ("c_fork_right_extend_sensor_1", ctypes.c_bool),  # // 货叉叉臂右到位
        ("c_fork_bc_exist_sensor_1", ctypes.c_bool),  # // 货叉有电池1
        ("c_fork_bc_exist_sensor_2", ctypes.c_bool),  # // 货叉有电池2
        ("c_vehaicl_l_work_sensor", ctypes.c_bool),  # // 左车辆举升工作位
        ("c_vehaicl_l_maintain_sensor", ctypes.c_bool),  # // 左车辆举升维护位
        ("c_vehaicl_l_safe_sensor", ctypes.c_bool),  # // 左车辆举升安全
        ("c_vehaicl_l_bc_safe_sensor", ctypes.c_bool),  # // 左车辆举升电池安全
        ("c_vehaicl_r_work_sensor", ctypes.c_bool),  # // 右车辆举升工作位
        ("c_vehaicl_r_maintain_sensor", ctypes.c_bool),  # // 右车辆举升维护位
        ("c_vehaicl_r_safe_sensor", ctypes.c_bool),  # // 右车辆举升安全
        ("c_vehaicl_r_bc_safe_sensor", ctypes.c_bool),  # // 右车辆举升电池安全
        ("c_bc_slot11_ec_retract_sensor_1", ctypes.c_bool),  # // 11仓NPA电插头上到位
        ("c_bc_slot11_ec_extend_sensor_1", ctypes.c_bool),  # // 11仓NPA电插头下到位
        ("c_bc_slot11_lc_retract_sensor_1", ctypes.c_bool),  # // 11仓NPD水插头上到位
        ("c_bc_slot11_lc_extend_sensor_1", ctypes.c_bool),  # // 11仓NPD水插头下到位
        ("c_bc_slot11_ec_retract_sensor_2", ctypes.c_bool),  # // 11仓NPA电插头上到位
        ("c_bc_slot11_ec_extend_sensor_2", ctypes.c_bool),  # // 11仓NPA电插头下到位
        ("c_bc_slot11_lc_retract_sensor_2", ctypes.c_bool),  # // 11仓NPD水插头上到位
        ("c_bc_slot11_lc_extend_sensor_2", ctypes.c_bool),  # // 11仓NPD水插头下到位
        ("c_bc_slot11_check_sensor_1", ctypes.c_bool),  # // 11仓电池区分NPA
        ("c_bc_slot11_check_sensor_2", ctypes.c_bool),  # // 11仓电池区分NPD
        ("c_bc_slot11_reached_sensor", ctypes.c_bool),  # // 11仓电池落到位
        ("c_bc_slot11_smoke_sensor", ctypes.c_bool),  # // 11仓烟雾报警
        ("c_bc_slot11_liq_flow_switch_st", ctypes.c_bool),  # // 11仓水冷流量开关
        ("c_bc_slot12_ec_retract_sensor_1", ctypes.c_bool),  # // 12仓NPA电插头上到位
        ("c_bc_slot12_ec_extend_sensor_1", ctypes.c_bool),  # // 12仓NPA电插头下到位
        ("c_bc_slot12_lc_retract_sensor_1", ctypes.c_bool),  # // 12仓NPA水插头上到位
        ("c_bc_slot12_lc_extend_sensor_1", ctypes.c_bool),  # // 12仓NPA水插头下到位
        ("c_bc_slot12_ec_retract_sensor_2", ctypes.c_bool),  # // 12仓NPD电插头上到位
        ("c_bc_slot12_ec_extend_sensor_2", ctypes.c_bool),  # // 12仓NPD电插头下到位
        ("c_bc_slot12_lc_retract_sensor_2", ctypes.c_bool),  # // 12仓NPD水插头上到位
        ("c_bc_slot12_lc_extend_sensor_2", ctypes.c_bool),  # // 12仓NPD水插头下到位
        ("c_bc_slot12_check_sensor_1", ctypes.c_bool),  # // 12仓电池区分NPA
        ("c_bc_slot12_check_sensor_2", ctypes.c_bool),  # // 12仓电池区分NPD
        ("c_bc_slot12_reached_sensor", ctypes.c_bool),  # // 12仓电池落到位
        ("c_bc_slot12_smoke_sensor", ctypes.c_bool),  # // 12仓烟雾报警
        ("c_bc_slot12_liq_flow_switch_st", ctypes.c_bool),  # // 12仓水冷流量开关
        ("c_bc_slot13_ec_retract_sensor_1", ctypes.c_bool),  # // 13仓NPA电插头上到位
        ("c_bc_slot13_ec_extend_sensor_1", ctypes.c_bool),  # // 13仓NPA电插头下到位
        ("c_bc_slot13_lc_retract_sensor_1", ctypes.c_bool),  # // 13仓NPA水插头上到位
        ("c_bc_slot13_lc_extend_sensor_1", ctypes.c_bool),  # // 13仓NPA水插头下到位
        ("c_bc_slot13_ec_retract_sensor_2", ctypes.c_bool),  # // 13仓NPD电插头上到位
        ("c_bc_slot13_ec_extend_sensor_2", ctypes.c_bool),  # // 13仓NPD电插头下到位
        ("c_bc_slot13_lc_retract_sensor_2", ctypes.c_bool),  # // 13仓NPD水插头上到位
        ("c_bc_slot13_lc_extend_sensor_2", ctypes.c_bool),  # // 13仓NPD水插头下到位
        ("c_bc_slot13_check_sensor_1", ctypes.c_bool),  # // 13仓电池区分NPA
        ("c_bc_slot13_check_sensor_2", ctypes.c_bool),  # // 13仓电池区分NPD
        ("c_bc_slot13_reached_sensor", ctypes.c_bool),  # // 13仓电池落到位
        ("c_bc_slot13_smoke_sensor", ctypes.c_bool),  # // 13仓烟雾报警
        ("c_bc_slot13_liq_flow_switch_st", ctypes.c_bool),  # // 13仓水冷流量开关
        ("c_bc_slot14_ec_retract_sensor_1", ctypes.c_bool),  # // 14仓NPA电插头上到位
        ("c_bc_slot14_ec_extend_sensor_1", ctypes.c_bool),  # // 14仓NPA电插头下到位
        ("c_bc_slot14_lc_retract_sensor_1", ctypes.c_bool),  # // 14仓NPA水插头上到位
        ("c_bc_slot14_lc_extend_sensor_1", ctypes.c_bool),  # // 14仓NPA水插头下到位
        ("c_bc_slot14_ec_retract_sensor_2", ctypes.c_bool),  # // 14仓NPD电插头上到位
        ("c_bc_slot14_ec_extend_sensor_2", ctypes.c_bool),  # // 14仓NPD电插头下到位
        ("c_bc_slot14_lc_retract_sensor_2", ctypes.c_bool),  # // 14仓NPD水插头上到位
        ("c_bc_slot14_lc_extend_sensor_2", ctypes.c_bool),  # // 14仓NPD水插头下到位
        ("c_bc_slot14_check_sensor_1", ctypes.c_bool),  # // 14仓电池区分NPA
        ("c_bc_slot14_check_sensor_2", ctypes.c_bool),  # // 14仓电池区分NPD
        ("c_bc_slot14_reached_sensor", ctypes.c_bool),  # // 14仓电池落到位
        ("c_bc_slot14_smoke_sensor", ctypes.c_bool),  # // 14仓烟雾报警
        ("c_bc_slot14_liq_flow_switch_st", ctypes.c_bool),  # // 14仓水冷流量开关
        ("c_bc_slot15_ec_retract_sensor_1", ctypes.c_bool),  # // 15仓NPA电插头上到位
        ("c_bc_slot15_ec_extend_sensor_1", ctypes.c_bool),  # // 15仓NPA电插头下到位
        ("c_bc_slot15_lc_retract_sensor_1", ctypes.c_bool),  # // 15仓NPA水插头上到位
        ("c_bc_slot15_lc_extend_sensor_1", ctypes.c_bool),  # // 15仓NPA水插头下到位
        ("c_bc_slot15_ec_retract_sensor_2", ctypes.c_bool),  # // 15仓NPD电插头上到位
        ("c_bc_slot15_ec_extend_sensor_2", ctypes.c_bool),  # // 15仓NPD电插头下到位
        ("c_bc_slot15_lc_retract_sensor_2", ctypes.c_bool),  # // 15仓NPD水插头上到位
        ("c_bc_slot15_lc_extend_sensor_2", ctypes.c_bool),  # // 15仓NPD水插头下到位
        ("c_bc_slot15_check_sensor_1", ctypes.c_bool),  # // 15仓电池区分NPA
        ("c_bc_slot15_check_sensor_2", ctypes.c_bool),  # // 15仓电池区分NPD
        ("c_bc_slot15_reached_sensor", ctypes.c_bool),  # // 15仓电池落到位
        ("c_bc_slot15_smoke_sensor", ctypes.c_bool),  # // 15仓烟雾报警
        ("c_bc_slot15_liq_flow_switch_st", ctypes.c_bool),  # // 15仓水冷流量开关
        ("c_bc_slot16_ec_retract_sensor_1", ctypes.c_bool),  # // 16仓NPA电插头上到位
        ("c_bc_slot16_ec_extend_sensor_1", ctypes.c_bool),  # // 16仓NPA电插头下到位
        ("c_bc_slot16_lc_retract_sensor_1", ctypes.c_bool),  # // 16仓NPA水插头上到位
        ("c_bc_slot16_lc_extend_sensor_1", ctypes.c_bool),  # // 16仓NPA水插头下到位
        ("c_bc_slot16_ec_retract_sensor_2", ctypes.c_bool),  # // 16仓NPD电插头上到位
        ("c_bc_slot16_ec_extend_sensor_2", ctypes.c_bool),  # // 16仓NPD电插头下到位
        ("c_bc_slot16_lc_retract_sensor_2", ctypes.c_bool),  # // 16仓NPD水插头上到位
        ("c_bc_slot16_lc_extend_sensor_2", ctypes.c_bool),  # // 16仓NPD水插头下到位
        ("c_bc_slot16_check_sensor_1", ctypes.c_bool),  # // 16仓电池区分NPA
        ("c_bc_slot16_check_sensor_2", ctypes.c_bool),  # // 16仓电池区分NPD
        ("c_bc_slot16_reached_sensor", ctypes.c_bool),  # // 16仓电池落到位
        ("c_bc_slot16_smoke_sensor", ctypes.c_bool),  # // 16仓烟雾报警
        ("c_bc_slot16_liq_flow_switch_st", ctypes.c_bool),  # // 16仓水冷流量开关
        ("c_bc_slot17_ec_retract_sensor_1", ctypes.c_bool),  # // 17仓NPA电插头上到位
        ("c_bc_slot17_ec_extend_sensor_1", ctypes.c_bool),  # // 17仓NPA电插头下到位
        ("c_bc_slot17_lc_retract_sensor_1", ctypes.c_bool),  # // 17仓NPA水插头上到位
        ("c_bc_slot17_lc_extend_sensor_1", ctypes.c_bool),  # // 17仓NPA水插头下到位
        ("c_bc_slot17_ec_retract_sensor_2", ctypes.c_bool),  # // 17仓NPD电插头上到位
        ("c_bc_slot17_ec_extend_sensor_2", ctypes.c_bool),  # // 17仓NPD电插头下到位
        ("c_bc_slot17_lc_retract_sensor_2", ctypes.c_bool),  # // 17仓NPD水插头上到位
        ("c_bc_slot17_lc_extend_sensor_2", ctypes.c_bool),  # // 17仓NPD水插头下到位
        ("c_bc_slot17_check_sensor_1", ctypes.c_bool),  # // 17仓电池区分NPA
        ("c_bc_slot17_check_sensor_2", ctypes.c_bool),  # // 17仓电池区分NPD
        ("c_bc_slot17_reached_sensor", ctypes.c_bool),  # // 17仓电池落到位
        ("c_bc_slot17_smoke_sensor", ctypes.c_bool),  # // 17仓烟雾报警
        ("c_bc_slot17_liq_flow_switch_st", ctypes.c_bool),  # // 17仓水冷流量开关
        ("c_bc_slot18_ec_retract_sensor_1", ctypes.c_bool),  # // 18仓NPA电插头上到位
        ("c_bc_slot18_ec_extend_sensor_1", ctypes.c_bool),  # // 18仓NPA电插头下到位
        ("c_bc_slot18_lc_retract_sensor_1", ctypes.c_bool),  # // 18仓NPA水插头上到位
        ("c_bc_slot18_lc_extend_sensor_1", ctypes.c_bool),  # // 18仓NPA水插头下到位
        ("c_bc_slot18_ec_retract_sensor_2", ctypes.c_bool),  # // 18仓NPD电插头上到位
        ("c_bc_slot18_ec_extend_sensor_2", ctypes.c_bool),  # // 18仓NPD电插头下到位
        ("c_bc_slot18_lc_retract_sensor_2", ctypes.c_bool),  # // 18仓NPD水插头上到位
        ("c_bc_slot18_lc_extend_sensor_2", ctypes.c_bool),  # // 18仓NPD水插头下到位
        ("c_bc_slot18_check_sensor_1", ctypes.c_bool),  # // 18仓电池区分NPA
        ("c_bc_slot18_check_sensor_2", ctypes.c_bool),  # // 18仓电池区分NPD
        ("c_bc_slot18_reached_sensor", ctypes.c_bool),  # // 18仓电池落到位
        ("c_bc_slot18_smoke_sensor", ctypes.c_bool),  # // 18仓烟雾报警
        ("c_bc_slot18_liq_flow_switch_st", ctypes.c_bool),  # // 18仓水冷流量开关
        ("c_bc_slot19_ec_retract_sensor_1", ctypes.c_bool),  # // 19仓NPA电插头上到位
        ("c_bc_slot19_ec_extend_sensor_1", ctypes.c_bool),  # // 19仓NPA电插头下到位
        ("c_bc_slot19_lc_retract_sensor_1", ctypes.c_bool),  # // 19仓NPA水插头上到位
        ("c_bc_slot19_lc_extend_sensor_1", ctypes.c_bool),  # // 19仓NPA水插头下到位
        ("c_bc_slot19_ec_retract_sensor_2", ctypes.c_bool),  # // 19仓NPD电插头上到位
        ("c_bc_slot19_ec_extend_sensor_2", ctypes.c_bool),  # // 19仓NPD电插头下到位
        ("c_bc_slot19_lc_retract_sensor_2", ctypes.c_bool),  # // 19仓NPD水插头上到位
        ("c_bc_slot19_lc_extend_sensor_2", ctypes.c_bool),  # // 19仓NPD水插头下到位
        ("c_bc_slot19_check_sensor_1", ctypes.c_bool),  # // 19仓电池区分NPA
        ("c_bc_slot19_check_sensor_2", ctypes.c_bool),  # // 19仓电池区分NPD
        ("c_bc_slot19_reached_sensor", ctypes.c_bool),  # // 19仓电池落到位
        ("c_bc_slot19_smoke_sensor", ctypes.c_bool),  # // 19仓烟雾报警
        ("c_bc_slot19_liq_flow_switch_st", ctypes.c_bool),  # // 19仓水冷流量开关
        ("c_bc_slot20_ec_retract_sensor_1", ctypes.c_bool),  # // 20仓NPA电插头上到位
        ("c_bc_slot20_ec_extend_sensor_1", ctypes.c_bool),  # // 20仓NPA电插头下到位
        ("c_bc_slot20_lc_retract_sensor_1", ctypes.c_bool),  # // 20仓NPA水插头上到位
        ("c_bc_slot20_lc_extend_sensor_1", ctypes.c_bool),  # // 20仓NPA水插头下到位
        ("c_bc_slot20_ec_retract_sensor_2", ctypes.c_bool),  # // 20仓NPD电插头上到位
        ("c_bc_slot20_ec_extend_sensor_2", ctypes.c_bool),  # // 20仓NPD电插头下到位
        ("c_bc_slot20_lc_retract_sensor_2", ctypes.c_bool),  # // 20仓NPD水插头上到位
        ("c_bc_slot20_lc_extend_sensor_2", ctypes.c_bool),  # // 20仓NPD水插头下到位
        ("c_bc_slot20_check_sensor_1", ctypes.c_bool),  # // 20仓电池区分NPA
        ("c_bc_slot20_check_sensor_2", ctypes.c_bool),  # // 20仓电池区分NPD
        ("c_bc_slot20_reached_sensor", ctypes.c_bool),  # // 20仓电池落到位
        ("c_bc_slot20_smoke_sensor", ctypes.c_bool),  # // 20仓烟雾报警
        ("c_bc_slot20_liq_flow_switch_st", ctypes.c_bool),  # // 20仓水冷流量开关
        ("c_bc_slot21_ec_retract_sensor_1", ctypes.c_bool),  # // 21仓NPA电插头上到位
        ("c_bc_slot21_ec_extend_sensor_1", ctypes.c_bool),  # // 21仓NPA电插头下到位
        ("c_bc_slot21_ec_retract_sensor_2", ctypes.c_bool),  # // 21仓NPD电插头上到位
        ("c_bc_slot21_ec_extend_sensor_2", ctypes.c_bool),  # // 21仓NPD电插头下到位
        ("c_bc_slot21_check_sensor_1", ctypes.c_bool),  # // 21仓电池区分NPA
        ("c_bc_slot21_check_sensor_2", ctypes.c_bool),  # // 21仓电池区分NPD
        ("c_bc_slot21_reached_sensor", ctypes.c_bool),  # // 21仓电池落到位
        ("c_bc_slot21_smoke_sensor", ctypes.c_bool),  # // 21仓烟雾报警
        ("c_bc_slot11_15_pressure_switch_st", ctypes.c_bool),  # // 11~15仓 水冷压力开关
        ("c_bc_slot16_20_pressure_switch_st", ctypes.c_bool),  # // 16~20仓 水冷压力开关
        ("c_bc_fire_push_retract_sensor_1", ctypes.c_bool),  # // 消防接驳前推杆缩回到位
        ("c_bc_fire_push_extend_sensor_1", ctypes.c_bool),  # // 消防接驳前推杆伸出到位
        ("c_bc_fire_push_retract_sensor_2", ctypes.c_bool),  # // 消防接驳后推杆缩回到位
        ("c_bc_fire_push_extend_sensor_2", ctypes.c_bool),  # // 消防接驳后推杆伸出到位
        ("c_fire_liq_check", ctypes.c_bool),  # // 消防液位检测
        ("c_fork_X_left_limit_sensor", ctypes.c_bool),  # // 堆垛机货叉左限位
        ("c_fork_X_right_limit_sensor", ctypes.c_bool),  # // 堆垛机货叉右限位
        ("c_fork_X_home_sensor", ctypes.c_bool),  # // 堆垛机货叉原点
        ("c_stacker_move_f_limit_sensor", ctypes.c_bool),  # // 堆垛机行走前限位
        ("c_stacker_move_r_limit_sensor", ctypes.c_bool),  # // 堆垛机行走后限位
        ("c_stacker_move_home_sensor", ctypes.c_bool),  # // 堆垛机行走原点
        ("c_stacker_lift_up_limit_sensor", ctypes.c_bool),  # // 堆垛机升降上限位
        ("c_stacker_lift_down_limit_sensor", ctypes.c_bool),  # // 堆垛机升降下限位
        ("c_stacker_lift_home_sensor", ctypes.c_bool),  # // 堆垛机升降原点
        ("c_pl_move_f_limit_sensor", ctypes.c_bool),  # // 加解锁平台平移前限位
        ("c_pl_move_r_limit_sensor", ctypes.c_bool),  # // 加解锁平台平移后限位
        ("c_pl_move_home_sensor", ctypes.c_bool),  # // 加解锁平台平移原点
        ("c_lr_lift_up_limit_sensor", ctypes.c_bool),  # // 加解锁平台升降上限位
        ("c_lr_lift_down_limit_sensor", ctypes.c_bool),  # // 加解锁平台升降下限位
        ("c_lr_lift_home_sensor", ctypes.c_bool),  # // 加解锁平台升降原点
        ("c_vehical_f_up_limit_sensor", ctypes.c_bool),  # // 左车辆举升上限位
        ("c_vehical_f_down_limit_sensor", ctypes.c_bool),  # // 左车辆举升下限位
        ("c_vehical_f_home_sensor", ctypes.c_bool),  # // 左车辆举升原点
        ("c_vehical_r_up_limit_sensor", ctypes.c_bool),  # // 右车辆举升上限位
        ("c_vehical_r_down_limit_sensor", ctypes.c_bool),  # // 右车辆举升下限位
        ("c_vehical_r_home_sensor", ctypes.c_bool),  # // 右车辆举升原点
        ("c_bc_lift_up_limit_sensor", ctypes.c_bool),  # // 升降仓上限位
        ("c_bc_lift_down_limit_sensor", ctypes.c_bool),  # // 升降仓下限位
        ("c_bc_lift_home_sensor", ctypes.c_bool),  # // 升降仓原点
        ("c_bc_lift_safe_sensor", ctypes.c_bool),  # // 接驳位举升电池安全
        ("c_left_buffer_safe_sensor", ctypes.c_bool),  # // 左缓存电池安全
        ("c_right_buffer_safe_sensor", ctypes.c_bool),  # // 右缓存电池安全
        ("c_bc_slot22_reached_sensor", ctypes.c_bool),  # // 消防仓电池落到位
        ("c_bc_lift_exist_sensor", ctypes.c_bool),  # // 接驳位上有电池检测
        ("c_rgv_bc_reach_sensor_07", ctypes.c_bool),  # // 电池平整7
        ("c_rgv_bc_reach_sensor_08", ctypes.c_bool),  # // 电池平整8
        ("c_liq_lift_zero_sensor", ctypes.c_bool),  # // 液压举升原点位
        ("c_reserved", ctypes.c_bool * 73),  # // 预留
    ]


def generate_PLC_SENSOR_STRUCT(obj, data):
    obj.c_roller_door_01_up_limt = data.get("c_roller_door_01_up_limt")[0]
    obj.c_roller_door_01_down_limt = data.get("c_roller_door_01_down_limt")[0]
    obj.c_roller_door_02_up_limt = data.get("c_roller_door_02_up_limt")[0]
    obj.c_roller_door_02_down_limt = data.get("c_roller_door_02_down_limt")[0]
    obj.c_front_roller_door_safety_01 = data.get("c_front_roller_door_safety_01")[0]
    obj.c_front_roller_door_safety_02 = data.get("c_front_roller_door_safety_02")[0]
    obj.c_rear_roller_door_safety_01 = data.get("c_rear_roller_door_safety_01")[0]
    obj.c_rear_roller_door_safety_02 = data.get("c_rear_roller_door_safety_02")[0]
    obj.c_maintain_area_safety_01 = data.get("c_maintain_area_safety_01")[0]
    obj.c_maintain_area_safety_02 = data.get("c_maintain_area_safety_02")[0]
    obj.c_pl_buffer_dece_sensor_1 = data.get("c_pl_buffer_dece_sensor_1")[0]
    obj.c_pl_buffer_sensor_f_1 = data.get("c_pl_buffer_sensor_f_1")[0]
    obj.c_pl_buffer_sensor_r_1 = data.get("c_pl_buffer_sensor_r_1")[0]
    obj.c_pl_lf_clamp_home_sensor = data.get("c_pl_lf_clamp_home_sensor")[0]
    obj.c_pl_lf_V_check_sensor = data.get("c_pl_lf_V_check_sensor")[0]
    obj.c_pl_l_V_lock_extend_sensor = data.get("c_pl_l_V_lock_extend_sensor")[0]
    obj.c_pl_l_V_lock_retract_sensor = data.get("c_pl_l_V_lock_retract_sensor")[0]
    obj.c_pl_rf_clamp_home_sensor = data.get("c_pl_rf_clamp_home_sensor")[0]
    obj.c_pl_rf_V_check_sensor = data.get("c_pl_rf_V_check_sensor")[0]
    obj.c_pl_r_V_lock_extend_sensor = data.get("c_pl_r_V_lock_extend_sensor")[0]
    obj.c_pl_r_V_lock_retract_sensor = data.get("c_pl_r_V_lock_retract_sensor")[0]
    obj.c_pl_f_guide_work_sensor = data.get("c_pl_f_guide_work_sensor")[0]
    obj.c_pl_f_guide_home_sensor = data.get("c_pl_f_guide_home_sensor")[0]
    obj.c_pl_r_guide_work_sensor = data.get("c_pl_r_guide_work_sensor")[0]
    obj.c_pl_r_guide_home_sensor = data.get("c_pl_r_guide_home_sensor")[0]
    obj.c_pl_lr_clamp_home_sensor = data.get("c_pl_lr_clamp_home_sensor")[0]
    obj.c_pl_rr_clamp_home_sensor = data.get("c_pl_rr_clamp_home_sensor")[0]
    obj.c_pl_door_01_open_sensor = data.get("c_pl_door_01_open_sensor")[0]
    obj.c_pl_door_01_close_sensor = data.get("c_pl_door_01_close_sensor")[0]
    obj.c_pl_door_02_open_sensor = data.get("c_pl_door_02_open_sensor")[0]
    obj.c_pl_door_02_close_sensor = data.get("c_pl_door_02_close_sensor")[0]
    obj.c_pl_door_close_safe_sensor = data.get("c_pl_door_close_safe_sensor")[0]
    obj.c_bc_lift_dece_sensor = data.get("c_bc_lift_dece_sensor")[0]
    obj.c_bc_lift_reach_sensor_f = data.get("c_bc_lift_reach_sensor_f")[0]
    obj.c_bc_lift_reach_sensor_r = data.get("c_bc_lift_reach_sensor_r")[0]
    obj.c_bc_lift_work_sensor = data.get("c_bc_lift_work_sensor")[0]
    obj.c_pl_buffer_dece_sensor_2 = data.get("c_pl_buffer_dece_sensor_2")[0]
    obj.c_pl_buffer_sensor_f_2 = data.get("c_pl_buffer_sensor_f_2")[0]
    obj.c_pl_buffer_sensor_r_2 = data.get("c_pl_buffer_sensor_r_2")[0]
    obj.c_buffer_stopper_01_extend_sensor_02 = data.get("c_buffer_stopper_01_extend_sensor_02")[0]
    obj.c_buffer_stopper_01_retract_sensor_02 = data.get("c_buffer_stopper_01_retract_sensor_02")[0]
    obj.c_buffer_stopper_02_extend_sensor_02 = data.get("c_buffer_stopper_02_extend_sensor_02")[0]
    obj.c_buffer_stopper_02_retract_sensor_02 = data.get("c_buffer_stopper_02_retract_sensor_02")[0]
    obj.c_RGV_bc_reach_sensor_01 = data.get("c_RGV_bc_reach_sensor_01")[0]
    obj.c_RGV_bc_reach_sensor_02 = data.get("c_RGV_bc_reach_sensor_02")[0]
    obj.c_RGV_bc_reach_sensor_03 = data.get("c_RGV_bc_reach_sensor_03")[0]
    obj.c_RGV_bc_reach_sensor_04 = data.get("c_RGV_bc_reach_sensor_04")[0]
    obj.c_RGV_bc_reach_sensor_05 = data.get("c_RGV_bc_reach_sensor_05")[0]
    obj.c_RGV_bc_reach_sensor_06 = data.get("c_RGV_bc_reach_sensor_06")[0]
    obj.c_lf_pin_extend_sensor = data.get("c_lf_pin_extend_sensor")[0]
    obj.c_lf_pin_retract_sensor = data.get("c_lf_pin_retract_sensor")[0]
    obj.c_lf_pin_touch_sensor = data.get("c_lf_pin_touch_sensor")[0]
    obj.c_rr_pin_extend_sensor = data.get("c_rr_pin_extend_sensor")[0]
    obj.c_rr_pin_retract_sensor = data.get("c_rr_pin_retract_sensor")[0]
    obj.c_rr_pin_touch_sensor = data.get("c_rr_pin_touch_sensor")[0]
    obj.c_lr_pin_extend_sensor = data.get("c_lr_pin_extend_sensor")[0]
    obj.c_lr_pin_retract_sensor = data.get("c_lr_pin_retract_sensor")[0]
    obj.c_lr_pin_touch_sensor = data.get("c_lr_pin_touch_sensor")[0]
    obj.c_gun1_lift_work_sensor = data.get("c_gun1_lift_work_sensor")[0]
    obj.c_gun1_lift_home_sensor = data.get("c_gun1_lift_home_sensor")[0]
    obj.c_gun2_lift_work_sensor = data.get("c_gun2_lift_work_sensor")[0]
    obj.c_gun2_lift_home_sensor = data.get("c_gun2_lift_home_sensor")[0]
    obj.c_gun9_move_home_sensor = data.get("c_gun9_move_home_sensor")[0]
    obj.c_gun9_move_work_sensor = data.get("c_gun9_move_work_sensor")[0]
    obj.c_gun9_lift_work_sensor = data.get("c_gun9_lift_work_sensor")[0]
    obj.c_gun9_lift_home_sensor = data.get("c_gun9_lift_home_sensor")[0]
    obj.c_gun10_move_home_sensor = data.get("c_gun10_move_home_sensor")[0]
    obj.c_gun10_move_work_sensor = data.get("c_gun10_move_work_sensor")[0]
    obj.c_gun10_lift_work_sensor = data.get("c_gun10_lift_work_sensor")[0]
    obj.c_gun10_lift_home_sensor = data.get("c_gun10_lift_home_sensor")[0]
    obj.c_gun11_lift_work_sensor = data.get("c_gun11_lift_work_sensor")[0]
    obj.c_gun11_lift_home_sensor = data.get("c_gun11_lift_home_sensor")[0]
    obj.c_gun12_lift_work_sensor = data.get("c_gun12_lift_work_sensor")[0]
    obj.c_gun12_lift_home_sensor = data.get("c_gun12_lift_home_sensor")[0]
    obj.c_RGV_work_sensor = data.get("c_RGV_work_sensor")[0]
    obj.c_RGV_maintain_sensor = data.get("c_RGV_maintain_sensor")[0]
    obj.c_pl_stopper_01_home_sensor = data.get("c_pl_stopper_01_home_sensor")[0]
    obj.c_pl_stopper_01_work_sensor = data.get("c_pl_stopper_01_work_sensor")[0]
    obj.c_pl_stopper_01_reach_sensor = data.get("c_pl_stopper_01_reach_sensor")[0]
    obj.c_pl_stopper_02_home_sensor = data.get("c_pl_stopper_02_home_sensor")[0]
    obj.c_pl_stopper_02_work_sensor = data.get("c_pl_stopper_02_work_sensor")[0]
    obj.c_pl_stopper_02_reach_sensor = data.get("c_pl_stopper_02_reach_sensor")[0]
    obj.c_pl_move_work_sensor_1 = data.get("c_pl_move_work_sensor_1")[0]
    obj.c_pl_move_work_sensor_2 = data.get("c_pl_move_work_sensor_2")[0]
    obj.c_pl_move_work_sensor_3 = data.get("c_pl_move_work_sensor_3")[0]
    obj.c_pl_move_work_sensor_4 = data.get("c_pl_move_work_sensor_4")[0]
    obj.c_pl_move_work_sensor_5 = data.get("c_pl_move_work_sensor_5")[0]
    obj.c_pl_stopper_01_dece_sensor = data.get("c_pl_stopper_01_dece_sensor")[0]
    obj.c_bc_slot1_ec_retract_sensor_1 = data.get("c_bc_slot1_ec_retract_sensor_1")[0]
    obj.c_bc_slot1_ec_extend_sensor_1 = data.get("c_bc_slot1_ec_extend_sensor_1")[0]
    obj.c_bc_slot1_lc_retract_sensor_1 = data.get("c_bc_slot1_lc_retract_sensor_1")[0]
    obj.c_bc_slot1_lc_extend_sensor_1 = data.get("c_bc_slot1_lc_extend_sensor_1")[0]
    obj.c_bc_slot1_ec_retract_sensor_2 = data.get("c_bc_slot1_ec_retract_sensor_2")[0]
    obj.c_bc_slot1_ec_extend_sensor_2 = data.get("c_bc_slot1_ec_extend_sensor_2")[0]
    obj.c_bc_slot1_lc_retract_sensor_2 = data.get("c_bc_slot1_lc_retract_sensor_2")[0]
    obj.c_bc_slot1_lc_extend_sensor_2 = data.get("c_bc_slot1_lc_extend_sensor_2")[0]
    obj.c_bc_slot1_check_sensor_1 = data.get("c_bc_slot1_check_sensor_1")[0]
    obj.c_bc_slot1_check_sensor_2 = data.get("c_bc_slot1_check_sensor_2")[0]
    obj.c_bc_slot1_reached_sensor = data.get("c_bc_slot1_reached_sensor")[0]
    obj.c_bc_slot1_smoke_sensor = data.get("c_bc_slot1_smoke_sensor")[0]
    obj.c_bc_slot1_liq_flow_switch_st = data.get("c_bc_slot1_liq_flow_switch_st")[0]
    obj.c_bc_sum_smoke_sensor = data.get("c_bc_sum_smoke_sensor")[0]
    obj.c_bc_slot2_ec_retract_sensor_1 = data.get("c_bc_slot2_ec_retract_sensor_1")[0]
    obj.c_bc_slot2_ec_extend_sensor_1 = data.get("c_bc_slot2_ec_extend_sensor_1")[0]
    obj.c_bc_slot2_lc_retract_sensor_1 = data.get("c_bc_slot2_lc_retract_sensor_1")[0]
    obj.c_bc_slot2_lc_extend_sensor_1 = data.get("c_bc_slot2_lc_extend_sensor_1")[0]
    obj.c_bc_slot2_ec_retract_sensor_2 = data.get("c_bc_slot2_ec_retract_sensor_2")[0]
    obj.c_bc_slot2_ec_extend_sensor_2 = data.get("c_bc_slot2_ec_extend_sensor_2")[0]
    obj.c_bc_slot2_lc_retract_sensor_2 = data.get("c_bc_slot2_lc_retract_sensor_2")[0]
    obj.c_bc_slot2_lc_extend_sensor_2 = data.get("c_bc_slot2_lc_extend_sensor_2")[0]
    obj.c_bc_slot2_check_sensor_1 = data.get("c_bc_slot2_check_sensor_1")[0]
    obj.c_bc_slot2_check_sensor_2 = data.get("c_bc_slot2_check_sensor_2")[0]
    obj.c_bc_slot2_reached_sensor = data.get("c_bc_slot2_reached_sensor")[0]
    obj.c_bc_slot2_smoke_sensor = data.get("c_bc_slot2_smoke_sensor")[0]
    obj.c_bc_slot2_liq_flow_switch_st = data.get("c_bc_slot2_liq_flow_switch_st")[0]
    obj.c_bc_slot3_ec_retract_sensor_1 = data.get("c_bc_slot3_ec_retract_sensor_1")[0]
    obj.c_bc_slot3_ec_extend_sensor_1 = data.get("c_bc_slot3_ec_extend_sensor_1")[0]
    obj.c_bc_slot3_lc_retract_sensor_1 = data.get("c_bc_slot3_lc_retract_sensor_1")[0]
    obj.c_bc_slot3_lc_extend_sensor_1 = data.get("c_bc_slot3_lc_extend_sensor_1")[0]
    obj.c_bc_slot3_ec_retract_sensor_2 = data.get("c_bc_slot3_ec_retract_sensor_2")[0]
    obj.c_bc_slot3_ec_extend_sensor_2 = data.get("c_bc_slot3_ec_extend_sensor_2")[0]
    obj.c_bc_slot3_lc_retract_sensor_2 = data.get("c_bc_slot3_lc_retract_sensor_2")[0]
    obj.c_bc_slot3_lc_extend_sensor_2 = data.get("c_bc_slot3_lc_extend_sensor_2")[0]
    obj.c_bc_slot3_check_sensor_1 = data.get("c_bc_slot3_check_sensor_1")[0]
    obj.c_bc_slot3_check_sensor_2 = data.get("c_bc_slot3_check_sensor_2")[0]
    obj.c_bc_slot3_reached_sensor = data.get("c_bc_slot3_reached_sensor")[0]
    obj.c_bc_slot3_smoke_sensor = data.get("c_bc_slot3_smoke_sensor")[0]
    obj.c_bc_slot3_liq_flow_switch_st = data.get("c_bc_slot3_liq_flow_switch_st")[0]
    obj.c_bc_slot4_ec_retract_sensor_1 = data.get("c_bc_slot4_ec_retract_sensor_1")[0]
    obj.c_bc_slot4_ec_extend_sensor_1 = data.get("c_bc_slot4_ec_extend_sensor_1")[0]
    obj.c_bc_slot4_lc_retract_sensor_1 = data.get("c_bc_slot4_lc_retract_sensor_1")[0]
    obj.c_bc_slot4_lc_extend_sensor_1 = data.get("c_bc_slot4_lc_extend_sensor_1")[0]
    obj.c_bc_slot4_ec_retract_sensor_2 = data.get("c_bc_slot4_ec_retract_sensor_2")[0]
    obj.c_bc_slot4_ec_extend_sensor_2 = data.get("c_bc_slot4_ec_extend_sensor_2")[0]
    obj.c_bc_slot4_lc_retract_sensor_2 = data.get("c_bc_slot4_lc_retract_sensor_2")[0]
    obj.c_bc_slot4_lc_extend_sensor_2 = data.get("c_bc_slot4_lc_extend_sensor_2")[0]
    obj.c_bc_slot4_check_sensor_1 = data.get("c_bc_slot4_check_sensor_1")[0]
    obj.c_bc_slot4_check_sensor_2 = data.get("c_bc_slot4_check_sensor_2")[0]
    obj.c_bc_slot4_reached_sensor = data.get("c_bc_slot4_reached_sensor")[0]
    obj.c_bc_slot4_smoke_sensor = data.get("c_bc_slot4_smoke_sensor")[0]
    obj.c_bc_slot4_liq_flow_switch_st = data.get("c_bc_slot4_liq_flow_switch_st")[0]
    obj.c_bc_slot5_ec_retract_sensor_1 = data.get("c_bc_slot5_ec_retract_sensor_1")[0]
    obj.c_bc_slot5_ec_extend_sensor_1 = data.get("c_bc_slot5_ec_extend_sensor_1")[0]
    obj.c_bc_slot5_lc_retract_sensor_1 = data.get("c_bc_slot5_lc_retract_sensor_1")[0]
    obj.c_bc_slot5_lc_extend_sensor_1 = data.get("c_bc_slot5_lc_extend_sensor_1")[0]
    obj.c_bc_slot5_ec_retract_sensor_2 = data.get("c_bc_slot5_ec_retract_sensor_2")[0]
    obj.c_bc_slot5_ec_extend_sensor_2 = data.get("c_bc_slot5_ec_extend_sensor_2")[0]
    obj.c_bc_slot5_lc_retract_sensor_2 = data.get("c_bc_slot5_lc_retract_sensor_2")[0]
    obj.c_bc_slot5_lc_extend_sensor_2 = data.get("c_bc_slot5_lc_extend_sensor_2")[0]
    obj.c_bc_slot5_check_sensor_1 = data.get("c_bc_slot5_check_sensor_1")[0]
    obj.c_bc_slot5_check_sensor_2 = data.get("c_bc_slot5_check_sensor_2")[0]
    obj.c_bc_slot5_reached_sensor = data.get("c_bc_slot5_reached_sensor")[0]
    obj.c_bc_slot5_smoke_sensor = data.get("c_bc_slot5_smoke_sensor")[0]
    obj.c_bc_slot5_liq_flow_switch_st = data.get("c_bc_slot5_liq_flow_switch_st")[0]
    obj.c_bc_slot1_5_pressure_switch_st = data.get("c_bc_slot1_5_pressure_switch_st")[0]
    obj.c_bc_slot6_ec_retract_sensor_1 = data.get("c_bc_slot6_ec_retract_sensor_1")[0]
    obj.c_bc_slot6_ec_extend_sensor_1 = data.get("c_bc_slot6_ec_extend_sensor_1")[0]
    obj.c_bc_slot6_lc_retract_sensor_1 = data.get("c_bc_slot6_lc_retract_sensor_1")[0]
    obj.c_bc_slot6_lc_extend_sensor_1 = data.get("c_bc_slot6_lc_extend_sensor_1")[0]
    obj.c_bc_slot6_ec_retract_sensor_2 = data.get("c_bc_slot6_ec_retract_sensor_2")[0]
    obj.c_bc_slot6_ec_extend_sensor_2 = data.get("c_bc_slot6_ec_extend_sensor_2")[0]
    obj.c_bc_slot6_lc_retract_sensor_2 = data.get("c_bc_slot6_lc_retract_sensor_2")[0]
    obj.c_bc_slot6_lc_extend_sensor_2 = data.get("c_bc_slot6_lc_extend_sensor_2")[0]
    obj.c_bc_slot6_check_sensor_1 = data.get("c_bc_slot6_check_sensor_1")[0]
    obj.c_bc_slot6_check_sensor_2 = data.get("c_bc_slot6_check_sensor_2")[0]
    obj.c_bc_slot6_reached_sensor = data.get("c_bc_slot6_reached_sensor")[0]
    obj.c_bc_slot6_smoke_sensor = data.get("c_bc_slot6_smoke_sensor")[0]
    obj.c_bc_slot6_liq_flow_switch_st = data.get("c_bc_slot6_liq_flow_switch_st")[0]
    obj.c_bc_slot7_ec_retract_sensor_1 = data.get("c_bc_slot7_ec_retract_sensor_1")[0]
    obj.c_bc_slot7_ec_extend_sensor_1 = data.get("c_bc_slot7_ec_extend_sensor_1")[0]
    obj.c_bc_slot7_lc_retract_sensor_1 = data.get("c_bc_slot7_lc_retract_sensor_1")[0]
    obj.c_bc_slot7_lc_extend_sensor_1 = data.get("c_bc_slot7_lc_extend_sensor_1")[0]
    obj.c_bc_slot7_ec_retract_sensor_2 = data.get("c_bc_slot7_ec_retract_sensor_2")[0]
    obj.c_bc_slot7_ec_extend_sensor_2 = data.get("c_bc_slot7_ec_extend_sensor_2")[0]
    obj.c_bc_slot7_lc_retract_sensor_2 = data.get("c_bc_slot7_lc_retract_sensor_2")[0]
    obj.c_bc_slot7_lc_extend_sensor_2 = data.get("c_bc_slot7_lc_extend_sensor_2")[0]
    obj.c_bc_slot7_check_sensor_1 = data.get("c_bc_slot7_check_sensor_1")[0]
    obj.c_bc_slot7_check_sensor_2 = data.get("c_bc_slot7_check_sensor_2")[0]
    obj.c_bc_slot7_reached_sensor = data.get("c_bc_slot7_reached_sensor")[0]
    obj.c_bc_slot7_smoke_sensor = data.get("c_bc_slot7_smoke_sensor")[0]
    obj.c_bc_slot7_liq_flow_switch_st = data.get("c_bc_slot7_liq_flow_switch_st")[0]
    obj.c_bc_slot8_ec_retract_sensor_1 = data.get("c_bc_slot8_ec_retract_sensor_1")[0]
    obj.c_bc_slot8_ec_extend_sensor_1 = data.get("c_bc_slot8_ec_extend_sensor_1")[0]
    obj.c_bc_slot8_lc_retract_sensor_1 = data.get("c_bc_slot8_lc_retract_sensor_1")[0]
    obj.c_bc_slot8_lc_extend_sensor_1 = data.get("c_bc_slot8_lc_extend_sensor_1")[0]
    obj.c_bc_slot8_ec_retract_sensor_2 = data.get("c_bc_slot8_ec_retract_sensor_2")[0]
    obj.c_bc_slot8_ec_extend_sensor_2 = data.get("c_bc_slot8_ec_extend_sensor_2")[0]
    obj.c_bc_slot8_lc_retract_sensor_2 = data.get("c_bc_slot8_lc_retract_sensor_2")[0]
    obj.c_bc_slot8_lc_extend_sensor_2 = data.get("c_bc_slot8_lc_extend_sensor_2")[0]
    obj.c_bc_slot8_check_sensor_1 = data.get("c_bc_slot8_check_sensor_1")[0]
    obj.c_bc_slot8_check_sensor_2 = data.get("c_bc_slot8_check_sensor_2")[0]
    obj.c_bc_slot8_reached_sensor = data.get("c_bc_slot8_reached_sensor")[0]
    obj.c_bc_slot8_smoke_sensor = data.get("c_bc_slot8_smoke_sensor")[0]
    obj.c_bc_slot8_liq_flow_switch_st = data.get("c_bc_slot8_liq_flow_switch_st")[0]
    obj.c_bc_slot9_ec_retract_sensor_1 = data.get("c_bc_slot9_ec_retract_sensor_1")[0]
    obj.c_bc_slot9_ec_extend_sensor_1 = data.get("c_bc_slot9_ec_extend_sensor_1")[0]
    obj.c_bc_slot9_lc_retract_sensor_1 = data.get("c_bc_slot9_lc_retract_sensor_1")[0]
    obj.c_bc_slot9_lc_extend_sensor_1 = data.get("c_bc_slot9_lc_extend_sensor_1")[0]
    obj.c_bc_slot9_ec_retract_sensor_2 = data.get("c_bc_slot9_ec_retract_sensor_2")[0]
    obj.c_bc_slot9_ec_extend_sensor_2 = data.get("c_bc_slot9_ec_extend_sensor_2")[0]
    obj.c_bc_slot9_lc_retract_sensor_2 = data.get("c_bc_slot9_lc_retract_sensor_2")[0]
    obj.c_bc_slot9_lc_extend_sensor_2 = data.get("c_bc_slot9_lc_extend_sensor_2")[0]
    obj.c_bc_slot9_check_sensor_1 = data.get("c_bc_slot9_check_sensor_1")[0]
    obj.c_bc_slot9_check_sensor_2 = data.get("c_bc_slot9_check_sensor_2")[0]
    obj.c_bc_slot9_reached_sensor = data.get("c_bc_slot9_reached_sensor")[0]
    obj.c_bc_slot9_smoke_sensor = data.get("c_bc_slot9_smoke_sensor")[0]
    obj.c_bc_slot9_liq_flow_switch_st = data.get("c_bc_slot9_liq_flow_switch_st")[0]
    obj.c_bc_slot10_ec_retract_sensor_1 = data.get("c_bc_slot10_ec_retract_sensor_1")[0]
    obj.c_bc_slot10_ec_extend_sensor_1 = data.get("c_bc_slot10_ec_extend_sensor_1")[0]
    obj.c_bc_slot10_lc_retract_sensor_1 = data.get("c_bc_slot10_lc_retract_sensor_1")[0]
    obj.c_bc_slot10_lc_extend_sensor_1 = data.get("c_bc_slot10_lc_extend_sensor_1")[0]
    obj.c_bc_slot10_ec_retract_sensor_2 = data.get("c_bc_slot10_ec_retract_sensor_2")[0]
    obj.c_bc_slot10_ec_extend_sensor_2 = data.get("c_bc_slot10_ec_extend_sensor_2")[0]
    obj.c_bc_slot10_lc_retract_sensor_2 = data.get("c_bc_slot10_lc_retract_sensor_2")[0]
    obj.c_bc_slot10_lc_extend_sensor_2 = data.get("c_bc_slot10_lc_extend_sensor_2")[0]
    obj.c_bc_slot10_check_sensor_1 = data.get("c_bc_slot10_check_sensor_1")[0]
    obj.c_bc_slot10_check_sensor_2 = data.get("c_bc_slot10_check_sensor_2")[0]
    obj.c_bc_slot10_reached_sensor = data.get("c_bc_slot10_reached_sensor")[0]
    obj.c_bc_slot10_smoke_sensor = data.get("c_bc_slot10_smoke_sensor")[0]
    obj.c_bc_slot10_liq_flow_switch_st = data.get("c_bc_slot10_liq_flow_switch_st")[0]
    obj.c_bc_slot6_10_pressure_switch_st = data.get("c_bc_slot6_10_pressure_switch_st")[0]
    obj.c_stacker_low_sensor_1 = data.get("c_stacker_low_sensor_1")[0]
    obj.c_stacker_low_sensor_2 = data.get("c_stacker_low_sensor_2")[0]
    obj.c_stacker_low_sensor_3 = data.get("c_stacker_low_sensor_3")[0]
    obj.c_stacker_low_sensor_4 = data.get("c_stacker_low_sensor_4")[0]
    obj.c_stacker_low_sensor_5 = data.get("c_stacker_low_sensor_5")[0]
    obj.c_stacker_low_sensor_6 = data.get("c_stacker_low_sensor_6")[0]
    obj.c_stacker_low_sensor_0 = data.get("c_stacker_low_sensor_0")[0]
    obj.c_stacker_move_f_sensor = data.get("c_stacker_move_f_sensor")[0]
    obj.c_stacker_move_r_sensor = data.get("c_stacker_move_r_sensor")[0]
    obj.c_stacker_move_RGV_sensor = data.get("c_stacker_move_RGV_sensor")[0]
    obj.c_stacker_left_safe_sensor_1 = data.get("c_stacker_left_safe_sensor_1")[0]
    obj.c_stacker_right_safe_sensor_1 = data.get("c_stacker_right_safe_sensor_1")[0]
    obj.c_stacker_left_safe_sensor_2 = data.get("c_stacker_left_safe_sensor_2")[0]
    obj.c_stacker_right_safe_sensor_2 = data.get("c_stacker_right_safe_sensor_2")[0]
    obj.c_fork_retract_sensor_1 = data.get("c_fork_retract_sensor_1")[0]
    obj.c_fork_retract_sensor_2 = data.get("c_fork_retract_sensor_2")[0]
    obj.c_fork_left_extend_sensor_1 = data.get("c_fork_left_extend_sensor_1")[0]
    obj.c_fork_left_extend_sensor_2 = data.get("c_fork_left_extend_sensor_2")[0]
    obj.c_fork_right_extend_sensor_1 = data.get("c_fork_right_extend_sensor_1")[0]
    obj.c_fork_bc_exist_sensor_1 = data.get("c_fork_bc_exist_sensor_1")[0]
    obj.c_fork_bc_exist_sensor_2 = data.get("c_fork_bc_exist_sensor_2")[0]
    obj.c_vehaicl_l_work_sensor = data.get("c_vehaicl_l_work_sensor")[0]
    obj.c_vehaicl_l_maintain_sensor = data.get("c_vehaicl_l_maintain_sensor")[0]
    obj.c_vehaicl_l_safe_sensor = data.get("c_vehaicl_l_safe_sensor")[0]
    obj.c_vehaicl_l_bc_safe_sensor = data.get("c_vehaicl_l_bc_safe_sensor")[0]
    obj.c_vehaicl_r_work_sensor = data.get("c_vehaicl_r_work_sensor")[0]
    obj.c_vehaicl_r_maintain_sensor = data.get("c_vehaicl_r_maintain_sensor")[0]
    obj.c_vehaicl_r_safe_sensor = data.get("c_vehaicl_r_safe_sensor")[0]
    obj.c_vehaicl_r_bc_safe_sensor = data.get("c_vehaicl_r_bc_safe_sensor")[0]
    obj.c_bc_slot11_ec_retract_sensor_1 = data.get("c_bc_slot11_ec_retract_sensor_1")[0]
    obj.c_bc_slot11_ec_extend_sensor_1 = data.get("c_bc_slot11_ec_extend_sensor_1")[0]
    obj.c_bc_slot11_lc_retract_sensor_1 = data.get("c_bc_slot11_lc_retract_sensor_1")[0]
    obj.c_bc_slot11_lc_extend_sensor_1 = data.get("c_bc_slot11_lc_extend_sensor_1")[0]
    obj.c_bc_slot11_ec_retract_sensor_2 = data.get("c_bc_slot11_ec_retract_sensor_2")[0]
    obj.c_bc_slot11_ec_extend_sensor_2 = data.get("c_bc_slot11_ec_extend_sensor_2")[0]
    obj.c_bc_slot11_lc_retract_sensor_2 = data.get("c_bc_slot11_lc_retract_sensor_2")[0]
    obj.c_bc_slot11_lc_extend_sensor_2 = data.get("c_bc_slot11_lc_extend_sensor_2")[0]
    obj.c_bc_slot11_check_sensor_1 = data.get("c_bc_slot11_check_sensor_1")[0]
    obj.c_bc_slot11_check_sensor_2 = data.get("c_bc_slot11_check_sensor_2")[0]
    obj.c_bc_slot11_reached_sensor = data.get("c_bc_slot11_reached_sensor")[0]
    obj.c_bc_slot11_smoke_sensor = data.get("c_bc_slot11_smoke_sensor")[0]
    obj.c_bc_slot11_liq_flow_switch_st = data.get("c_bc_slot11_liq_flow_switch_st")[0]
    obj.c_bc_slot12_ec_retract_sensor_1 = data.get("c_bc_slot12_ec_retract_sensor_1")[0]
    obj.c_bc_slot12_ec_extend_sensor_1 = data.get("c_bc_slot12_ec_extend_sensor_1")[0]
    obj.c_bc_slot12_lc_retract_sensor_1 = data.get("c_bc_slot12_lc_retract_sensor_1")[0]
    obj.c_bc_slot12_lc_extend_sensor_1 = data.get("c_bc_slot12_lc_extend_sensor_1")[0]
    obj.c_bc_slot12_ec_retract_sensor_2 = data.get("c_bc_slot12_ec_retract_sensor_2")[0]
    obj.c_bc_slot12_ec_extend_sensor_2 = data.get("c_bc_slot12_ec_extend_sensor_2")[0]
    obj.c_bc_slot12_lc_retract_sensor_2 = data.get("c_bc_slot12_lc_retract_sensor_2")[0]
    obj.c_bc_slot12_lc_extend_sensor_2 = data.get("c_bc_slot12_lc_extend_sensor_2")[0]
    obj.c_bc_slot12_check_sensor_1 = data.get("c_bc_slot12_check_sensor_1")[0]
    obj.c_bc_slot12_check_sensor_2 = data.get("c_bc_slot12_check_sensor_2")[0]
    obj.c_bc_slot12_reached_sensor = data.get("c_bc_slot12_reached_sensor")[0]
    obj.c_bc_slot12_smoke_sensor = data.get("c_bc_slot12_smoke_sensor")[0]
    obj.c_bc_slot12_liq_flow_switch_st = data.get("c_bc_slot12_liq_flow_switch_st")[0]
    obj.c_bc_slot13_ec_retract_sensor_1 = data.get("c_bc_slot13_ec_retract_sensor_1")[0]
    obj.c_bc_slot13_ec_extend_sensor_1 = data.get("c_bc_slot13_ec_extend_sensor_1")[0]
    obj.c_bc_slot13_lc_retract_sensor_1 = data.get("c_bc_slot13_lc_retract_sensor_1")[0]
    obj.c_bc_slot13_lc_extend_sensor_1 = data.get("c_bc_slot13_lc_extend_sensor_1")[0]
    obj.c_bc_slot13_ec_retract_sensor_2 = data.get("c_bc_slot13_ec_retract_sensor_2")[0]
    obj.c_bc_slot13_ec_extend_sensor_2 = data.get("c_bc_slot13_ec_extend_sensor_2")[0]
    obj.c_bc_slot13_lc_retract_sensor_2 = data.get("c_bc_slot13_lc_retract_sensor_2")[0]
    obj.c_bc_slot13_lc_extend_sensor_2 = data.get("c_bc_slot13_lc_extend_sensor_2")[0]
    obj.c_bc_slot13_check_sensor_1 = data.get("c_bc_slot13_check_sensor_1")[0]
    obj.c_bc_slot13_check_sensor_2 = data.get("c_bc_slot13_check_sensor_2")[0]
    obj.c_bc_slot13_reached_sensor = data.get("c_bc_slot13_reached_sensor")[0]
    obj.c_bc_slot13_smoke_sensor = data.get("c_bc_slot13_smoke_sensor")[0]
    obj.c_bc_slot13_liq_flow_switch_st = data.get("c_bc_slot13_liq_flow_switch_st")[0]
    obj.c_bc_slot14_ec_retract_sensor_1 = data.get("c_bc_slot14_ec_retract_sensor_1")[0]
    obj.c_bc_slot14_ec_extend_sensor_1 = data.get("c_bc_slot14_ec_extend_sensor_1")[0]
    obj.c_bc_slot14_lc_retract_sensor_1 = data.get("c_bc_slot14_lc_retract_sensor_1")[0]
    obj.c_bc_slot14_lc_extend_sensor_1 = data.get("c_bc_slot14_lc_extend_sensor_1")[0]
    obj.c_bc_slot14_ec_retract_sensor_2 = data.get("c_bc_slot14_ec_retract_sensor_2")[0]
    obj.c_bc_slot14_ec_extend_sensor_2 = data.get("c_bc_slot14_ec_extend_sensor_2")[0]
    obj.c_bc_slot14_lc_retract_sensor_2 = data.get("c_bc_slot14_lc_retract_sensor_2")[0]
    obj.c_bc_slot14_lc_extend_sensor_2 = data.get("c_bc_slot14_lc_extend_sensor_2")[0]
    obj.c_bc_slot14_check_sensor_1 = data.get("c_bc_slot14_check_sensor_1")[0]
    obj.c_bc_slot14_check_sensor_2 = data.get("c_bc_slot14_check_sensor_2")[0]
    obj.c_bc_slot14_reached_sensor = data.get("c_bc_slot14_reached_sensor")[0]
    obj.c_bc_slot14_smoke_sensor = data.get("c_bc_slot14_smoke_sensor")[0]
    obj.c_bc_slot14_liq_flow_switch_st = data.get("c_bc_slot14_liq_flow_switch_st")[0]
    obj.c_bc_slot15_ec_retract_sensor_1 = data.get("c_bc_slot15_ec_retract_sensor_1")[0]
    obj.c_bc_slot15_ec_extend_sensor_1 = data.get("c_bc_slot15_ec_extend_sensor_1")[0]
    obj.c_bc_slot15_lc_retract_sensor_1 = data.get("c_bc_slot15_lc_retract_sensor_1")[0]
    obj.c_bc_slot15_lc_extend_sensor_1 = data.get("c_bc_slot15_lc_extend_sensor_1")[0]
    obj.c_bc_slot15_ec_retract_sensor_2 = data.get("c_bc_slot15_ec_retract_sensor_2")[0]
    obj.c_bc_slot15_ec_extend_sensor_2 = data.get("c_bc_slot15_ec_extend_sensor_2")[0]
    obj.c_bc_slot15_lc_retract_sensor_2 = data.get("c_bc_slot15_lc_retract_sensor_2")[0]
    obj.c_bc_slot15_lc_extend_sensor_2 = data.get("c_bc_slot15_lc_extend_sensor_2")[0]
    obj.c_bc_slot15_check_sensor_1 = data.get("c_bc_slot15_check_sensor_1")[0]
    obj.c_bc_slot15_check_sensor_2 = data.get("c_bc_slot15_check_sensor_2")[0]
    obj.c_bc_slot15_reached_sensor = data.get("c_bc_slot15_reached_sensor")[0]
    obj.c_bc_slot15_smoke_sensor = data.get("c_bc_slot15_smoke_sensor")[0]
    obj.c_bc_slot15_liq_flow_switch_st = data.get("c_bc_slot15_liq_flow_switch_st")[0]
    obj.c_bc_slot16_ec_retract_sensor_1 = data.get("c_bc_slot16_ec_retract_sensor_1")[0]
    obj.c_bc_slot16_ec_extend_sensor_1 = data.get("c_bc_slot16_ec_extend_sensor_1")[0]
    obj.c_bc_slot16_lc_retract_sensor_1 = data.get("c_bc_slot16_lc_retract_sensor_1")[0]
    obj.c_bc_slot16_lc_extend_sensor_1 = data.get("c_bc_slot16_lc_extend_sensor_1")[0]
    obj.c_bc_slot16_ec_retract_sensor_2 = data.get("c_bc_slot16_ec_retract_sensor_2")[0]
    obj.c_bc_slot16_ec_extend_sensor_2 = data.get("c_bc_slot16_ec_extend_sensor_2")[0]
    obj.c_bc_slot16_lc_retract_sensor_2 = data.get("c_bc_slot16_lc_retract_sensor_2")[0]
    obj.c_bc_slot16_lc_extend_sensor_2 = data.get("c_bc_slot16_lc_extend_sensor_2")[0]
    obj.c_bc_slot16_check_sensor_1 = data.get("c_bc_slot16_check_sensor_1")[0]
    obj.c_bc_slot16_check_sensor_2 = data.get("c_bc_slot16_check_sensor_2")[0]
    obj.c_bc_slot16_reached_sensor = data.get("c_bc_slot16_reached_sensor")[0]
    obj.c_bc_slot16_smoke_sensor = data.get("c_bc_slot16_smoke_sensor")[0]
    obj.c_bc_slot16_liq_flow_switch_st = data.get("c_bc_slot16_liq_flow_switch_st")[0]
    obj.c_bc_slot17_ec_retract_sensor_1 = data.get("c_bc_slot17_ec_retract_sensor_1")[0]
    obj.c_bc_slot17_ec_extend_sensor_1 = data.get("c_bc_slot17_ec_extend_sensor_1")[0]
    obj.c_bc_slot17_lc_retract_sensor_1 = data.get("c_bc_slot17_lc_retract_sensor_1")[0]
    obj.c_bc_slot17_lc_extend_sensor_1 = data.get("c_bc_slot17_lc_extend_sensor_1")[0]
    obj.c_bc_slot17_ec_retract_sensor_2 = data.get("c_bc_slot17_ec_retract_sensor_2")[0]
    obj.c_bc_slot17_ec_extend_sensor_2 = data.get("c_bc_slot17_ec_extend_sensor_2")[0]
    obj.c_bc_slot17_lc_retract_sensor_2 = data.get("c_bc_slot17_lc_retract_sensor_2")[0]
    obj.c_bc_slot17_lc_extend_sensor_2 = data.get("c_bc_slot17_lc_extend_sensor_2")[0]
    obj.c_bc_slot17_check_sensor_1 = data.get("c_bc_slot17_check_sensor_1")[0]
    obj.c_bc_slot17_check_sensor_2 = data.get("c_bc_slot17_check_sensor_2")[0]
    obj.c_bc_slot17_reached_sensor = data.get("c_bc_slot17_reached_sensor")[0]
    obj.c_bc_slot17_smoke_sensor = data.get("c_bc_slot17_smoke_sensor")[0]
    obj.c_bc_slot17_liq_flow_switch_st = data.get("c_bc_slot17_liq_flow_switch_st")[0]
    obj.c_bc_slot18_ec_retract_sensor_1 = data.get("c_bc_slot18_ec_retract_sensor_1")[0]
    obj.c_bc_slot18_ec_extend_sensor_1 = data.get("c_bc_slot18_ec_extend_sensor_1")[0]
    obj.c_bc_slot18_lc_retract_sensor_1 = data.get("c_bc_slot18_lc_retract_sensor_1")[0]
    obj.c_bc_slot18_lc_extend_sensor_1 = data.get("c_bc_slot18_lc_extend_sensor_1")[0]
    obj.c_bc_slot18_ec_retract_sensor_2 = data.get("c_bc_slot18_ec_retract_sensor_2")[0]
    obj.c_bc_slot18_ec_extend_sensor_2 = data.get("c_bc_slot18_ec_extend_sensor_2")[0]
    obj.c_bc_slot18_lc_retract_sensor_2 = data.get("c_bc_slot18_lc_retract_sensor_2")[0]
    obj.c_bc_slot18_lc_extend_sensor_2 = data.get("c_bc_slot18_lc_extend_sensor_2")[0]
    obj.c_bc_slot18_check_sensor_1 = data.get("c_bc_slot18_check_sensor_1")[0]
    obj.c_bc_slot18_check_sensor_2 = data.get("c_bc_slot18_check_sensor_2")[0]
    obj.c_bc_slot18_reached_sensor = data.get("c_bc_slot18_reached_sensor")[0]
    obj.c_bc_slot18_smoke_sensor = data.get("c_bc_slot18_smoke_sensor")[0]
    obj.c_bc_slot18_liq_flow_switch_st = data.get("c_bc_slot18_liq_flow_switch_st")[0]
    obj.c_bc_slot19_ec_retract_sensor_1 = data.get("c_bc_slot19_ec_retract_sensor_1")[0]
    obj.c_bc_slot19_ec_extend_sensor_1 = data.get("c_bc_slot19_ec_extend_sensor_1")[0]
    obj.c_bc_slot19_lc_retract_sensor_1 = data.get("c_bc_slot19_lc_retract_sensor_1")[0]
    obj.c_bc_slot19_lc_extend_sensor_1 = data.get("c_bc_slot19_lc_extend_sensor_1")[0]
    obj.c_bc_slot19_ec_retract_sensor_2 = data.get("c_bc_slot19_ec_retract_sensor_2")[0]
    obj.c_bc_slot19_ec_extend_sensor_2 = data.get("c_bc_slot19_ec_extend_sensor_2")[0]
    obj.c_bc_slot19_lc_retract_sensor_2 = data.get("c_bc_slot19_lc_retract_sensor_2")[0]
    obj.c_bc_slot19_lc_extend_sensor_2 = data.get("c_bc_slot19_lc_extend_sensor_2")[0]
    obj.c_bc_slot19_check_sensor_1 = data.get("c_bc_slot19_check_sensor_1")[0]
    obj.c_bc_slot19_check_sensor_2 = data.get("c_bc_slot19_check_sensor_2")[0]
    obj.c_bc_slot19_reached_sensor = data.get("c_bc_slot19_reached_sensor")[0]
    obj.c_bc_slot19_smoke_sensor = data.get("c_bc_slot19_smoke_sensor")[0]
    obj.c_bc_slot19_liq_flow_switch_st = data.get("c_bc_slot19_liq_flow_switch_st")[0]
    obj.c_bc_slot20_ec_retract_sensor_1 = data.get("c_bc_slot20_ec_retract_sensor_1")[0]
    obj.c_bc_slot20_ec_extend_sensor_1 = data.get("c_bc_slot20_ec_extend_sensor_1")[0]
    obj.c_bc_slot20_lc_retract_sensor_1 = data.get("c_bc_slot20_lc_retract_sensor_1")[0]
    obj.c_bc_slot20_lc_extend_sensor_1 = data.get("c_bc_slot20_lc_extend_sensor_1")[0]
    obj.c_bc_slot20_ec_retract_sensor_2 = data.get("c_bc_slot20_ec_retract_sensor_2")[0]
    obj.c_bc_slot20_ec_extend_sensor_2 = data.get("c_bc_slot20_ec_extend_sensor_2")[0]
    obj.c_bc_slot20_lc_retract_sensor_2 = data.get("c_bc_slot20_lc_retract_sensor_2")[0]
    obj.c_bc_slot20_lc_extend_sensor_2 = data.get("c_bc_slot20_lc_extend_sensor_2")[0]
    obj.c_bc_slot20_check_sensor_1 = data.get("c_bc_slot20_check_sensor_1")[0]
    obj.c_bc_slot20_check_sensor_2 = data.get("c_bc_slot20_check_sensor_2")[0]
    obj.c_bc_slot20_reached_sensor = data.get("c_bc_slot20_reached_sensor")[0]
    obj.c_bc_slot20_smoke_sensor = data.get("c_bc_slot20_smoke_sensor")[0]
    obj.c_bc_slot20_liq_flow_switch_st = data.get("c_bc_slot20_liq_flow_switch_st")[0]
    obj.c_bc_slot21_ec_retract_sensor_1 = data.get("c_bc_slot21_ec_retract_sensor_1")[0]
    obj.c_bc_slot21_ec_extend_sensor_1 = data.get("c_bc_slot21_ec_extend_sensor_1")[0]
    obj.c_bc_slot21_ec_retract_sensor_2 = data.get("c_bc_slot21_ec_retract_sensor_2")[0]
    obj.c_bc_slot21_ec_extend_sensor_2 = data.get("c_bc_slot21_ec_extend_sensor_2")[0]
    obj.c_bc_slot21_check_sensor_1 = data.get("c_bc_slot21_check_sensor_1")[0]
    obj.c_bc_slot21_check_sensor_2 = data.get("c_bc_slot21_check_sensor_2")[0]
    obj.c_bc_slot21_reached_sensor = data.get("c_bc_slot21_reached_sensor")[0]
    obj.c_bc_slot21_smoke_sensor = data.get("c_bc_slot21_smoke_sensor")[0]
    obj.c_bc_slot11_15_pressure_switch_st = data.get("c_bc_slot11_15_pressure_switch_st")[0]
    obj.c_bc_slot16_20_pressure_switch_st = data.get("c_bc_slot16_20_pressure_switch_st")[0]
    obj.c_bc_fire_push_retract_sensor_1 = data.get("c_bc_fire_push_retract_sensor_1")[0]
    obj.c_bc_fire_push_extend_sensor_1 = data.get("c_bc_fire_push_extend_sensor_1")[0]
    obj.c_bc_fire_push_retract_sensor_2 = data.get("c_bc_fire_push_retract_sensor_2")[0]
    obj.c_bc_fire_push_extend_sensor_2 = data.get("c_bc_fire_push_extend_sensor_2")[0]
    obj.c_fire_liq_check = data.get("c_fire_liq_check")[0]
    obj.c_fork_X_left_limit_sensor = data.get("c_fork_X_left_limit_sensor")[0]
    obj.c_fork_X_right_limit_sensor = data.get("c_fork_X_right_limit_sensor")[0]
    obj.c_fork_X_home_sensor = data.get("c_fork_X_home_sensor")[0]
    obj.c_stacker_move_f_limit_sensor = data.get("c_stacker_move_f_limit_sensor")[0]
    obj.c_stacker_move_r_limit_sensor = data.get("c_stacker_move_r_limit_sensor")[0]
    obj.c_stacker_move_home_sensor = data.get("c_stacker_move_home_sensor")[0]
    obj.c_stacker_lift_up_limit_sensor = data.get("c_stacker_lift_up_limit_sensor")[0]
    obj.c_stacker_lift_down_limit_sensor = data.get("c_stacker_lift_down_limit_sensor")[0]
    obj.c_stacker_lift_home_sensor = data.get("c_stacker_lift_home_sensor")[0]
    obj.c_pl_move_f_limit_sensor = data.get("c_pl_move_f_limit_sensor")[0]
    obj.c_pl_move_r_limit_sensor = data.get("c_pl_move_r_limit_sensor")[0]
    obj.c_pl_move_home_sensor = data.get("c_pl_move_home_sensor")[0]
    obj.c_lr_lift_up_limit_sensor = data.get("c_lr_lift_up_limit_sensor")[0]
    obj.c_lr_lift_down_limit_sensor = data.get("c_lr_lift_down_limit_sensor")[0]
    obj.c_lr_lift_home_sensor = data.get("c_lr_lift_home_sensor")[0]
    obj.c_vehical_f_up_limit_sensor = data.get("c_vehical_f_up_limit_sensor")[0]
    obj.c_vehical_f_down_limit_sensor = data.get("c_vehical_f_down_limit_sensor")[0]
    obj.c_vehical_f_home_sensor = data.get("c_vehical_f_home_sensor")[0]
    obj.c_vehical_r_up_limit_sensor = data.get("c_vehical_r_up_limit_sensor")[0]
    obj.c_vehical_r_down_limit_sensor = data.get("c_vehical_r_down_limit_sensor")[0]
    obj.c_vehical_r_home_sensor = data.get("c_vehical_r_home_sensor")[0]
    obj.c_bc_lift_up_limit_sensor = data.get("c_bc_lift_up_limit_sensor")[0]
    obj.c_bc_lift_down_limit_sensor = data.get("c_bc_lift_down_limit_sensor")[0]
    obj.c_bc_lift_home_sensor = data.get("c_bc_lift_home_sensor")[0]
    obj.c_bc_lift_safe_sensor = data.get("c_bc_lift_safe_sensor")[0]
    obj.c_left_buffer_safe_sensor = data.get("c_left_buffer_safe_sensor")[0]
    obj.c_right_buffer_safe_sensor = data.get("c_right_buffer_safe_sensor")[0]
    # 2023.3.28新增
    obj.c_bc_slot22_reached_sensor = data.get("c_bc_slot22_reached_sensor")[0]
    obj.c_bc_lift_exist_sensor = data.get("c_bc_lift_exist_sensor")[0]
    obj.c_rgv_bc_reach_sensor_07 = data.get("c_rgv_bc_reach_sensor_07")[0]
    obj.c_rgv_bc_reach_sensor_08 = data.get("c_rgv_bc_reach_sensor_08")[0]
    obj.c_liq_lift_zero_sensor = data.get("c_liq_lift_zero_sensor")[0]
    for i in range(73):
        obj.c_reserved[i] = data.get("c_reserved")[i][0]


class PLC_DI_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_emergency_stop_switch_01", ctypes.c_bool),  # // 急停
        ("c_liq_level_warning", ctypes.c_bool),  # // 液位报警
        ("c_I_power_st_1", ctypes.c_bool),  # // 扩展箱控制供电脱扣报警
        ("c_I_power_st_2", ctypes.c_bool),  # // 扩展箱动力供电脱扣报警
        ("c_I_power_st_3", ctypes.c_bool),  # // 堆垛机货叉伺服供电脱扣报警
        ("c_I_power_st_4", ctypes.c_bool),  # // 堆垛机行走伺服供电脱扣报警
        ("c_I_power_st_5", ctypes.c_bool),  # // 堆垛机升降伺服供电脱扣报警
        ("c_I_power_st_6", ctypes.c_bool),  # // 刹车开关电源后端配电脱扣报警
        ("c_I_power_st_7", ctypes.c_bool),  # // 前轮推杆伺服供电脱扣报警
        ("c_I_power_st_8", ctypes.c_bool),  # // 后轮推杆伺服供电脱扣报警
        ("c_I_power_st_9", ctypes.c_bool),  # // V槽&导向条伺服供电脱扣报警
        ("c_I_power_st_10", ctypes.c_bool),  # // 车身定位销伺服供电脱扣报警
        ("c_I_power_st_11", ctypes.c_bool),  # // 拧紧枪1 伺服供电脱扣报警
        ("c_I_power_st_12", ctypes.c_bool),  # // 拧紧枪2 伺服供电脱扣报警
        ("c_I_power_st_13", ctypes.c_bool),  # // 拧紧枪3&4 伺服供电脱扣报警
        ("c_I_power_st_14", ctypes.c_bool),  # // 拧紧枪5&6 伺服供电脱扣报警
        ("c_I_power_st_15", ctypes.c_bool),  # // 拧紧枪7&8 伺服供电脱扣报警
        ("c_I_power_st_16", ctypes.c_bool),  # // 拧紧枪9 伺服供电脱扣报警
        ("c_I_power_st_17", ctypes.c_bool),  # // 拧紧枪10 伺服供电脱扣报警
        ("c_I_power_st_18", ctypes.c_bool),  # // 拧紧枪11 伺服供电脱扣报警
        ("c_I_power_st_19", ctypes.c_bool),  # // 拧紧枪12 伺服供电脱扣报警
        ("c_I_power_st_20", ctypes.c_bool),  # // 开阖门伺服供电脱扣报警
        ("c_I_power_st_21", ctypes.c_bool),  # // RGV伺服供电脱扣报警
        ("c_I_power_st_22", ctypes.c_bool),  # // 车辆举升伺服供电脱扣报警
        ("c_I_power_st_23", ctypes.c_bool),  # // 接驳位举升伺服供电脱扣报警
        ("c_I_power_st_24", ctypes.c_bool),  # // 变频器供电脱扣报警
        ("c_A01_A1_check", ctypes.c_bool),  # // A01A1检测
        ("c_A01_A2_check", ctypes.c_bool),  # // A01A2检测
        ("c_A01_A3_check", ctypes.c_bool),  # // A01A3检测
        ("c_A01_A4_check", ctypes.c_bool),  # // A01A4检测
        ("c_A01_A5_check", ctypes.c_bool),  # // A01A5检测
        ("c_A01_A6_check", ctypes.c_bool),  # // A01A6检测
        ("c_A01_A7_check", ctypes.c_bool),  # // A01A7检测
        ("c_A01_A8_check", ctypes.c_bool),  # // A01A8检测
        ("c_A01_A9_check", ctypes.c_bool),  # // A01A9检测
        ("c_A01_A10_check", ctypes.c_bool),  # // A01A10检测
        ("c_A02_A1_module_status", ctypes.c_bool),  # // A02A1模块状态
        ("c_A02_A2_module_status", ctypes.c_bool),  # // A02A2模块状态
        ("c_A02_A3_module_status", ctypes.c_bool),  # // A02A3模块状态
        ("c_A02_A4_module_status", ctypes.c_bool),  # // A02A4模块状态
        ("c_A02_A5_module_status", ctypes.c_bool),  # // A02A5模块状态
        ("c_A02_A6_module_check", ctypes.c_bool),  # // A02A6模块状态
        ("c_reserved", ctypes.c_bool * 58),  # // 预留
    ]


def generate_PLC_DI_STRUCT(obj, data):
    obj.c_emergency_stop_switch_01 = data.get("c_emergency_stop_switch_01")[0]
    obj.c_liq_level_warning = data.get("c_liq_level_warning")[0]
    obj.c_I_power_st_1 = data.get("c_I_power_st_1")[0]
    obj.c_I_power_st_2 = data.get("c_I_power_st_2")[0]
    obj.c_I_power_st_3 = data.get("c_I_power_st_3")[0]
    obj.c_I_power_st_4 = data.get("c_I_power_st_4")[0]
    obj.c_I_power_st_5 = data.get("c_I_power_st_5")[0]
    obj.c_I_power_st_6 = data.get("c_I_power_st_6")[0]
    obj.c_I_power_st_7 = data.get("c_I_power_st_7")[0]
    obj.c_I_power_st_8 = data.get("c_I_power_st_8")[0]
    obj.c_I_power_st_9 = data.get("c_I_power_st_9")[0]
    obj.c_I_power_st_10 = data.get("c_I_power_st_10")[0]
    obj.c_I_power_st_11 = data.get("c_I_power_st_11")[0]
    obj.c_I_power_st_12 = data.get("c_I_power_st_12")[0]
    obj.c_I_power_st_13 = data.get("c_I_power_st_13")[0]
    obj.c_I_power_st_14 = data.get("c_I_power_st_14")[0]
    obj.c_I_power_st_15 = data.get("c_I_power_st_15")[0]
    obj.c_I_power_st_16 = data.get("c_I_power_st_16")[0]
    obj.c_I_power_st_17 = data.get("c_I_power_st_17")[0]
    obj.c_I_power_st_18 = data.get("c_I_power_st_18")[0]
    obj.c_I_power_st_19 = data.get("c_I_power_st_19")[0]
    obj.c_I_power_st_20 = data.get("c_I_power_st_20")[0]
    obj.c_I_power_st_21 = data.get("c_I_power_st_21")[0]
    obj.c_I_power_st_22 = data.get("c_I_power_st_22")[0]
    obj.c_I_power_st_23 = data.get("c_I_power_st_23")[0]
    obj.c_I_power_st_24 = data.get("c_I_power_st_24")[0]
    obj.c_A01_A1_check = data.get("c_A01_A1_check")[0]
    obj.c_A01_A2_check = data.get("c_A01_A2_check")[0]
    obj.c_A01_A3_check = data.get("c_A01_A3_check")[0]
    obj.c_A01_A4_check = data.get("c_A01_A4_check")[0]
    obj.c_A01_A5_check = data.get("c_A01_A5_check")[0]
    obj.c_A01_A6_check = data.get("c_A01_A6_check")[0]
    obj.c_A01_A7_check = data.get("c_A01_A7_check")[0]
    obj.c_A01_A8_check = data.get("c_A01_A8_check")[0]
    obj.c_A01_A9_check = data.get("c_A01_A9_check")[0]
    obj.c_A01_A10_check = data.get("c_A01_A10_check")[0]
    obj.c_A02_A1_module_status = data.get("c_A02_A1_module_status")[0]
    obj.c_A02_A2_module_status = data.get("c_A02_A2_module_status")[0]
    obj.c_A02_A3_module_status = data.get("c_A02_A3_module_status")[0]
    obj.c_A02_A4_module_status = data.get("c_A02_A4_module_status")[0]
    obj.c_A02_A5_module_status = data.get("c_A02_A5_module_status")[0]
    obj.c_A02_A6_module_check = data.get("c_A02_A6_module_check")[0]
    for i in range(58):
        obj.c_reserved[i] = data.get("c_reserved")[i][0]


class PLC_ALARM_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_error_code", ctypes.c_bool * 2000),
    ]


def generate_PLC_ALARM_STRUCT(obj, data):
    temp = data.get("c_error_code")
    for i in range(2000):
        obj.c_error_code[i] = temp[i][0]


class PLC_MOTION_PARAMETER_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_id", ctypes.c_int16),
        ("c_interlock_number", ctypes.c_int16),
        ("c_interlock_condition", ctypes.c_bool * 20),
        ("c_start", ctypes.c_bool),
        ("c_finished", ctypes.c_bool),
        ("c_interlock", ctypes.c_bool),
        ("c_error", ctypes.c_bool),
        ("c_is_running", ctypes.c_bool),
    ]


def generate_PLC_MOTION_PARAMETER_STRUCT(obj, data):
    obj.c_id = data.get("c_id")[0]
    obj.c_interlock_number = data.get("c_interlock_number")[0]
    for i in range(20):
        obj.c_interlock_condition[i] = data.get("c_interlock_condition")[i][0]
    obj.c_start = data.get("c_start")[0]
    obj.c_finished = data.get("c_finished")[0]
    obj.c_interlock = data.get("c_interlock")[0]
    obj.c_error = data.get("c_error")[0]
    obj.c_is_running = data.get("c_is_running")[0]


class PLC_JOB_STATUS_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_bc_job_id", ctypes.c_int16),
        ("c_bc_job_step", ctypes.c_int16),
        ("c_bc_job_finish", ctypes.c_bool),
        ("c_pl_job_id", ctypes.c_int16),
        ("c_pl_job_step", ctypes.c_int16),
        ("c_pl_job_finish", ctypes.c_bool),
    ]


def generate_PLC_JOB_STATUS_STRUCT(obj, data):
    obj.c_bc_job_id = data.get("c_bc_job_id")[0]
    obj.c_bc_job_step = data.get("c_bc_job_step")[0]
    obj.c_bc_job_finish = data.get("c_bc_job_finish")[0]
    obj.c_pl_job_id = data.get("c_pl_job_id")[0]
    obj.c_pl_job_step = data.get("c_pl_job_step")[0]
    obj.c_pl_job_finish = data.get("c_pl_job_finish")[0]


class PLC_SETTING_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_pl_lf_clamp_pos_work", ctypes.c_int),  # // 左前推杆工作位
        ("c_pl_lr_clamp_pos_work", ctypes.c_int),  # // 左后推杆工作位
        ("c_pl_rf_clamp_pos_work", ctypes.c_int),  # // 右前推杆工作位
        ("c_pl_rr_clamp_pos_work", ctypes.c_int),  # // 右后推杆工作位
        ("c_pl_v_pos_work", ctypes.c_int),  # // V槽工作位
        ("c_pl_move_pos_work_NPA", ctypes.c_int),  # // 加解锁平台平移工作位_NPA
        ("c_pl_move_pos_work_NPD", ctypes.c_int),  # // 加解锁平台平移工作位_NPD
        ("c_lr_pos_material_fixed", ctypes.c_int),  # // 加解锁平台抬升至卡销位
        ("c_lr_pos_pin_extend", ctypes.c_int),  # // 加解锁平台抬升至销子伸出位
        ("c_lr_pos_plug_approach", ctypes.c_int),  # // 加解锁平台抬升至接近插头位
        ("c_lr_pos_lock", ctypes.c_int),  # // 加解锁平台抬升至加解锁位
        ("c_lr_lf_vehicle_fixed_pin_pos_work", ctypes.c_int),  # // 左前车身定位销伸出位
        ("c_lr_rr_vehicle_fixed_pin_pos_work", ctypes.c_int),  # // 右后车身定位销伸出位
        ("c_lr_lr_vehicle_fixed_pin_pos_work", ctypes.c_int),  # // 左后车身定位销伸出位
        ("c_pl_f_guide_pos_work", ctypes.c_int),  # // 停车平台前导向条伸出位
        ("c_pl_r_guide_pos_work", ctypes.c_int),  # // 停车平台后导向条伸出位
        ("c_door_01_close_pos", ctypes.c_int),  # // 左开合门关到位
        ("c_door_02_close_pos", ctypes.c_int),  # // 右开合门关到位
        ("c_pl_lifter_pos_work", ctypes.c_int),  # // 升降仓工作位
        ("c_stacker_move_f_pos_work", ctypes.c_int),  # // 堆垛机平移至前仓
        ("c_stacker_move_r_pos_work", ctypes.c_int),  # // 堆垛机平移至后仓
        ("c_fork_X_pos_work_01", ctypes.c_int),  # // 货叉伸出左到位
        ("c_fork_X_pos_work_02", ctypes.c_int),  # // 货叉伸出右到位
        ("c_gun1_Z_pos_work", ctypes.c_int),  # // 1号枪头伸出至工作位
        ("c_gun2_Z_pos_work", ctypes.c_int),  # // 2号枪头伸出至工位位
        ("c_gun9_Z_pos_work", ctypes.c_int),  # // 9号枪头伸出至工作位
        ("c_gun10_Z_pos_work", ctypes.c_int),  # // 10号枪头伸出至工作位
        ("c_gun9_X_pos_work_02", ctypes.c_int),  # // 9号枪头横移至NPD位
        ("c_gun10_X_pos_work_02", ctypes.c_int),  # // 10号枪头横移至NPD位
        ("c_gun11_Z_pos_work", ctypes.c_int),  # // 1'号枪头伸出至工作位
        ("c_gun21_Z_pos_work", ctypes.c_int),  # // 2'号枪头伸出至工位位
        ("c_soft_pos_limit", ctypes.c_int),  # // 伺服软限位
        ("c_fork_X_pos_work_03", ctypes.c_int),  # // 货叉接驳位伸出工作位
        ("c_stacker_lift_low_pos_C1", ctypes.c_int),  # // 堆垛机C1仓低位
        ("c_stacker_lift_low_pos_C2", ctypes.c_int),  # // 堆垛机C2仓低位
        ("c_stacker_lift_low_pos_C3", ctypes.c_int),  # // 堆垛机C3仓低位
        ("c_stacker_lift_low_pos_C4", ctypes.c_int),  # // 堆垛机C4仓低位
        ("c_stacker_lift_low_pos_C5", ctypes.c_int),  # // 堆垛机C5仓低位
        ("c_stacker_lift_low_pos_C6", ctypes.c_int),  # // 堆垛机C6仓低位
        ("c_stacker_lift_low_pos_C7", ctypes.c_int),  # // 堆垛机C7仓低位
        ("c_stacker_lift_low_pos_C8", ctypes.c_int),  # // 堆垛机C8仓低位
        ("c_stacker_lift_low_pos_C9", ctypes.c_int),  # // 堆垛机C9仓低位
        ("c_stacker_lift_low_pos_C10", ctypes.c_int),  # // 堆垛机C10仓低位
        ("c_stacker_lift_low_pos_A1", ctypes.c_int),  # // 堆垛机A1仓低位
        ("c_stacker_lift_low_pos_A2", ctypes.c_int),  # // 堆垛机A2仓低位
        ("c_stacker_lift_low_pos_A3", ctypes.c_int),  # // 堆垛机A3仓低位
        ("c_stacker_lift_low_pos_A4", ctypes.c_int),  # // 堆垛机A4仓低位
        ("c_stacker_lift_low_pos_A5", ctypes.c_int),  # // 堆垛机A5仓低位
        ("c_stacker_lift_low_pos_A6", ctypes.c_int),  # // 堆垛机A6仓低位
        ("c_stacker_lift_low_pos_A7", ctypes.c_int),  # // 堆垛机A7仓低位
        ("c_stacker_lift_low_pos_A8", ctypes.c_int),  # // 堆垛机A8仓低位
        ("c_stacker_lift_low_pos_A9", ctypes.c_int),  # // 堆垛机A9仓低位
        ("c_stacker_lift_low_pos_A10", ctypes.c_int),  # // 堆垛机A10仓低位
        ("c_stacker_lift_low_pos_A11", ctypes.c_int),  # // 堆垛机A11仓低位
        ("c_stacker_lift_low_pos_A12", ctypes.c_int),  # // 消防仓低位

        ("c_stacker_move_A12_pos_work", ctypes.c_int),  # // 堆垛机平移消防仓位
        ("c_fork_X_pos_work_A12", ctypes.c_int),  # // 货叉消防仓伸出工作位
        ("c_fork_X_pos_work_C6", ctypes.c_int),  # // 货叉伸出C6_C10
        ("c_fork_X_pos_work_A6", ctypes.c_int),  # // 货叉伸出A6_A11
        ("c_stacker_move_pos_work_A1", ctypes.c_int),  # // 堆垛机平移至A1_A5
        ("c_stacker_move_pos_work_A6", ctypes.c_int),  # // 堆垛机平移至A6_A11
        ("c_gun_1_sign_torque", ctypes.c_int),  # // 1枪标定扭矩
        ("c_gun_2_sign_torque", ctypes.c_int),  # // 2枪标定扭矩
        ("c_gun_3_sign_torque", ctypes.c_int),  # // 3枪标定扭矩
        ("c_gun_4_sign_torque", ctypes.c_int),  # // 4枪标定扭矩
        ("c_gun_5_sign_torque", ctypes.c_int),  # // 5枪标定扭矩
        ("c_gun_6_sign_torque", ctypes.c_int),  # // 6枪标定扭矩
        ("c_gun_7_sign_torque", ctypes.c_int),  # // 7枪标定扭矩
        ("c_gun_8_sign_torque", ctypes.c_int),  # // 8枪标定扭矩
        ("c_gun_9_sign_torque", ctypes.c_int),  # // 9枪标定扭矩
        ("c_gun_10_sign_torque", ctypes.c_int),  # // 10枪标定扭矩
        ("c_gun_11_sign_torque", ctypes.c_int),  # // 1'枪标定扭矩
        ("c_gun_12_sign_torque", ctypes.c_int),  # // 2'枪标定扭矩
        ("c_reserved", ctypes.c_int * 5),  # // 预留
    ]


def generate_PLC_SETTING_STRUCT(obj, data):
    obj.c_pl_lf_clamp_pos_work = data.get("c_pl_lf_clamp_pos_work")[0]
    obj.c_pl_lr_clamp_pos_work = data.get("c_pl_lr_clamp_pos_work")[0]
    obj.c_pl_rf_clamp_pos_work = data.get("c_pl_rf_clamp_pos_work")[0]
    obj.c_pl_rr_clamp_pos_work = data.get("c_pl_rr_clamp_pos_work")[0]
    obj.c_pl_v_pos_work = data.get("c_pl_v_pos_work")[0]
    obj.c_pl_move_pos_work_NPA = data.get("c_pl_move_pos_work_NPA")[0]
    obj.c_pl_move_pos_work_NPD = data.get("c_pl_move_pos_work_NPD")[0]
    obj.c_lr_pos_material_fixed = data.get("c_lr_pos_material_fixed")[0]
    obj.c_lr_pos_pin_extend = data.get("c_lr_pos_pin_extend")[0]
    obj.c_lr_pos_plug_approach = data.get("c_lr_pos_plug_approach")[0]
    obj.c_lr_pos_lock = data.get("c_lr_pos_lock")[0]
    obj.c_lr_lf_vehicle_fixed_pin_pos_work = data.get("c_lr_lf_vehicle_fixed_pin_pos_work")[0]
    obj.c_lr_rr_vehicle_fixed_pin_pos_work = data.get("c_lr_rr_vehicle_fixed_pin_pos_work")[0]
    obj.c_lr_lr_vehicle_fixed_pin_pos_work = data.get("c_lr_lr_vehicle_fixed_pin_pos_work")[0]
    obj.c_pl_f_guide_pos_work = data.get("c_pl_f_guide_pos_work")[0]
    obj.c_pl_r_guide_pos_work = data.get("c_pl_r_guide_pos_work")[0]
    obj.c_door_01_close_pos = data.get("c_door_01_close_pos")[0]
    obj.c_door_02_close_pos = data.get("c_door_02_close_pos")[0]
    obj.c_pl_lifter_pos_work = data.get("c_pl_lifter_pos_work")[0]
    obj.c_stacker_move_f_pos_work = data.get("c_stacker_move_f_pos_work")[0]
    obj.c_stacker_move_r_pos_work = data.get("c_stacker_move_r_pos_work")[0]
    obj.c_fork_X_pos_work_01 = data.get("c_fork_X_pos_work_01")[0]
    obj.c_fork_X_pos_work_02 = data.get("c_fork_X_pos_work_02")[0]
    obj.c_gun1_Z_pos_work = data.get("c_gun1_Z_pos_work")[0]
    obj.c_gun2_Z_pos_work = data.get("c_gun2_Z_pos_work")[0]
    obj.c_gun9_Z_pos_work = data.get("c_gun9_Z_pos_work")[0]
    obj.c_gun10_Z_pos_work = data.get("c_gun10_Z_pos_work")[0]
    obj.c_gun9_X_pos_work_02 = data.get("c_gun9_X_pos_work_02")[0]
    obj.c_gun10_X_pos_work_02 = data.get("c_gun10_X_pos_work_02")[0]
    obj.c_gun11_Z_pos_work = data.get("c_gun11_Z_pos_work")[0]
    obj.c_gun21_Z_pos_work = data.get("c_gun21_Z_pos_work")[0]
    obj.c_soft_pos_limit = data.get("c_soft_pos_limit")[0]
    obj.c_fork_X_pos_work_03 = data.get("c_fork_X_pos_work_03")[0]
    obj.c_stacker_lift_low_pos_C1 = data.get("c_stacker_lift_low_pos_C1")[0]
    obj.c_stacker_lift_low_pos_C2 = data.get("c_stacker_lift_low_pos_C2")[0]
    obj.c_stacker_lift_low_pos_C3 = data.get("c_stacker_lift_low_pos_C3")[0]
    obj.c_stacker_lift_low_pos_C4 = data.get("c_stacker_lift_low_pos_C4")[0]
    obj.c_stacker_lift_low_pos_C5 = data.get("c_stacker_lift_low_pos_C5")[0]
    obj.c_stacker_lift_low_pos_C6 = data.get("c_stacker_lift_low_pos_C6")[0]
    obj.c_stacker_lift_low_pos_C7 = data.get("c_stacker_lift_low_pos_C7")[0]
    obj.c_stacker_lift_low_pos_C8 = data.get("c_stacker_lift_low_pos_C8")[0]
    obj.c_stacker_lift_low_pos_C9 = data.get("c_stacker_lift_low_pos_C9")[0]
    obj.c_stacker_lift_low_pos_C10 = data.get("c_stacker_lift_low_pos_C10")[0]
    obj.c_stacker_lift_low_pos_A1 = data.get("c_stacker_lift_low_pos_A1")[0]
    obj.c_stacker_lift_low_pos_A2 = data.get("c_stacker_lift_low_pos_A2")[0]
    obj.c_stacker_lift_low_pos_A3 = data.get("c_stacker_lift_low_pos_A3")[0]
    obj.c_stacker_lift_low_pos_A4 = data.get("c_stacker_lift_low_pos_A4")[0]
    obj.c_stacker_lift_low_pos_A5 = data.get("c_stacker_lift_low_pos_A5")[0]
    obj.c_stacker_lift_low_pos_A6 = data.get("c_stacker_lift_low_pos_A6")[0]
    obj.c_stacker_lift_low_pos_A7 = data.get("c_stacker_lift_low_pos_A7")[0]
    obj.c_stacker_lift_low_pos_A8 = data.get("c_stacker_lift_low_pos_A8")[0]
    obj.c_stacker_lift_low_pos_A9 = data.get("c_stacker_lift_low_pos_A9")[0]
    obj.c_stacker_lift_low_pos_A10 = data.get("c_stacker_lift_low_pos_A10")[0]
    obj.c_stacker_lift_low_pos_A11 = data.get("c_stacker_lift_low_pos_A11")[0]
    obj.c_stacker_lift_low_pos_A12 = data.get("c_stacker_lift_low_pos_A12")[0]

    obj.c_stacker_move_A12_pos_work = data.get("c_stacker_move_A12_pos_work")[0]
    obj.c_fork_X_pos_work_A12 = data.get("c_fork_X_pos_work_A12")[0]
    obj.c_fork_X_pos_work_C6 = data.get("c_fork_X_pos_work_C6")[0]
    obj.c_fork_X_pos_work_A6 = data.get("c_fork_X_pos_work_A6")[0]
    obj.c_stacker_move_pos_work_A1 = data.get("c_stacker_move_pos_work_A1")[0]
    obj.c_stacker_move_pos_work_A6 = data.get("c_stacker_move_pos_work_A6")[0]
    obj.c_gun_1_sign_torque = data.get("c_gun_1_sign_torque")[0]
    obj.c_gun_2_sign_torque = data.get("c_gun_2_sign_torque")[0]
    obj.c_gun_3_sign_torque = data.get("c_gun_3_sign_torque")[0]
    obj.c_gun_4_sign_torque = data.get("c_gun_4_sign_torque")[0]
    obj.c_gun_5_sign_torque = data.get("c_gun_5_sign_torque")[0]
    obj.c_gun_6_sign_torque = data.get("c_gun_6_sign_torque")[0]
    obj.c_gun_7_sign_torque = data.get("c_gun_7_sign_torque")[0]
    obj.c_gun_8_sign_torque = data.get("c_gun_8_sign_torque")[0]
    obj.c_gun_9_sign_torque = data.get("c_gun_9_sign_torque")[0]
    obj.c_gun_10_sign_torque = data.get("c_gun_10_sign_torque")[0]
    obj.c_gun_11_sign_torque = data.get("c_gun_11_sign_torque")[0]
    obj.c_gun_12_sign_torque = data.get("c_gun_12_sign_torque")[0]
    for i in range(5):
        obj.c_reserved[i] = data.get("c_reserved")[i][0]


class PLC_SYS_CMD_STATUS_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_setting", ctypes.c_bool),
        ("c_stop", ctypes.c_bool),
        ("c_pause", ctypes.c_bool),
        ("c_continue_st", ctypes.c_bool),
        ("c_reset", ctypes.c_bool),
        ("c_change_mode", ctypes.c_bool),
        ("c_initialize", ctypes.c_bool),
        ("c_homing", ctypes.c_bool),
    ]


def generate_PLC_SYS_CMD_STATUS_STRUCT(obj, data):
    obj.c_setting = data.get("c_setting")[0]
    obj.c_stop = data.get("c_stop")[0]
    obj.c_pause = data.get("c_pause")[0]
    obj.c_continue_st = data.get("c_continue_st")[0]
    obj.c_reset = data.get("c_reset")[0]
    obj.c_change_mode = data.get("c_change_mode")[0]
    obj.c_initialize = data.get("c_initialize")[0]
    obj.c_homing = data.get("c_homing")[0]


class PLC_VERSION_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_version", ctypes.c_byte * 11),
        # ("c_version", POINTER(c_char)),
    ]


def generate_PLC_VERSION_STRUCT(obj, data):
    # obj.c_version = (c_byte * 11)(0, 2, 3, 0, 2, 5, 0, 0, 1, 0, 0)
    tmp = [0 for _ in range(11)]
    # print(data.get("c_version"), "***")
    for i in range(len(data.get("c_version"))):
        t = data.get("c_version")[i][0]
        if isinstance(t, str) and t.isnumeric():
            tmp[i] = int(t)
    # print(tmp)
    obj.c_version = (ctypes.c_byte * 11)(*tmp)
    # print(bytes(obj.c_version))


class PLC_CONVERTER_TYPE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_error_code", ctypes.c_int16),  # //故障码
        ("c_power", ctypes.c_int16),  # //功率
        ("c_current", ctypes.c_int16),  # //电流
        ("c_frequency", ctypes.c_int16),  # //频率
    ]


def generate_PLC_CONVERTER_TYPE_STRUCT(obj, data):
    obj.c_error_code = data.get("c_error_code")[0]
    obj.c_power = data.get("c_power")[0]
    obj.c_current = data.get("c_current")[0]
    obj.c_frequency = data.get("c_frequency")[0]


class PLC_CONVERTER_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_converter_lift_roller", PLC_CONVERTER_TYPE_STRUCT),  # // 升降仓滚筒变频器
        ("c_converter_tranship", PLC_CONVERTER_TYPE_STRUCT),  # // 接驳位变频器
        ("c_converter_pl_roller", PLC_CONVERTER_TYPE_STRUCT),  # // 停车平台滚筒变频器
        ("c_converter_pl_buffer", PLC_CONVERTER_TYPE_STRUCT),  # // 停车平台缓存位变频器
    ]


def generate_PLC_CONVERTER_STRUCT(obj, data):
    generate_PLC_CONVERTER_TYPE_STRUCT(obj.c_converter_lift_roller, data.get("c_converter_lift_roller"))
    generate_PLC_CONVERTER_TYPE_STRUCT(obj.c_converter_tranship, data.get("c_converter_tranship"))
    generate_PLC_CONVERTER_TYPE_STRUCT(obj.c_converter_pl_roller, data.get("c_converter_pl_roller"))
    generate_PLC_CONVERTER_TYPE_STRUCT(obj.c_converter_pl_buffer, data.get("c_converter_pl_buffer"))


class PLC_FB_BAT_POS_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_pos", ctypes.c_int8),  # 选定电池当前仓位号 反馈
    ]


def generate_PLC_FB_BAT_POS_STRUCT(obj, data):
    obj.c_pos = data.get("c_pos")[0]


class PLC_FB_PHOTOGRAPH_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_step1", ctypes.c_bool),  # //车辆定位_01_定位状态
        ("c_step2", ctypes.c_bool),  # //亏电池下表面视觉状态
        ("c_step3", ctypes.c_bool),  # //服务电池上表面视觉状态
        ("c_step4", ctypes.c_bool),  # //车辆定位_02_定位状态
        ("c_step5", ctypes.c_bool),  # //服务电池下表面视觉状态
        ("c_step6", ctypes.c_bool),  # //亏电电池上表面视觉状态
    ]


def generate_PLC_FB_PHOTOGRAPH_STRUCT(obj, data):
    obj.c_step1 = data.get("c_step1")[0]
    obj.c_step2 = data.get("c_step2")[0]
    obj.c_step3 = data.get("c_step3")[0]
    obj.c_step4 = data.get("c_step4")[0]
    obj.c_step5 = data.get("c_step5")[0]
    obj.c_step6 = data.get("c_step6")[0]


class PLC_FB_FIRE_FINISH_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_door_status", ctypes.c_bool),  # //开合门关闭反馈
        ("c_status", ctypes.c_bool),  # //消防完成标志
        ("c_bat_arrived", ctypes.c_bool),  # //电池是否到达消防仓
        ("c_trans_finish", ctypes.c_bool),  # //消防电池转运完成(无人值守)
        ("c_button_status", ctypes.c_bool),  # // 一键落水机械按键状态
        ("c_pl_action_finish", ctypes.c_bool)  # // 停车平台动作完成（有人值守）
    ]


def generate_PLC_FB_FIRE_FINISH_STRUCT(obj, data):
    obj.c_door_status = data.get("c_door_status")[0]
    obj.c_status = data.get("c_status")[0]
    obj.c_bat_arrived = data.get("c_bat_arrived")[0]
    obj.c_trans_finish = data.get("c_trans_finish")[0]
    obj.c_button_status = data.get("c_bat_arrived")[0]
    obj.c_pl_action_finish = data.get("c_trans_finish")[0]


class PLC_FB_HOME_FINISH_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_status", ctypes.c_int8),  # 零点标定标志位反馈
    ]


def generate_PLC_FB_HOME_FINISH_STRUCT(obj, data):
    obj.c_status = data.get("c_status")[0]


class PLC_FB_ONE_LOCK_UNLOCK_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_status", ctypes.c_bool * 13),  # //[0]加解锁判断标志位,1：加锁，0：解锁;[1~12]代表1～12轴加解锁
    ]


def generate_PLC_FB_ONE_LOCK_UNLOCK_STRUCT(obj, data):
    for i in range(13):
        obj.c_status[i] = data.get("c_status")[i][0]


class PLC_FB_STACKER_POS_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_pos", ctypes.c_uint8),  # 堆垛机当前仓位号
    ]


def generate_PLC_FB_STACKER_POS_STRUCT(obj, data):
    obj.c_pos = data.get("c_pos")[0]


class PLC_FB_STATION_TYPE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_type", ctypes.c_int8),  # PLC整站类型匹配反馈
    ]


def generate_PLC_FB_STATION_TYPE_STRUCT(obj, data):
    obj.c_type = data.get("c_type")[0]


class PLC_FB_WHEEL_ADAPT_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_result", ctypes.c_int8),  # PLC轮毂自适应结果反馈
    ]


def generate_PLC_FB_WHEEL_ADAPT_STRUCT(obj, data):
    obj.c_result = data.get("c_result")[0]


class PLC_FB_VEHICLE_TYPE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_type", ctypes.c_int8),  # PLC车辆类型结果反馈
    ]


def generate_PLC_FB_VEHICLE_TYPE_STRUCT(obj, data):
    obj.c_type = data.get("c_type")[0]


class PLC_FB_BAT_TYPE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_type", ctypes.c_int8 * 21),  # PLC仓内电池类型结果反馈
    ]


def generate_PLC_FB_BAT_TYPE_STRUCT(obj, data):
    for i in range(21):
        obj.c_type[i] = data.get("c_type")[i][0]


class PLC_FB_PL_SWAP_CONTINUE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_result", ctypes.c_int8),  # PLC停车平台可继续动作结果反馈
    ]


def generate_PLC_FB_PL_SWAP_CONTINUE_STRUCT(obj, data):
    obj.c_result = data.get("c_result")[0]


class PLC_FB_CHANGE_BAT_STRUCT(ctypes.Structure):
    # PLC倒仓结果反馈
    _fields_ = [
        ("c_step", ctypes.c_int8),  # // 倒仓步骤号
        ("c_ongoing", ctypes.c_bool),  # // 是否在倒仓中
        ("c_finished", ctypes.c_bool),  # // 是否倒仓完成
    ]


def generate_PLC_FB_CHANGE_BAT_STRUCT(obj, data):
    obj.c_step = data.get("c_step")[0]
    obj.c_ongoing = data.get("c_ongoing")[0]
    obj.c_finished = data.get("c_finished")[0]


class PLC_FB_PRESSURE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_lf_value", ctypes.c_int32),
        ("c_lr_value", ctypes.c_int32),
        ("c_rr_value", ctypes.c_int32),
    ]


def generate_PLC_FB_PRESSURE_STRUCT(obj, data):
    obj.c_lf_value = data.get("c_lf_value")[0]
    obj.c_lr_value = data.get("c_lr_value")[0]
    obj.c_rr_value = data.get("c_rr_value")[0]


class PLC_FB_LOCK_DIRECTION_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_direction", ctypes.c_int8),
    ]


def generate_PLC_FB_LOCK_DIRECTION_STRUCT(obj, data):
    obj.c_direction = data.get("c_direction")[0]


class PLC_FB_VEHICLE_DIAGNOSE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_allow", ctypes.c_int8),
    ]


def generate_PLC_FB_VEHICLE_DIAGNOSE_STRUCT(obj, data):
    obj.c_allow = data.get("c_allow")[0]


class PLC_FB_BC_LIFT_TYPE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_type", ctypes.c_int8),
    ]


def generate_PLC_FB_BC_LIFT_TYPE_STRUCT(obj, data):
    obj.c_type = data.get("c_type")[0]


class PLC_FB_ROLLING_DOOR_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_front_up", ctypes.c_int8),
        ("c_front_stop", ctypes.c_int8),
        ("c_front_down", ctypes.c_int8),
        ("c_back_up", ctypes.c_int8),
        ("c_back_stop", ctypes.c_int8),
        ("c_back_down", ctypes.c_int8),
    ]


def generate_PLC_FB_ROLLING_DOOR_STRUCT(obj, data):
    obj.c_front_up = data.get("c_front_up")[0]
    obj.c_front_stop = data.get("c_front_stop")[0]
    obj.c_front_down = data.get("c_front_down")[0]
    obj.c_back_up = data.get("c_back_up")[0]
    obj.c_back_stop = data.get("c_back_stop")[0]
    obj.c_back_down = data.get("c_back_down")[0]


class PLC_FB_SWAP_ROLLBACK_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_trailer_state", ctypes.c_int8),
        ("c_swap_rollback", ctypes.c_int8),
    ]


def generate_PLC_FB_SWAP_ROLLBACK_STRUCT(obj, data):
    obj.c_trailer_state = data.get("c_trailer_state")[0]
    obj.c_swap_rollback = data.get("c_swap_rollback")[0]


class PLC_FB_SAFE_LIGHT_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_state", ctypes.c_int8),
    ]


def generate_PLC_FB_SAFE_LIGHT_STRUCT(obj, data):
    obj.c_state = data.get("c_state")[0]


class PLC_FB_FIRE_MODE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_mode", ctypes.c_int8),
    ]


def generate_PLC_FB_FIRE_MODE_STRUCT(obj, data):
    obj.c_mode = data.get("c_mode")[0]


class PLC_FB_STATION_MODE_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_mode", ctypes.c_int8),
    ]


def generate_PLC_FB_STATION_MODE_STRUCT(obj, data):
    obj.c_mode = data.get("c_mode")[0]


class PLC_FB_SERVO_TEMP_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_temp", ctypes.c_int16 * 38),
    ]


def generate_PLC_FB_SERVO_TEMP_STRUCT(obj, data):
    for i in range(38):
        obj.c_temp[i] = data.get("c_temp")[i][0]


class PLC_FB_FIRE_STATUS_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_transfer_type", ctypes.c_int8),
        ("c_drop_type", ctypes.c_int8),
        ("c_step", ctypes.c_int8),
        ("c_slot", ctypes.c_int8),
    ]


def generate_PLC_FB_FIRE_STATUS_STRUCT(obj, data):
    obj.c_transfer_type = data.get("c_transfer_type")[0]
    obj.c_drop_type = data.get("c_drop_type")[0]
    obj.c_step = data.get("c_step")[0]
    obj.c_slot = data.get("c_slot")[0]


class PLC_FB_DROP_KEY_RESULT_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_result", ctypes.c_int8),
    ]


def generate_PLC_FB_DROP_KEY_RESULT_STRUCT(obj, data):
    obj.c_result = data.get("c_result")[0]


class PLC_FB_PLUG_MOVING_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_npa_liq_state", ctypes.c_bool * 21),
        ("c_npa_pwr_state", ctypes.c_bool * 21),
        ("c_npd_liq_state", ctypes.c_bool * 21),
        ("c_npd_pwr_state", ctypes.c_bool * 21),
    ]


def generate_PLC_FB_PLUG_MOVING_STRUCT(obj, data):
    for i in range(21):
        obj.c_npa_liq_state[i] = data.get("c_npa_liq_state")[i][0]
        obj.c_npa_pwr_state[i] = data.get("c_npa_pwr_state")[i][0]
        obj.c_npd_liq_state[i] = data.get("c_npd_liq_state")[i][0]
        obj.c_npd_pwr_state[i] = data.get("c_npd_pwr_state")[i][0]


class PLC_FB_SWAP_CMD_RESULT_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_cmd_a", ctypes.c_int8),
        ("c_cmd_b", ctypes.c_int8),
        ("c_cmd_c", ctypes.c_int8)
    ]


def generate_PLC_FB_SWAP_CMD_RESULT_STRUCT(obj, data):
    obj.c_cmd_a = data.get("c_cmd_a")[0]
    obj.c_cmd_b = data.get("c_cmd_b")[0]
    obj.c_cmd_c = data.get("c_cmd_c")[0]


class PLC_FB_RGV_POSITION_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_rgv_position", ctypes.c_int8)
    ]


def generate_PLC_FB_RGV_POSITION_STRUCT(obj, data):
    obj.c_rgv_position = data.get("c_rgv_position")[0]


class PLC_CMD_FEEDBACK_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_fb_bat_pos", PLC_FB_BAT_POS_STRUCT),  # // PLC电池当前仓位号反馈
        ("c_fb_photograph", PLC_FB_PHOTOGRAPH_STRUCT),  # // PLC视觉拍照步骤反馈
        ("c_fb_fire", PLC_FB_FIRE_FINISH_STRUCT),  # // PLC消防完成标志位反馈
        ("c_fb_home", PLC_FB_HOME_FINISH_STRUCT),  # // PLC零点标定标志位反馈
        ("c_fb_lock_unlock", PLC_FB_ONE_LOCK_UNLOCK_STRUCT),  # // PLC一键加/解锁失败反馈
        ("c_fb_stacker_pos", PLC_FB_STACKER_POS_STRUCT),  # // PLC堆垛机当前仓位号反馈
        ("c_fb_station", PLC_FB_STATION_TYPE_STRUCT),  # // PLC整站类型反馈
        ("c_fb_adapt", PLC_FB_WHEEL_ADAPT_STRUCT),  # // PLC轮毂自适应结果反馈
        ("c_fb_vehicle", PLC_FB_VEHICLE_TYPE_STRUCT),  # // PLC车辆类型结果反馈
        ("c_fb_bat_type", PLC_FB_BAT_TYPE_STRUCT),  # // PLC仓内电池类型反馈
        ("c_fb_pl_swap_continue", PLC_FB_PL_SWAP_CONTINUE_STRUCT),  # // PLC停车平台可继续动作结果反馈
        ("c_fb_change_bat", PLC_FB_CHANGE_BAT_STRUCT),  # // PLC倒仓结果反馈
        ("c_fb_pin_pressure", PLC_FB_PRESSURE_STRUCT),  # // PLC车身定位销压力结果反馈
        ("c_fb_lock_direction", PLC_FB_LOCK_DIRECTION_STRUCT),  # PLC加解锁方向结果反馈
        ("c_fb_vehicle_diagnose", PLC_FB_VEHICLE_DIAGNOSE_STRUCT),  # PLC允许车辆自检结果反馈
        ("c_fb_bc_lift_type", PLC_FB_BC_LIFT_TYPE_STRUCT),  # PLC接驳机结构类型结果反馈
        ("c_fb_rolling_door", PLC_FB_ROLLING_DOOR_STRUCT),  # # PLC卷帘门执行结果反馈
        ("c_fb_swap_rollback", PLC_FB_SWAP_ROLLBACK_STRUCT),  # // PLC不挂车及回退状态反馈
        ("c_fb_safe_light", PLC_FB_SAFE_LIGHT_STRUCT),  # // PLC安全光幕使能状态反馈
        ("c_fb_fire_mode", PLC_FB_FIRE_MODE_STRUCT),  # // PLC消防模式状态反馈
        ("c_fb_station_mode", PLC_FB_STATION_MODE_STRUCT),  # // PLC整站模式维护/运营反馈
        ("c_fb_servo_temp", PLC_FB_SERVO_TEMP_STRUCT),  # // PLC伺服温度反馈
        ("c_fb_fire_status", PLC_FB_FIRE_STATUS_STRUCT),  # // PLC消防状态步骤反馈
        ("c_fb_drop_key", PLC_FB_DROP_KEY_RESULT_STRUCT),  # // PLC落水按键改造反馈
        ("c_fb_plug_moving_state", PLC_FB_PLUG_MOVING_STRUCT),  # // PLC水电插头运动状态反馈
        ("c_fb_swap_cmd", PLC_FB_SWAP_CMD_RESULT_STRUCT),  # // PLC车站并行动作命令状态反馈
        ("c_fb_rgv_position", PLC_FB_RGV_POSITION_STRUCT),  # // PLC的RGV位置反馈
        ("c_reserved", ctypes.c_int8 * 21),  # // 预留
    ]


def generate_PLC_CMD_FEEDBACK_STRUCT(obj, data):
    generate_PLC_FB_BAT_POS_STRUCT(obj.c_fb_bat_pos, data.get("c_fb_bat_pos"))
    generate_PLC_FB_PHOTOGRAPH_STRUCT(obj.c_fb_photograph, data.get("c_fb_photograph"))
    generate_PLC_FB_FIRE_FINISH_STRUCT(obj.c_fb_fire, data.get("c_fb_fire"))
    generate_PLC_FB_HOME_FINISH_STRUCT(obj.c_fb_home, data.get("c_fb_home"))
    generate_PLC_FB_ONE_LOCK_UNLOCK_STRUCT(obj.c_fb_lock_unlock, data.get("c_fb_lock_unlock"))
    generate_PLC_FB_STACKER_POS_STRUCT(obj.c_fb_stacker_pos, data.get("c_fb_stacker_pos"))
    generate_PLC_FB_STATION_TYPE_STRUCT(obj.c_fb_station, data.get("c_fb_station"))
    generate_PLC_FB_WHEEL_ADAPT_STRUCT(obj.c_fb_adapt, data.get("c_fb_adapt"))
    generate_PLC_FB_VEHICLE_TYPE_STRUCT(obj.c_fb_vehicle, data.get("c_fb_vehicle"))
    generate_PLC_FB_BAT_TYPE_STRUCT(obj.c_fb_bat_type, data.get("c_fb_bat_type"))
    generate_PLC_FB_PL_SWAP_CONTINUE_STRUCT(obj.c_fb_pl_swap_continue, data.get("c_fb_pl_swap_continue"))
    generate_PLC_FB_CHANGE_BAT_STRUCT(obj.c_fb_change_bat, data.get("c_fb_change_bat"))
    generate_PLC_FB_PRESSURE_STRUCT(obj.c_fb_pin_pressure, data.get("c_fb_pin_pressure"))
    generate_PLC_FB_LOCK_DIRECTION_STRUCT(obj.c_fb_lock_direction, data.get("c_fb_lock_direction"))
    generate_PLC_FB_VEHICLE_DIAGNOSE_STRUCT(obj.c_fb_vehicle_diagnose, data.get("c_fb_vehicle_diagnose"))
    generate_PLC_FB_BC_LIFT_TYPE_STRUCT(obj.c_fb_bc_lift_type, data.get("c_fb_bc_lift_type"))
    generate_PLC_FB_ROLLING_DOOR_STRUCT(obj.c_fb_rolling_door, data.get("c_fb_rolling_door"))
    generate_PLC_FB_SWAP_ROLLBACK_STRUCT(obj.c_fb_swap_rollback, data.get("c_fb_swap_rollback"))
    generate_PLC_FB_SAFE_LIGHT_STRUCT(obj.c_fb_safe_light, data.get("c_fb_safe_light"))
    generate_PLC_FB_FIRE_MODE_STRUCT(obj.c_fb_fire_mode, data.get("c_fb_fire_mode"))
    generate_PLC_FB_STATION_MODE_STRUCT(obj.c_fb_station_mode, data.get("c_fb_station_mode"))
    generate_PLC_FB_SERVO_TEMP_STRUCT(obj.c_fb_servo_temp, data.get("c_fb_servo_temp"))
    generate_PLC_FB_FIRE_STATUS_STRUCT(obj.c_fb_fire_status, data.get("c_fb_fire_status"))
    generate_PLC_FB_DROP_KEY_RESULT_STRUCT(obj.c_fb_drop_key, data.get("c_fb_drop_key"))
    generate_PLC_FB_PLUG_MOVING_STRUCT(obj.c_fb_plug_moving_state, data.get("c_fb_plug_moving_state"))
    generate_PLC_FB_SWAP_CMD_RESULT_STRUCT(obj.c_fb_swap_cmd, data.get("c_fb_swap_cmd"))
    generate_PLC_FB_RGV_POSITION_STRUCT(obj.c_fb_rgv_position, data.get("c_fb_rgv_position"))
    for i in range(21):
        obj.c_reserved[i] = data.get("c_reserved")[i][0]


class PLC_STATUS_REP_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_plc_msg_size", PLC_MSG_SIZE_STRUCT),  # // PLC字节长度
        ("c_mode", PLC_MODE_STRUCT),  # // PLC模式
        ("c_lr", PLC_LR_STRUCT),  # // 拆卸机器人数据
        ("c_bc", PLC_BC_STRUCT),  # // 电池仓数据
        ("c_vp", PLC_VP_STRUCT),  # // 停车平台数据
        ("c_sensor", PLC_SENSOR_STRUCT),  # // 传感器数据
        ("c_di", PLC_DI_STRUCT),  # // DI数据
        ("c_alarm", PLC_ALARM_STRUCT),  # // 告警数据
        ("c_motion", PLC_MOTION_PARAMETER_STRUCT * 280),  # // 运动控制数据
        ("c_job_status", PLC_JOB_STATUS_STRUCT),  # // 一键换电步骤状态数据
        ("c_settings", PLC_SETTING_STRUCT),  # // 参数设置数据
        ("c_sys_cmd_st", PLC_SYS_CMD_STATUS_STRUCT),  # // 系统命令状态
        ("c_plc_version", PLC_VERSION_STRUCT),  # // 版本号
        ("c_plc_converter", PLC_CONVERTER_STRUCT),  # // 变频器数据
        ("c_plc_cmd_fd", PLC_CMD_FEEDBACK_STRUCT),  # // PLC命令状态反馈
    ]


def generate_PLC_STATUS_REP_STRUCT(data):
    obj = PLC_STATUS_REP_STRUCT()
    generate_PLC_MSG_SIZE_STRUCT(obj.c_plc_msg_size, data.get("c_plc_msg_size"))
    generate_PLC_MODE_STRUCT(obj.c_mode, data.get("c_mode"))
    generate_PLC_LR_STRUCT(obj.c_lr, data.get("c_lr"))
    generate_PLC_BC_STRUCT(obj.c_bc, data.get("c_bc"))
    generate_PLC_VP_STRUCT(obj.c_vp, data.get("c_vp"))
    generate_PLC_SENSOR_STRUCT(obj.c_sensor, data.get("c_sensor"))
    generate_PLC_DI_STRUCT(obj.c_di, data.get("c_di"))
    generate_PLC_ALARM_STRUCT(obj.c_alarm, data.get("c_alarm"))
    for i in range(280):
        generate_PLC_MOTION_PARAMETER_STRUCT(obj.c_motion[i], data.get("c_motion")[i])
    generate_PLC_JOB_STATUS_STRUCT(obj.c_job_status, data.get("c_job_status"))
    generate_PLC_SETTING_STRUCT(obj.c_settings, data.get("c_settings"))
    generate_PLC_SYS_CMD_STATUS_STRUCT(obj.c_sys_cmd_st, data.get("c_sys_cmd_st"))
    generate_PLC_VERSION_STRUCT(obj.c_plc_version, data.get("c_plc_version"))
    generate_PLC_CONVERTER_STRUCT(obj.c_plc_converter, data.get("c_plc_converter"))
    generate_PLC_CMD_FEEDBACK_STRUCT(obj.c_plc_cmd_fd, data.get("c_plc_cmd_fd"))
    # log.warning(f"obj.c_plc_cmd_fd.c_fb_pl_swap_continue.c_result:{obj.c_plc_cmd_fd.c_fb_pl_swap_continue.c_result}")
    return obj


if __name__ == '__main__':
    pass
    print(ctypes.sizeof(PLC_STATUS_REP_STRUCT))
    ver = PLC_VERSION_STRUCT()
    print(type(ver.c_version))
    print(len(ver.c_version))
    # ver.c_version[0] = b'0'
    # obj.c_version = b'\x00\x02\x03\x00\x02\x05\x00\x00\x01\x00\x00'
    char_array = ctypes.c_char * 11
    # print(type(char_array))
    # ver.c_version = bytes(char_array(b'0', b'2', b'3', b'0', b'2', b'5', b'0', b'0', b'1', b'0', b'0'))
    # ver.c_version = bytes(char_array(chr(0),chr(2),chr(3),chr(0),chr(2),chr(5),chr(0),chr(0),chr(1),chr(0),chr(0)))
    # print(len(ver.c_version))
    # print(ver.c_version)
    # obj.c_version = char_array(0,2,3,0,2,5,0,0,1,0,0)
    # for i in range(len(data.get("c_version"))):
    #     obj.c_version[i] = bytes(data.get("c_version")[0], encoding='utf-8')
    # obj.c_version = [b'\x00', b'\x02',b'\x03',b'\x00',b'\x02',b'\x05',b'\x00',b'\x00',b'\x01',b'\x00',b'\x00']

    # for fiels in PLC_SETTING_STRUCT._fields_:
    #     print(f'obj.{fiels[0]} = data.get("{fiels[0]}")')
    print("******")
    # char_array_2 = (ctypes.c_char * 11)(1, 2, 3, 1, 2, 5, 1, 1, 1, 1, 1,)
    char_array_2 = (ctypes.c_char * 3)()
    char_array_2[:] = bytes([0, 2, 3])
    print(type(char_array_2.value))
    print(len(char_array_2.value))
    print(char_array_2.value)
    # char_array_2 = (ctypes.c_char * 3)(1, 0, 3)
    # print(char_array_2.value)
    # print(len(char_array_2.value), "##")
    # ver.c_version = char_array_2.value
    # print(ver.c_version)
    # print(type(ver.c_version))
    # print(ver.c_version)
