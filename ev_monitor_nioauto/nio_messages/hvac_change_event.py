#!/usr/bin/env python
# coding=utf-8


import time
import zlib

from nio_messages import pb2

from nio_messages import pbjson
from nio_messages.data_unit import gen_hvac_status
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import hvac_status_change_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, hvac_status=None):
    """
    生成空调状态变化事件的消息
    trigger：SVT事件发生时
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param hvac_status: 空调状态数据，默认为None表示随机取值
    :return: 包含空调状态事件变化消息的nextev_msg以及charge_end_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # HVACStatusChangeEvent
    hvac_status_change_msg = hvac_status_change_msg_pb2.HVACStatusChangeEvent()
    hvac_status_change_msg.id = vin
    hvac_status_change_msg.version = protobuf_v
    hvac_status_change_msg.sample_ts = sample_ts

    # HVACStatus
    hvac_status_change_msg.hvac_status.MergeFrom(gen_hvac_status(hvac_status))
    nextev_msg = gen_nextev_message('hvac_change_event',
                                    hvac_status_change_msg,
                                    hvac_status_change_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    hvac_status_change_obj = pbjson.pb2dict(hvac_status_change_msg)
    return nextev_msg, hvac_status_change_obj

def parse_message(message):
    event = hvac_status_change_msg_pb2.HVACStatusChangeEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status