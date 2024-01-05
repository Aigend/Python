""" 
功能：SA备用电池健康报警事件
上报时机：SA Bacup battery Status changed. BGW received the message update from SA.
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
from nio_messages.pb2 import sa_batt_health_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, sa_batt_health=None):
    """
    :param sa_batt_health: 
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :return:
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    sa_batt_health_msg = sa_batt_health_msg_pb2.SABattHealthEvent()
    sa_batt_health_msg.id = vin
    sa_batt_health_msg.version = protobuf_v
    sa_batt_health_msg.sample_ts = sample_ts

    sa_batt_health_msg.sa_batt_health = random.choice([0, 1]) if sa_batt_health is None else sa_batt_health

    nextev_msg = gen_nextev_message('sa_batt_status_event',
                                    sa_batt_health_msg,
                                    sa_batt_health_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    trip_end_event_obj = pbjson.pb2dict(sa_batt_health_msg)
    return nextev_msg, trip_end_event_obj


def parse_message(message):
    event = sa_batt_health_msg_pb2.SABattHealthEvent()
    proto = event.FromString(zlib.decompress(message))
    sa_batt_health_msg = protobuf_to_dict(proto)
    return sa_batt_health_msg
