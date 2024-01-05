#!/usr/bin/env python
# coding=utf-8


import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.data_unit import gen_soc_status, gen_position_status, gen_vehicle_status
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import journey_end_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, journey_id=None, sample_ts=None, soc_status=None, position_status=None,
                     vehicle_status=None, clear_fields=None):
    """
    生成行程结束消息
    trigger：行程结束时
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param icc_id: SIM卡ID
    :param journey_id: 行程ID
    :param sample_ts: 消息采样时间
    :param soc_status: 电池状态数据，默认为None表示随机取值
    :param position_status: 位置状态数据，默认为None表示随机取值
    :param vehicle_status: 车辆状态数据，默认为None表示随机取值
    :return: 包含行程结束事件的nextev_msg以及journey_end_msg本身
    """
    if journey_id is None:
        journey_id = time.strftime("%Y%m%d", time.localtime()) + '0001'
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # JourneyEndEvent
    journey_end_msg = journey_end_msg_pb2.JourneyEndEvent()
    journey_end_msg.id = vin
    journey_end_msg.version = protobuf_v
    journey_end_msg.journey_id = journey_id
    journey_end_msg.sample_ts = sample_ts

    # SOCStatus
    journey_end_msg.soc_status.MergeFrom(gen_soc_status(soc_status))
    # PositionStatus
    journey_end_msg.position_status.MergeFrom(gen_position_status(position_status))
    # VehicleStatus
    journey_end_msg.vehicle_status.MergeFrom(gen_vehicle_status(vehicle_status))

    # exclude
    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('journey_end_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('journey_end_event',
                                    journey_end_msg,
                                    journey_end_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    # journey_end_obj = pbjson.pb2dict(journey_end_msg)
    journey_end_obj = pbjson.parse_pb_string("JourneyEndEvent", journey_end_msg.SerializeToString())
    return nextev_msg, journey_end_obj

def parse_message(message):
    event = journey_end_msg_pb2.JourneyEndEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status