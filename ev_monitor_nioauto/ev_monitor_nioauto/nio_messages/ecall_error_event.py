""" 
@author:dun.yuan
@time: 2022/5/6 12:15 AM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import time
import zlib
import random
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.ecall_error_msg_pb2 import EcallErrorEvent
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid, sample_ts=None, protobuf_v=19, emgc_call_flr_sts=None):
    ecall_error_msg = EcallErrorEvent()

    ecall_error_msg.id = vin
    ecall_error_msg.version = protobuf_v
    if sample_ts is None:
        sample_ts = round(time.time() * 1000)
    ecall_error_msg.sample_ts = sample_ts
    if emgc_call_flr_sts is None:
        emgc_call_flr_sts = random.choice([0, 1, 2, 3])
    ecall_error_msg.emgc_call_flr_sts = emgc_call_flr_sts

    nextev_msg = gen_nextev_message('ecall_error_event',
                                    ecall_error_msg,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    ecall_error_obj = pbjson.pb2dict(ecall_error_msg)

    return nextev_msg, ecall_error_obj


def parse_message(message):
    event = EcallErrorEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status
