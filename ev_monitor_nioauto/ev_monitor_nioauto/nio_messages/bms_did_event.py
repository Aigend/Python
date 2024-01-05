#!/usr/bin/env python
# coding=utf-8

"""
功能：TSP存储车端的DID数据，并给SO提供接口查阅。
需求来源：预测小电池寿命，避免驾驶故障/FOTA失败等
上报时机：CGW计时满14天，且车辆从未充电状态变为充电时，详情见需求文档
上报频率：14天
支持版本：BL250之后
应用方：SO
需求文档：https://confluence.nevint.com/display/DigitalArchitecture/BMS+DID+collection+and+upload
由这个FOTA confluence看到，初衷可能是为了解决FOTA在BMS刷新和换电模式的矛盾：https://confluence.nevint.com/display/VSF/20170410+FOTA+BMS+strategy+session+2
"""

import time
import random
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.did import DIDS
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import bms_dids_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None,
                     did_info=None, clear_fields=None):
    """
    生成BMS_DID事件
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param did_info: BMS_DID信息
    :return: 包含BMS_DID消息的nextev_msg以及bms_did_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # BMSDidEvent
    bms_did_msg = bms_dids_msg_pb2.BMSDIDEvent()
    bms_did_msg.id = vin
    bms_did_msg.version = protobuf_v
    bms_did_msg.sample_ts = sample_ts

    # did_info
    if not did_info:
        did_info = random.sample(DIDS, 1)[0]['dids']
    for itme in did_info:
        did_info = bms_did_msg.did_info.add()
        did_info.id = itme['id']
        did_info.value = itme['value']

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('bms_did_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('bms_did_event',
                                    bms_did_msg,
                                    bms_did_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    # bms_did_obj = pbjson.parse_pb_string("BMSDidEvent", bms_did_msg.SerializeToString())
    bms_did_obj = pbjson.pb2dict(bms_did_msg)

    return nextev_msg, bms_did_obj


def parse_message(message):
    event = bms_dids_msg_pb2.BMSDIDEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status