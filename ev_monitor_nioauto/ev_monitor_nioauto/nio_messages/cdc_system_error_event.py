""" 
@author:dun.yuan
@time: 2022/5/5 2:10 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import time
import zlib
import random
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.cdc_err_msg_pb2 import CDCSystemErrorEvent
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid, sample_ts=None, protobuf_v=19, can_cdc_sys_err=None):
    cdc_sys_err = CDCSystemErrorEvent()

    cdc_sys_err.id = vin
    cdc_sys_err.version = protobuf_v
    if sample_ts is None:
        sample_ts = round(time.time() * 1000)
    cdc_sys_err.sample_ts = sample_ts
    if can_cdc_sys_err is None:
        can_cdc_sys_err = random.choice([0, 1])
    cdc_sys_err.can_cdc_sys_err = can_cdc_sys_err

    nextev_msg = gen_nextev_message('cdc_system_error_event',
                                    cdc_sys_err,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    cdc_sys_err_obj = pbjson.pb2dict(cdc_sys_err)

    return nextev_msg, cdc_sys_err_obj


def parse_message(message):
    event = CDCSystemErrorEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status
