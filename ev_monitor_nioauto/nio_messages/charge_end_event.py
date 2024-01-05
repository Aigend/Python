#!/usr/bin/env python
# coding=utf-8

import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import charge_end_msg_pb2
from nio_messages.data_unit import gen_soc_status, gen_charging_info, gen_position_status, gen_vehicle_status
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, charge_id=None, sample_ts=None, soc_status=None, charging_info=None,
                     position_status=None, vehicle_status=None, clear_fields=None):
    """
    生成充电结束事件
    trigger：充电结束时
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param charge_id: 充电ID
    :param sample_ts: 上报的时间戳
    :param soc_status: 电池状态数据，默认为None表示随机取值
    :param charging_info: 充电状态数据，默认为None表示随机取值
    :param position_status: 位置状态数据，默认为None表示随机取值
    :param vehicle_status: 车辆状态数据，默认为None表示随机取值
    :return: 包含充电结束消息的nextev_msg以及charge_end_msg本身
    """
    # ChargeEndEvent
    if charge_id is None:
        charge_id = time.strftime("%Y%m%d", time.localtime()) + '0001'
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    charge_end_msg = charge_end_msg_pb2.ChargeEndEvent()
    charge_end_msg.id = vin
    charge_end_msg.version = protobuf_v
    charge_end_msg.charge_id = charge_id
    charge_end_msg.sample_ts = sample_ts

    # SOCStatus
    charge_end_msg.soc_status.MergeFrom(gen_soc_status(soc_status))

    # ChargingInfo
    charge_end_msg.charging_info.MergeFrom(gen_charging_info(charging_info))
    # PositionStatus
    charge_end_msg.position_status.MergeFrom(gen_position_status(position_status))
    # VehicleStatus
    charge_end_msg.vehicle_status.MergeFrom(gen_vehicle_status(vehicle_status))

    # exclude
    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('charge_end_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('charge_end_event',
                                    charge_end_msg,
                                    charge_end_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    # charge_end_obj = pbjson.pb2dict(charge_end_msg)

    charge_end_obj = pbjson.parse_pb_string("ChargeEndEvent", charge_end_msg.SerializeToString())

    return nextev_msg, charge_end_obj

def parse_message(message):
    event = charge_end_msg_pb2.ChargeEndEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status

