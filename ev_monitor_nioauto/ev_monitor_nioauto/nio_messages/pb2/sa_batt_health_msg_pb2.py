# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sa_batt_health_msg.proto

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
  name='sa_batt_health_msg.proto',
  package='',
  serialized_pb=_b('\n\x18sa_batt_health_msg.proto\"\xaa\x01\n\x11SABattHealthEvent\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\x12\x11\n\tsample_ts\x18\x03 \x01(\x04\x12\x37\n\x0esa_batt_health\x18\x04 \x01(\x0e\x32\x1f.SABattHealthEvent.SABattHealth\",\n\x0cSABattHealth\x12\x0b\n\x07HEALTHY\x10\x00\x12\x0f\n\x0bNOT_HEALTHY\x10\x01\x42;\n$com.nextev.cvs_proto.protobuf.eventsB\x13SABattHealthMessage')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_SABATTHEALTHEVENT_SABATTHEALTH = _descriptor.EnumDescriptor(
  name='SABattHealth',
  full_name='SABattHealthEvent.SABattHealth',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='HEALTHY', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOT_HEALTHY', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=155,
  serialized_end=199,
)
_sym_db.RegisterEnumDescriptor(_SABATTHEALTHEVENT_SABATTHEALTH)


_SABATTHEALTHEVENT = _descriptor.Descriptor(
  name='SABattHealthEvent',
  full_name='SABattHealthEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='SABattHealthEvent.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='SABattHealthEvent.version', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sample_ts', full_name='SABattHealthEvent.sample_ts', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sa_batt_health', full_name='SABattHealthEvent.sa_batt_health', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SABATTHEALTHEVENT_SABATTHEALTH,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=199,
)

_SABATTHEALTHEVENT.fields_by_name['sa_batt_health'].enum_type = _SABATTHEALTHEVENT_SABATTHEALTH
_SABATTHEALTHEVENT_SABATTHEALTH.containing_type = _SABATTHEALTHEVENT
DESCRIPTOR.message_types_by_name['SABattHealthEvent'] = _SABATTHEALTHEVENT

SABattHealthEvent = _reflection.GeneratedProtocolMessageType('SABattHealthEvent', (_message.Message,), dict(
  DESCRIPTOR = _SABATTHEALTHEVENT,
  __module__ = 'sa_batt_health_msg_pb2'
  # @@protoc_insertion_point(class_scope:SABattHealthEvent)
  ))
_sym_db.RegisterMessage(SABattHealthEvent)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.eventsB\023SABattHealthMessage'))
# @@protoc_insertion_point(module_scope)
