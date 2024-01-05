#!/usr/bin/env python
# coding=utf-8

"""
功能：上报全量实时事件
上报时机：
    1. occupant_statu值变化时，修复场景：停车前，副驾驶上有人，但是停车后副驾驶上人离开；
    2. veh_state值变化时，修复场景：停车后，进入到software update状态. 或由software update状态进入到停车状态
    3. 重新联网后，立即会发送一个全量实时事件
"""


import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import instant_status_msg_pb2
from nio_messages.data_unit import (gen_door_status, gen_soc_status, gen_charging_info, gen_position_status,
                                    gen_vehicle_status, gen_driving_data, gen_extremum_data, gen_bms_status, gen_can_msg,
                                    gen_hvac_status, gen_tyre_status, gen_occupant_status, gen_driving_motor, gen_can_signal,
                                    gen_light_status, gen_window_status, gen_battery_package_info, gen_signal_status, gen_alarm_signal,
                                    gen_body_status, gen_trip_status)
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, icc_id=None, request_id=None, outside_sample_ts=None,
                     sample_point=None, config_version=None, signallib_version=None, clear_fields=None):
    """
    实时数据事件上报
    :param clear_fields:
    :param signallib_version: for NT2, the current dbc version
    :param config_version: for NT2, the version of can_signal configure
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param icc_id: SIM卡ID
    :param outside_sample_ts:最外层时间戳
    :param request_id:远程下发查询命令的command_id
    :param sample_point: 采样点，注意！这里的sample_point不是一个list对象,而是一个dict对象
    :return: 包含实时数据事件上报消息的nextev_msg以及alarm_signal_update_obj本身
    """
    # InstantStatusResp
    instant_status_msg = instant_status_msg_pb2.InstantStatusResp()

    instant_status_msg.id = vin
    instant_status_msg.version = protobuf_v
    instant_status_msg.icc_id = icc_id if icc_id else ('ICC' + vin)
    instant_status_msg.request_id = request_id if request_id else time.strftime("%Y%m%d", time.localtime()) + '0001'
    instant_status_msg.config_version = config_version if config_version else 'ES8_0.6.1'
    instant_status_msg.signallib_version = signallib_version if signallib_version else 'BL00.06.01_DA_00'

    if sample_point is None:
        sample_point = {}

    if outside_sample_ts:
        instant_status_msg.sample_ts = outside_sample_ts

    instant_status_msg.sample_point.sample_ts = sample_point['sample_ts'] if ('sample_ts' in sample_point
                                                                              and sample_point['sample_ts']) else int(round(time.time() * 1000))

    instant_status_msg.sample_point.evm_flag = sample_point.get('evm_flag', True)

    # DoorStatus
    instant_status_msg.sample_point.door_status.MergeFrom(gen_door_status(sample_point.get('door_status', {})))

    # DrivingData
    instant_status_msg.sample_point.driving_data.MergeFrom(gen_driving_data(sample_point.get('driving_data', {})))

    # HVACStatus
    instant_status_msg.sample_point.hvac_status.MergeFrom(gen_hvac_status(sample_point.get('hvac_status', {})))

    # LightStatus
    instant_status_msg.sample_point.light_status.MergeFrom(gen_light_status(sample_point.get('light_status', {})))

    # OccupantStatus
    instant_status_msg.sample_point.occupant_status.MergeFrom(
        gen_occupant_status(sample_point.get('occupant_status', {})))

    # SignalStatus
    instant_status_msg.sample_point.signal_status.MergeFrom(gen_signal_status(sample_point.get('signal_status', {})))

    # SOCStatus
    instant_status_msg.sample_point.soc_status.MergeFrom(gen_soc_status(sample_point.get('soc_status', {})))

    # VehicleStatus
    instant_status_msg.sample_point.vehicle_status.MergeFrom(gen_vehicle_status(sample_point.get('vehicle_status', {})))

    # TyreStatus
    instant_status_msg.sample_point.tyre_status.MergeFrom(gen_tyre_status(sample_point.get('tyre_status', {})))

    # WindowStatus
    instant_status_msg.sample_point.window_status.MergeFrom(gen_window_status(sample_point.get('window_status', {})))

    # DrivingMotor
    instant_status_msg.sample_point.driving_motor.MergeFrom(gen_driving_motor(sample_point.get('driving_motor', {})))

    # ExtremumData
    instant_status_msg.sample_point.extremum_data.MergeFrom(gen_extremum_data(sample_point.get('extremum_data', {})))

    # PositionStatus
    instant_status_msg.sample_point.position_status.MergeFrom(
        gen_position_status(sample_point.get('position_status', {})))

    # BatteryPackageInfo
    instant_status_msg.sample_point.battery_package_info.MergeFrom(
        gen_battery_package_info(sample_point.get('battery_package_info', {}), vin))

    # BmsStatus
    instant_status_msg.sample_point.bms_status.MergeFrom(gen_bms_status(sample_point.get('bms_status', {})))

    # ChargingInfo
    instant_status_msg.sample_point.charging_info.MergeFrom(gen_charging_info(sample_point.get('charging_info', {})))

    # CanMsg
    instant_status_msg.sample_point.can_msg.MergeFrom(gen_can_msg(sample_point.get('can_msg', {})))

    # AlarmSignal
    instant_status_msg.sample_point.alarm_signal.MergeFrom(gen_alarm_signal(sample_point.get('alarm_signal', {})))

    # body_status
    instant_status_msg.sample_point.body_status.MergeFrom(gen_body_status(sample_point.get('body_status', {})))

    # trip_status
    instant_status_msg.sample_point.trip_status.MergeFrom(gen_trip_status(sample_point.get('trip_status', {})))

    # CanSignal
    instant_status_msg.sample_point.can_signal.MergeFrom(gen_can_signal(sample_point.get('can_signal', {})))

    if instant_status_msg.signallib_version < 'BL00.07.00_DA_01':
        eval('instant_status_msg.sample_point.ClearField("can_signal")')

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('instant_status_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('instant_status_resp',
                                    instant_status_msg,
                                    max(instant_status_msg.sample_point.sample_ts, instant_status_msg.sample_ts) + 2000,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    # instant_status_obj = pbjson.pb2dict(instant_status_msg)
    instant_status_obj = pbjson.parse_pb_string("InstantStatusResp", instant_status_msg.SerializeToString())

    return nextev_msg, instant_status_obj


def parse_message(message):
    event = instant_status_msg_pb2.InstantStatusResp()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status