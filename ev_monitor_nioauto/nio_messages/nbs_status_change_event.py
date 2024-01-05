#!/usr/bin/env python
# coding=utf-8

"""
功能：用于与TSP进行基于IMX6处理器的NBS功能的通信。
需求来源：近场召唤功能
上报时机：NBS状态改变时
上报频率：实时通信
支持版本：BL250之后
应用方：APP
设计文档：https://confluence.nevint.com/display/DigitalArchitecture/Nearby+Summon
各字段含义：https://git.nevint.com/greatwall/cvs_proto/uploads/4bd25258e70825b8e49793f5692e5cb0/NBS_related_Signal_Request_20191107.xlsx
"""

import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.data_unit import gen_nbs_status
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import nbs_status_change_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, nbs_status=None, clear_fields=None):
    """
    生成NBS状态变化事件的消息
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param nbs_status: NBS状态数据，默认为None表示随机取值
    :return: 包含NBS状态变化事件的nextev_msg以及nbs_status_change_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # NBSStatusChangeEvent
    nbs_status_change_msg = nbs_status_change_msg_pb2.NBSStatusChangeEvent()
    nbs_status_change_msg.id = vin
    nbs_status_change_msg.version = protobuf_v
    nbs_status_change_msg.sample_ts = sample_ts

    # NBS status
    nbs_status_change_msg.nbs_status.MergeFrom(gen_nbs_status(nbs_status))

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('nbs_status_change_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('nbs_status_change_event',
                                    nbs_status_change_msg,
                                    nbs_status_change_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    # nbs_status_change_obj = pbjson.parse_pb_string("NBSStatusChangeEvent", nbs_status_change_msg.SerializeToString())
    nbs_status_change_obj = pbjson.pb2dict(nbs_status_change_msg)

    return nextev_msg, nbs_status_change_obj


def parse_message(message):
    event = nbs_status_change_msg_pb2.NBSStatusChangeEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status