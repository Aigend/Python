#!/usr/bin/env python
# coding=utf-8

import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.data_unit import gen_door_status
from nio_messages.pb2 import door_status_change_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, door_status=None, clear_fields=None):
    """
    生成车门状态变化事件的消息
    trigger：门状态改变时
    :param clear_fields:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param door_status: 车门状态，默认为None表示随机取值
    :return: 包含车门状态变化事件的nextev_msg以及door_status_change_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # DoorStatusChangeEvent
    door_status_change_msg = door_status_change_msg_pb2.DoorStatusChangeEvent()
    door_status_change_msg.id = vin
    door_status_change_msg.version = protobuf_v
    door_status_change_msg.sample_ts = sample_ts

    # DoorStatus
    door_status_change_msg.door_status.MergeFrom(gen_door_status(door_status))

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('door_status_change_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('door_change_event',
                                    door_status_change_msg,
                                    door_status_change_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    door_status_change_obj = pbjson.parse_pb_string('DoorStatusChangeEvent', door_status_change_msg.SerializeToString())
    return nextev_msg, door_status_change_obj


def parse_message(message):
    event = door_status_change_msg_pb2.DoorStatusChangeEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status