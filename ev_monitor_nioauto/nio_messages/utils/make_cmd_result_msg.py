#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/06/30 14:20
@contact: hongzhen.bi@nio.com
@description: 生成和解析command_result的proto
"""

import random
import time
import json
import logging
from nio_messages.data_unit import gen_hvac_status, gen_door_status, gen_window_status, gen_heating_status
from nio_messages.pb2 import nextev_msg_pb2, generic_config_result_pb2, cmd_result_pb2, \
    door_status_pb2, soc_status_pb2, position_status_pb2, heating_status_pb2


def make_nextev_message(type, sub_type, command_name, message):
    # NextevMessage
    nextev_msg = nextev_msg_pb2.Message()
    nextev_msg.publish_ts = int(time.time() * 1000)
    nextev_msg.ttl = 1000
    nextev_msg.type = nextev_msg_pb2.Message.COMMAND_RESULT
    nextev_msg.sub_type = sub_type
    params1 = nextev_msg.params.add()
    params1.key = command_name
    params1.value = message.SerializeToString()
    nextev_message = nextev_msg.SerializeToString()
    logging.debug("-----nextevmsg----")
    logging.debug(nextev_msg.FromString(nextev_message))
    logging.debug("----{0}----".format(sub_type))
    message_payload = message.FromString(params1.value)
    logging.debug(message_payload)
    return nextev_message


def make_default_result_message(command):
    default_result_msg = generic_config_result_pb2.ConfigResult()
    default_result_msg.command_id = command['command_id']
    default_result_msg.status = generic_config_result_pb2.ConfigResult.SUCCESS
    default_result_msg.fail_reason.append("fail_reason")
    return default_result_msg


def make_generic_config_result_message(command):
    config_result_msg = generic_config_result_pb2.ConfigResult()
    config_result_msg.command_id = command['command_id']
    config_result_msg.status = generic_config_result_pb2.ConfigResult.SUCCESS
    config_result_msg.fail_reason.append("fail_reason")
    # config_result_msg.type = 'evm_config'
    config_result_msg.type = command['type']
    payload = json.loads(command['payload'])
    if 'values' not in payload:
        config_result_msg.values = "{\"evm_common\": {\"vehl_storage_period_ms\": 19,\"" \
                                   "normal_report_period_sec\": 10, \"normal_direct_report_period_sec\": 10, " \
                                   "\"alarm_report_period_ms\": 1000,     \"sample_period_ms\": 1,     \"" \
                                   "vehl_heartbeat_period_sec\": 5,\"login_delay_aft3_fails\": 60,\"vehl_resp_timeout\": 600,\"" \
                                   "platform_resp_timeout\": 600,\"in_sampling_inspection\": true }, \"direct_connect\": " \
                                   "{\"gb_platform_host\": \"225.54.0.10\",\"gb_platform_port\": 9999,\"" \
                                   "start_ts\": 1491793939,\"end_ts\": 1491893939 } }"
    else:
        # print("&&&&&&&&&&&&&:")
        # print(json.loads(command['payload'])['values'])
        config_result_msg.values = json.dumps(json.loads(command['payload'])['values'])
    return config_result_msg


def make_air_conditioner_cmdresult(command, status=0, fail_reason='fail_reason', hvac_status=None):
    air_conditioner_cmdresult = cmd_result_pb2.CmdResult()
    air_conditioner_cmdresult.command_id = command['command_id']
    if int(status) == 0:
        air_conditioner_cmdresult.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        air_conditioner_cmdresult.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        air_conditioner_cmdresult.status = cmd_result_pb2.CmdResult.RUNNING

    air_conditioner_cmdresult.fail_reason.append(fail_reason)

    air_conditioner_cmdresult.hvac_status.MergeFrom(gen_hvac_status(hvac_status))

    return air_conditioner_cmdresult


def make_air_purifier_cmdresult(command, status=0, fail_reason='fail_reason', hvac_status=None):
    air_purifier_cmdresult = cmd_result_pb2.CmdResult()
    air_purifier_cmdresult.command_id = command['command_id']
    if int(status) == 0:
        air_purifier_cmdresult.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        air_purifier_cmdresult.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        air_purifier_cmdresult.status = cmd_result_pb2.CmdResult.RUNNING

    air_purifier_cmdresult.fail_reason.append(fail_reason)
    if hvac_status:
        air_purifier_cmdresult.hvac_status.MergeFrom(gen_hvac_status(hvac_status))
    else:
        air_purifier_cmdresult.hvac_status.amb_temp_c = float(10)
        air_purifier_cmdresult.hvac_status.outside_temp_c = float(-5)
        air_purifier_cmdresult.hvac_status.air_con_on = True
        air_purifier_cmdresult.hvac_status.pm_2p5_cabin = 33
        air_purifier_cmdresult.hvac_status.pm_2p5_filter_active = int(command['switch'])
    return air_purifier_cmdresult


def make_doorlock_cmdresult(command, status=0, fail_reason='fail_reason', door_status=None):
    doorlock_cmdresult_msg = cmd_result_pb2.CmdResult()
    doorlock_cmdresult_msg.command_id = command['command_id']
    if int(status) == 0:
        doorlock_cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        doorlock_cmdresult_msg.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        doorlock_cmdresult_msg.status = cmd_result_pb2.CmdResult.RUNNING

    doorlock_cmdresult_msg.fail_reason.append(fail_reason)
    if door_status:
        doorlock_cmdresult_msg.door_status.MergeFrom(gen_door_status(door_status))
    else:
        if command['doorlock'] == b'1':
            doorlock_status = door_status_pb2.DoorStatus.LOCK_LOCKED
            doorajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
            vehicle_lock_status = door_status_pb2.DoorStatus.FULLY_LOCKED
        else:
            doorlock_status = door_status_pb2.DoorStatus.LOCK_UNLOCKED
            doorajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
            vehicle_lock_status = door_status_pb2.DoorStatus.NOT_FULLY_LOCKED
        doorlock_cmdresult_msg.door_status.door_locks.door_lock_frnt_le_sts = doorlock_status
        doorlock_cmdresult_msg.door_status.door_locks.door_lock_frnt_ri_sts = doorlock_status
        doorlock_cmdresult_msg.door_status.door_ajars.door_ajar_frnt_le_sts = doorajar_status
        doorlock_cmdresult_msg.door_status.door_ajars.door_ajar_frnt_ri_sts = doorajar_status
        doorlock_cmdresult_msg.door_status.door_ajars.door_ajar_re_le_sts = doorajar_status
        doorlock_cmdresult_msg.door_status.door_ajars.door_ajar_re_ri_sts = doorajar_status
        charge_port_status_1 = doorlock_cmdresult_msg.door_status.charge_port_status.add()
        charge_port_status_1.charge_port_sn = 0
        charge_port_status_1.ajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
        charge_port_status_2 = doorlock_cmdresult_msg.door_status.charge_port_status.add()
        charge_port_status_2.charge_port_sn = 1
        charge_port_status_2.ajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
        doorlock_cmdresult_msg.door_status.tailgate_status.ajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
        doorlock_cmdresult_msg.door_status.engine_hood_status.ajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
        doorlock_cmdresult_msg.door_status.vehicle_lock_status = vehicle_lock_status
    return doorlock_cmdresult_msg


def make_tailgate_cmdresult(command, status=0, fail_reason='fail_reason', door_status=None):
    doorlock_cmdresult_msg = cmd_result_pb2.CmdResult()
    doorlock_cmdresult_msg.command_id = command['command_id']
    doorlock_cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 0:
        doorlock_cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        doorlock_cmdresult_msg.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        doorlock_cmdresult_msg.status = cmd_result_pb2.CmdResult.RUNNING

    doorlock_cmdresult_msg.fail_reason.append(fail_reason)
    if door_status:
        doorlock_cmdresult_msg.door_status.MergeFrom(gen_door_status(door_status))
    else:
        doorlock_cmdresult_msg.door_status.door_locks.door_lock_frnt_le_sts = door_status_pb2.DoorStatus.LOCK_LOCKED
        doorlock_cmdresult_msg.door_status.door_locks.door_lock_frnt_ri_sts = door_status_pb2.DoorStatus.LOCK_LOCKED
        doorlock_cmdresult_msg.door_status.door_ajars.door_ajar_frnt_le_sts = door_status_pb2.DoorStatus.AJAR_CLOSED
        doorlock_cmdresult_msg.door_status.door_ajars.door_ajar_frnt_ri_sts = door_status_pb2.DoorStatus.AJAR_CLOSED
        doorlock_cmdresult_msg.door_status.door_ajars.door_ajar_re_le_sts = door_status_pb2.DoorStatus.AJAR_CLOSED
        doorlock_cmdresult_msg.door_status.door_ajars.door_ajar_re_ri_sts = door_status_pb2.DoorStatus.AJAR_CLOSED
        charge_port_status_1 = doorlock_cmdresult_msg.door_status.charge_port_status.add()
        charge_port_status_1.charge_port_sn = 0
        charge_port_status_1.ajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
        charge_port_status_2 = doorlock_cmdresult_msg.door_status.charge_port_status.add()
        charge_port_status_2.charge_port_sn = 1
        charge_port_status_2.ajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
        if command['tailgate'] == b'1':
            doorlock_cmdresult_msg.door_status.tailgate_status.ajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
        else:
            doorlock_cmdresult_msg.door_status.tailgate_status.ajar_status = door_status_pb2.DoorStatus.AJAR_OPENED
        doorlock_cmdresult_msg.door_status.engine_hood_status.ajar_status = door_status_pb2.DoorStatus.AJAR_CLOSED
        doorlock_cmdresult_msg.door_status.vehicle_lock_status = door_status_pb2.DoorStatus.FULLY_LOCKED
    return doorlock_cmdresult_msg


def make_windows_sunroof_cmdresult_message(command, status=0, fail_reason='fail_reason', window_status=None):
    windows_sunroof_cmdresult_msg = cmd_result_pb2.CmdResult()
    windows_sunroof_cmdresult_msg.command_id = command['command_id']
    if int(status) == 0:
        windows_sunroof_cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        windows_sunroof_cmdresult_msg.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        windows_sunroof_cmdresult_msg.status = cmd_result_pb2.CmdResult.RUNNING

    windows_sunroof_cmdresult_msg.fail_reason.append(fail_reason)
    if window_status:
        windows_sunroof_cmdresult_msg.window_status.MergeFrom(gen_window_status(window_status))
    else:
        windows_sunroof_cmdresult_msg.window_status.window_positions.win_frnt_le_posn = int(command['win_frnt_le_posn'])
        windows_sunroof_cmdresult_msg.window_status.window_positions.win_frnt_ri_posn = int(command['win_frnt_ri_posn'])
        windows_sunroof_cmdresult_msg.window_status.window_positions.win_re_le_posn = int(command['win_re_le_posn'])
        windows_sunroof_cmdresult_msg.window_status.window_positions.win_re_ri_posn = int(command['win_re_ri_posn'])
        windows_sunroof_cmdresult_msg.window_status.sun_roof_positions.sun_roof_posn = int(command['sun_roof_posn'])
        windows_sunroof_cmdresult_msg.window_status.sun_roof_positions.sun_roof_shade_posn = int(command.get("sun_roof_shade_posn", random.randint(0, 100)))
        windows_sunroof_cmdresult_msg.window_status.sun_roof_positions.sun_roof_posn_sts = int(command.get("sun_roof_posn_sts", 4))
    return windows_sunroof_cmdresult_msg


def make_findme_cmdresult(command, status=0, fail_reason='fail_reason'):
    findme_cmdresult_msg = cmd_result_pb2.CmdResult()
    findme_cmdresult_msg.command_id = command['command_id']
    if int(status) == 0:
        findme_cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        findme_cmdresult_msg.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        findme_cmdresult_msg.status = cmd_result_pb2.CmdResult.RUNNING

    findme_cmdresult_msg.fail_reason.append(fail_reason)
    return findme_cmdresult_msg


def make_ac_plan_cmdresult(command, status=0, fail_reason='fail_reason'):
    ac_plan_cmdresult_msg = cmd_result_pb2.CmdResult()
    ac_plan_cmdresult_msg.command_id = command['command_id']
    if int(status) == 0:
        ac_plan_cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        ac_plan_cmdresult_msg.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        ac_plan_cmdresult_msg.status = cmd_result_pb2.CmdResult.RUNNING

    ac_plan_cmdresult_msg.fail_reason.append(fail_reason)
    return ac_plan_cmdresult_msg


def make_hvh_heating_cmdresult(command, status=0, fail_reason='fail_reason', heating_status=None):
    hvh_heating_cmdresult_msg = cmd_result_pb2.CmdResult()
    hvh_heating_cmdresult_msg.command_id = command['command_id']
    if int(status) == 0:
        hvh_heating_cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        hvh_heating_cmdresult_msg.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        hvh_heating_cmdresult_msg.status = cmd_result_pb2.CmdResult.RUNNING

    hvh_heating_cmdresult_msg.fail_reason.append(fail_reason)
    if heating_status:
        hvh_heating_cmdresult_msg.heating_status.MergeFrom(gen_heating_status(heating_status))
    else:
        hvh_heating_cmdresult_msg.heating_status.seat_heat_frnt_le_sts = heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        hvh_heating_cmdresult_msg.heating_status.seat_heat_frnt_ri_sts = heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        hvh_heating_cmdresult_msg.heating_status.seat_heat_re_le_sts = heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        hvh_heating_cmdresult_msg.heating_status.seat_heat_re_ri_sts = heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        hvh_heating_cmdresult_msg.heating_status.steer_wheel_heat_sts = heating_status_pb2.HeatingStatus.STEER_WHEEL_HEAT_OFF
        hvh_heating_cmdresult_msg.heating_status.hv_batt_pre_sts = int(command['switch'])
        hvh_heating_cmdresult_msg.heating_status.seat_vent_frnt_le_sts = heating_status_pb2.HeatingStatus.SEAT_VENT_OFF
        hvh_heating_cmdresult_msg.heating_status.seat_vent_frnt_ri_sts = heating_status_pb2.HeatingStatus.SEAT_VENT_OFF

    return hvh_heating_cmdresult_msg


def make_seats_heating_cmdresult(command, status=0, fail_reason='fail_reason', heating_status=None):
    seats_heating_cmdresult_msg = cmd_result_pb2.CmdResult()
    seats_heating_cmdresult_msg.command_id = command['command_id']
    if int(status) == 0:
        seats_heating_cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        seats_heating_cmdresult_msg.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        seats_heating_cmdresult_msg.status = cmd_result_pb2.CmdResult.RUNNING

    seats_heating_cmdresult_msg.fail_reason.append(fail_reason)
    # {"re_le":"3","re_ri":"3","frnt_ri":"3","frnt_le":"3","max_duration":"20"}
    if heating_status:
        seats_heating_cmdresult_msg.heating_status.MergeFrom(gen_heating_status(heating_status))
    else:
        seats_heating_cmdresult_msg.heating_status.seat_heat_frnt_le_sts = int(command['frnt_le']) if int(command['frnt_le']) > 0 else 0
        seats_heating_cmdresult_msg.heating_status.seat_heat_frnt_ri_sts = int(command['frnt_ri']) if int(command['frnt_ri']) > 0 else 0
        seats_heating_cmdresult_msg.heating_status.seat_heat_re_le_sts = int(command['re_le']) if 're_le' in command else heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        seats_heating_cmdresult_msg.heating_status.seat_heat_re_ri_sts = int(command['re_ri']) if 're_ri' in command else heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        seats_heating_cmdresult_msg.heating_status.steer_wheel_heat_sts = heating_status_pb2.HeatingStatus.STEER_WHEEL_HEAT_OFF
        seats_heating_cmdresult_msg.heating_status.hv_batt_pre_sts = heating_status_pb2.HeatingStatus.BVBATT_HEAT_OFF
        seats_heating_cmdresult_msg.heating_status.seat_vent_frnt_le_sts = abs(int(command['frnt_le'])) if int(command['frnt_le']) < 0 else 0
        seats_heating_cmdresult_msg.heating_status.seat_vent_frnt_ri_sts = abs(int(command['frnt_ri'])) if int(command['frnt_ri']) < 0 else 0

    return seats_heating_cmdresult_msg


def make_steering_heating_cmdresult(command, status=0, fail_reason='fail_reason', heating_status=None):
    steering_heating_cmdresult_msg = cmd_result_pb2.CmdResult()
    steering_heating_cmdresult_msg.command_id = command['command_id']
    if int(status) == 0:
        steering_heating_cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    if int(status) == 1:
        steering_heating_cmdresult_msg.status = cmd_result_pb2.CmdResult.FAILURE
    if int(status) == 2:
        steering_heating_cmdresult_msg.status = cmd_result_pb2.CmdResult.RUNNING

    steering_heating_cmdresult_msg.fail_reason.append(fail_reason)
    if heating_status:
        steering_heating_cmdresult_msg.heating_status.MergeFrom(gen_heating_status(heating_status))
    else:
        steering_heating_cmdresult_msg.heating_status.seat_heat_frnt_le_sts = heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        steering_heating_cmdresult_msg.heating_status.seat_heat_frnt_ri_sts = heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        steering_heating_cmdresult_msg.heating_status.seat_heat_re_le_sts = heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        steering_heating_cmdresult_msg.heating_status.seat_heat_re_ri_sts = heating_status_pb2.HeatingStatus.SEAT_HEAT_OFF
        steering_heating_cmdresult_msg.heating_status.steer_wheel_heat_sts = int(command['switch'])
        steering_heating_cmdresult_msg.heating_status.hv_batt_pre_sts = heating_status_pb2.HeatingStatus.BVBATT_HEAT_OFF
        steering_heating_cmdresult_msg.heating_status.seat_vent_frnt_le_sts = heating_status_pb2.HeatingStatus.SEAT_VENT_OFF
        steering_heating_cmdresult_msg.heating_status.seat_vent_frnt_ri_sts = heating_status_pb2.HeatingStatus.SEAT_VENT_OFF

    return steering_heating_cmdresult_msg


# def make_instant_data_triger_cmdresult(command):
#     cmdresult_msg = cmd_result_pb2.CmdResult()
#     cmdresult_msg.command_id = command['command_id']
#     cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
#     cmdresult_msg.fail_reason.append("fail_reason")
#
#     # soc
#     cmdresult_msg.soc_status.soc = random.randint(0, 100)  # 电池剩余百分比
#     cmdresult_msg.soc_status.chrg_state = soc_status_pb2.SOCStatus.CHARGE_COMPLETE
#     cmdresult_msg.soc_status.btry_cap = random.randint(0, 1000)  # 电池容量，来自需求文档，范围0-1000
#     # cmdresult_msg.soc_status.estimate_chrg_time = random.randint(0, 1440)  # 预计充满电需要几分钟
#     cmdresult_msg.soc_status.hivolt_btry_curnt = random.randint(-20000,
#                                                                 20000)  # 高压电池的电流，0~20000代表-1000A~+1000A，0xFFFE异常(-2),0xFFFF无效(-1)
#     btry_paks1 = cmdresult_msg.soc_status.btry_paks.add()
#     btry_paks1.btry_pak_sn = 1  # 动力蓄电池包序号(SH)/ 可充电储能子系统号(GB)
#     btry_paks1.btry_pak_hist_temp = random.randint(-80, 170)  # 电池包最高温度值
#     btry_paks1.btry_pak_lwst_temp = random.randint(-80, 170)  # 电池包最低温度值
#     btry_paks1.btry_pak_voltage = random.randint(0, 600)  # 可充电储能装置电压
#     btry_paks1.btry_pak_curnt = random.randint(-2000, 2000)  # 可充电储能装置电流
#     btry_paks1.sin_btry_qunty_of_pak = 3  # 单体电池总数
#     btry_paks1.frm_start_btry_sn = 1  # 本帧起始电池序号
#     btry_paks1.sin_btry_qunty_of_frm = 3  # 本帧单体电池总数
#     btry_paks1.sin_btry_voltage.extend([1, 14, 11])  # 单体电池电压
#     btry_paks1.temp_prb_qunty = 3  # 可充电储能温度探针个数
#     btry_paks1.prb_temp_lst.extend([3, 1, 5])  # 可充电储能子系统各温度探针检测到的温度值列表
#
#     cmdresult_msg.soc_status.dump_enrgy = random.randint(0,
#                                                          1000)  # 剩余能量，0~9999表示0kmh~999.9kmh，0xFFFE异常(-2),0xFFFF无效(-1)
#     cmdresult_msg.soc_status.sin_btry_hist_temp = random.randint(-50,
#                                                                  200)  # 单体电池最高温度，0~165代表-40度~125度，0xFE缺省(-2),0xFF无效(-1)
#     cmdresult_msg.soc_status.sin_btry_lwst_temp = random.randint(-50,
#                                                                  200)  # 单体电池最高温度，0~165代表-40度~125度，0xFE缺省(-2),0xFF无效(-1)
#     cmdresult_msg.soc_status.btry_qual_actvtn = True  # 电池均衡激活，1代表均衡激活中，0代表无均衡
#     cmdresult_msg.soc_status.realtime_power_consumption = random.randint(0, 1000)
#     # cmdresult_msg.soc_status.charger_type = 1
#     cmdresult_msg.soc_status.remaining_range = random.randint(0,
#                                                               1000)  # 剩余里程, Remaining Travel Range in km, where e=n/10
#     cmdresult_msg.soc_status.chrg_final_soc = random.randint(0, 100)  # 充电截止soc
#
#     # position
#     cmdresult_msg.position_status.posng_valid_type = position_status_pb2.PositionStatus.VALID  # 定位状态
#     cmdresult_msg.position_status.longitude = round(random.uniform(-180, 180),
#                                                     6)  # 0~180，以度为单位的经度值乘以 10的6次方，+代表东经，-代表西经
#     cmdresult_msg.position_status.latitude = round(random.uniform(-180, 180),
#                                                    6)  # 0~180，以度为单位的纬度值乘以 10的6次方，+代表北纬，-代表南纬
#     cmdresult_msg.position_status.heading = random.randint(0, 359)  # SH车头方向，0~359，正北为0，顺势针
#     cmdresult_msg.position_status.altitude = random.randint(-1000, 5000)  # 海拔
#     cmdresult_msg.position_status.gps_speed = random.randint(0, 360)  # PRD
#
#     return cmdresult_msg


def get_msg_comm_success_command_id(command):
    cmdresult_msg = cmd_result_pb2.CmdResult()
    cmdresult_msg.command_id = command['command_id']
    cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    cmdresult_msg.fail_reason.append("fail_reason")
    return cmdresult_msg


# def make_rvs_exe_dids_cmdreuslt_message(command):
#     cmdresult_msg=get_msg_comm_success_command_id(command)
#     cmdresult_msg.

def make_syslog_cmdresult(command):
    cmdresult_msg = cmd_result_pb2.CmdResult()
    cmdresult_msg.command_id = command['command_id']
    cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    cmdresult_msg.fail_reason.append("fail_reason")

    cmdresult_msg.file_info.file_path.append("/test_path/logs/18_01_02.log")
    cmdresult_msg.file_info.file_path.append("/test_path/logs/18_01_03.log")

    return cmdresult_msg


def get_rvs_upload_syslog(command):
    cmdresult_msg = cmd_result_pb2.CmdResult()
    cmdresult_msg.command_id = command['command_id']
    cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    # cmdresult_msg.status = cmd_result_pb2.CmdResult.FAILURE
    cmdresult_msg.fail_reason.append("fail_reason")
    #
    cmdresult_msg.file_info.file_path.append(u'vehicle_logs/10005/sys_log/20180730/cda06f904ca04d0f95b600a0978304be/49C9DD434794E68BA26BBC221E5FA916_VMS é¡¹ç\u009bè¿\u009båº¦è¡¨20180727.xlsx')
    # cmdresult_msg.file_info.append('1234214123')
    # print(l)
    # ao.file_path = '123322'
    # cmdresult_msg.file_info.file_path = '12132q'
    # ll = "123456"
    # file_path1=""

    return cmdresult_msg


def get_rvs_upload_adclog(command, file_path=None):
    cmdresult_msg = cmd_result_pb2.CmdResult()
    cmdresult_msg.command_id = command['command_id']
    cmdresult_msg.status = cmd_result_pb2.CmdResult.SUCCESS
    cmdresult_msg.fail_reason.append("fail_reason")
    cmdresult_msg.file_info.file_path.append(file_path)
    return cmdresult_msg
