# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: oss/southbound/device2cloud/common/UniversalDataModel.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='oss/southbound/device2cloud/common/UniversalDataModel.proto',
  package='oss.southbound',
  syntax='proto2',
  serialized_options=b'\n@com.nextev.pm.oss.common.protobuf.southbound.device2cloud.commonB\027UniversalDataModelProto',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n;oss/southbound/device2cloud/common/UniversalDataModel.proto\x12\x0eoss.southbound\"\xc0\x01\n\x12UniversalDataModel\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\x11\x12\x12\n\nvalue_bool\x18\x03 \x01(\x08\x12\x11\n\tvalue_int\x18\x04 \x01(\x11\x12\x12\n\nvalue_long\x18\x05 \x01(\x12\x12\x13\n\x0bvalue_float\x18\x06 \x01(\x02\x12\x14\n\x0cvalue_double\x18\x07 \x01(\x01\x12\x14\n\x0cvalue_string\x18\x08 \x01(\x0c\x12\x13\n\x0bvalue_bytes\x18\t \x01(\x0c\x42[\n@com.nextev.pm.oss.common.protobuf.southbound.device2cloud.commonB\x17UniversalDataModelProto'
)




_UNIVERSALDATAMODEL = _descriptor.Descriptor(
  name='UniversalDataModel',
  full_name='oss.southbound.UniversalDataModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='oss.southbound.UniversalDataModel.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='oss.southbound.UniversalDataModel.type', index=1,
      number=2, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value_bool', full_name='oss.southbound.UniversalDataModel.value_bool', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value_int', full_name='oss.southbound.UniversalDataModel.value_int', index=3,
      number=4, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value_long', full_name='oss.southbound.UniversalDataModel.value_long', index=4,
      number=5, type=18, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value_float', full_name='oss.southbound.UniversalDataModel.value_float', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value_double', full_name='oss.southbound.UniversalDataModel.value_double', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value_string', full_name='oss.southbound.UniversalDataModel.value_string', index=7,
      number=8, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value_bytes', full_name='oss.southbound.UniversalDataModel.value_bytes', index=8,
      number=9, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=80,
  serialized_end=272,
)

DESCRIPTOR.message_types_by_name['UniversalDataModel'] = _UNIVERSALDATAMODEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UniversalDataModel = _reflection.GeneratedProtocolMessageType('UniversalDataModel', (_message.Message,), {
  'DESCRIPTOR' : _UNIVERSALDATAMODEL,
  '__module__' : 'oss.southbound.device2cloud.common.UniversalDataModel_pb2'
  # @@protoc_insertion_point(class_scope:oss.southbound.UniversalDataModel)
  })
_sym_db.RegisterMessage(UniversalDataModel)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
