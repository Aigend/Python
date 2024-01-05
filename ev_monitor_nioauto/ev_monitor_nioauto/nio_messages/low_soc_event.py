#!/usr/bin/env python
# coding=utf-8
"""
功能：处理cdc上报的低电量事件，状态存redis-SpecialStatus，更新成功之后转发push_event kafka
需求来源：需要处理的推送、提醒
上报时机：电量低于阈值触发
上报频率：实时通信
支持版本：
应用方：Hermes
showdoc：http://showdoc.nevint.com/index.php?s=/11&page_id=24395
"""
import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.data_unit import gen_low_soc_range
from nio_messages.pb2 import low_soc_event_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, low_soc_range=None):
    """
    生成车门状态变化事件的消息
    trigger：门状态改变时
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param LowSocRange: 车门状态，默认为None表示随机取值
    :return: 低电量事件
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # LowSocEvent
    low_soc_event_msg = low_soc_event_pb2.LowSocEvent()
    low_soc_event_msg.id = vin
    low_soc_event_msg.version = protobuf_v
    low_soc_event_msg.sample_ts = sample_ts

    # LowSocRange
    low_soc_event_msg.low_soc_range.MergeFrom(gen_low_soc_range(low_soc_range))

    nextev_msg = gen_nextev_message('low_soc_event',
                                    low_soc_event_msg,
                                    low_soc_event_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    low_soc_event_obj = pbjson.pb2dict(low_soc_event_msg)
    return nextev_msg, low_soc_event_obj


def parse_message(message):
    event = low_soc_event_pb2.LowSocEvent()
    proto = event.FromString(zlib.decompress(message))
    low_soc_status = protobuf_to_dict(proto)
    return low_soc_status
