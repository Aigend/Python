#!/usr/bin/env python
# coding=utf-8
"""
功能：车端主动请求更新地图数据
需求来源：https://nio.feishu.cn/wiki/wikcnLJJ6TIJ48i2eDAfiDG8tEd
上报时机：车端主动请求更新地图数据的时候，需要主动上报一个地图更新类型的消息到 TSP 云平台，采集管理平台需要对该种类型的消息进行记录和落盘
上报频率：实时通信
支持版本：NT2
应用方：AA
showdoc：https://nio.feishu.cn/docs/doccnhcPE2fylMfnzKSgH2ZjaDd#
"""
import time
import random
import uuid
from nio_messages import pb2, pbjson
from nio_messages.data_unit import gen_adas_header
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.map_update_tile_pb2 import map_update_tile


def generate_message(vin, vid=None, sample_ts=None, protobuf_v=pb2.VERSION, adas_header_data=None,
                     map_update_tile_data=None):
    """
    :param map_update_tile_data:
    :param sample_ts:
    :param protobuf_v:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param adas_header_data: adas header数据
    :return: 包含np事件事件的nextev_msg以及feature_status_update本身
    """
    if map_update_tile_data is None:
        map_update_tile_data = {}
    map_update_tile_info = map_update_tile()

    map_update_tile_info.uuid = map_update_tile_data.get('uuid', str(uuid.uuid1()))
    map_update_tile_info.global_version = map_update_tile_data.get('global_version', random.randint(0, 100))
    map_update_tile_info.timestamp = map_update_tile_data.get('timestamp', round(time.time() * 1000))
    map_update_tile_info.version = map_update_tile_data.get('version', random.randint(0, 10000))
    map_update_tile_info.tileID = map_update_tile_data.get('tileID', random.randint(0, 10000000000))

    if sample_ts is None:
        sample_ts = round(time.time() * 1000)
    adas_header = gen_adas_header(adas_header_data, sample_ts)

    map_update_tile_event = {'AdasHeader': adas_header, 'map_update_tile': map_update_tile_info}

    # type为DATA_REPORT  sub_type为FeatureStatusUpdate
    # header的params的key为AdasHeader
    # status的params的key为FeatureStatusUpdate

    nextev_msg = gen_nextev_message('map_update_tile',
                                    map_update_tile_event,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    map_update_tile_obj = {
        'AdasHeader': pbjson.pb2dict(adas_header),
        'map_update_tile': pbjson.pb2dict(map_update_tile_info)
    }
    return nextev_msg, map_update_tile_obj
