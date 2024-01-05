# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bms_power_swap_msg.proto

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
  name='bms_power_swap_msg.proto',
  package='',
  serialized_pb=_b('\n\x18\x62ms_power_swap_msg.proto\"\x8e\x01\n\x11\x42MSPowerSwapEvent\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\x12\x11\n\tsample_ts\x18\x03 \x01(\x04\x12$\n\x0f\x64id_data_before\x18\x04 \x03(\x0b\x32\x0b.BMSDIDInfo\x12#\n\x0e\x64id_data_after\x18\x05 \x03(\x0b\x32\x0b.BMSDIDInfo\"\'\n\nBMSDIDInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\tB;\n$com.nextev.cvs_proto.protobuf.eventsB\x13\x42MSPowerSwapMessage')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BMSPOWERSWAPEVENT = _descriptor.Descriptor(
  name='BMSPowerSwapEvent',
  full_name='BMSPowerSwapEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='BMSPowerSwapEvent.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='BMSPowerSwapEvent.version', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sample_ts', full_name='BMSPowerSwapEvent.sample_ts', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='did_data_before', full_name='BMSPowerSwapEvent.did_data_before', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='did_data_after', full_name='BMSPowerSwapEvent.did_data_after', index=4,
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
  serialized_start=29,
  serialized_end=171,
)


_BMSDIDINFO = _descriptor.Descriptor(
  name='BMSDIDInfo',
  full_name='BMSDIDInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='BMSDIDInfo.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='BMSDIDInfo.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=173,
  serialized_end=212,
)

_BMSPOWERSWAPEVENT.fields_by_name['did_data_before'].message_type = _BMSDIDINFO
_BMSPOWERSWAPEVENT.fields_by_name['did_data_after'].message_type = _BMSDIDINFO
DESCRIPTOR.message_types_by_name['BMSPowerSwapEvent'] = _BMSPOWERSWAPEVENT
DESCRIPTOR.message_types_by_name['BMSDIDInfo'] = _BMSDIDINFO

BMSPowerSwapEvent = _reflection.GeneratedProtocolMessageType('BMSPowerSwapEvent', (_message.Message,), dict(
  DESCRIPTOR = _BMSPOWERSWAPEVENT,
  __module__ = 'bms_power_swap_msg_pb2'
  # @@protoc_insertion_point(class_scope:BMSPowerSwapEvent)
  ))
_sym_db.RegisterMessage(BMSPowerSwapEvent)

BMSDIDInfo = _reflection.GeneratedProtocolMessageType('BMSDIDInfo', (_message.Message,), dict(
  DESCRIPTOR = _BMSDIDINFO,
  __module__ = 'bms_power_swap_msg_pb2'
  # @@protoc_insertion_point(class_scope:BMSDIDInfo)
  ))
_sym_db.RegisterMessage(BMSDIDInfo)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.eventsB\023BMSPowerSwapMessage'))
# @@protoc_insertion_point(module_scope)
