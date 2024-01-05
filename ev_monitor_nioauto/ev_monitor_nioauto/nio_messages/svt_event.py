#!/usr/bin/env python
# coding=utf-8
"""
需求文档：https://confluence.nioint.com/pages/viewpage.action?pageId=161468424
设计文档FDS：https://confluence.nevint.com/display/SHEE/Stolen+Vehicle+Tracking%3AES8
实现详情SRD：https://confluence.nevint.com/display/CVS/Stolen+Vehicle+Tracking

svt 总体分为配置下发和事件上报两部分。
1. 配置下发：
系统默认配置为svt mode关闭，4个tigger关闭。车机上没有任何配置文件。
通过generic接口可以下发所有配置。车机返回的结果会存到mysql的svt_mode表中
通过set svt mode（提供给SCR）接口调用内部的svt_setting接口可以设置svt mode打开或者关闭。车机返回的结果会存到mysql的svt_mode表中
generic setting: http://showdoc.nevint.com/index.php?s=/11&page_id=908
set svt mode：http://showdoc.nevint.com/index.php?s=/11&page_id=17338
svt_setting: http://showdoc.nevint.com/index.php?s=/11&page_id=17594

query svt data: http://showdoc.nevint.com/index.php?s=/11&page_id=17333
query svt mode: http://showdoc.nevint.com/index.php?s=/11&page_id=17336

2. 事件上报：
1) trigger
四个trigger分别为lv_bat_remove，anti_theft_alarm，gnss_ant_fault，unauth_mv_alarm。
LV电源的断开与恢复,alarm信号的开关,天线的断开与恢复,非法移动及用户手动开关非法移动的trigger会触发svt事件。触发前提是：
    当车辆不处于维修模式（
    remote_vehicle_test:vehicle_status:{vid}:SpecialStatus repaired=1 或者
    remote_vehicle_test:vehicle_status:{vid}:ExteriorStatus ntester=false）时，
    且相应的trigger配置为开时。
上报的情况会存入到mysql的svt_event表中

2）如果有掉线的话，svt数据会补发

3. 向主用车人下发推送通知
    只有当车辆为激活状态且上报的reason_code为如下这四种情况时，才会推送app：
    1、lv_bat_removal_on
    2、gnss_ant_fault_on
    3、anti_theft_alarm_on
    4、unauth_movement_on

4. svt mode
    车辆被盗后，用户致电SCR，运营人员可通过后台将车辆置于被盗追踪模式(SVT)模式，在SVT模式下：
        车辆的远程车控功能无法使用，TSP应拒绝处于SVT模式下的远程车控
        TSP返回的失败文案应为：异常状态锁定中，暂时无法进行此操作
        车辆状态和定位查看等功能暂不受影响
        车辆设置的功能暂不受影响
        车辆充电信息显示不受影响（充电错误、充满等状态信息）
        服务板块的功能暂不受影响
        App爱车页需要显式告知，车辆当前处于被盗追踪状态
        状态提醒栏中，增加提示：异常状态锁定中，等级同1级车辆故障；
        如果伴有其他车辆状态提醒，则应提示：异常状态锁定中 ... 等n个提醒

        在车辆信息页面中，新增”车辆锁定“分组，显示”异常状态锁定中“这个提醒

        用户可进一步查看此状态的详细介绍：
        在异常状态锁定中，车辆一旦停泊后将无法再次启动，必须等待救援。
        当车辆处于此状态下时，车辆所有的远程控制功能也将暂时无法使用，如需解除该锁定状态，请联系你的专属蔚来顾问或致电蔚来官方服务热线。


    当配置了svt mode=on时，每30秒会有reason_code=data_report的tracking型svt事件上报。目前data_report类型的svt不会存到svt_event表中。后续据说会改。


"""

import time
import random
import zlib

from nio_messages import pb2, pbjson
from nio_messages.data_unit import gen_position_status, gen_vehicle_status
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import svt_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, event_id=None, reason_code=None, status=None):

    """
    生成偷盗车辆跟踪事件消息
    trigger：当SVT mode配置为on时，每30秒触发一次SVT
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param sample_ts: 消息采样时间
    :param event_id: 事件产生时对应编号
    :param reason_code: 紧急电话产生的原因
    :param status: 发送变化的告警信号
    :return: 包含偷盗车辆跟踪事件的nextev_msg以及journey_end_msg本身
    """

    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))
    # SVTEvent
    svt_event_msg = svt_msg_pb2.SVTEvent()
    svt_event_msg.id = vin
    svt_event_msg.version = protobuf_v
    svt_event_msg.sample_ts = sample_ts
    svt_event_msg.event_id = event_id if event_id else sample_ts - 1000
    svt_event_msg.reason_code = reason_code if reason_code else random.choice(['lv_bat_removal_on', 'lv_bat_removal_off', 'gnss_ant_fault_on', 'gnss_ant_fault_off',
                                               'anti_theft_alarm_on', 'anti_theft_alarm_off', 'unauth_movement_on', 'unauth_movement_trigger_on','unauth_movement_trigger_off',
                                               'data_report'])

    if status is None:
        status = {}

    # PositionStatus
    svt_event_msg.status.position_status.MergeFrom(gen_position_status(status.get('position_status', {})))

    # VehicleStatus
    svt_event_msg.status.vehicle_status.MergeFrom(gen_vehicle_status(status.get('vehicle_status', {})))

    # PowSupplySourceType
    svt_event_msg.status.pow_supply_source = status.get('pow_supply_source', random.choice([0, 1]))

    # backup_battery_level
    svt_event_msg.status.backup_battery_level = status.get('backup_battery_level', round(random.uniform(-180, 180), 3))

    # AntennaStatus
    svt_event_msg.status.gnss_ant_stats = status.get('gnss_ant_stats', random.choice([0, 1, 2]))

    # anti_theft_alarm
    svt_event_msg.status.anti_theft_alarm = status.get('anti_theft_alarm', random.choice([True, False]))

    nextev_msg = gen_nextev_message('svt_event',
                                    svt_event_msg,
                                    svt_event_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    svt_event_obj = pbjson.pb2dict(svt_event_msg)
    return nextev_msg, svt_event_obj


def parse_message(message):
    event = svt_msg_pb2.SVTEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status