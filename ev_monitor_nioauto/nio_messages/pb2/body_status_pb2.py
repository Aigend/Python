# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: body_status.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='body_status.proto',
  package='',
  serialized_pb=_b('\n\x11\x62ody_status.proto\"\xd7\x03\n\nBodyStatus\x12\x11\n\twiper_req\x18\x01 \x01(\x05\x12\x1c\n\x14rain_sensor_fail_sts\x18\x02 \x01(\x05\x12\x1b\n\x13\x66rnt_wipr_inter_spd\x18\x03 \x01(\x05\x12\x1b\n\x13\x66rnt_wiper_park_sts\x18\x04 \x01(\x05\x12\x19\n\x11\x66rnt_wipr_swt_sts\x18\x05 \x01(\x05\x12\x1c\n\x14wiper_swith_position\x18\x06 \x01(\x05\x12\x1e\n\x16\x64rv_cushion_length_pos\x18\x07 \x01(\x05\x12\x1d\n\x15\x64rv_cushion_hight_pos\x18\x08 \x01(\x05\x12\x18\n\x10\x64rv_backrest_pos\x18\t \x01(\x05\x12\x1c\n\x14\x64rv_cushion_tilt_pos\x18\n \x01(\x05\x12\x1f\n\x17pass_cushion_length_pos\x18\x0b \x01(\x05\x12\x1c\n\x14pass_leg_support_pos\x18\x0c \x01(\x05\x12\x19\n\x11pass_backrest_pos\x18\r \x01(\x05\x12-\n%seat_adjmt_frnt_ri_cush_lift_mot_posn\x18\x0e \x01(\x05\x12%\n\x1dseat_adjmt_foot_rest_mot_posn\x18\x0f \x01(\x05\x42\x36\n$com.nextev.cvs_proto.protobuf.customB\x0e\x42odyStatusUnit')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BODYSTATUS = _descriptor.Descriptor(
  name='BodyStatus',
  full_name='BodyStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='wiper_req', full_name='BodyStatus.wiper_req', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rain_sensor_fail_sts', full_name='BodyStatus.rain_sensor_fail_sts', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frnt_wipr_inter_spd', full_name='BodyStatus.frnt_wipr_inter_spd', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frnt_wiper_park_sts', full_name='BodyStatus.frnt_wiper_park_sts', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='frnt_wipr_swt_sts', full_name='BodyStatus.frnt_wipr_swt_sts', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='wiper_swith_position', full_name='BodyStatus.wiper_swith_position', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drv_cushion_length_pos', full_name='BodyStatus.drv_cushion_length_pos', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drv_cushion_hight_pos', full_name='BodyStatus.drv_cushion_hight_pos', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drv_backrest_pos', full_name='BodyStatus.drv_backrest_pos', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drv_cushion_tilt_pos', full_name='BodyStatus.drv_cushion_tilt_pos', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pass_cushion_length_pos', full_name='BodyStatus.pass_cushion_length_pos', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pass_leg_support_pos', full_name='BodyStatus.pass_leg_support_pos', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pass_backrest_pos', full_name='BodyStatus.pass_backrest_pos', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_adjmt_frnt_ri_cush_lift_mot_posn', full_name='BodyStatus.seat_adjmt_frnt_ri_cush_lift_mot_posn', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_adjmt_foot_rest_mot_posn', full_name='BodyStatus.seat_adjmt_foot_rest_mot_posn', index=14,
      number=15, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=493,
)

DESCRIPTOR.message_types_by_name['BodyStatus'] = _BODYSTATUS

BodyStatus = _reflection.GeneratedProtocolMessageType('BodyStatus', (_message.Message,), dict(
  DESCRIPTOR = _BODYSTATUS,
  __module__ = 'body_status_pb2'
  # @@protoc_insertion_point(class_scope:BodyStatus)
  ))
_sym_db.RegisterMessage(BodyStatus)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.customB\016BodyStatusUnit'))
# @@protoc_insertion_point(module_scope)