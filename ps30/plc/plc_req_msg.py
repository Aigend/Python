# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2022/11/15 19:24
# @File: plc_req_msg.py
import ctypes


class PLC_REQ_HEADER_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_com_id", ctypes.c_int8),  # /*命令ID*/
        ("c_execute", ctypes.c_bool),  # /*执行*/
    ]


class PLC_HB_REQ_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_st", ctypes.c_int),
    ]


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
        ("c_stacker_move_f_pos_work", ctypes.c_int),  # // 堆垛机平移至C1_C5
        ("c_stacker_move_r_pos_work", ctypes.c_int),  # // 堆垛机平移至C6_C10
        ("c_fork_X_pos_work_01", ctypes.c_int),  # // 货叉伸出C1_C5
        ("c_fork_X_pos_work_02", ctypes.c_int),  # // 货叉伸出A1_A5
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
        ("c_gun_1_8_sign_speed", ctypes.c_int),  # // 1~8、1'、2'枪标定速度
        ("c_gun_1_8_sign_torque", ctypes.c_int),  # // 1~8、1'、2'枪标定扭矩
        ("c_gun_9_10_sign_speed", ctypes.c_int),  # // 9、10枪标定速度
        ("c_gun_9_10_sign_torque", ctypes.c_int),  # // 9、10枪标定扭矩
        ("c_reserved", ctypes.c_int * 5),  # // 预留
    ]


class PLC_STOP_REQ_STRUCT(ctypes.Structure):
    _fields_ = [

    ]


class PLC_PAUSE_REQ_STRUCT(ctypes.Structure):
    _fields_ = [

    ]


class PLC_CONTINUE_REQ_STRUCT(ctypes.Structure):
    _fields_ = [

    ]


class PLC_RESET_REQ_STRUCT(ctypes.Structure):
    _fields_ = [

    ]


class PLC_CHANGE_MODE_REQ_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_mode", ctypes.c_int),
    ]


class PLC_HOME_REQ_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_id", ctypes.c_int),
    ]


class PLC_JOG_REQ_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_device_type", ctypes.c_int),
        ("c_id", ctypes.c_int),
        ("c_param3", ctypes.c_int),
        ("c_param4", ctypes.c_int),
        ("c_param5", ctypes.c_int),
        ("c_param6", ctypes.c_int),
        ("c_param7", ctypes.c_int),
        ("c_param8", ctypes.c_int),
    ]


class PLC_MANUAL_REQ_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_device_type", ctypes.c_int),
        ("c_id", ctypes.c_int),
        ("c_param3", ctypes.c_int),
        ("c_param4", ctypes.c_int),
        ("c_param5", ctypes.c_int),
        ("c_param6", ctypes.c_int),
        ("c_param7", ctypes.c_int),
        ("c_param8", ctypes.c_int),
    ]


class PLC_JOB_REQ_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_id", ctypes.c_int),
        ("c_param2", ctypes.c_int),
        ("c_param3", ctypes.c_int),
        ("c_param4", ctypes.c_int),
        ("c_param5", ctypes.c_int),
        ("c_param6", ctypes.c_int),
        ("c_param7", ctypes.c_int),
        ("c_param8", ctypes.c_int),
    ]


class PLC_CMD_DO_CTRL_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_id", ctypes.c_int),
        ("c_param2", ctypes.c_int),
    ]


class PLC_PHOTOGRAPH_REQ_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_param1", ctypes.c_int),  # //车辆定位_01_定位状态
        ("c_param2", ctypes.c_int),  # //亏电池下表面视觉状态
        ("c_param3", ctypes.c_int),  # //服务电池上表面视觉状态
        ("c_param4", ctypes.c_int),  # //车辆定位_02_定位状态
        ("c_param5", ctypes.c_int),  # //服务电池下表面视觉状态
        ("c_param6", ctypes.c_int),  # //亏电电池上表面视觉状态
        ("c_reserved", ctypes.c_int * 9),  # //预留
    ]


class PLC_FIRE_REQ_STRUCT(ctypes.Structure):
    _fields_ = [
        ("c_param1", ctypes.c_int),  # //消防仓位号
        ("c_param2", ctypes.c_int),  # //是否有车 0：无，1：有
        ("c_param3", ctypes.c_int),  # //是否扔水箱 0:不使能，1:使能
        ("c_param4", ctypes.c_int),  # // 消防转运类型 1:本地自动转运，2:云端远程转运
    ]


class PLC_REQUEST_BODY(ctypes.Union):
    _fields_ = [
        ("c_hb_req_msg", PLC_HB_REQ_STRUCT),  # // 心跳
        ("c_settings_req_msg", PLC_SETTING_STRUCT),  # // 参数设置
        ("c_stop_req_msg", PLC_STOP_REQ_STRUCT),  # // 预留
        ("c_pause_req_msg", PLC_PAUSE_REQ_STRUCT),  # // 预留
        ("c_continue_req_msg", PLC_CONTINUE_REQ_STRUCT),  # // 预留
        ("c_reset_req_msg", PLC_RESET_REQ_STRUCT),  # // 预留
        ("c_change_mode_req_msg", PLC_CHANGE_MODE_REQ_STRUCT),  # // 模式切换
        ("c_home_req_msg", PLC_HOME_REQ_STRUCT),  # // 零点标定
        ("c_jog_req_msg", PLC_JOG_REQ_STRUCT),  # // 点动控制
        ("c_manual_req_msg", PLC_MANUAL_REQ_STRUCT),  # // 单步控制
        ("c_job_req_msg", PLC_JOB_REQ_STRUCT),  # // JOB控制
        ("c_do_ctrl_msg", PLC_CMD_DO_CTRL_STRUCT),  # // DO控制
        ("c_photograph_req_msg", PLC_PHOTOGRAPH_REQ_STRUCT),  # // 视觉拍照请求数据
        ("c_fire_rep_msg", PLC_FIRE_REQ_STRUCT),  # // 消防请求数据
    ]


class PLC_REQUSET_STRUCT(ctypes.Structure):
    _fields_ = [

        ("c_request_header", PLC_REQ_HEADER_STRUCT),

        ("c_request_body", PLC_REQUEST_BODY)

    ]


def generate_PLC_REQUSET_STRUCT(data):
    req = PLC_REQUSET_STRUCT()
    ctypes.memmove(ctypes.addressof(req), data, ctypes.sizeof(req))

    print("#", req.c_request_header.c_com_id)
    print("##", req.c_request_header.c_execute)
    print("###", req.c_request_body.c_hb_req_msg.c_st)
    return req


if __name__ == '__main__':
    # 实际接收到的主控发送的plc的请求数据
    data = b'\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ss = PLC_REQUSET_STRUCT()
    ctypes.memmove(ctypes.addressof(ss), data, ctypes.sizeof(ss))
    print(ss.c_request_body.c_hb_req_msg)
    print(ss.c_request_header.c_com_id)

    print(ctypes.sizeof(PLC_REQUSET_STRUCT))
    req = PLC_REQUSET_STRUCT()
    req.c_request_header.c_com_id = 5
    req.c_request_header.c_execute = True
    buf = ctypes.string_at(ctypes.addressof(req), ctypes.sizeof(req))
    print(type(buf))
    ss = PLC_REQUSET_STRUCT()
    ctypes.memmove(ctypes.addressof(ss), buf, ctypes.sizeof(ss))
    print(ss.c_request_header.c_com_id)
