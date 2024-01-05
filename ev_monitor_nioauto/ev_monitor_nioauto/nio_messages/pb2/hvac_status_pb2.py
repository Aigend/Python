# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hvac_status.proto

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
  name='hvac_status.proto',
  package='',
  serialized_pb=_b('\n\x11hvac_status.proto\"\xc3\x05\n\nHVACStatus\x12\x12\n\namb_temp_c\x18\x01 \x01(\x02\x12\x16\n\x0eoutside_temp_c\x18\x02 \x01(\x02\x12\x12\n\nair_con_on\x18\x03 \x01(\x08\x12\x14\n\x0cpm_2p5_cabin\x18\x04 \x01(\x05\x12\x1c\n\x14pm_2p5_filter_active\x18\x05 \x01(\x08\x12*\n\x0b\x63\x62n_pre_sts\x18\x06 \x01(\x0e\x32\x15.HVACStatus.CbnPreSts\x12=\n\x16\x63\x63u_cbn_pre_ac_ena_sts\x18\x07 \x01(\x0e\x32\x1d.HVACStatus.CCUCbnPreACEnaSts\x12?\n\x17\x63\x63u_cbn_pre_aqs_ena_sts\x18\x08 \x01(\x0e\x32\x1e.HVACStatus.CCUCbnPreAQSEnaSts\x12\x32\n\x10\x63\x62n_hi_t_dry_sts\x18\t \x01(\x0e\x32\x18.HVACStatus.CbnHiTDrySts\x12;\n\x12\x63\x63u_max_defrst_sts\x18\n \x01(\x0e\x32\x1f.HVACStatus.CCUMaxDefrstLampReq\"O\n\tCbnPreSts\x12\x07\n\x03OFF\x10\x00\x12\x06\n\x02ON\x10\x01\x12#\n\x1f\x43\x41LCULATE_ESTIMATED_TIME_STATUS\x10\x02\x12\x0c\n\x08RESERVED\x10\x03\"2\n\x11\x43\x43UCbnPreACEnaSts\x12\x0e\n\nDISABLE_AC\x10\x00\x12\r\n\tENABLE_AC\x10\x01\"5\n\x12\x43\x43UCbnPreAQSEnaSts\x12\x0f\n\x0b\x44ISABLE_AQS\x10\x00\x12\x0e\n\nENABLE_AQS\x10\x01\"6\n\x0c\x43\x62nHiTDrySts\x12\x0b\n\x07\x44RY_OFF\x10\x00\x12\n\n\x06\x44RY_ON\x10\x01\x12\r\n\tDRY_ERROR\x10\x02\"0\n\x13\x43\x43UMaxDefrstLampReq\x12\x0c\n\x08LAMP_OFF\x10\x00\x12\x0b\n\x07LAMP_ON\x10\x01\x42\x36\n$com.nextev.cvs_proto.protobuf.customB\x0eHVACStatusUnit')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_HVACSTATUS_CBNPRESTS = _descriptor.EnumDescriptor(
  name='CbnPreSts',
  full_name='HVACStatus.CbnPreSts',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OFF', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ON', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CALCULATE_ESTIMATED_TIME_STATUS', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESERVED', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=437,
  serialized_end=516,
)
_sym_db.RegisterEnumDescriptor(_HVACSTATUS_CBNPRESTS)

_HVACSTATUS_CCUCBNPREACENASTS = _descriptor.EnumDescriptor(
  name='CCUCbnPreACEnaSts',
  full_name='HVACStatus.CCUCbnPreACEnaSts',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DISABLE_AC', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENABLE_AC', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=518,
  serialized_end=568,
)
_sym_db.RegisterEnumDescriptor(_HVACSTATUS_CCUCBNPREACENASTS)

_HVACSTATUS_CCUCBNPREAQSENASTS = _descriptor.EnumDescriptor(
  name='CCUCbnPreAQSEnaSts',
  full_name='HVACStatus.CCUCbnPreAQSEnaSts',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DISABLE_AQS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ENABLE_AQS', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=570,
  serialized_end=623,
)
_sym_db.RegisterEnumDescriptor(_HVACSTATUS_CCUCBNPREAQSENASTS)

_HVACSTATUS_CBNHITDRYSTS = _descriptor.EnumDescriptor(
  name='CbnHiTDrySts',
  full_name='HVACStatus.CbnHiTDrySts',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DRY_OFF', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DRY_ON', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DRY_ERROR', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=625,
  serialized_end=679,
)
_sym_db.RegisterEnumDescriptor(_HVACSTATUS_CBNHITDRYSTS)

_HVACSTATUS_CCUMAXDEFRSTLAMPREQ = _descriptor.EnumDescriptor(
  name='CCUMaxDefrstLampReq',
  full_name='HVACStatus.CCUMaxDefrstLampReq',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LAMP_OFF', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LAMP_ON', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=681,
  serialized_end=729,
)
_sym_db.RegisterEnumDescriptor(_HVACSTATUS_CCUMAXDEFRSTLAMPREQ)


_HVACSTATUS = _descriptor.Descriptor(
  name='HVACStatus',
  full_name='HVACStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='amb_temp_c', full_name='HVACStatus.amb_temp_c', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='outside_temp_c', full_name='HVACStatus.outside_temp_c', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='air_con_on', full_name='HVACStatus.air_con_on', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pm_2p5_cabin', full_name='HVACStatus.pm_2p5_cabin', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pm_2p5_filter_active', full_name='HVACStatus.pm_2p5_filter_active', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cbn_pre_sts', full_name='HVACStatus.cbn_pre_sts', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ccu_cbn_pre_ac_ena_sts', full_name='HVACStatus.ccu_cbn_pre_ac_ena_sts', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ccu_cbn_pre_aqs_ena_sts', full_name='HVACStatus.ccu_cbn_pre_aqs_ena_sts', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cbn_hi_t_dry_sts', full_name='HVACStatus.cbn_hi_t_dry_sts', index=8,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ccu_max_defrst_sts', full_name='HVACStatus.ccu_max_defrst_sts', index=9,
      number=10, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HVACSTATUS_CBNPRESTS,
    _HVACSTATUS_CCUCBNPREACENASTS,
    _HVACSTATUS_CCUCBNPREAQSENASTS,
    _HVACSTATUS_CBNHITDRYSTS,
    _HVACSTATUS_CCUMAXDEFRSTLAMPREQ,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=729,
)

_HVACSTATUS.fields_by_name['cbn_pre_sts'].enum_type = _HVACSTATUS_CBNPRESTS
_HVACSTATUS.fields_by_name['ccu_cbn_pre_ac_ena_sts'].enum_type = _HVACSTATUS_CCUCBNPREACENASTS
_HVACSTATUS.fields_by_name['ccu_cbn_pre_aqs_ena_sts'].enum_type = _HVACSTATUS_CCUCBNPREAQSENASTS
_HVACSTATUS.fields_by_name['cbn_hi_t_dry_sts'].enum_type = _HVACSTATUS_CBNHITDRYSTS
_HVACSTATUS.fields_by_name['ccu_max_defrst_sts'].enum_type = _HVACSTATUS_CCUMAXDEFRSTLAMPREQ
_HVACSTATUS_CBNPRESTS.containing_type = _HVACSTATUS
_HVACSTATUS_CCUCBNPREACENASTS.containing_type = _HVACSTATUS
_HVACSTATUS_CCUCBNPREAQSENASTS.containing_type = _HVACSTATUS
_HVACSTATUS_CBNHITDRYSTS.containing_type = _HVACSTATUS
_HVACSTATUS_CCUMAXDEFRSTLAMPREQ.containing_type = _HVACSTATUS
DESCRIPTOR.message_types_by_name['HVACStatus'] = _HVACSTATUS

HVACStatus = _reflection.GeneratedProtocolMessageType('HVACStatus', (_message.Message,), dict(
  DESCRIPTOR = _HVACSTATUS,
  __module__ = 'hvac_status_pb2'
  # @@protoc_insertion_point(class_scope:HVACStatus)
  ))
_sym_db.RegisterMessage(HVACStatus)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.customB\016HVACStatusUnit'))
# @@protoc_insertion_point(module_scope)
