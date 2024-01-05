#!/usr/bin/env python
# coding=utf-8

"""
:file: periodical_charge_update.py
:author: chunming.liu
:contact: Chunming.liu@nextev.com
:Date: Created on 2016/12/08
:Description:每条消息都会记录到cassandra的ev_monitoring_test.vehicle_history，最终上报给政府平台
"""
import time
import random
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import charge_update_msg_pb2
from nio_messages.data_unit import (gen_soc_status, gen_charging_info, gen_position_status, gen_vehicle_status,
                                    gen_driving_data, gen_extremum_data, gen_bms_status, gen_can_msg, gen_hvac_status,
                                    gen_tyre_status, gen_occupant_status, gen_driving_motor, gen_alarm_signal, gen_alarm_data,
                                    gen_body_status, gen_can_signal)
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, reissue=False, icc_id=None, charge_id=None,
                     around_alarm=None, sample_points=None, config_version=None, signallib_version=None,
                     clear_fields=None):
    charge_update_msg = charge_update_msg_pb2.ChargeUpdateMsg()

    charge_update_msg.id = vin
    charge_update_msg.version = protobuf_v
    charge_update_msg.reissue = reissue
    charge_update_msg.icc_id = icc_id if icc_id else ('ICC' + vin)
    charge_update_msg.charge_id = charge_id if charge_id else time.strftime("%Y%m%d", time.localtime()) + '00001'
    charge_update_msg.around_alarm = around_alarm if around_alarm else random.choice([0, 1])
    charge_update_msg.config_version = config_version if config_version else 'ES8_0.6.1'
    charge_update_msg.signallib_version = signallib_version if signallib_version else 'BL00.06.01_DA_00'

    if sample_points is None:
        sample_points = [{}]

    for i in range(len(sample_points)):
        sample_point = charge_update_msg.sample_points.add()
        sample_point.sample_ts = sample_points[i]['sample_ts'] if ('sample_ts' in sample_points[i]
                                                                   and sample_points[i]['sample_ts']) else int(round(time.time() * 1000))
        sample_point.evm_flag = sample_points[i].get('evm_flag', True)

        # PositionStatus
        sample_point.position_status.MergeFrom(gen_position_status(sample_points[i].get('position_status', {})))

        # VehicleStatus
        sample_point.vehicle_status.MergeFrom(gen_vehicle_status(sample_points[i].get('vehicle_status', {})))

        # OccupantStatus
        sample_point.occupant_status.MergeFrom(gen_occupant_status(sample_points[i].get('occupant_status', {})))

        # SOCStatus
        sample_point.soc_status.MergeFrom(gen_soc_status(sample_points[i].get('soc_status', {})))

        # DrivingData
        sample_point.driving_data.MergeFrom(gen_driving_data(sample_points[i].get('driving_data', {})))

        # DrivingMotor
        sample_point.driving_motor.MergeFrom(gen_driving_motor(sample_points[i].get('driving_motor', {})))

        # ExtremumData
        sample_point.extremum_data.MergeFrom(gen_extremum_data(sample_points[i].get('extremum_data', {})))

        # BmsStatus
        sample_point.bms_status.MergeFrom(gen_bms_status(sample_points[i].get('bms_status', {})))

        # ChargingInfo
        sample_point.charging_info.MergeFrom(gen_charging_info(sample_points[i].get('charging_info', {})))

        # CanMsg
        sample_point.can_msg.MergeFrom(gen_can_msg(sample_points[i].get('can_msg', {})))

        # HVACStatus
        sample_point.hvac_status.MergeFrom(gen_hvac_status(sample_points[i].get('hvac_status', {})))

        # TyreStatus
        sample_point.tyre_status.MergeFrom(gen_tyre_status(sample_points[i].get('tyre_status', {})))

        # AlarmSignal
        sample_point.alarm_signal.MergeFrom(gen_alarm_signal(sample_points[i].get('alarm_signal', {}), sample_point.sample_ts))

        # AlarmData
        sample_point.alarm_data.MergeFrom(gen_alarm_data(sample_points[i].get('alarm_data', {})))

        # body_status
        sample_point.body_status.MergeFrom(gen_body_status(sample_points[i].get('body_status', {})))

        # CanSignal
        sample_point.can_signal.MergeFrom(gen_can_signal(sample_points[i].get('can_signal', {})))

    if charge_update_msg.signallib_version < 'BL00.07.00_DA_01':
        eval('charge_update_msg.sample_points[0].ClearField("can_signal")')

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('charge_update_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('periodical_charge_update',
                                    charge_update_msg,
                                    charge_update_msg.sample_points[len(sample_points) - 1].sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    charge_update_obj = pbjson.parse_pb_string("ChargeUpdateMsg", charge_update_msg.SerializeToString())
    return nextev_msg, charge_update_obj


def parse_message(message):
    event = charge_update_msg_pb2.ChargeUpdateMsg()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status