# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: script_channel.proto

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
  name='script_channel.proto',
  package='',
  serialized_pb=_b('\n\x14script_channel.proto\"S\n\rScriptChannel\x12\x0f\n\x07\x61vl_cmd\x18\x01 \x03(\t\x12\x11\n\texit_code\x18\x02 \x01(\x05\x12\x0e\n\x06stdout\x18\x03 \x01(\t\x12\x0e\n\x06stderr\x18\x04 \x01(\tB9\n!com.nextev.cvs_proto.protobuf.rvsB\x14ScriptSupportChannel')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_SCRIPTCHANNEL = _descriptor.Descriptor(
  name='ScriptChannel',
  full_name='ScriptChannel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='avl_cmd', full_name='ScriptChannel.avl_cmd', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='exit_code', full_name='ScriptChannel.exit_code', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stdout', full_name='ScriptChannel.stdout', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stderr', full_name='ScriptChannel.stderr', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=24,
  serialized_end=107,
)

DESCRIPTOR.message_types_by_name['ScriptChannel'] = _SCRIPTCHANNEL

ScriptChannel = _reflection.GeneratedProtocolMessageType('ScriptChannel', (_message.Message,), dict(
  DESCRIPTOR = _SCRIPTCHANNEL,
  __module__ = 'script_channel_pb2'
  # @@protoc_insertion_point(class_scope:ScriptChannel)
  ))
_sym_db.RegisterMessage(ScriptChannel)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n!com.nextev.cvs_proto.protobuf.rvsB\024ScriptSupportChannel'))
# @@protoc_insertion_point(module_scope)