#!/usr/bin/env python
# coding=utf-8

"""
Description: 如果上次上报的故障在本次没有报，那就认为该信号引起的故障已经结束了。status_wti_alarm将上次的故障信号的alarm_level标记为0

流程：
    车机推送告警信号
        |
        V
    Slytherin服务落库
        |
        |--->如果const_wti表 app_display=1 -->APP轮训调用remote_vehicle服务接口(/api/1/vehicle/{vid}/alarm_for_app)显示告警
        |
        |--->如果const_wti表 app_push_enabled=1-->推送kafka(swc-cvs-tsp-{env}-80001-wti_alarm)--->hermes---调用接口---->APP Msg（api/1/in/app_msg/common）--->APP Message api(nofify)--->APP
        |
        |--->推送kafka(swc-cvs-tsp-{env}-80001-wti_can_signal)-->电池告警系统等下游服务

WTI时序图： https://confluence.nioint.com/pages/viewpage.action?pageId=304201644

接口：
    For APP: /api/1/vehicle/{vehicle_id}/alarm_for_app http://showdoc.nevint.com/index.php?s=/11&page_id=6195
    For VMS: /api/1/in/vehicle/vms/signal_to_wti http://showdoc.nevint.com/index.php?s=/11&page_id=8715

"""
import time
import zlib
import logging
from nio_messages.pb2 import alarm_signal_update_msg_pb2
from nio_messages import pb2
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.data_unit import (gen_soc_status, gen_position_status, gen_vehicle_status, gen_can_signal,
                                    gen_driving_data, gen_extremum_data, gen_bms_status, gen_can_msg, gen_hvac_status,
                                    gen_tyre_status, gen_occupant_status, gen_driving_motor, gen_alarm_signal)
from nio_messages import pbjson
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, alarm_signal=None, sample_points=None,
                     config_version=None, signallib_version=None, clear_fields=None):
    """
    随机上报数据或者上报指定数据
    trigger：告警相关CAN信号值发生改变时
    :param signallib_version: for NT2, the current dbc version
    :param config_version: for NT2, the version of can_signal configure
    :param clear_fields:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param alarm_signal: 报警消息数据
    :param sample_points: 采样点，注意！这里的sample_point不是一个list对象,而是一个dict对象
    :return: 包含报警信号消息的nextev_msg以及alarm_signal_update_obj本身
    """
    alarm_signal_update_msg = alarm_signal_update_msg_pb2.AlarmSignalUpdateEvent()
    alarm_signal_update_msg.id = vin
    alarm_signal_update_msg.version = protobuf_v
    alarm_signal_update_msg.sample_ts = sample_ts if sample_ts else (round(time.time() * 1000))
    alarm_signal_update_msg.config_version = config_version if config_version else 'ES8_0.6.1'
    alarm_signal_update_msg.signallib_version = signallib_version if signallib_version else 'BL00.06.01_DA_00'

    # AlarmSignal
    alarm_signal_update_msg.alarm_signal.MergeFrom(gen_alarm_signal(alarm_signal, alarm_signal_update_msg.sample_ts))

    if sample_points is None:
        sample_points = {}

    # PositionStatus
    alarm_signal_update_msg.sample_points.position_status.MergeFrom(gen_position_status(sample_points.get('position_status', {})))

    # VehicleStatus
    alarm_signal_update_msg.sample_points.vehicle_status.MergeFrom(gen_vehicle_status(sample_points.get('vehicle_status', {})))

    # OccupantStatus
    alarm_signal_update_msg.sample_points.occupant_status.MergeFrom(gen_occupant_status(sample_points.get('occupant_status', {})))

    # SOCStatus
    alarm_signal_update_msg.sample_points.soc_status.MergeFrom(gen_soc_status(sample_points.get('soc_status', {})))

    # DrivingData
    alarm_signal_update_msg.sample_points.driving_data.MergeFrom(gen_driving_data(sample_points.get('driving_data', {})))

    # DrivingMotor
    alarm_signal_update_msg.sample_points.driving_motor.MergeFrom(gen_driving_motor(sample_points.get('driving_motor', {})))

    # ExtremumData
    alarm_signal_update_msg.sample_points.extremum_data.MergeFrom(gen_extremum_data(sample_points.get('extremum_data', {})))

    # BmsStatus
    alarm_signal_update_msg.sample_points.bms_status.MergeFrom(gen_bms_status(sample_points.get('bms_status', {})))

    # CanMsg
    alarm_signal_update_msg.sample_points.can_msg.MergeFrom(gen_can_msg(sample_points.get('can_msg', {})))

    # HVACStatus
    alarm_signal_update_msg.sample_points.hvac_status.MergeFrom(gen_hvac_status(sample_points.get('hvac_status', {})))

    # TyreStatus
    alarm_signal_update_msg.sample_points.tyre_status.MergeFrom(gen_tyre_status(sample_points.get('tyre_status', {})))

    # CanSignal
    alarm_signal_update_msg.sample_points.can_signal.MergeFrom(gen_can_signal(sample_points.get('can_signal', {})))

    if alarm_signal_update_msg.signallib_version < 'BL00.07.00_DA_01':
        eval('alarm_signal_update_msg.sample_points.ClearField("can_signal")')

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('alarm_signal_update_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('alarm_signal_update_event',
                                    alarm_signal_update_msg,
                                    alarm_signal_update_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    alarm_signal_update_obj = pbjson.parse_pb_string("AlarmSignalUpdateEvent", alarm_signal_update_msg.SerializeToString())

    return nextev_msg, alarm_signal_update_obj


def parse_message(message):
    event = alarm_signal_update_msg_pb2.AlarmSignalUpdateEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status
