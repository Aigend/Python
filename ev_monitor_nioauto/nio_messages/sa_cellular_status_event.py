""" 
功能：SA蜂窝网络变化事件
上报时机：SA cellular connection Status changed. BGW received the message update from SA.
上报频率：单次
支持版本：NT2
应用方：
相关jira：https://jira.nioint.com/browse/CVS-16324
"""
import random
import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import sa_cellular_status_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict
from nio_messages.data_unit import gen_sa_cellular_status


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, sa_cellular_status=None):
    """
    :param sa_cellular_status:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :return:
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # MaxSOCChangeEvent
    sa_cellular_status_msg = sa_cellular_status_msg_pb2.SACellularStatusEvent()
    sa_cellular_status_msg.id = vin
    sa_cellular_status_msg.version = protobuf_v
    sa_cellular_status_msg.sample_ts = sample_ts

    sa_cellular_status_msg.sa_cellular_status.MergeFrom(gen_sa_cellular_status(sa_cellular_status))

    nextev_msg = gen_nextev_message('sa_cellular_status_event',
                                    sa_cellular_status_msg,
                                    sa_cellular_status_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    trip_end_event_obj = pbjson.pb2dict(sa_cellular_status_msg)
    return nextev_msg, trip_end_event_obj


def parse_message(message):
    event = sa_cellular_status_msg_pb2.SACellularStatusEvent()
    proto = event.FromString(zlib.decompress(message))
    sa_cellular_status_msg = protobuf_to_dict(proto)
    return sa_cellular_status_msg
