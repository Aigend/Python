#!/usr/bin/env python
# coding=utf-8
"""
功能：上报adas nio pilot的feature_status_event事件
上报时机：24小时都会一直报数据，只要车在就会报，不管车是不是停车或者休眠
上报频率：状态变化则立即上报，状态不变时隔30s上报一次

支持版本：BL230之后车会上报np数据。2020-3-1之后，tsp会处理np数据并在app端展现
应用方：NIO App
需求文档：
    np: https://confluence.nevint.com/pages/viewpage.action?pageId=215830747
    nop: https://confluence.nioint.com/pages/viewpage.action?pageId=293031595

API文档：
    旅程详情api http://showdoc.nevint.com/index.php?s=/11&page_id=2428 np_mileage,np_duration,np_status三个字段
    旅程月报api http://showdoc.nevint.com/index.php?s=/11&page_id=20289 np_mileage,np_duration两个字段
    np版本api http://showdoc.nevint.com/index.php?s=/11&page_id=22005 np_type字段
相关jira：
附件：
字段描述：
    tsp用到的主要是时间戳，np_mileage, acc_np_sts 字段
    事件有三个时间戳，如下
        AdasHeader.timestamp 反映的是事件的采样时间，即30s间隔。单位是毫秒
        feature_status_update.FeatureStatusUpdate.timestamp 反映的是acc_np_sts发生变化的事件。注意单位是秒
        feature_status_update.timestamp 这个时间在tsp这边没有用处，没有任何处理
    feature_status_update.FeatureStatus.acc_np_sts（0-7）
        ACC_SYSTEM_OFF=0;SYSTEM_PASSIVE=1;SYSTEM_READY=2;ACC_ACTIVE=3;ACC_STANDBY=4;PILOT_ACTIVE=5;LATERAL_UNAVAILABLE=6;PILOT_STANDBY=7;
    AdasHeader.np_mileage
        产生np事件时抓取的里程数，注意可能和其他事件抓取的里程数不一致
其他:
    无

"""

import time
import zlib

from nio_messages import pb2, pbjson
from nio_messages.data_unit import gen_adas_header, gen_feature_status, gen_position_status
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.feature_status_update_pb2 import FeatureStatusUpdate
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, adas_header_data=None,
                     feature_status_data=None, position_status=None):
    """
    :param position_status:
    :param protobuf_v:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param sample_ts: 时间戳。如果adas_header_data或feature_status_data已传时间戳则用自己的，否则可以用sample_ts指定
    :param adas_header_data: adas header数据
    :param feature_status_data: feature_status_update.feature_status数据
    :return: 包含np事件事件的nextev_msg以及feature_status_update本身
    """

    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))
    adas_header = gen_adas_header(adas_header_data, sample_ts)
    feature_status = gen_feature_status(feature_status_data)

    feature_status_update = FeatureStatusUpdate()
    feature_status_update.timestamp = int(round(time.time() * 1000))
    feature_status_update.feature_status.MergeFrom(feature_status)
    feature_status_update.position.MergeFrom(gen_position_status(position_status))

    feature_status_update_event = {'AdasHeader': adas_header, 'FeatureStatusUpdate': feature_status_update}

    # type为DATA_REPORT  sub_type为FeatureStatusUpdate
    # header的params的key为AdasHeader
    # status的params的key为FeatureStatusUpdate

    nextev_msg = gen_nextev_message('FeatureStatusUpdate',
                                    feature_status_update_event,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    feature_status_update_obj = {
        'AdasHeader': pbjson.pb2dict(adas_header),
        'FeatureStatusUpdate': pbjson.pb2dict(feature_status_update)
    }
    return nextev_msg, feature_status_update_obj

def parse_message(message):
    event = FeatureStatusUpdate()
    proto = event.FromString(message)
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status