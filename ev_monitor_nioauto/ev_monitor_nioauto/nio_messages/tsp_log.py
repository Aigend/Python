#!/usr/bin/env python
# coding=utf-8
"""
@author:dun.yuan
@time: 2021/12/3 11:36 上午
@contact: dun.yuan@nio.com
"""
import time
import random
from nio_messages import pb2, pbjson
from nio_messages.data_unit import gen_adas_header
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.tsp_log_pb2 import TspLogList


def generate_message(vin, vid=None, sample_ts=None, protobuf_v=pb2.VERSION, adas_header_data=None, tsp_log_list=None):
    """
    :param sample_ts:
    :param tsp_log_list:
    :param protobuf_v:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param adas_header_data: adas header数据
    :return: 包含np事件事件的nextev_msg以及feature_status_update本身
    """
    tsp_logs = TspLogList()

    if tsp_log_list is None:
        tsp_log_list = [{}]

    for i in range(len(tsp_log_list)):
        tsp_log = tsp_logs.log.add()
        tsp_log.key = tsp_log_list[i].get('key', 'adc')
        tsp_log.level = tsp_log_list[i].get('level', random.choice([0, 1, 2, 3, 4, 5]))
        tsp_log.timestamp = tsp_log_list[i].get('timestamp', round(time.time() * 1000))
        tsp_log.comment = tsp_log_list[i].get('comment', 'abcdefghijklmnopq....')
        tsp_log.value = tsp_log_list[i].get('value', random.randint(0, 10000000000))

    if sample_ts is None:
        sample_ts = round(time.time() * 1000)
    adas_header = gen_adas_header(adas_header_data, sample_ts)

    tsp_log_list_event = {'AdasHeader': adas_header, 'TspLogList': tsp_logs}

    # type为DATA_REPORT  sub_type为FeatureStatusUpdate
    # header的params的key为AdasHeader
    # status的params的key为FeatureStatusUpdate

    nextev_msg = gen_nextev_message('TspLogList',
                                    tsp_log_list_event,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    feature_status_update_obj = {
        'AdasHeader': pbjson.pb2dict(adas_header),
        'TspLogList': pbjson.pb2dict(tsp_logs)
    }
    return nextev_msg, feature_status_update_obj
