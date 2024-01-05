#!/usr/bin/env python
# coding=utf-8
"""
功能：修复了给tsp回复命令结果时没有上报当前命令执行后socstatus状态数据的问题
上报时机：如果tsp下发的命令是用户设置的max soc，那么socstatus的proto字段的max soc就要被set然后上报。如果是下发的加锁命令，那么socstatus的proto字段中的lock soc以及lock soc status就要被set然后上报。
上报频率：单次
支持版本：BL310之后
应用方：行程相关应用
相关jira：https://jira.nioint.com/browse/DSYSL-9003
"""

import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.data_unit import gen_soc_status
from nio_messages.pb2 import max_soc_change_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, soc_status=None):
    """
    生成车门状态变化事件的消息
    trigger：车辆处于停泊状态并完全锁车
    :param soc_status:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :return:
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # MaxSOCChangeEvent
    max_soc_change_msg = max_soc_change_msg_pb2.MaxSOCChangeEvent()
    max_soc_change_msg.id = vin
    max_soc_change_msg.version = protobuf_v
    max_soc_change_msg.sample_ts = sample_ts

    max_soc_change_msg.soc_status.MergeFrom(gen_soc_status(soc_status))

    nextev_msg = gen_nextev_message('max_soc_change_event',
                                    max_soc_change_msg,
                                    max_soc_change_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    trip_end_event_obj = pbjson.pb2dict(max_soc_change_msg)
    return nextev_msg, trip_end_event_obj


def parse_message(message):
    event = max_soc_change_msg_pb2.MaxSOCChangeEvent()
    proto = event.FromString(zlib.decompress(message))
    max_soc_change_msg = protobuf_to_dict(proto)
    return max_soc_change_msg
