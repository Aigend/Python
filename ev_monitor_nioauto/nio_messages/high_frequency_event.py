""" 
@author:dun.yuan
@time: 2022/5/6 10:37 PM
@contact: dun.yuan@nio.com
@description: 
@showdoc：
"""
import time
import zlib
import random
from nio_messages import pbjson
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.high_frequency_msg_pb2 import HighFrequencyEvent
from nio_messages.proto_parser import protobuf_to_dict
from nio_messages.data_unit import gen_high_fre_data


def generate_message(vin, vid, sample_ts=None, protobuf_v=19, dbc_type=None, high_fre_data=None):
    high_freq = HighFrequencyEvent()

    high_freq.id = vin
    high_freq.version = protobuf_v
    if sample_ts is None:
        sample_ts = round(time.time() * 1000)
    high_freq.sample_ts = sample_ts
    if dbc_type is None:
        high_freq.dbc_type = random.choice(["es8_7.5.10", "ES8_7.5.11"])

    if high_fre_data is None:
        for i in range(2):
            data = high_freq.high_fre_data.add()
            data.MergeFrom(gen_high_fre_data(None))
            time.sleep(0.01)
    else:
        for it in high_fre_data:
            data = high_freq.high_fre_data.add()
            data.MergeFrom(it)

    nextev_msg = gen_nextev_message('high_frequency_event',
                                    high_freq,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    high_freq_obj = pbjson.pb2dict(high_freq)

    return nextev_msg, high_freq_obj


def parse_message(message):
    event = HighFrequencyEvent()
    proto = event.FromString(zlib.decompress(message))
    vehicle_status = protobuf_to_dict(proto)
    return vehicle_status
