#!/usr/bin/env python
# coding=utf-8


import time
import zlib
from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.data_unit import gen_window_status
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import window_status_change_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, window_status=None, clear_fields=None):
    """
    生成车窗状态改变事件的消息
    trigger：车窗状态改变时
    :param vin:车辆vin
    :param vid:车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v:protobuf版本
    :param sample_ts:消息采样时间
    :param window_status:车窗状态数据，默认为None表示随机取值
    :return:包含车窗状态变化事件的nextev_msg以及light_change_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # WindowStatusChangeEvent
    window_status_change_msg = window_status_change_msg_pb2.WindowStatusChangeEvent()
    window_status_change_msg.id = vin
    window_status_change_msg.version = protobuf_v
    window_status_change_msg.sample_ts = sample_ts

    # Window status
    window_status_change_msg.window_status.MergeFrom(gen_window_status(window_status))

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('window_status_change_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('window_change_event',
                                    window_status_change_msg,
                                    window_status_change_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    window_status_change_obj = pbjson.parse_pb_string("WindowStatusChangeEvent", window_status_change_msg.SerializeToString())

    return nextev_msg, window_status_change_obj

def parse_message(message):
    event = window_status_change_msg_pb2.WindowStatusChangeEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status