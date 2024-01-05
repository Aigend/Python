# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: high_frequency_msg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import can_msg_pb2
import position_status_pb2
import driving_data_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='high_frequency_msg.proto',
  package='',
  serialized_pb=_b('\n\x18high_frequency_msg.proto\x1a\rcan_msg.proto\x1a\x15position_status.proto\x1a\x12\x64riving_data.proto\"{\n\x12HighFrequencyEvent\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08\x64\x62\x63_type\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\x05\x12\x11\n\tsample_ts\x18\x04 \x01(\x04\x12#\n\rhigh_fre_data\x18\x05 \x03(\x0b\x32\x0c.HighFreData\"\x8a\x01\n\x0bHighFreData\x12\x13\n\x0bsample_time\x18\x01 \x01(\x04\x12\x18\n\x07\x63\x61n_msg\x18\x02 \x01(\x0b\x32\x07.CanMsg\x12*\n\x08\x61ttitude\x18\x03 \x01(\x0b\x32\x18.PositionStatus.Attitude\x12 \n\nsteerWhlag\x18\x04 \x01(\x0b\x32\x0c.DrivingDataB<\n$com.nextev.cvs_proto.protobuf.eventsB\x14HighFrequencyMessage')
  ,
  dependencies=[can_msg_pb2.DESCRIPTOR,position_status_pb2.DESCRIPTOR,driving_data_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_HIGHFREQUENCYEVENT = _descriptor.Descriptor(
  name='HighFrequencyEvent',
  full_name='HighFrequencyEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='HighFrequencyEvent.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dbc_type', full_name='HighFrequencyEvent.dbc_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='HighFrequencyEvent.version', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sample_ts', full_name='HighFrequencyEvent.sample_ts', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='high_fre_data', full_name='HighFrequencyEvent.high_fre_data', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=86,
  serialized_end=209,
)


_HIGHFREDATA = _descriptor.Descriptor(
  name='HighFreData',
  full_name='HighFreData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sample_time', full_name='HighFreData.sample_time', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='can_msg', full_name='HighFreData.can_msg', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='attitude', full_name='HighFreData.attitude', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='steerWhlag', full_name='HighFreData.steerWhlag', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=212,
  serialized_end=350,
)

_HIGHFREQUENCYEVENT.fields_by_name['high_fre_data'].message_type = _HIGHFREDATA
_HIGHFREDATA.fields_by_name['can_msg'].message_type = can_msg_pb2._CANMSG
_HIGHFREDATA.fields_by_name['attitude'].message_type = position_status_pb2._POSITIONSTATUS_ATTITUDE
_HIGHFREDATA.fields_by_name['steerWhlag'].message_type = driving_data_pb2._DRIVINGDATA
DESCRIPTOR.message_types_by_name['HighFrequencyEvent'] = _HIGHFREQUENCYEVENT
DESCRIPTOR.message_types_by_name['HighFreData'] = _HIGHFREDATA

HighFrequencyEvent = _reflection.GeneratedProtocolMessageType('HighFrequencyEvent', (_message.Message,), dict(
  DESCRIPTOR = _HIGHFREQUENCYEVENT,
  __module__ = 'high_frequency_msg_pb2'
  # @@protoc_insertion_point(class_scope:HighFrequencyEvent)
  ))
_sym_db.RegisterMessage(HighFrequencyEvent)

HighFreData = _reflection.GeneratedProtocolMessageType('HighFreData', (_message.Message,), dict(
  DESCRIPTOR = _HIGHFREDATA,
  __module__ = 'high_frequency_msg_pb2'
  # @@protoc_insertion_point(class_scope:HighFreData)
  ))
_sym_db.RegisterMessage(HighFreData)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.eventsB\024HighFrequencyMessage'))
# @@protoc_insertion_point(module_scope)