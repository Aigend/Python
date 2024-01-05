#!/usr/bin/env python
# coding=utf-8

"""
功能：[TSP] should store them for inquire
需求来源：[CGW] should trigger the following data record when one of the following events happened
上报时机：条件较多且偏底层，详细见下方相关jira
上报频率：单次
支持版本：BL310之后
应用方：VMS等监控方
相关jira：https://jira.nioint.com/browse/CVS-13938
"""

import time
import zlib
import random

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.data_unit import gen_can_msg
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import nbs_abort_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, dbc_type=None, can_msg=None):
    """
    :param dbc_type:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 上报的时间戳
    :param can_msg: can_msg数据，默认为None表示随机取值
    :return: 包含小电池充电消息的nextev_msg以及lv_batt_charging_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    if dbc_type is None:
        dbc_type = random.choice(["es8_7.5.10", "ES8_7.5.11"])

    # NBSAbortEvent
    nbs_abort_msg = nbs_abort_msg_pb2.NBSAbortEvent()
    nbs_abort_msg.id = vin
    nbs_abort_msg.version = protobuf_v
    nbs_abort_msg.sample_ts = sample_ts
    nbs_abort_msg.dbc_type = dbc_type

    # CanMsg
    if can_msg is None:
        for i in range(3):
            can_data = nbs_abort_msg.can_msg.add()
            can_data.MergeFrom(gen_can_msg(can_msg))
    else:
        for it in can_msg:
            can_data = nbs_abort_msg.can_msg.add()
            can_data.MergeFrom(it)

    nextev_msg = gen_nextev_message('nbs_abort_event',
                                    nbs_abort_msg,
                                    nbs_abort_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    nbs_abort_obj = pbjson.pb2dict(nbs_abort_msg)

    return nextev_msg, nbs_abort_obj


def parse_message(message):
    event = nbs_abort_msg_pb2.NBSAbortEvent()
    proto = event.FromString(zlib.decompress(message))
    nbs_abort_msg = protobuf_to_dict(proto)
    return nbs_abort_msg
