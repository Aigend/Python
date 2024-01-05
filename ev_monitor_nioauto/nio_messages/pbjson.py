#
# Copyright (c) 2013, Next Tuesday GmbH
#       Authored by: Seif Lotfy <sfl@nexttuesday.de>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of the FreeBSD Project.
#
import traceback
import logging
from google.protobuf.descriptor import FieldDescriptor as FD
from nio_messages.pb2 import (alarm_signal_pb2, alarm_data_pb2, alarm_signal_update_msg_pb2,
                              charge_end_msg_pb2, charge_start_msg_pb2, charge_update_msg_pb2, bms_status_pb2,
                              attach_file_pb2 , nfc_authorization_pb2, can_msg_pb2, signal_status_pb2, driving_behaviour_msg_pb2,
                              occupant_status_pb2, tyre_status_pb2, extremum_data_pb2, driving_data_pb2, did_data_pb2, did_update_msg_pb2,
                              door_status_change_msg_pb2, door_status_pb2, ecall_msg_pb2, evm_param_pb2, hvac_status_change_msg_pb2,
                              hvac_status_pb2, instant_status_msg_pb2, journey_start_msg_pb2, journey_update_msg_pb2, light_change_msg_pb2,
                              light_status_pb2, position_status_pb2, soc_status_pb2, vehicle_status_pb2, window_status_change_msg_pb2,
                              window_status_pb2, driving_motor_pb2, cmd_result_pb2, did_resp_pb2, dtc_resp_pb2, generic_config_result_pb2,
                              journey_end_msg_pb2, nextev_msg_pb2, svt_msg_pb2)

from nio_messages.proto_parser import _get_field_value_adaptor, TYPE_CALLABLE_MAP, FieldDescriptor, repeated, EXTENSION_CONTAINER

class ConvertException(Exception):
    pass

def dict2pb(cls, adict, strict=False):
    """
    Takes a class representing the ProtoBuf Message and fills it with data from
    the dict.
    """
    obj = cls()
    for field in obj.DESCRIPTOR.fields:
        if not field.label == field.LABEL_REQUIRED:
            continue
        if not field.has_default_value:
            continue
        if not field.name in adict:
            raise ConvertException('Field "%s" missing from descriptor dictionary.'
                                   % field.name)
    field_names = set([field.name for field in obj.DESCRIPTOR.fields])
    if strict:
        for key in adict.keys():
            if key not in field_names:
                raise ConvertException(
                    'Key "%s" can not be mapped to field in %s class.'
                    % (key, type(obj)))
    for field in obj.DESCRIPTOR.fields:
        if not field.name in adict:
            continue
        msg_type = field.message_type
        if field.label == FD.LABEL_REPEATED:
            if field.type == FD.TYPE_MESSAGE:
                for sub_dict in adict[field.name]:
                    item = getattr(obj, field.name).add()
                    item.CopyFrom(dict2pb(msg_type._concrete_class, sub_dict))
            else:
                map(getattr(obj, field.name).append, adict[field.name])
        else:
            if field.type == FD.TYPE_MESSAGE:
                value = dict2pb(msg_type._concrete_class, adict[field.name])
                getattr(obj, field.name).CopyFrom(value)
            else:
                setattr(obj, field.name, adict[field.name])
    return obj


def pb2dict(obj):
    """
    Takes a ProtoBuf Message obj and convertes it to a dict.
    """
    adict = {}
    if not obj.IsInitialized():
        return None
    for field in obj.DESCRIPTOR.fields:
        # if not getattr(obj, field.name):
        #     continue
        if not field.label == FD.LABEL_REPEATED:
            if not field.type == FD.TYPE_MESSAGE:
                adict[field.name] = getattr(obj, field.name)
            else:
                value = pb2dict(getattr(obj, field.name))
                if value:
                    adict[field.name] = value
        else:
            if field.type == FD.TYPE_MESSAGE:
                adict[field.name] = \
                    [pb2dict(v) for v in getattr(obj, field.name)]
            else:
                adict[field.name] = [v for v in getattr(obj, field.name)]
    return adict


def parse_pb_string(key_name, pb_str):
    """
    Args:
        key_name: the objective protobuf message name
        pb_str: string you want to deserialize
    """
    ret = dict()
    # assert pb_str, "Invaild pb_str to be desrizalized"
    obj_class = None
    try:
        for item in globals().keys():
            if item.endswith("_pb2"):
                for key in globals()[item].__dict__:
                    if key.__eq__(key_name):
                        obj_class = globals()[item].__dict__[key]
    except Exception:
        if obj_class != None:
            pass
        else:
            raise Exception("Cannot find the provided key_name: %s with protobuf_files" % key_name)
    key_object = obj_class()
    try:
        key_object.ParseFromString(pb_str)
        ret = protobuf_to_dict(key_object)
        return ret
    except Exception:
        traceback.format_exc()
        return ret


def protobuf_to_dict(pb, type_callable_map=TYPE_CALLABLE_MAP, use_enum_labels=False):
    result_dict = {}
    extensions = {}
    for field, value in pb.ListFields():
        type_callable = _get_field_value_adaptor(pb, field, type_callable_map, use_enum_labels)
        if field.label == FieldDescriptor.LABEL_REPEATED:
            type_callable = repeated(type_callable)

        if field.is_extension:
            extensions[str(field.number)] = type_callable(value)
            continue

        result_dict[field.name] = type_callable(value)
        # log("DEBUG", '--------------------------------------%s %s' % (field.name, str(value)))
    if extensions:
        result_dict[EXTENSION_CONTAINER] = extensions
    return result_dict