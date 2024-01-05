# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: journey_start_msg.proto

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
import position_status_pb2
import vehicle_status_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='journey_start_msg.proto',
  package='',
  serialized_pb=_b('\n\x17journey_start_msg.proto\x1a\x10soc_status.proto\x1a\x15position_status.proto\x1a\x14vehicle_status.proto\"\xa8\x02\n\x11JourneyStartEvent\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\x12\x12\n\njourney_id\x18\x03 \x01(\t\x12\x0e\n\x06icc_id\x18\x04 \x01(\t\x12\x11\n\tsample_ts\x18\x05 \x01(\x04\x12;\n\x14\x62\x61ttery_package_info\x18\x06 \x01(\x0b\x32\x1d.SOCStatus.BatteryPackageInfo\x12(\n\x0fposition_status\x18\x07 \x01(\x0b\x32\x0f.PositionStatus\x12\x1e\n\nsoc_status\x18\x08 \x01(\x0b\x32\n.SOCStatus\x12&\n\x0evehicle_status\x18\t \x01(\x0b\x32\x0e.VehicleStatus\x12\x10\n\x08pm25_fil\x18\n \x01(\x05\x42;\n$com.nextev.cvs_proto.protobuf.eventsB\x13JourneyStartMessage')
  ,
  dependencies=[soc_status_pb2.DESCRIPTOR,position_status_pb2.DESCRIPTOR,vehicle_status_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_JOURNEYSTARTEVENT = _descriptor.Descriptor(
  name='JourneyStartEvent',
  full_name='JourneyStartEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='JourneyStartEvent.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='JourneyStartEvent.version', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='journey_id', full_name='JourneyStartEvent.journey_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='icc_id', full_name='JourneyStartEvent.icc_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sample_ts', full_name='JourneyStartEvent.sample_ts', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='battery_package_info', full_name='JourneyStartEvent.battery_package_info', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='position_status', full_name='JourneyStartEvent.position_status', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='soc_status', full_name='JourneyStartEvent.soc_status', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vehicle_status', full_name='JourneyStartEvent.vehicle_status', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pm25_fil', full_name='JourneyStartEvent.pm25_fil', index=9,
      number=10, type=5, cpp_type=1, label=1,
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
  serialized_start=91,
  serialized_end=387,
)

_JOURNEYSTARTEVENT.fields_by_name['battery_package_info'].message_type = soc_status_pb2._SOCSTATUS_BATTERYPACKAGEINFO
_JOURNEYSTARTEVENT.fields_by_name['position_status'].message_type = position_status_pb2._POSITIONSTATUS
_JOURNEYSTARTEVENT.fields_by_name['soc_status'].message_type = soc_status_pb2._SOCSTATUS
_JOURNEYSTARTEVENT.fields_by_name['vehicle_status'].message_type = vehicle_status_pb2._VEHICLESTATUS
DESCRIPTOR.message_types_by_name['JourneyStartEvent'] = _JOURNEYSTARTEVENT

JourneyStartEvent = _reflection.GeneratedProtocolMessageType('JourneyStartEvent', (_message.Message,), dict(
  DESCRIPTOR = _JOURNEYSTARTEVENT,
  __module__ = 'journey_start_msg_pb2'
  # @@protoc_insertion_point(class_scope:JourneyStartEvent)
  ))
_sym_db.RegisterMessage(JourneyStartEvent)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.eventsB\023JourneyStartMessage'))
# @@protoc_insertion_point(module_scope)
