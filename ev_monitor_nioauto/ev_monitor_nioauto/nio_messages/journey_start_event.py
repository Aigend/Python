#!/usr/bin/env python
# coding=utf-8
import random
import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.data_unit import gen_soc_status, gen_position_status, gen_vehicle_status, gen_battery_package_info
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import journey_start_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, icc_id=None, journey_id=None, pm25_fil=None, sample_ts=None, soc_status=None,
                     position_status=None, vehicle_status=None, battery_package_info=None, clear_fields=None):
    """
    生成行程开始事件的消息
    trigger：行程开始时
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param icc_id: SIM卡ID
    :param journey_id: 行程ID
    :param pm25_fil: 空调滤芯的寿命(0-100%)
    :param sample_ts: 消息采样时间
    :param soc_status: 电池状态数据，默认为None表示随机取值
    :param position_status: 位置状态数据，默认为None表示随机取值
    :param vehicle_status: 车辆状态数据，默认为None表示随机取值
    :param battery_package_info: 电池包数据，默认为None表示随机取值
    :return: 包含行程开始事件消息的nextev_msg以及journey_start_msg本身
    """
    if journey_id is None:
        journey_id = time.strftime("%Y%m%d", time.localtime()) + '0001'
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))
    if icc_id is None:
        icc_id = "ICC" + vin
    if pm25_fil is None:
        pm25_fil = random.randint(0, 100)

    # JourneyStartEvent
    journey_start_msg = journey_start_msg_pb2.JourneyStartEvent()
    journey_start_msg.id = vin
    journey_start_msg.version = protobuf_v
    journey_start_msg.journey_id = journey_id
    journey_start_msg.icc_id = icc_id
    journey_start_msg.pm25_fil = pm25_fil
    journey_start_msg.sample_ts = sample_ts

    # SOCStatus.BatteryPackageInfo
    journey_start_msg.battery_package_info.MergeFrom(gen_battery_package_info(battery_package_info, vin))
    # SOCStatus
    journey_start_msg.soc_status.MergeFrom(gen_soc_status(soc_status))
    # PositionStatus
    journey_start_msg.position_status.MergeFrom(gen_position_status(position_status))
    # VehicleStatus
    journey_start_msg.vehicle_status.MergeFrom(gen_vehicle_status(vehicle_status))

    # exclude
    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('journey_start_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('journey_start_event',
                                    journey_start_msg,
                                    journey_start_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    # journey_start_obj = pbjson.pb2dict(journey_start_msg)
    journey_start_obj = pbjson.parse_pb_string("JourneyStartEvent", journey_start_msg.SerializeToString())
    return nextev_msg, journey_start_obj

def parse_message(message):
    event = journey_start_msg_pb2.JourneyStartEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status