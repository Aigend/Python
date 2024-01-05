#!/usr/bin/env python
# coding=utf-8

"""
功能：ecall(emergency call) 紧急事件触发时，上报车辆信息及呼叫ecall电话

需求文档FDS：https://confluence.nioint.com/pages/viewpage.action?pageId=197665476

设计文档SRD：https://confluence.nioint.com/display/CVS/Advanced+E-Call

时序图：https://confluence.nioint.com/display/SEQ/Ecall

上报时机：
    hard_trigger,soft_trigger, collision_trigger,airbag_pump_trigger, nio_call_trigger， urgt_prw_shtdwn, voice_trigger
    ！！截止6/5/2020 只实现了hard_trigger 和airbag_pump_trgger

    * Hard trigger means it is triggered by pushing the ecall button
    * Soft trigger means it is triggered by pushing the soft button in HU
    * Voice means it is triggered by voice
    * Collision means it is triggered by collision
    * Airbag pump means airbag pump
    * Nio Call trigger means it’s a NIO Call 车机上有个蔚来服务热线400电话，目前没用

上报频率：触发时上报

上报方式：
    有4G网络时，以MQTT通道上报。4G不畅时以手机短信SMS形式上报
    MQTT: 车---->tsp nmp--(kafka)-->rvs_server
    SMS:  车--(短信)-->移动---->联想--(API)-->MNO--(kafka)-->rvs_server

应用方：SCR

API:
    ecall_setting
        http://showdoc.nevint.com/index.php?s=/11&page_id=5309
        主要配置ecall电话。nio_call指的是蔚来服务热线400电话，目前没用
        ecall电话是一开始就配置在车上的

    query: /{vehicle_id}/e_call
        http://showdoc.nevint.com/index.php?s=/11&page_id=5306

    get ecall list:
        /{vehicle_id}/e_calls  http://showdoc.nevint.com/index.php?s=/11&page_id=5305

    get before ecall data:
        /{vehicle_id}/journey/before_ecall http://showdoc.nevint.com/index.php?s=/11&page_id=5308

    sms: mno/push/text_message
        https://tsp-test-int.nio.com/api/1/in/mno/push/text_message

Kafka：
    * rvs_server 上游
        sms  swc-cvs-mno-{env}-push
        mqtt swc-cvs-nmp-{env}_tsp-10005-data_report
    * rvs_server 下游
        comm_kakfa swc-cvs-tsp-{env}-80001-ecall  http://showdoc.nevint.com/index.php?s=/11&page_id=5307

mysql：
    rvs_server服务写入remote_vehicle_{env}.ecall_event
    mno服务写入mno_{env}.text_message

其他：
    * ecall是actived，即处于如下三种状态: Parked(Comfort Enable), Driver Present, Driving.
    * 触发ecall时，只打ecall电话，不会拨打紧急联系人，nio_call等的电话。

"""

import time
import random
import zlib

from nio_messages import pb2, pbjson
from nio_messages.data_unit import gen_vehicle_status, gen_position_status, gen_soc_status, gen_door_status, gen_window_status, gen_alarm_signal, gen_tyre_status, gen_driving_behaviour_event
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import ecall_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, event_id=None, reason_code=None, status=None, clear_fields=None):
    """
    生成紧急电话呼出事件消息
    车辆发生紧急情况上报ecall事件，rvs server消费并落库后，推动到kafka中，由hermers消费并把数据推给SCR(客服中心)，相关人员将收到邮件和短信通知。
    trigger：紧急电话呼出时
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param sample_ts: 消息采样时间
    :param event_id: 事件产生时对应编号
    :param reason_code: 紧急电话产生的原因
    :param status: 产生紧急电话时的车辆状态值
    :return: 包含紧急电话呼出事件的nextev_msg以及journey_end_msg本身
    """

    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))
    # ECallEvent
    ecall_event_msg = ecall_msg_pb2.ECallEvent()
    ecall_event_msg.id = vin
    ecall_event_msg.version = protobuf_v
    ecall_event_msg.sample_ts = sample_ts
    ecall_event_msg.event_id = event_id if event_id else sample_ts
    ecall_event_msg.reason_code = reason_code if reason_code else random.choice(['hard_trigger', 'EDA_trigger',
                                                                                 'soft_trigger', 'voice_trigger', 'collision_trigger',
                                                                                 'airbag_pump_trigger', 'nio_call_trigger'])

    if status is None:
        status = {}

    # PositionStatus
    ecall_event_msg.status.position_status.MergeFrom(gen_position_status(status.get('position_status', {})))

    # VehicleStatus
    ecall_event_msg.status.vehicle_status.MergeFrom(gen_vehicle_status(status.get('vehicle_status', {})))

    # SOCStatus
    ecall_event_msg.status.soc_status.MergeFrom(gen_soc_status(status.get('soc_status', {})))

    # DoorStatus
    ecall_event_msg.status.door_status.MergeFrom(gen_door_status(status.get('door_status', {})))

    # Window status
    ecall_event_msg.status.window_status.MergeFrom(gen_window_status(status.get('window_status', {})))

    # AlarmSignal
    ecall_event_msg.status.alarm_signal.MergeFrom(gen_alarm_signal(status.get('alarm_signal', {}), ecall_event_msg.sample_ts))

    # TyreStatus
    ecall_event_msg.status.tyre_status.MergeFrom(gen_tyre_status(status.get('tyre_status', {})))

    # DrivingBehaviourEvent
    ecall_event_msg.status.driving_behaviour_event.MergeFrom(gen_driving_behaviour_event(vin, status.get('driving_behaviour_event', {})))

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('ecall_event_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('ecall_event',
                                    ecall_event_msg,
                                    ecall_event_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    ecall_event_obj = pbjson.parse_pb_string("ECallEvent", ecall_event_msg.SerializeToString())
    return nextev_msg, ecall_event_obj


def parse_message(message):
    event = ecall_msg_pb2.ECallEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status