# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: internal.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='internal.proto',
  package='aec',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x0einternal.proto\x12\x03\x61\x65\x63\"$\n\x07\x63ommand\x12\x0b\n\x03\x63md\x18\x01 \x02(\t\x12\x0c\n\x04\x61rgs\x18\x02 \x03(\t\"&\n\x06\x61nswer\x12\x0e\n\x06source\x18\x01 \x02(\t\x12\x0c\n\x04\x61rgs\x18\x02 \x03(\t\"\'\n\x06status\x12\x0e\n\x06source\x18\x01 \x02(\t\x12\r\n\x05state\x18\x02 \x02(\x05\"A\n\rmcs_step_json\x12\x0c\n\x04step\x18\x01 \x02(\t\x12\x12\n\nservice_id\x18\x02 \x01(\t\x12\x0e\n\x06params\x18\x03 \x01(\t')
)




_COMMAND = _descriptor.Descriptor(
  name='command',
  full_name='aec.command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cmd', full_name='aec.command.cmd', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='args', full_name='aec.command.args', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=59,
)


_ANSWER = _descriptor.Descriptor(
  name='answer',
  full_name='aec.answer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='aec.answer.source', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='args', full_name='aec.answer.args', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=61,
  serialized_end=99,
)


_STATUS = _descriptor.Descriptor(
  name='status',
  full_name='aec.status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='aec.status.source', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='state', full_name='aec.status.state', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=101,
  serialized_end=140,
)


_MCS_STEP_JSON = _descriptor.Descriptor(
  name='mcs_step_json',
  full_name='aec.mcs_step_json',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='step', full_name='aec.mcs_step_json.step', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='service_id', full_name='aec.mcs_step_json.service_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='params', full_name='aec.mcs_step_json.params', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=142,
  serialized_end=207,
)

DESCRIPTOR.message_types_by_name['command'] = _COMMAND
DESCRIPTOR.message_types_by_name['answer'] = _ANSWER
DESCRIPTOR.message_types_by_name['status'] = _STATUS
DESCRIPTOR.message_types_by_name['mcs_step_json'] = _MCS_STEP_JSON
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

command = _reflection.GeneratedProtocolMessageType('command', (_message.Message,), {
  'DESCRIPTOR' : _COMMAND,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:aec.command)
  })
_sym_db.RegisterMessage(command)

answer = _reflection.GeneratedProtocolMessageType('answer', (_message.Message,), {
  'DESCRIPTOR' : _ANSWER,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:aec.answer)
  })
_sym_db.RegisterMessage(answer)

status = _reflection.GeneratedProtocolMessageType('status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:aec.status)
  })
_sym_db.RegisterMessage(status)

mcs_step_json = _reflection.GeneratedProtocolMessageType('mcs_step_json', (_message.Message,), {
  'DESCRIPTOR' : _MCS_STEP_JSON,
  '__module__' : 'internal_pb2'
  # @@protoc_insertion_point(class_scope:aec.mcs_step_json)
  })
_sym_db.RegisterMessage(mcs_step_json)


# @@protoc_insertion_point(module_scope)