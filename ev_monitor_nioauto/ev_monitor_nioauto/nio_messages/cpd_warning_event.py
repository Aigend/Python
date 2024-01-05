""" 
@author:dun.yuan
@time: 2022/5/5 7:03 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import time
import zlib
import random
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.cpd_warning_msg_pb2 import CPDWarningEvent
from nio_messages.proto_parser import protobuf_to_dict


def generate_message(vin, vid, account_id, sample_ts=None, protobuf_v=19, cpd_sts=None):
    cpd_warn = CPDWarningEvent()

    cpd_warn.id = vin
    cpd_warn.version = protobuf_v
    cpd_warn.account_id = account_id
    if sample_ts is None:
        sample_ts = round(time.time() * 1000)
    cpd_warn.sample_ts = sample_ts
    if cpd_sts is None:
        cpd_sts = random.choice([0, 1])
    cpd_warn.cpd_sts = cpd_sts

    nextev_msg = gen_nextev_message('cpd_warning_event',
                                    cpd_warn,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    cdc_sys_err_obj = pbjson.pb2dict(cpd_warn)

    return nextev_msg, cdc_sys_err_obj


def parse_message(message):
    event = CPDWarningEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status
