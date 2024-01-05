# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: heating_status.proto

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
  name='heating_status.proto',
  package='',
  serialized_pb=_b('\n\x14heating_status.proto\"\x9a\n\n\rHeatingStatus\x12\x44\n\x14steer_wheel_heat_sts\x18\x01 \x01(\x0e\x32&.HeatingStatus.SteerWheelHeatingStatus\x12?\n\x15seat_heat_frnt_le_sts\x18\x02 \x01(\x0e\x32 .HeatingStatus.SeatHeatingStatus\x12?\n\x15seat_heat_frnt_ri_sts\x18\x03 \x01(\x0e\x32 .HeatingStatus.SeatHeatingStatus\x12=\n\x13seat_heat_re_le_sts\x18\x04 \x01(\x0e\x32 .HeatingStatus.SeatHeatingStatus\x12=\n\x13seat_heat_re_ri_sts\x18\x05 \x01(\x0e\x32 .HeatingStatus.SeatHeatingStatus\x12;\n\x0fhv_batt_pre_sts\x18\x06 \x01(\x0e\x32\".HeatingStatus.HVBattHeatingStatus\x12<\n\x15seat_vent_frnt_le_sts\x18\x07 \x01(\x0e\x32\x1d.HeatingStatus.SeatVentStatus\x12<\n\x15seat_vent_frnt_ri_sts\x18\x08 \x01(\x0e\x32\x1d.HeatingStatus.SeatVentStatus\x12\x39\n\x10\x62try_warm_up_sts\x18\t \x01(\x0e\x32\x1f.HeatingStatus.BtryWarmUpStatus\x12:\n\x13seat_vent_re_le_sts\x18\n \x01(\x0e\x32\x1d.HeatingStatus.SeatVentStatus\x12:\n\x13seat_vent_re_ri_sts\x18\x0b \x01(\x0e\x32\x1d.HeatingStatus.SeatVentStatus\"\x89\x01\n\x17SteerWheelHeatingStatus\x12\x18\n\x14STEER_WHEEL_HEAT_OFF\x10\x00\x12\x17\n\x13STEER_WHEEL_HEAT_ON\x10\x01\x12\x1d\n\x19STEER_WHEEL_HEAT_RESERVED\x10\x02\x12\x1c\n\x18STEER_WHEEL_HEAT_INVALID\x10\x03\"z\n\x11SeatHeatingStatus\x12\x11\n\rSEAT_HEAT_OFF\x10\x00\x12\x11\n\rSEAT_HEAT_LOW\x10\x01\x12\x14\n\x10SEAT_HEAT_MIDDLE\x10\x02\x12\x12\n\x0eSEAT_HEAT_HIGH\x10\x03\x12\x15\n\x11SEAT_HEAT_INVALID\x10\x07\"}\n\x13HVBattHeatingStatus\x12\x13\n\x0f\x42VBATT_HEAT_OFF\x10\x00\x12\x1b\n\x17\x42VBATT_HEAT_PRE_HEATING\x10\x01\x12\x1b\n\x17\x42VBATT_HEAT_CALCULATING\x10\x02\x12\x17\n\x13\x42VBATT_HEAT_INVALID\x10\x03\"w\n\x0eSeatVentStatus\x12\x11\n\rSEAT_VENT_OFF\x10\x00\x12\x11\n\rSEAT_VENT_LOW\x10\x01\x12\x14\n\x10SEAT_VENT_MIDDLE\x10\x02\x12\x12\n\x0eSEAT_VENT_HIGH\x10\x03\x12\x15\n\x11SEAT_VENT_INVALID\x10\x07\"W\n\x10\x42tryWarmUpStatus\x12\x14\n\x10\x42TRY_WARM_UP_OFF\x10\x00\x12\x13\n\x0f\x42TRY_WARM_UP_ON\x10\x01\x12\x18\n\x14\x42TRY_WARM_UP_INVALID\x10\x02\x42\x39\n$com.nextev.cvs_proto.protobuf.customB\x11HeatingStatusUnit')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_HEATINGSTATUS_STEERWHEELHEATINGSTATUS = _descriptor.EnumDescriptor(
  name='SteerWheelHeatingStatus',
  full_name='HeatingStatus.SteerWheelHeatingStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STEER_WHEEL_HEAT_OFF', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STEER_WHEEL_HEAT_ON', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STEER_WHEEL_HEAT_RESERVED', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STEER_WHEEL_HEAT_INVALID', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=733,
  serialized_end=870,
)
_sym_db.RegisterEnumDescriptor(_HEATINGSTATUS_STEERWHEELHEATINGSTATUS)

_HEATINGSTATUS_SEATHEATINGSTATUS = _descriptor.EnumDescriptor(
  name='SeatHeatingStatus',
  full_name='HeatingStatus.SeatHeatingStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SEAT_HEAT_OFF', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEAT_HEAT_LOW', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEAT_HEAT_MIDDLE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEAT_HEAT_HIGH', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEAT_HEAT_INVALID', index=4, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=872,
  serialized_end=994,
)
_sym_db.RegisterEnumDescriptor(_HEATINGSTATUS_SEATHEATINGSTATUS)

_HEATINGSTATUS_HVBATTHEATINGSTATUS = _descriptor.EnumDescriptor(
  name='HVBattHeatingStatus',
  full_name='HeatingStatus.HVBattHeatingStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BVBATT_HEAT_OFF', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BVBATT_HEAT_PRE_HEATING', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BVBATT_HEAT_CALCULATING', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BVBATT_HEAT_INVALID', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=996,
  serialized_end=1121,
)
_sym_db.RegisterEnumDescriptor(_HEATINGSTATUS_HVBATTHEATINGSTATUS)

_HEATINGSTATUS_SEATVENTSTATUS = _descriptor.EnumDescriptor(
  name='SeatVentStatus',
  full_name='HeatingStatus.SeatVentStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SEAT_VENT_OFF', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEAT_VENT_LOW', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEAT_VENT_MIDDLE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEAT_VENT_HIGH', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEAT_VENT_INVALID', index=4, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1123,
  serialized_end=1242,
)
_sym_db.RegisterEnumDescriptor(_HEATINGSTATUS_SEATVENTSTATUS)

_HEATINGSTATUS_BTRYWARMUPSTATUS = _descriptor.EnumDescriptor(
  name='BtryWarmUpStatus',
  full_name='HeatingStatus.BtryWarmUpStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BTRY_WARM_UP_OFF', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_WARM_UP_ON', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_WARM_UP_INVALID', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1244,
  serialized_end=1331,
)
_sym_db.RegisterEnumDescriptor(_HEATINGSTATUS_BTRYWARMUPSTATUS)


_HEATINGSTATUS = _descriptor.Descriptor(
  name='HeatingStatus',
  full_name='HeatingStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='steer_wheel_heat_sts', full_name='HeatingStatus.steer_wheel_heat_sts', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_heat_frnt_le_sts', full_name='HeatingStatus.seat_heat_frnt_le_sts', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_heat_frnt_ri_sts', full_name='HeatingStatus.seat_heat_frnt_ri_sts', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_heat_re_le_sts', full_name='HeatingStatus.seat_heat_re_le_sts', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_heat_re_ri_sts', full_name='HeatingStatus.seat_heat_re_ri_sts', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hv_batt_pre_sts', full_name='HeatingStatus.hv_batt_pre_sts', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_vent_frnt_le_sts', full_name='HeatingStatus.seat_vent_frnt_le_sts', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_vent_frnt_ri_sts', full_name='HeatingStatus.seat_vent_frnt_ri_sts', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='btry_warm_up_sts', full_name='HeatingStatus.btry_warm_up_sts', index=8,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_vent_re_le_sts', full_name='HeatingStatus.seat_vent_re_le_sts', index=9,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seat_vent_re_ri_sts', full_name='HeatingStatus.seat_vent_re_ri_sts', index=10,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HEATINGSTATUS_STEERWHEELHEATINGSTATUS,
    _HEATINGSTATUS_SEATHEATINGSTATUS,
    _HEATINGSTATUS_HVBATTHEATINGSTATUS,
    _HEATINGSTATUS_SEATVENTSTATUS,
    _HEATINGSTATUS_BTRYWARMUPSTATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=1331,
)

_HEATINGSTATUS.fields_by_name['steer_wheel_heat_sts'].enum_type = _HEATINGSTATUS_STEERWHEELHEATINGSTATUS
_HEATINGSTATUS.fields_by_name['seat_heat_frnt_le_sts'].enum_type = _HEATINGSTATUS_SEATHEATINGSTATUS
_HEATINGSTATUS.fields_by_name['seat_heat_frnt_ri_sts'].enum_type = _HEATINGSTATUS_SEATHEATINGSTATUS
_HEATINGSTATUS.fields_by_name['seat_heat_re_le_sts'].enum_type = _HEATINGSTATUS_SEATHEATINGSTATUS
_HEATINGSTATUS.fields_by_name['seat_heat_re_ri_sts'].enum_type = _HEATINGSTATUS_SEATHEATINGSTATUS
_HEATINGSTATUS.fields_by_name['hv_batt_pre_sts'].enum_type = _HEATINGSTATUS_HVBATTHEATINGSTATUS
_HEATINGSTATUS.fields_by_name['seat_vent_frnt_le_sts'].enum_type = _HEATINGSTATUS_SEATVENTSTATUS
_HEATINGSTATUS.fields_by_name['seat_vent_frnt_ri_sts'].enum_type = _HEATINGSTATUS_SEATVENTSTATUS
_HEATINGSTATUS.fields_by_name['btry_warm_up_sts'].enum_type = _HEATINGSTATUS_BTRYWARMUPSTATUS
_HEATINGSTATUS.fields_by_name['seat_vent_re_le_sts'].enum_type = _HEATINGSTATUS_SEATVENTSTATUS
_HEATINGSTATUS.fields_by_name['seat_vent_re_ri_sts'].enum_type = _HEATINGSTATUS_SEATVENTSTATUS
_HEATINGSTATUS_STEERWHEELHEATINGSTATUS.containing_type = _HEATINGSTATUS
_HEATINGSTATUS_SEATHEATINGSTATUS.containing_type = _HEATINGSTATUS
_HEATINGSTATUS_HVBATTHEATINGSTATUS.containing_type = _HEATINGSTATUS
_HEATINGSTATUS_SEATVENTSTATUS.containing_type = _HEATINGSTATUS
_HEATINGSTATUS_BTRYWARMUPSTATUS.containing_type = _HEATINGSTATUS
DESCRIPTOR.message_types_by_name['HeatingStatus'] = _HEATINGSTATUS

HeatingStatus = _reflection.GeneratedProtocolMessageType('HeatingStatus', (_message.Message,), dict(
  DESCRIPTOR = _HEATINGSTATUS,
  __module__ = 'heating_status_pb2'
  # @@protoc_insertion_point(class_scope:HeatingStatus)
  ))
_sym_db.RegisterMessage(HeatingStatus)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.customB\021HeatingStatusUnit'))
# @@protoc_insertion_point(module_scope)
