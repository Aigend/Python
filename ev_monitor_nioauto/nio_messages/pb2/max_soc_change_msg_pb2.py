# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: max_soc_change_msg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import soc_status_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='max_soc_change_msg.proto',
  package='',
  serialized_pb=_b('\n\x18max_soc_change_msg.proto\x1a\x10soc_status.proto\"c\n\x11MaxSOCChangeEvent\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\x12\x11\n\tsample_ts\x18\x03 \x01(\x04\x12\x1e\n\nsoc_status\x18\x04 \x01(\x0b\x32\n.SOCStatusB;\n$com.nextev.cvs_proto.protobuf.eventsB\x13MaxSOCChangeMessage')
  ,
  dependencies=[soc_status_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_MAXSOCCHANGEEVENT = _descriptor.Descriptor(
  name='MaxSOCChangeEvent',
  full_name='MaxSOCChangeEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='MaxSOCChangeEvent.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='MaxSOCChangeEvent.version', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sample_ts', full_name='MaxSOCChangeEvent.sample_ts', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='soc_status', full_name='MaxSOCChangeEvent.soc_status', index=3,
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
  serialized_start=46,
  serialized_end=145,
)

_MAXSOCCHANGEEVENT.fields_by_name['soc_status'].message_type = soc_status_pb2._SOCSTATUS
DESCRIPTOR.message_types_by_name['MaxSOCChangeEvent'] = _MAXSOCCHANGEEVENT

MaxSOCChangeEvent = _reflection.GeneratedProtocolMessageType('MaxSOCChangeEvent', (_message.Message,), dict(
  DESCRIPTOR = _MAXSOCCHANGEEVENT,
  __module__ = 'max_soc_change_msg_pb2'
  # @@protoc_insertion_point(class_scope:MaxSOCChangeEvent)
  ))
_sym_db.RegisterMessage(MaxSOCChangeEvent)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.eventsB\023MaxSOCChangeMessage'))
# @@protoc_insertion_point(module_scope)