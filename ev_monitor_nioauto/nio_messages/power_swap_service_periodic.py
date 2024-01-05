""" 
功能：二代换电站服务相关的信号上报
https://git.nevint.com/greatwall/data_collection_server/merge_requests/269/diffs
上报时机：[CGW] should upload the Power Swap service related signals via periodically upload channel and normal event channel
上报频率：5s一上报
支持版本：BL3.1.0
应用方：换电相关应用
"""
import time
import random
import zlib

from nio_messages import pb2
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2 import power_swap_msg_pb2
from nio_messages.data_unit import gen_power_swap_periodic
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid=None, protobuf_v=pb2.VERSION, sample_ts=None, power_swap_periodic=None):
    if sample_ts is None:
        sample_ts = int(round(time.time() * 1000))

    # PowerSwapChangeEvent
    power_swap_change_msg = power_swap_msg_pb2.PowerSwapChangePeriodic()
    power_swap_change_msg.id = vin
    power_swap_change_msg.version = protobuf_v
    power_swap_change_msg.sample_ts = sample_ts
    power_swap_change_msg.power_swap_periodic.MergeFrom(gen_power_swap_periodic(power_swap_periodic))

    nextev_msg = gen_nextev_message('power_swap_service_periodic',
                                    power_swap_change_msg,
                                    power_swap_change_msg.sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    power_swap_change_event_obj = pbjson.pb2dict(power_swap_change_msg)
    return nextev_msg, power_swap_change_event_obj


def parse_message(message):
    event = power_swap_msg_pb2.PowerSwapChangeEvent()
    proto = event.FromString(zlib.decompress(message))
    power_swap = protobuf_to_dict(proto)
    return power_swap