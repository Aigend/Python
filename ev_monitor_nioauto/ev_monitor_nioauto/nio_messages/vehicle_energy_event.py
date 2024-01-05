#!/usr/bin/env python
# coding=utf-8

"""
功能：在APP上显示电耗曲线。
上报时机：
上报频率：
支持版本：BL250之后，【before】App上没有能量曲线，【after】App follow same/similar product design with ICS energy comsumption curve to be consistent.
应用方：NIO App
需求文档：https://confluence.nevint.com/download/attachments/151405484/%5B%23ES6IRD-1029%5D%20Menu-Energy%20consumption%20curve-%20ES8-BL2.5.0%26%20ES6-BL2.5.0.pdf?version=1&modificationDate=1567744757000&api=v2
相关jira：【ES6】https://jira.nevint.com/browse/EDMS-28200
         【ES8】https://jira.nevint.com/browse/EDMS-25515
附件：https://jira.nevint.com/secure/attachment/227682/Requirements for The ICS Remaining Range Display V1.3.docx
字段描述：https://jira.nevint.com/browse/CVS-8633
"""

import time
import random
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import vehicle_energy_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None,
                     veh_elec_cns=None, veh_elecc_cns_resd=None, clear_fields=None):
    """
    生成车辆瞬时能量事件
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 上报的时间戳
    :param veh_elec_cns: 10公里的瞬时能耗
    :param veh_elecc_cns_resd: 百公里瞬时能耗
    :return: 包含车辆瞬时能量消息的nextev_msg以及vehicle_energy_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # VehicleEnergyEvent
    vehicle_energy_msg = vehicle_energy_msg_pb2.VehicleEnergyEvent()
    vehicle_energy_msg.id = vin
    vehicle_energy_msg.version = protobuf_v
    vehicle_energy_msg.sample_ts = sample_ts

    # veh_elec_cns
    if not veh_elec_cns:
        for i in range(random.randint(1, 5)):
            item = vehicle_energy_msg.veh_elec_cns.add()
            item.VehElecCns = round(random.uniform(0, 100), 1)
            item.VehRemainingEyg = round(random.uniform(0, 100), 1)
            item.BMSCustomerUsage = round(random.uniform(0, 100), 1)
            item.sample_ts = sample_ts - 1000
    else:
        for i, item in enumerate(veh_elec_cns):
            item = vehicle_energy_msg.veh_elec_cns.add()
            item.VehElecCns = veh_elec_cns[i].get('VehElecCns', round(random.uniform(0, 100), 1))
            item.VehRemainingEyg = veh_elec_cns[i].get('VehRemainingEyg', round(random.uniform(0, 100), 1))
            item.BMSCustomerUsage = veh_elec_cns[i].get('BMSCustomerUsage', round(random.uniform(0, 100), 1))
            item.sample_ts = veh_elec_cns[i]['sample_ts'] if ('sample_ts' in veh_elec_cns[i] and veh_elec_cns[i]['sample_ts']) else sample_ts - i * 1000

    # veh_elecc_cns_resd
    if not veh_elecc_cns_resd:
        for i in range(random.randint(1, 5)):
            item = vehicle_energy_msg.veh_elecc_cns_resd.add()
            item.VehElecCns = round(random.uniform(0, 100), 1)
            item.VehRemainingEyg = round(random.uniform(0, 100), 1)
            item.BMSCustomerUsage = round(random.uniform(0, 100), 1)
            item.sample_ts = sample_ts - 1000
    else:
        for i, item in enumerate(veh_elecc_cns_resd):
            item = vehicle_energy_msg.veh_elecc_cns_resd.add()
            item.VehElecCns = veh_elecc_cns_resd[i].get('VehElecCns', round(random.uniform(0, 100), 1))
            item.VehRemainingEyg = veh_elecc_cns_resd[i].get('VehRemainingEyg', round(random.uniform(0, 100), 1))
            item.BMSCustomerUsage = veh_elecc_cns_resd[i].get('BMSCustomerUsage', round(random.uniform(0, 100), 1))
            item.sample_ts = veh_elecc_cns_resd[i]['sample_ts'] if ('sample_ts' in veh_elecc_cns_resd[i] and veh_elecc_cns_resd[i]['sample_ts']) else sample_ts - i * 1000

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('vehicle_energy_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('vehicle_energy_event',
                                    vehicle_energy_msg,
                                    vehicle_energy_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    # vehicle_energy_obj = pbjson.parse_pb_string("VehicleEnergyEvent", vehicle_energy_msg.SerializeToString())
    vehicle_energy_obj = pbjson.pb2dict(vehicle_energy_msg)

    return nextev_msg, vehicle_energy_obj


def parse_message(message):
    event = vehicle_energy_msg_pb2.VehicleEnergyEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status