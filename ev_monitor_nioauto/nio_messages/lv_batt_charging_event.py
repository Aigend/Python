#!/usr/bin/env python
# coding=utf-8

"""
功能：监控小电池状况。
需求来源：预测小电池寿命，避免驾驶故障/FOTA失败等
上报时机：条件较多且偏底层，详细见下方相关jira
上报频率：1Hz
支持版本：BL260之后
应用方：VMS等监控方
相关jira：https://jira.nevint.com/browse/EDMS-37440
"""

import time
import random
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.data_unit import gen_vehicle_status, gen_can_msg
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import lv_batt_charging_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, event_id=None, event_num=None,
                     cgw_log_voltage=None, cgw_log_soc=None, can_msg=None, vehicle_status=None, pre_cgw_log_info=None, clear_fields=None):
    """
    生成小电池充电事件
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 上报的时间戳
    :param event_id: 事件ID，小电池充电事件的第一个毫秒级时间戳
    :param event_num: 1,2,3,4,5
    :param cgw_log_voltage: 当前 CGW log voltage, 0~65535 mv, -1: invalid
    :param cgw_log_soc: 当前CGW log soc, 0~100%, -1:invalid
    :param can_msg: can_msg数据，默认为None表示随机取值
    :param vehicle_status: 车辆状态数据，默认为None表示随机取值
    :param pre_cgw_log_info: 小电池充电事件之前的10组 cgw log info
    :return: 包含小电池充电消息的nextev_msg以及lv_batt_charging_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))
    if event_id is None:
        event_id = int(time.strftime("%Y%m%d", time.localtime()) + '0001')
    if event_num is None:
        event_num = random.choice([1, 2, 3, 4, 5])
    if cgw_log_voltage is None:
        cgw_log_voltage = random.randint(0, 6000) * 0.1
    if cgw_log_soc is None:
        cgw_log_soc = random.randint(0, 200) * 0.5

    # LvBattChargingEvent
    lv_batt_charging_msg = lv_batt_charging_msg_pb2.LvBattChargingEvent()
    lv_batt_charging_msg.id = vin
    lv_batt_charging_msg.version = protobuf_v
    lv_batt_charging_msg.sample_ts = sample_ts
    lv_batt_charging_msg.event_id = event_id
    lv_batt_charging_msg.event_num = event_num
    lv_batt_charging_msg.cgw_log_voltage = cgw_log_voltage
    lv_batt_charging_msg.cgw_log_soc = cgw_log_soc

    # VehicleStatus
    lv_batt_charging_msg.vehicle_status.MergeFrom(gen_vehicle_status(vehicle_status))
    # CanMsg
    lv_batt_charging_msg.can_msg.MergeFrom(gen_can_msg(can_msg))
    # PreCgwLogInfo
    if not pre_cgw_log_info:
        for i in range(10):
            item = lv_batt_charging_msg.pre_cgw_log_info.add()
            item.sample_ts = sample_ts - i * 1000
            item.cgw_log_volatage = round(random.uniform(0, 600), 1)
            item.cgw_log_soc = round(random.uniform(0, 100), 1)
    else:
        for i, item in enumerate(pre_cgw_log_info):
            item = lv_batt_charging_msg.pre_cgw_log_info.add()
            item.sample_ts = pre_cgw_log_info[i]['sample_ts'] if ('sample_ts' in pre_cgw_log_info[i] and pre_cgw_log_info[i]['sample_ts']) else sample_ts - i * 1000
            item.cgw_log_volatage = pre_cgw_log_info[i].get('cgw_log_voltage', round(random.uniform(0, 600), 1))
            item.cgw_log_soc = pre_cgw_log_info[i].get('cgw_log_soc', round(random.uniform(0, 100), 1))

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('lv_batt_charging_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('lv_batt_charging_event',
                                    lv_batt_charging_msg,
                                    lv_batt_charging_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    # heating_status_change_obj = pbjson.parse_pb_string("HeatingStatusChangeEvent", heating_status_change_msg.SerializeToString())
    heating_status_change_obj = pbjson.pb2dict(lv_batt_charging_msg)

    return nextev_msg, heating_status_change_obj


def parse_message(message):
    event = lv_batt_charging_msg_pb2.LvBattChargingEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status