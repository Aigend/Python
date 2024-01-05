# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: driving_motor.proto

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
  name='driving_motor.proto',
  package='',
  serialized_pb=_b('\n\x13\x64riving_motor.proto\"\xbe\x04\n\x0c\x44rivingMotor\x12/\n\nmotor_list\x18\x01 \x03(\x0b\x32\x1b.DrivingMotor.MotorDataUnit\x12\x13\n\x0bpwr_sys_rdy\x18\x02 \x01(\x08\x1a\xe7\x03\n\rMotorDataUnit\x12\x12\n\ndrvmotr_sn\x18\x01 \x01(\x05\x12\x41\n\x0b\x64rvmotr_sts\x18\x02 \x01(\x0e\x32,.DrivingMotor.MotorDataUnit.DriveMotorStatus\x12\x1a\n\x12\x64rvmotr_cntrl_temp\x18\x03 \x01(\x11\x12\x18\n\x10\x64rvmotr_rotn_spd\x18\x04 \x01(\x11\x12\x19\n\x11\x64rvmotr_rotn_torq\x18\x05 \x01(\x02\x12\x14\n\x0c\x64rvmotr_temp\x18\x06 \x01(\x11\x12\x1c\n\x14\x64rvmotr_contl_involt\x18\x07 \x01(\x02\x12\"\n\x1a\x64rvmotr_contl_dc_bus_curnt\x18\x08 \x01(\x02\x12\x14\n\x0ctorq_command\x18\t \x01(\x02\x12\x17\n\x0fmax_pos_torq_st\x18\n \x01(\x02\x12\x17\n\x0fmax_neg_torq_st\x18\x0b \x01(\x02\"\x8d\x01\n\x10\x44riveMotorStatus\x12\x16\n\x12\x45NERGY_CONSUMPTION\x10\x01\x12\x15\n\x11\x45NERGY_GENERATION\x10\x02\x12\x16\n\x12STATUSOF_SHUT_DOWN\x10\x03\x12\x12\n\x0eSTATUSOF_READY\x10\x04\x12\x10\n\x0bMALFUNCTION\x10\xfe\x01\x12\x0c\n\x07INVALID\x10\xff\x01\x42\x37\n#com.nextev.cvs_proto.protobuf.gb_dbB\x10\x44rivingMotorUnit')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_DRIVINGMOTOR_MOTORDATAUNIT_DRIVEMOTORSTATUS = _descriptor.EnumDescriptor(
  name='DriveMotorStatus',
  full_name='DrivingMotor.MotorDataUnit.DriveMotorStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ENERGY_CONSUMPTION', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENERGY_GENERATION', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATUSOF_SHUT_DOWN', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STATUSOF_READY', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MALFUNCTION', index=4, number=254,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID', index=5, number=255,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=457,
  serialized_end=598,
)
_sym_db.RegisterEnumDescriptor(_DRIVINGMOTOR_MOTORDATAUNIT_DRIVEMOTORSTATUS)


_DRIVINGMOTOR_MOTORDATAUNIT = _descriptor.Descriptor(
  name='MotorDataUnit',
  full_name='DrivingMotor.MotorDataUnit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='drvmotr_sn', full_name='DrivingMotor.MotorDataUnit.drvmotr_sn', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drvmotr_sts', full_name='DrivingMotor.MotorDataUnit.drvmotr_sts', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drvmotr_cntrl_temp', full_name='DrivingMotor.MotorDataUnit.drvmotr_cntrl_temp', index=2,
      number=3, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drvmotr_rotn_spd', full_name='DrivingMotor.MotorDataUnit.drvmotr_rotn_spd', index=3,
      number=4, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drvmotr_rotn_torq', full_name='DrivingMotor.MotorDataUnit.drvmotr_rotn_torq', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drvmotr_temp', full_name='DrivingMotor.MotorDataUnit.drvmotr_temp', index=5,
      number=6, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drvmotr_contl_involt', full_name='DrivingMotor.MotorDataUnit.drvmotr_contl_involt', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='drvmotr_contl_dc_bus_curnt', full_name='DrivingMotor.MotorDataUnit.drvmotr_contl_dc_bus_curnt', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='torq_command', full_name='DrivingMotor.MotorDataUnit.torq_command', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_pos_torq_st', full_name='DrivingMotor.MotorDataUnit.max_pos_torq_st', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='max_neg_torq_st', full_name='DrivingMotor.MotorDataUnit.max_neg_torq_st', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DRIVINGMOTOR_MOTORDATAUNIT_DRIVEMOTORSTATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=111,
  serialized_end=598,
)

_DRIVINGMOTOR = _descriptor.Descriptor(
  name='DrivingMotor',
  full_name='DrivingMotor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='motor_list', full_name='DrivingMotor.motor_list', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pwr_sys_rdy', full_name='DrivingMotor.pwr_sys_rdy', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DRIVINGMOTOR_MOTORDATAUNIT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=598,
)

_DRIVINGMOTOR_MOTORDATAUNIT.fields_by_name['drvmotr_sts'].enum_type = _DRIVINGMOTOR_MOTORDATAUNIT_DRIVEMOTORSTATUS
_DRIVINGMOTOR_MOTORDATAUNIT.containing_type = _DRIVINGMOTOR
_DRIVINGMOTOR_MOTORDATAUNIT_DRIVEMOTORSTATUS.containing_type = _DRIVINGMOTOR_MOTORDATAUNIT
_DRIVINGMOTOR.fields_by_name['motor_list'].message_type = _DRIVINGMOTOR_MOTORDATAUNIT
DESCRIPTOR.message_types_by_name['DrivingMotor'] = _DRIVINGMOTOR

DrivingMotor = _reflection.GeneratedProtocolMessageType('DrivingMotor', (_message.Message,), dict(

  MotorDataUnit = _reflection.GeneratedProtocolMessageType('MotorDataUnit', (_message.Message,), dict(
    DESCRIPTOR = _DRIVINGMOTOR_MOTORDATAUNIT,
    __module__ = 'driving_motor_pb2'
    # @@protoc_insertion_point(class_scope:DrivingMotor.MotorDataUnit)
    ))
  ,
  DESCRIPTOR = _DRIVINGMOTOR,
  __module__ = 'driving_motor_pb2'
  # @@protoc_insertion_point(class_scope:DrivingMotor)
  ))
_sym_db.RegisterMessage(DrivingMotor)
_sym_db.RegisterMessage(DrivingMotor.MotorDataUnit)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n#com.nextev.cvs_proto.protobuf.gb_dbB\020DrivingMotorUnit'))
# @@protoc_insertion_point(module_scope)