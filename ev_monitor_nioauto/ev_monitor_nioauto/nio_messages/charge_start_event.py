#!/usr/bin/env python
# coding=utf-8


import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import charge_start_msg_pb2

from nio_messages.data_unit import gen_soc_status, gen_charging_info, gen_position_status, gen_vehicle_status, \
    gen_battery_package_info
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, charge_id=None, sample_ts=None, icc_id=None, soc_status=None,
                     charging_info=None, position_status=None, vehicle_status=None, battery_package_info=None, clear_fields=None):
    """
    生成充电开始事件
    trigger：充电开始时
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param charge_id: 充电ID
    :param sample_ts: 上报的时间戳
    :param icc_id: SIM卡ID
    :param soc_status: 电池状态数据，默认为None表示随机取值
    :param charging_info: 充电状态数据，默认为None表示随机取值
    :param position_status: 位置状态数据，默认为None表示随机取值
    :param vehicle_status: 车辆状态数据，默认为None表示随机取值
    :param battery_package_info:电池包信息
    :return: 包含充电开始消息的nextev_msg以及charge_start_msg本身
    """
    # ChargeStartEvent
    if charge_id is None:
        charge_id = time.strftime("%Y%m%d", time.localtime()) + '0001'
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))
    if icc_id is None:
        icc_id = 'ICC' + vin

    charge_start_msg = charge_start_msg_pb2.ChargeStartEvent()
    charge_start_msg.id = vin
    charge_start_msg.version = protobuf_v
    charge_start_msg.icc_id = icc_id
    charge_start_msg.sample_ts = sample_ts
    charge_start_msg.charge_id = charge_id

    # SOCStatus
    charge_start_msg.soc_status.MergeFrom(gen_soc_status(soc_status))
    # BatteryPackageInfo
    charge_start_msg.battery_package_info.MergeFrom(gen_battery_package_info(battery_package_info, vin))
    # ChargingInfo
    charge_start_msg.charging_info.MergeFrom(gen_charging_info(charging_info))
    # PositionStatus
    charge_start_msg.position_status.MergeFrom(gen_position_status(position_status))
    # VehicleStatus
    charge_start_msg.vehicle_status.MergeFrom(gen_vehicle_status(vehicle_status))

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('charge_start_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('charge_start_event',
                                    charge_start_msg,
                                    charge_start_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    # charge_start_obj = pbjson.pb2dict(charge_start_msg)
    charge_start_obj = pbjson.parse_pb_string("ChargeStartEvent", charge_start_msg.SerializeToString())
    return nextev_msg, charge_start_obj


def parse_message(message):
    event = charge_start_msg_pb2.ChargeStartEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status