# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: driving_data.proto

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
  name='driving_data.proto',
  package='',
  serialized_pb=_b('\n\x12\x64riving_data.proto\"\x9c\x05\n\x0b\x44rivingData\x12-\n\x0cvcu_drvg_mod\x18\x01 \x01(\x0e\x32\x17.DrivingData.VehDrvgMod\x12\x19\n\x11steer_whl_rotn_ag\x18\x02 \x01(\x02\x12\x1a\n\x12steer_whl_rotn_spd\x18\x03 \x01(\x11\x12\x19\n\x11\x61\x63lrtn_pedal_posn\x18\x04 \x01(\x02\x12\x32\n\rbrk_pedal_sts\x18\x05 \x01(\x0b\x32\x1b.DrivingData.BrkPedalStatus\x12\x15\n\raverage_speed\x18\x06 \x01(\x02\x12\x11\n\tmax_speed\x18\x07 \x01(\x02\x12\x11\n\tmin_speed\x18\x08 \x01(\x02\x12\x15\n\rveh_dispd_spd\x18\t \x01(\x02\x12\x14\n\x0cveh_outd_hum\x18\n \x01(\x05\x12\x19\n\x11veh_dispd_spd_sts\x18\x0b \x01(\x05\x1a\x66\n\x0e\x42rkPedalStatus\x12)\n\x05state\x18\x01 \x01(\x0e\x32\x1a.DrivingData.BrkPedalState\x12)\n\x05valid\x18\x02 \x01(\x0e\x32\x1a.DrivingData.BrkPedalValid\"G\n\rBrkPedalState\x12\x0f\n\x0bNOT_PRESSED\x10\x00\x12\x0b\n\x07PRESSED\x10\x01\x12\r\n\tRESERVERD\x10\x02\x12\t\n\x05\x45RROR\x10\x03\"7\n\rBrkPedalValid\x12\x11\n\rBRK_PED_VALID\x10\x00\x12\x13\n\x0f\x42RK_PED_INVALID\x10\x01\"i\n\nVehDrvgMod\x12\x12\n\x0e\x41UTOMATIC_MODE\x10\x00\x12\x10\n\x0c\x45\x43ONOMY_MODE\x10\x01\x12\x10\n\x0c\x43OMFORT_MODE\x10\x02\x12\x0e\n\nSPORT_MODE\x10\x03\x12\x13\n\x0f\x44RV_MOD_INVALID\x10\x07\x42\x37\n$com.nextev.cvs_proto.protobuf.customB\x0f\x44rivingDataUnit')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_DRIVINGDATA_BRKPEDALSTATE = _descriptor.EnumDescriptor(
  name='BrkPedalState',
  full_name='DrivingData.BrkPedalState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NOT_PRESSED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRESSED', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESERVERD', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=456,
  serialized_end=527,
)
_sym_db.RegisterEnumDescriptor(_DRIVINGDATA_BRKPEDALSTATE)

_DRIVINGDATA_BRKPEDALVALID = _descriptor.EnumDescriptor(
  name='BrkPedalValid',
  full_name='DrivingData.BrkPedalValid',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BRK_PED_VALID', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BRK_PED_INVALID', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=529,
  serialized_end=584,
)
_sym_db.RegisterEnumDescriptor(_DRIVINGDATA_BRKPEDALVALID)

_DRIVINGDATA_VEHDRVGMOD = _descriptor.EnumDescriptor(
  name='VehDrvgMod',
  full_name='DrivingData.VehDrvgMod',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='AUTOMATIC_MODE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ECONOMY_MODE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COMFORT_MODE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SPORT_MODE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DRV_MOD_INVALID', index=4, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=586,
  serialized_end=691,
)
_sym_db.RegisterEnumDescriptor(_DRIVINGDATA_VEHDRVGMOD)


_DRIVINGDATA_BRKPEDALSTATUS = _descriptor.Descriptor(
  name='BrkPedalStatus',
  full_name='DrivingData.BrkPedalStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='DrivingData.BrkPedalStatus.state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='valid', full_name='DrivingData.BrkPedalStatus.valid', index=1,
      number=2, type=14, cpp_type=8, label=1,
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
  serialized_start=352,
  serialized_end=454,
)

_DRIVINGDATA = _descriptor.Descriptor(
  name='DrivingData',
  full_name='DrivingData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vcu_drvg_mod', full_name='DrivingData.vcu_drvg_mod', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='steer_whl_rotn_ag', full_name='DrivingData.steer_whl_rotn_ag', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='steer_whl_rotn_spd', full_name='DrivingData.steer_whl_rotn_spd', index=2,
      number=3, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='aclrtn_pedal_posn', full_name='DrivingData.aclrtn_pedal_posn', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='brk_pedal_sts', full_name='DrivingData.brk_pedal_sts', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='average_speed', full_name='DrivingData.average_speed', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_speed', full_name='DrivingData.max_speed', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='min_speed', full_name='DrivingData.min_speed', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='veh_dispd_spd', full_name='DrivingData.veh_dispd_spd', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='veh_outd_hum', full_name='DrivingData.veh_outd_hum', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='veh_dispd_spd_sts', full_name='DrivingData.veh_dispd_spd_sts', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DRIVINGDATA_BRKPEDALSTATUS, ],
  enum_types=[
    _DRIVINGDATA_BRKPEDALSTATE,
    _DRIVINGDATA_BRKPEDALVALID,
    _DRIVINGDATA_VEHDRVGMOD,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=691,
)

_DRIVINGDATA_BRKPEDALSTATUS.fields_by_name['state'].enum_type = _DRIVINGDATA_BRKPEDALSTATE
_DRIVINGDATA_BRKPEDALSTATUS.fields_by_name['valid'].enum_type = _DRIVINGDATA_BRKPEDALVALID
_DRIVINGDATA_BRKPEDALSTATUS.containing_type = _DRIVINGDATA
_DRIVINGDATA.fields_by_name['vcu_drvg_mod'].enum_type = _DRIVINGDATA_VEHDRVGMOD
_DRIVINGDATA.fields_by_name['brk_pedal_sts'].message_type = _DRIVINGDATA_BRKPEDALSTATUS
_DRIVINGDATA_BRKPEDALSTATE.containing_type = _DRIVINGDATA
_DRIVINGDATA_BRKPEDALVALID.containing_type = _DRIVINGDATA
_DRIVINGDATA_VEHDRVGMOD.containing_type = _DRIVINGDATA
DESCRIPTOR.message_types_by_name['DrivingData'] = _DRIVINGDATA

DrivingData = _reflection.GeneratedProtocolMessageType('DrivingData', (_message.Message,), dict(

  BrkPedalStatus = _reflection.GeneratedProtocolMessageType('BrkPedalStatus', (_message.Message,), dict(
    DESCRIPTOR = _DRIVINGDATA_BRKPEDALSTATUS,
    __module__ = 'driving_data_pb2'
    # @@protoc_insertion_point(class_scope:DrivingData.BrkPedalStatus)
    ))
  ,
  DESCRIPTOR = _DRIVINGDATA,
  __module__ = 'driving_data_pb2'
  # @@protoc_insertion_point(class_scope:DrivingData)
  ))
_sym_db.RegisterMessage(DrivingData)
_sym_db.RegisterMessage(DrivingData.BrkPedalStatus)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.customB\017DrivingDataUnit'))
# @@protoc_insertion_point(module_scope)
