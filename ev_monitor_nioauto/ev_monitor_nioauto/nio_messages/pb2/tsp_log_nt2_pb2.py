# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tsp_log_nt2.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import tsplog_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tsp_log_nt2.proto',
  package='',
  serialized_pb=_b('\n\x11tsp_log_nt2.proto\x1a\x0ctsplog.proto\"b\n\x0bTspLogList2\x12\x14\n\x0cvehicle_uuid\x18\x01 \x01(\t\x12\x12\n\nvehicle_id\x18\x02 \x01(\t\x12\x13\n\x0b\x61\x64\x63_version\x18\x03 \x01(\t\x12\x14\n\x03log\x18\x04 \x03(\x0b\x32\x07.TspLogB5\n\"com.nextev.cvs_proto.protobuf.adasB\x0fTspLogList2Unit')
  ,
  dependencies=[tsplog_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_TSPLOGLIST2 = _descriptor.Descriptor(
  name='TspLogList2',
  full_name='TspLogList2',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vehicle_uuid', full_name='TspLogList2.vehicle_uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vehicle_id', full_name='TspLogList2.vehicle_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='adc_version', full_name='TspLogList2.adc_version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='log', full_name='TspLogList2.log', index=3,
      number=4, type=11, cpp_type=10, label=3,
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
  serialized_start=35,
  serialized_end=133,
)

_TSPLOGLIST2.fields_by_name['log'].message_type = tsplog_pb2._TSPLOG
DESCRIPTOR.message_types_by_name['TspLogList2'] = _TSPLOGLIST2

TspLogList2 = _reflection.GeneratedProtocolMessageType('TspLogList2', (_message.Message,), dict(
  DESCRIPTOR = _TSPLOGLIST2,
  __module__ = 'tsp_log_nt2_pb2'
  # @@protoc_insertion_point(class_scope:TspLogList2)
  ))
_sym_db.RegisterMessage(TspLogList2)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\"com.nextev.cvs_proto.protobuf.adasB\017TspLogList2Unit'))
# @@protoc_insertion_point(module_scope)