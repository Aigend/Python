#!/usr/bin/env python
# coding=utf-8

"""
功能：APP增加座椅/方向盘/高压电池预加热功能。
需求来源：EE
上报时机：加热状态改变时
支持版本：BL250之后。【Before】只能在车上实现开启加热【After】能够远程控制立即加热
         BL270之后，增加了座椅通风
应用方：APP
FDS：https://confluence.nevint.com/display/DigitalArchitecture/Remote+Cabin+Preconditioning%3A+ES6
相关jira：【remote immediate seats heating control】https://jira.nevint.com/browse/EDMS-13528
         【HVH preheating function OnOff at APP】https://jira.nevint.com/browse/EDMS-22661
         【remote immediate steering wheel heating】https://jira.nevint.com/browse/EDMS-13527
"""

import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.data_unit import gen_heating_status
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import heating_status_change_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, heating_status=None, clear_fields=None):
    """
    生成加热状态变化事件的消息
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 上报的时间戳
    :param heating_status: 加热状态数据，默认为None表示随机取值
    :return: 包含预加热状态变化事件的nextev_msg以及heating_status_change_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # HeatingStatusChangeEvent
    heating_status_change_msg = heating_status_change_msg_pb2.HeatingStatusChangeEvent()
    heating_status_change_msg.id = vin
    heating_status_change_msg.version = protobuf_v
    heating_status_change_msg.sample_ts = sample_ts

    # Heating status
    heating_status_change_msg.heating_status.MergeFrom(gen_heating_status(heating_status))

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('heating_status_change_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('heating_status_change_event',
                                    heating_status_change_msg,
                                    heating_status_change_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    # heating_status_change_obj = pbjson.parse_pb_string("HeatingStatusChangeEvent", heating_status_change_msg.SerializeToString())
    heating_status_change_obj = pbjson.pb2dict(heating_status_change_msg)

    return nextev_msg, heating_status_change_obj

def parse_message(message):
    event = heating_status_change_msg_pb2.HeatingStatusChangeEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status