# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: alarm_data.proto

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
  name='alarm_data.proto',
  package='',
  serialized_pb=_b('\n\x10\x61larm_data.proto\"\xaa\x0c\n\tAlarmData\x12\x30\n\x0e\x63ommon_failure\x18\x01 \x03(\x0b\x32\x18.AlarmData.CommonFailure\x12(\n\x0c\x62j_extension\x18\x02 \x03(\x0b\x32\x12.AlarmData.BJAlarm\x12(\n\x0csh_extension\x18\x03 \x03(\x0b\x32\x12.AlarmData.SHAlarm\x1ai\n\rCommonFailure\x12,\n\talarm_tag\x18\x01 \x01(\x0e\x32\x19.AlarmData.CommonAlarmTag\x12*\n\x0b\x61larm_level\x18\x02 \x01(\x0e\x32\x15.AlarmData.AlarmLevel\x1a_\n\x07\x42JAlarm\x12(\n\talarm_tag\x18\x01 \x01(\x0e\x32\x15.AlarmData.BJAlarmTag\x12*\n\x0b\x61larm_level\x18\x02 \x01(\x0e\x32\x15.AlarmData.AlarmLevel\x1a_\n\x07SHAlarm\x12(\n\talarm_tag\x18\x01 \x01(\x0e\x32\x15.AlarmData.SHAlarmTag\x12*\n\x0b\x61larm_level\x18\x02 \x01(\x0e\x32\x15.AlarmData.AlarmLevel\"y\n\nAlarmLevel\x12\x0e\n\nNO_FAILURE\x10\x00\x12\x0b\n\x07LEVEL_1\x10\x01\x12\x0b\n\x07LEVEL_2\x10\x02\x12\x0b\n\x07LEVEL_3\x10\x03\x12\x1a\n\x15\x41LARM_LEVEL_EXCEPTION\x10\xfe\x01\x12\x18\n\x13\x41LARM_LEVEL_INVALID\x10\xff\x01\"\xe4\x03\n\x0e\x43ommonAlarmTag\x12\x16\n\x12\x42TRY_TEMP_DIF_ALRM\x10\x00\x12\x15\n\x11\x42TRY_HI_TEMP_ALRM\x10\x01\x12\x1b\n\x17OVER_VOLT_BTRY_PAK_ALRM\x10\x02\x12\x1b\n\x17UNDR_VOLT_BTRY_PAK_ALRM\x10\x03\x12\x0f\n\x0bLW_SOC_ALRM\x10\x04\x12\x1d\n\x19OVER_VOLT_SINGL_BTRY_ALRM\x10\x05\x12\x1d\n\x19UNDR_VOLT_SINGL_BTRY_ALRM\x10\x06\x12\x14\n\x10OVER_HI_SOC_ALRM\x10\x07\x12\x15\n\x11SOC_JMP_CHNG_ALRM\x10\x08\x12\x19\n\x15\x42TRY_PAK_MISMTCH_ALRM\x10\t\x12\x1c\n\x18\x42TRY_PAK_BAD_CONSIS_ALRM\x10\n\x12\x11\n\rINSULATN_ALRM\x10\x0b\x12\x12\n\x0e\x44\x43\x44\x43_TEMP_ALRM\x10\x0c\x12\x10\n\x0c\x42RK_SYS_ALRM\x10\r\x12\x11\n\rDCDC_STS_ALRM\x10\x0e\x12\x1b\n\x17\x44RVMOTR_CNTRL_TEMP_ALRM\x10\x0f\x12\x1b\n\x17HI_VOLT_INTRLK_STS_ALRM\x10\x10\x12\x15\n\x11\x44RVMOTR_TEMP_ALRM\x10\x11\x12\x17\n\x13\x42TRY_OVER_CHRG_ALRM\x10\x12\"\xaf\x01\n\nSHAlarmTag\x12\x15\n\x11\x44RV_SYS_FAIL_ALRM\x10\x00\x12\x17\n\x13\x42TRY_TOTL_VOLT_ALRM\x10\x01\x12\x1d\n\x19SINGL_BTRY_HIST_TEMP_ALRM\x10\x02\x12\x1d\n\x19SINGL_BTRY_LWST_TEMP_ALRM\x10\x03\x12\x15\n\x11\x43OLLISN_SIGNL_STS\x10\x04\x12\x1c\n\x18POWR_STORE_FAILR_INDICTN\x10\x05\"\xd5\x02\n\nBJAlarmTag\x12\x1a\n\x16VEHICLE_CAN_COMMU_ALRM\x10\x00\x12\x19\n\x15\x43HARGE_STATE_ERR_ALRM\x10\x01\x12!\n\x1d\x43HARGE_COMMUNICATION_ERR_ALRM\x10\x02\x12\x17\n\x13\x42TRY_CAN_COMMU_ALRM\x10\x03\x12$\n BTRY_TOTAL_CURNT_OVER_CURNT_ALRM\x10\x04\x12\x18\n\x14\x43HARGE_CONN_ERR_ALRM\x10\x05\x12\x1a\n\x16VEHICLE_CHAGE_ERR_ALRM\x10\x06\x12\x18\n\x14\x42TRY_HI_TEMP_ALRM_BJ\x10\x07\x12\x17\n\x13MOTR_CAN_COMMU_ALRM\x10\x08\x12$\n DRV_MOTR_ROTATE_SPD_OVER_HI_ALRM\x10\t\x12\x1f\n\x1b\x44RV_MOTR_CURNT_OVER_HI_ALRM\x10\nB4\n#com.nextev.cvs_proto.protobuf.gb_dbB\rAlarmDataUnit')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_ALARMDATA_ALARMLEVEL = _descriptor.EnumDescriptor(
  name='AlarmLevel',
  full_name='AlarmData.AlarmLevel',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NO_FAILURE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEVEL_1', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEVEL_2', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEVEL_3', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ALARM_LEVEL_EXCEPTION', index=4, number=254,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ALARM_LEVEL_INVALID', index=5, number=255,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=469,
  serialized_end=590,
)
_sym_db.RegisterEnumDescriptor(_ALARMDATA_ALARMLEVEL)

_ALARMDATA_COMMONALARMTAG = _descriptor.EnumDescriptor(
  name='CommonAlarmTag',
  full_name='AlarmData.CommonAlarmTag',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BTRY_TEMP_DIF_ALRM', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_HI_TEMP_ALRM', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OVER_VOLT_BTRY_PAK_ALRM', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNDR_VOLT_BTRY_PAK_ALRM', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LW_SOC_ALRM', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OVER_VOLT_SINGL_BTRY_ALRM', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNDR_VOLT_SINGL_BTRY_ALRM', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OVER_HI_SOC_ALRM', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SOC_JMP_CHNG_ALRM', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_PAK_MISMTCH_ALRM', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_PAK_BAD_CONSIS_ALRM', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INSULATN_ALRM', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DCDC_TEMP_ALRM', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BRK_SYS_ALRM', index=13, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DCDC_STS_ALRM', index=14, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DRVMOTR_CNTRL_TEMP_ALRM', index=15, number=15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HI_VOLT_INTRLK_STS_ALRM', index=16, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DRVMOTR_TEMP_ALRM', index=17, number=17,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_OVER_CHRG_ALRM', index=18, number=18,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=593,
  serialized_end=1077,
)
_sym_db.RegisterEnumDescriptor(_ALARMDATA_COMMONALARMTAG)

_ALARMDATA_SHALARMTAG = _descriptor.EnumDescriptor(
  name='SHAlarmTag',
  full_name='AlarmData.SHAlarmTag',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DRV_SYS_FAIL_ALRM', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_TOTL_VOLT_ALRM', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SINGL_BTRY_HIST_TEMP_ALRM', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SINGL_BTRY_LWST_TEMP_ALRM', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COLLISN_SIGNL_STS', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POWR_STORE_FAILR_INDICTN', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1080,
  serialized_end=1255,
)
_sym_db.RegisterEnumDescriptor(_ALARMDATA_SHALARMTAG)

_ALARMDATA_BJALARMTAG = _descriptor.EnumDescriptor(
  name='BJAlarmTag',
  full_name='AlarmData.BJAlarmTag',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='VEHICLE_CAN_COMMU_ALRM', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHARGE_STATE_ERR_ALRM', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHARGE_COMMUNICATION_ERR_ALRM', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_CAN_COMMU_ALRM', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_TOTAL_CURNT_OVER_CURNT_ALRM', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHARGE_CONN_ERR_ALRM', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VEHICLE_CHAGE_ERR_ALRM', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BTRY_HI_TEMP_ALRM_BJ', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MOTR_CAN_COMMU_ALRM', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DRV_MOTR_ROTATE_SPD_OVER_HI_ALRM', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DRV_MOTR_CURNT_OVER_HI_ALRM', index=10, number=10,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1258,
  serialized_end=1599,
)
_sym_db.RegisterEnumDescriptor(_ALARMDATA_BJALARMTAG)


_ALARMDATA_COMMONFAILURE = _descriptor.Descriptor(
  name='CommonFailure',
  full_name='AlarmData.CommonFailure',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='alarm_tag', full_name='AlarmData.CommonFailure.alarm_tag', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='alarm_level', full_name='AlarmData.CommonFailure.alarm_level', index=1,
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
  serialized_start=168,
  serialized_end=273,
)

_ALARMDATA_BJALARM = _descriptor.Descriptor(
  name='BJAlarm',
  full_name='AlarmData.BJAlarm',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='alarm_tag', full_name='AlarmData.BJAlarm.alarm_tag', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='alarm_level', full_name='AlarmData.BJAlarm.alarm_level', index=1,
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
  serialized_start=275,
  serialized_end=370,
)

_ALARMDATA_SHALARM = _descriptor.Descriptor(
  name='SHAlarm',
  full_name='AlarmData.SHAlarm',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='alarm_tag', full_name='AlarmData.SHAlarm.alarm_tag', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='alarm_level', full_name='AlarmData.SHAlarm.alarm_level', index=1,
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
  serialized_start=372,
  serialized_end=467,
)

_ALARMDATA = _descriptor.Descriptor(
  name='AlarmData',
  full_name='AlarmData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='common_failure', full_name='AlarmData.common_failure', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bj_extension', full_name='AlarmData.bj_extension', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sh_extension', full_name='AlarmData.sh_extension', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_ALARMDATA_COMMONFAILURE, _ALARMDATA_BJALARM, _ALARMDATA_SHALARM, ],
  enum_types=[
    _ALARMDATA_ALARMLEVEL,
    _ALARMDATA_COMMONALARMTAG,
    _ALARMDATA_SHALARMTAG,
    _ALARMDATA_BJALARMTAG,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=1599,
)

_ALARMDATA_COMMONFAILURE.fields_by_name['alarm_tag'].enum_type = _ALARMDATA_COMMONALARMTAG
_ALARMDATA_COMMONFAILURE.fields_by_name['alarm_level'].enum_type = _ALARMDATA_ALARMLEVEL
_ALARMDATA_COMMONFAILURE.containing_type = _ALARMDATA
_ALARMDATA_BJALARM.fields_by_name['alarm_tag'].enum_type = _ALARMDATA_BJALARMTAG
_ALARMDATA_BJALARM.fields_by_name['alarm_level'].enum_type = _ALARMDATA_ALARMLEVEL
_ALARMDATA_BJALARM.containing_type = _ALARMDATA
_ALARMDATA_SHALARM.fields_by_name['alarm_tag'].enum_type = _ALARMDATA_SHALARMTAG
_ALARMDATA_SHALARM.fields_by_name['alarm_level'].enum_type = _ALARMDATA_ALARMLEVEL
_ALARMDATA_SHALARM.containing_type = _ALARMDATA
_ALARMDATA.fields_by_name['common_failure'].message_type = _ALARMDATA_COMMONFAILURE
_ALARMDATA.fields_by_name['bj_extension'].message_type = _ALARMDATA_BJALARM
_ALARMDATA.fields_by_name['sh_extension'].message_type = _ALARMDATA_SHALARM
_ALARMDATA_ALARMLEVEL.containing_type = _ALARMDATA
_ALARMDATA_COMMONALARMTAG.containing_type = _ALARMDATA
_ALARMDATA_SHALARMTAG.containing_type = _ALARMDATA
_ALARMDATA_BJALARMTAG.containing_type = _ALARMDATA
DESCRIPTOR.message_types_by_name['AlarmData'] = _ALARMDATA

AlarmData = _reflection.GeneratedProtocolMessageType('AlarmData', (_message.Message,), dict(

  CommonFailure = _reflection.GeneratedProtocolMessageType('CommonFailure', (_message.Message,), dict(
    DESCRIPTOR = _ALARMDATA_COMMONFAILURE,
    __module__ = 'alarm_data_pb2'
    # @@protoc_insertion_point(class_scope:AlarmData.CommonFailure)
    ))
  ,

  BJAlarm = _reflection.GeneratedProtocolMessageType('BJAlarm', (_message.Message,), dict(
    DESCRIPTOR = _ALARMDATA_BJALARM,
    __module__ = 'alarm_data_pb2'
    # @@protoc_insertion_point(class_scope:AlarmData.BJAlarm)
    ))
  ,

  SHAlarm = _reflection.GeneratedProtocolMessageType('SHAlarm', (_message.Message,), dict(
    DESCRIPTOR = _ALARMDATA_SHALARM,
    __module__ = 'alarm_data_pb2'
    # @@protoc_insertion_point(class_scope:AlarmData.SHAlarm)
    ))
  ,
  DESCRIPTOR = _ALARMDATA,
  __module__ = 'alarm_data_pb2'
  # @@protoc_insertion_point(class_scope:AlarmData)
  ))
_sym_db.RegisterMessage(AlarmData)
_sym_db.RegisterMessage(AlarmData.CommonFailure)
_sym_db.RegisterMessage(AlarmData.BJAlarm)
_sym_db.RegisterMessage(AlarmData.SHAlarm)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n#com.nextev.cvs_proto.protobuf.gb_dbB\rAlarmDataUnit'))
# @@protoc_insertion_point(module_scope)