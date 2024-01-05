#!/usr/bin/env python
# coding=utf-8

import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.data_unit import gen_light_status
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import light_change_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, light_status=None, publish_ts=None):
    """
    生成车灯状态变化事件的消息
    trigger：车灯状态改变时
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param light_status: 车灯状态数据，默认为None表示随机取值
    :return: 包含车灯状态变化事件的nextev_msg以及light_change_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # LightChangeEvent
    light_change_msg = light_change_msg_pb2.LightChangeEvent()
    light_change_msg.id = vin
    light_change_msg.version = protobuf_v
    light_change_msg.sample_ts = sample_ts

    # LightStatus
    light_change_msg.light_status.MergeFrom(gen_light_status(light_status))

    nextev_msg = gen_nextev_message('light_change_event',
                                    light_change_msg,
                                    publish_ts if publish_ts else light_change_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    light_change_obj = pbjson.pb2dict(light_change_msg)
    return nextev_msg, light_change_obj

def parse_message(message):
    event = light_change_msg_pb2.LightChangeEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status