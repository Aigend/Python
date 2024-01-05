#!/usr/bin/env python
# coding=utf-8


import time
from nio_messages import pbjson
from nio_messages.data_unit import gen_connection_status, gen_soc_status, gen_position_status, gen_vehicle_status
from nio_messages.nextev_msg import gen_nextev_message, parse_nextev_message
from nio_messages.pb2 import connection_status_message_pb2
import zlib

from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vid, sample_ts=None, connection_status=None, process_id=None, soc_status=None, position_status=None, vehicle_status=None):
    """
    ecu连接状态消息。
    cgw 连接检查有两种方式
    1.云端按照设置的keepalive心跳包2倍时长间隔（默认心跳是30s，则检查间隔为60秒）去检查连接情况，如果检查到没有连接，则发送connection_lost到kafka中处理并落库。
    2.车机端的toby程序每隔60s（默认，可配置）去探查是否和云端的连接失败，如果失败，会上报specific_event.modem_event事件，并尝试重新连接。上报的modem_event事件云端不做断网处理。只会rvs处理后
    存到history_modem_event表中

    连接状态可能是connect或者connect_lost, 3个ecu都不会主动发disconnect到云端。

    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param sample_ts: 消息采样时间
    :param connection_status: ecu_type("CDC", "CGW", "ADC"); status("CONNECTION_LOST", "OFFLINE", "ONLINE")
    :return:包含ecu状态事件的nextev_msg以及connection_status_msg本身
    """

    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # ConnectionStatusEvent
    connection_status_message = connection_status_message_pb2.ConnectionStatusMsg()
    connection_status_message.vid = vid
    connection_status_message.sample_ts = sample_ts
    connection_status_message.process_id = process_id
    connection_status_message.connection_status.MergeFrom(gen_connection_status(connection_status))

    # SOCStatus
    connection_status_message.soc_status.MergeFrom(gen_soc_status(soc_status))
    # PositionStatus
    connection_status_message.position_status.MergeFrom(gen_position_status(position_status))
    # VehicleStatus
    connection_status_message.vehicle_status.MergeFrom(gen_vehicle_status(vehicle_status))

    nextev_msg = gen_nextev_message('connection_status_event',
                                    connection_status_message,
                                    connection_status_message.sample_ts,
                                    account_id=vid
                                    )
    # connection_status_obj = pbjson.pb2dict(connection_status_message)
    connection_status_obj = pbjson.parse_pb_string("ConnectionStatusMsg", connection_status_message.SerializeToString())

    return nextev_msg, connection_status_obj


def parse_connection_status_message(connection_status_message):
    """
    解析nextev消息，生成一个字典
    :param message: nextev消息的proto格式数据
    :return: 包含nextev消息各个字段的字典
    """
    # connection_status_message = zlib.decompress(connection_status_message)
    # nextev_message = connection_status_message_pb2.ConnectionStatusMsg()
    # data = nextev_message.FromString(connection_status_message)
    parsed_message = {"vid": connection_status_message.get('vid'),
                      "sample_ts": connection_status_message.get('sample_ts'),
                      "connection_status": {
                          "ecu_type": connection_status_message.get('connection_status', {}).get('ecu_type'),
                          "status": connection_status_message.get('connection_status', {}).get('status'),
                          "latest_msg_type": connection_status_message.get('connection_status', {}).get('latest_msg_type')
                      },
                      "vehicle_status": {
                          "vehl_state": connection_status_message.get('vehicle_status', {}).get('vehl_state'),
                          "chrg_state": connection_status_message.get('vehicle_status', {}).get('chrg_state'),
                          "oprtn_mode": connection_status_message.get('vehicle_status', {}).get('oprtn_mode'),
                          "speed": round(connection_status_message.get('vehicle_status', {}).get('speed')),
                          "mileage": connection_status_message.get('vehicle_status', {}).get('mileage'),
                          "vehl_totl_volt": round(connection_status_message.get('vehicle_status', {}).get('vehl_totl_volt'), 1),
                          "vehl_totl_curnt": round(connection_status_message.get('vehicle_status', {}).get('vehl_totl_curnt'), 1),
                          "soc": connection_status_message.get('vehicle_status', {}).get('soc'),
                          "dc_dc_sts": connection_status_message.get('vehicle_status', {}).get('dc_dc_sts'),
                          "gear": connection_status_message.get('vehicle_status', {}).get('gear'),
                          "insulatn_resis": connection_status_message.get('vehicle_status', {}).get('insulatn_resis'),
                          "urgt_prw_shtdwn": connection_status_message.get('vehicle_status', {}).get('urgt_prw_shtdwn'),
                          "comf_ena": connection_status_message.get('vehicle_status', {}).get('comf_ena')
                      },
                      "soc_status": {
                          "chrg_state": connection_status_message.get('soc_status', {}).get('chrg_state'),
                          "btry_cap": round(connection_status_message.get('soc_status', {}).get('btry_cap'), 1),
                          "remaining_range": connection_status_message.get('soc_status', {}).get('remaining_range'),
                          "hivolt_btry_curnt": round(connection_status_message.get('soc_status', {}).get('hivolt_btry_curnt'), 1),
                          "chrg_final_soc": connection_status_message.get('soc_status', {}).get('chrg_final_soc'),
                          "dump_enrgy": round(connection_status_message.get('soc_status', {}).get('dump_enrgy'), 1),
                          "sin_btry_hist_temp": connection_status_message.get('soc_status', {}).get('sin_btry_hist_temp'),
                          "sin_btry_lwst_temp": connection_status_message.get('soc_status', {}).get('sin_btry_lwst_temp'),
                          "btry_qual_actvtn": connection_status_message.get('soc_status', {}).get('btry_qual_actvtn'),
                          "realtime_power_consumption": connection_status_message.get('soc_status', {}).get('realtime_power_consumption'),
                      },
                      "position_status": {
                          "posng_valid_type": connection_status_message.get('position_status', {}).get('posng_valid_type'),
                          "longitude": round(connection_status_message.get('position_status', {}).get('longitude'), 1)
                          if 'longitude' in connection_status_message['position_status'] else None,
                          "latitude": round(connection_status_message.get('position_status', {}).get('latitude'), 1)
                          if 'latitude' in connection_status_message['position_status'] else None,
                          "heading": connection_status_message.get('position_status', {}).get('heading'),
                          "altitude": connection_status_message.get('position_status', {}).get('altitude'),
                          "gps_speed": connection_status_message.get('position_status', {}).get('gps_speed'),
                          "climb": connection_status_message.get('position_status', {}).get('climb'),
                          "gps_ts": connection_status_message.get('position_status', {}).get('gps_ts'),
                      },
                      "process_id": connection_status_message.get('process_id')
                      }
    return parsed_message


def parse_message(message):
    event = connection_status_message_pb2.ConnectionStatusMsg()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status