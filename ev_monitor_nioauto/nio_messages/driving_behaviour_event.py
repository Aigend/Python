#!/usr/bin/env python
# coding=utf-8

import time
import random
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import driving_behaviour_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, driving_behaviour_status=None):
    """
    生成驾驶行为消息
    trigger：关键驾驶行为发生或恢复正常时
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param driving_behaviour_status: 列表形式，驾驶行为数据，默认为None表示随机取值
    :return: 包含驾驶行为事件的nextev_msg以及driving_behaviour_msg本身
    """
    # DrivingBehaviourEvent
    driving_behaviour_msg = driving_behaviour_msg_pb2.DrivingBehaviourEvent()
    driving_behaviour_msg.id = vin
    driving_behaviour_msg.version = protobuf_v
    driving_behaviour_msg.sample_ts = sample_ts if sample_ts else (round(time.time() * 1000))
    # Behavior
    if driving_behaviour_status is None:
        driving_behaviour_msg.behaviour.extend(random.sample([0, 1, 2], 1))
    else:
        driving_behaviour_msg.behaviour.extend(driving_behaviour_status)
    nextev_msg = gen_nextev_message('driving_behaviour_event',
                                    driving_behaviour_msg,
                                    driving_behaviour_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    driving_behaviour_obj = pbjson.pb2dict(driving_behaviour_msg)
    return nextev_msg, driving_behaviour_obj

def parse_message(message):
    event = driving_behaviour_msg_pb2.DrivingBehaviourEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status