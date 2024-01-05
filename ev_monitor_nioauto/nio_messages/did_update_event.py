#!/usr/bin/env python
# coding=utf-8


import time
import random
import zlib

from nio_messages import pb2, pbjson
from nio_messages.did import DIDS
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import did_update_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, did_data_num=1, did_data_list=None, did_tag=None):
    """
    随机上报数据(传参vin和did_num)或者上报指定数据（传参data）
    trigger：当一个预定义的FOTA DID和ECU版本更新事件发生时
    :param vin: vin码
    :param protobuf_v: protobuf 版本
    :param did_data_num:随机上报数据个数，在实际情况中，did数据是会全上报
    :param did_data_list: 上报指定数据
    :return:复合消息平台格式的消息
    """
    did_update_msg = did_update_msg_pb2.DIDUpdateEvent()
    did_update_msg.id = vin
    did_update_msg.version = protobuf_v
    did_update_msg.did_tag = "did_tag" + str(int(time.time())) if did_tag is None else did_tag  # did_tag是根据车上的ecu的did计算出来的，用于表示一个版本集合。
    did_update_msg.command_id = ''  # command_id 是从云端拿到的用于标识一个命令的，云端会使用。如果是车主动上报did，command_id就不填写

    # DIDData
    if not did_data_list and did_data_num:
        did_data_list = []
        did_data_list.extend(random.sample(DIDS, did_data_num))
        for d in did_data_list:
            for item in d['dids']:
                item['value'] = "P{:0>7} AD".format(random.randint(0, 9999999))

    ts_now = int(time.time() * 1000)
    if did_data_list:
        for d in did_data_list:
            did_data = did_update_msg.did_data.add()
            did_data.ecu = d['ecu']
            for item in d['dids']:
                did = did_data.dids.add()
                did.id = item['id']
                did.value = item['value']
                did.sample_ts = item.get('sample_ts', ts_now)

    nextev_msg = gen_nextev_message('did_update_event',
                                    did_update_msg,
                                    int(time.time() * 1000),
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    did_update_obj = pbjson.pb2dict(did_update_msg)
    return nextev_msg, did_update_obj


def parse_message(message):
    event = did_update_msg_pb2.DIDUpdateEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status
