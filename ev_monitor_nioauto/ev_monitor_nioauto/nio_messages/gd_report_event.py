""" 
@author:dun.yuan
@time: 2021/5/30 2:34 上午
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import gd_event_report_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict
from nio_messages.data_unit import gen_event_item


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, mon_window_sec=None, event_items=None):
    """
    绿龙上报车机系统的状态信息
    :param mon_window_sec:
    :param event_items:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :return:
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # GdEventReport
    gd_event_report = gd_event_report_msg_pb2.GDEventReportEvent()
    # gd_system_info.version = protobuf_v
    gd_event_report.sample_ts = sample_ts

    if mon_window_sec is not None:
        gd_event_report.mon_window_sec = mon_window_sec

    if event_items is None:
        event_items = [{}]

    for i in range(len(event_items)):
        event_item = gd_event_report.event_items.add()
        event_item.MergeFrom(gen_event_item(event_items[i]))

    nextev_msg = gen_nextev_message('gd_report_event',
                                    gd_event_report,
                                    gd_event_report.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    gd_system_info_obj = pbjson.pb2dict(gd_event_report)
    return nextev_msg, gd_system_info_obj


def parse_message(message):
    event = gd_event_report_msg_pb2.GDEventReportEvent()
    proto = event.FromString(zlib.decompress(message))
    return protobuf_to_dict(proto)
