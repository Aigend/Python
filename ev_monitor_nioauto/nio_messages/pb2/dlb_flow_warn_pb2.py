# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dlb_flow_warn.proto

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
  name='dlb_flow_warn.proto',
  package='',
  serialized_pb=_b('\n\x13\x64lb_flow_warn.proto\"\xa6\x01\n\x0b\x44lbFlowWarn\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0e\n\x06statid\x18\x02 \x01(\x03\x12\x13\n\x0b\x61\x64\x63_version\x18\x03 \x01(\t\x12\x1a\n\x12utc_nano_timestamp\x18\x04 \x01(\x03\x12\x12\n\nvehicle_id\x18\x05 \x01(\t\x12\x14\n\x0cvehicle_type\x18\x06 \x01(\t\x12\x1e\n\x0bupload_info\x18\x07 \x01(\x0b\x32\t.FlowInfo\"o\n\x08\x46lowInfo\x12\x16\n\x0estat_starttime\x18\x01 \x01(\x03\x12\x14\n\x0cstat_endtime\x18\x02 \x01(\x03\x12\x11\n\tflow_used\x18\x03 \x01(\x03\x12\"\n\nevent_info\x18\x04 \x03(\x0b\x32\x0e.EventFlowInfo\"I\n\rEventFlowInfo\x12\x10\n\x08\x61pp_name\x18\x01 \x01(\t\x12\x12\n\nevent_name\x18\x02 \x01(\t\x12\x12\n\nevent_flow\x18\x03 \x01(\x03\x42\x35\n\"com.nextev.cvs_proto.protobuf.adasB\x0f\x44lbFlowWarnUnit')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_DLBFLOWWARN = _descriptor.Descriptor(
  name='DlbFlowWarn',
  full_name='DlbFlowWarn',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uuid', full_name='DlbFlowWarn.uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='statid', full_name='DlbFlowWarn.statid', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='adc_version', full_name='DlbFlowWarn.adc_version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='utc_nano_timestamp', full_name='DlbFlowWarn.utc_nano_timestamp', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vehicle_id', full_name='DlbFlowWarn.vehicle_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vehicle_type', full_name='DlbFlowWarn.vehicle_type', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='upload_info', full_name='DlbFlowWarn.upload_info', index=6,
      number=7, type=11, cpp_type=10, label=1,
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
  serialized_start=24,
  serialized_end=190,
)


_FLOWINFO = _descriptor.Descriptor(
  name='FlowInfo',
  full_name='FlowInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stat_starttime', full_name='FlowInfo.stat_starttime', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stat_endtime', full_name='FlowInfo.stat_endtime', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='flow_used', full_name='FlowInfo.flow_used', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='event_info', full_name='FlowInfo.event_info', index=3,
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
  serialized_start=192,
  serialized_end=303,
)


_EVENTFLOWINFO = _descriptor.Descriptor(
  name='EventFlowInfo',
  full_name='EventFlowInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_name', full_name='EventFlowInfo.app_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='event_name', full_name='EventFlowInfo.event_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='event_flow', full_name='EventFlowInfo.event_flow', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  serialized_start=305,
  serialized_end=378,
)

_DLBFLOWWARN.fields_by_name['upload_info'].message_type = _FLOWINFO
_FLOWINFO.fields_by_name['event_info'].message_type = _EVENTFLOWINFO
DESCRIPTOR.message_types_by_name['DlbFlowWarn'] = _DLBFLOWWARN
DESCRIPTOR.message_types_by_name['FlowInfo'] = _FLOWINFO
DESCRIPTOR.message_types_by_name['EventFlowInfo'] = _EVENTFLOWINFO

DlbFlowWarn = _reflection.GeneratedProtocolMessageType('DlbFlowWarn', (_message.Message,), dict(
  DESCRIPTOR = _DLBFLOWWARN,
  __module__ = 'dlb_flow_warn_pb2'
  # @@protoc_insertion_point(class_scope:DlbFlowWarn)
  ))
_sym_db.RegisterMessage(DlbFlowWarn)

FlowInfo = _reflection.GeneratedProtocolMessageType('FlowInfo', (_message.Message,), dict(
  DESCRIPTOR = _FLOWINFO,
  __module__ = 'dlb_flow_warn_pb2'
  # @@protoc_insertion_point(class_scope:FlowInfo)
  ))
_sym_db.RegisterMessage(FlowInfo)

EventFlowInfo = _reflection.GeneratedProtocolMessageType('EventFlowInfo', (_message.Message,), dict(
  DESCRIPTOR = _EVENTFLOWINFO,
  __module__ = 'dlb_flow_warn_pb2'
  # @@protoc_insertion_point(class_scope:EventFlowInfo)
  ))
_sym_db.RegisterMessage(EventFlowInfo)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\"com.nextev.cvs_proto.protobuf.adasB\017DlbFlowWarnUnit'))
# @@protoc_insertion_point(module_scope)
