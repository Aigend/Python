""" 
@author:dun.yuan
@time: 2021/6/29 8:23 下午
@contact: dun.yuan@nio.com
功能：TSP存储车端的DID数据，并给SO提供接口查阅。
需求来源：1.需精确知道每块电池包在每辆车上的使用情况。
电池包的精确使用情况累加记录在BMS DID中（包括SOH/累计充电安时/累计放电安时/低温使用情况/大电流冲击次数及持续时长/继电器寿命信息/保险丝寿命信息等等），所以需要收集电池包上车时的BMS DID 和下车时的BMS DID，以记录该电池包在某辆车上的使用情况。
2. 同时也优化当前换电后电池ID更新不及时的情况（该情况会导致1.电池包数据混乱；2.电池监控系统误报；3.真实告警时无法准确定位故障电池包）
上报时机：send both BMSDID_AfterHVOff and BMSDID_AfterBatterySwap together to TSP
需求文档：https://confluence.nioint.com/display/DigitalArchitecture/BMS+DID+collection+and+upload
"""

import time
import random
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.did import DIDS
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import bms_power_swap_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None,
                     did_info_before=None, did_info_after=None, clear_fields=None):
    """
    生成BMS_DID事件
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :param did_info_before: BMS_DID信息
    :param did_info_after: BMS_DID信息
    :return: 包含BMS_DID消息的nextev_msg以及bms_did_msg本身
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # BMSDidEvent
    bms_power_swap_msg = bms_power_swap_msg_pb2.BMSPowerSwapEvent()
    bms_power_swap_msg.id = vin
    bms_power_swap_msg.version = protobuf_v
    bms_power_swap_msg.sample_ts = sample_ts

    # did_info
    if did_info_before is None:
        did_info_before = random.sample(DIDS, 1)[0]['dids']
    for item in did_info_before:
        did_info = bms_power_swap_msg.did_data_before.add()
        did_info.id = item['id']
        did_info.value = item['value']
    if did_info_after is None:
        did_info_after = random.sample(DIDS, 1)[0]['dids']
    for item in did_info_after:
        did_info = bms_power_swap_msg.did_data_after.add()
        did_info.id = item['id']
        did_info.value = item['value']

    if clear_fields:
        for item in clear_fields:
            message, field = ('.'.join(item.split('.')[:-1]), item.split('.')[-1])
            message = message + '.' if message else ''
            eval('bms_power_swap_msg.' + message + 'ClearField("' + field + '")')

    nextev_msg = gen_nextev_message('bms_power_swap_event',
                                    bms_power_swap_msg,
                                    bms_power_swap_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )

    # bms_did_obj = pbjson.parse_pb_string("BMSDidEvent", bms_power_swap_msg.SerializeToString())
    bms_did_obj = pbjson.pb2dict(bms_power_swap_msg)

    return nextev_msg, bms_did_obj


def parse_message(message):
    event = bms_power_swap_msg_pb2.BMSPowerSwapEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status
