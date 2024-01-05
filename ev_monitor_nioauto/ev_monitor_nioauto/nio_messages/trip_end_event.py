#!/usr/bin/env python
# coding=utf-8
"""
功能：上报当前单次行程中的相关行程数据
上报时机：1 vehicle status is "Parked" and fully locked
        2 Power swap mode is ON and gear position is parking
        3 charging in procesing
        4 vehicle in software update
        5 vehicle status from "Driver Present" to "Park" after 10min
上报频率：单次
支持版本：BL300之后
应用方：行程相关应用
"""
import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.data_unit import gen_trip_status, gen_position_status, gen_soc_status, gen_vehicle_status
from nio_messages.pb2 import trip_end_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, trip_status=None, position_status=None, soc_status=None, vehicle_status=None, clear_fields=None):
    """
    生成车门状态变化事件的消息
    trigger：车辆处于停泊状态并完全锁车
    :param vehicle_status:
    :param soc_status:
    :param position_status:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param trip_status: 旅程状态，默认为None表示随机取值
    :return: 低电量事件
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # TripEndEvent
    trip_end_msg = trip_end_msg_pb2.TripEndEvent()
    trip_end_msg.id = vin
    trip_end_msg.version = protobuf_v
    trip_end_msg.sample_ts = sample_ts

    trip_end_msg.trip_status.MergeFrom(gen_trip_status(trip_status))
    trip_end_msg.position_status.MergeFrom(gen_position_status(position_status))
    trip_end_msg.soc_status.MergeFrom(gen_soc_status(soc_status))
    trip_end_msg.vehicle_status.MergeFrom(gen_vehicle_status(vehicle_status))

    # exclude
    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('trip_end_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('trip_end_event',
                                    trip_end_msg,
                                    trip_end_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    trip_end_event_obj = pbjson.pb2dict(trip_end_msg)
    return nextev_msg, trip_end_event_obj


def parse_message(message):
    event = trip_end_msg_pb2.TripEndEvent()
    proto = event.FromString(zlib.decompress(message))
    trip_status = protobuf_to_dict(proto)
    return trip_status
