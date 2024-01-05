# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: generic_config_result.proto

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
  name='generic_config_result.proto',
  package='',
  serialized_pb=_b('\n\x1bgeneric_config_result.proto\"\xb8\x01\n\x0c\x43onfigResult\x12\x12\n\ncommand_id\x18\x01 \x01(\x03\x12*\n\x06status\x18\x02 \x01(\x0e\x32\x1a.ConfigResult.ResultStatus\x12\x13\n\x0b\x66\x61il_reason\x18\x03 \x03(\t\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x0e\n\x06values\x18\x05 \x01(\t\"5\n\x0cResultStatus\x12\x0b\n\x07SUCCESS\x10\x00\x12\x0b\n\x07\x46\x41ILURE\x10\x01\x12\x0b\n\x07RUNNING\x10\x02\x42;\n!com.nextev.cvs_proto.protobuf.rvsB\x16GenericConfigResultMsg')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_CONFIGRESULT_RESULTSTATUS = _descriptor.EnumDescriptor(
  name='ResultStatus',
  full_name='ConfigResult.ResultStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILURE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RUNNING', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=163,
  serialized_end=216,
)
_sym_db.RegisterEnumDescriptor(_CONFIGRESULT_RESULTSTATUS)


_CONFIGRESULT = _descriptor.Descriptor(
  name='ConfigResult',
  full_name='ConfigResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='command_id', full_name='ConfigResult.command_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='ConfigResult.status', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='fail_reason', full_name='ConfigResult.fail_reason', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='ConfigResult.type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='ConfigResult.values', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONFIGRESULT_RESULTSTATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=216,
)

_CONFIGRESULT.fields_by_name['status'].enum_type = _CONFIGRESULT_RESULTSTATUS
_CONFIGRESULT_RESULTSTATUS.containing_type = _CONFIGRESULT
DESCRIPTOR.message_types_by_name['ConfigResult'] = _CONFIGRESULT

ConfigResult = _reflection.GeneratedProtocolMessageType('ConfigResult', (_message.Message,), dict(
  DESCRIPTOR = _CONFIGRESULT,
  __module__ = 'generic_config_result_pb2'
  # @@protoc_insertion_point(class_scope:ConfigResult)
  ))
_sym_db.RegisterMessage(ConfigResult)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n!com.nextev.cvs_proto.protobuf.rvsB\026GenericConfigResultMsg'))
# @@protoc_insertion_point(module_scope)