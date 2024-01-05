""" 
功能：CGW换电站场景连接WIFI时长信息数据上报
上报时机：1.当有WIFI连接成功建立时，触发事件上报
        2.当有WIFI Scan扫描事件，并1分钟之内无有效连接时，触发事件上报
上报频率：单次
支持版本：BL325
应用方： 主要应用于换电泊车过程
相关jira：https://jira.nioint.com/browse/CVS-17772
"""
import random
import time
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import wifi_connect_msg_pb2
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, data=None):
    """
    :param data:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param protobuf_v: protobuf版本
    :param sample_ts: 消息采样时间
    :return:
    """
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    if data is None:
        data = {}

    wifi_connect_msg = wifi_connect_msg_pb2.WifiConnectEvent()
    wifi_connect_msg.id = vin
    wifi_connect_msg.version = protobuf_v
    wifi_connect_msg.sample_ts = sample_ts
    wifi_connect_msg.result = data.get('result', random.choice([0, 1]))
    wifi_connect_msg.connect_time = data.get('connect_time', random.choice(['time out', 'auto connect', str(random.randint(0, 60))]))
    wifi_connect_msg.psap_pwr_swap_sts = data.get('psap_pwr_swap_sts', random.choice([0, 1, 2]))
    wifi_connect_msg.pwr_swap_man_park_req = data.get('pwr_swap_man_park_req', random.choice([0, 1]))
    wifi_connect_msg.veh_pwr_swap_mod_req = data.get('veh_pwr_swap_mod_req', random.choice([0, 1, 2, 3]))

    nextev_msg = gen_nextev_message('wifi_connect_event',
                                    wifi_connect_msg,
                                    wifi_connect_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    wifi_connect_obj = pbjson.pb2dict(wifi_connect_msg)
    return nextev_msg, wifi_connect_obj


def parse_message(message):
    event = wifi_connect_msg_pb2.WifiConnectEvent()
    proto = event.FromString(zlib.decompress(message))
    wifi_connect_msg = protobuf_to_dict(proto)
    return wifi_connect_msg
