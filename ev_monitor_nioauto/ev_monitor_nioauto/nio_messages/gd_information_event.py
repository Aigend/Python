""" 
@author:dun.yuan
@time: 2021/5/30 2:31 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import gd_system_information_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict
from nio_messages.data_unit import gen_sys_info_item


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, mon_window_sec=None, sys_info_items=None):
    """
    绿龙上报车机系统的状态信息
    :param mon_window_sec:
    :param sys_info_items:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :return:
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # GdSystemInfo
    gd_system_info = gd_system_information_msg_pb2.GDSystemInformationEvent()
    # gd_system_info.version = protobuf_v
    gd_system_info.sample_ts = sample_ts

    if mon_window_sec is not None:
        gd_system_info.mon_window_sec = mon_window_sec

    if sys_info_items is None:
        sys_info_items = [{}]

    for i in range(len(sys_info_items)):
        sys_info_item = gd_system_info.sys_info_items.add()
        sys_info_item.MergeFrom(gen_sys_info_item(sys_info_items[i]))

    nextev_msg = gen_nextev_message('gd_information_event',
                                    gd_system_info,
                                    gd_system_info.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    gd_system_info_obj = pbjson.pb2dict(gd_system_info)
    return nextev_msg, gd_system_info_obj


def parse_message(message):
    event = gd_system_information_msg_pb2.GDSystemInformationEvent()
    proto = event.FromString(zlib.decompress(message))
    return protobuf_to_dict(proto)
