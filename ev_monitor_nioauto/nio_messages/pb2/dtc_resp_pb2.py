# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dtc_resp.proto

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
  name='dtc_resp.proto',
  package='',
  serialized_pb=_b('\n\x0e\x64tc_resp.proto\"\xe1\x04\n\rDTCStatusResp\x12&\n\x04\x64tcs\x18\x01 \x03(\x0b\x32\x18.DTCStatusResp.DTCStatus\x12/\n\x0c\x64tc_ext_data\x18\x02 \x01(\x0b\x32\x19.DTCStatusResp.DTCExtData\x12,\n\x07\x63lr_dtc\x18\x03 \x03(\x0b\x32\x1b.DTCStatusResp.ClrDTCStatus\x12\x30\n\x0c\x64tc_snapshot\x18\x04 \x01(\x0b\x32\x1a.DTCStatusResp.DTCSnapshot\x1a\x9a\x01\n\nDTCExtData\x12\x0e\n\x06\x65\x63u_no\x18\x01 \x01(\x05\x12\x0e\n\x06\x64tc_no\x18\x02 \x01(\x05\x12\x13\n\x0bocc_counter\x18\x03 \x01(\r\x12\x0e\n\x06occ_ts\x18\x04 \x01(\x04\x12\x0f\n\x07odo_val\x18\x05 \x01(\x05\x12\x13\n\x0blv_batt_vol\x18\x06 \x01(\x05\x12\x11\n\tveh_speed\x18\x07 \x01(\x05\x12\x0e\n\x06status\x18\x08 \x01(\x05\x1a.\n\x0c\x43lrDTCStatus\x12\x0e\n\x06\x65\x63u_no\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x05\x1a;\n\tDTCStatus\x12\x0e\n\x06\x65\x63u_no\x18\x01 \x01(\x05\x12\x0e\n\x06\x64tc_no\x18\x02 \x01(\x05\x12\x0e\n\x06status\x18\x03 \x01(\x05\x1a\x8c\x01\n\x0b\x44TCSnapshot\x12\x0e\n\x06\x65\x63u_no\x18\x01 \x01(\x05\x12\x0e\n\x06\x64tc_no\x18\x02 \x01(\x05\x12\x0e\n\x06status\x18\x03 \x01(\x05\x12\x11\n\trecord_no\x18\x04 \x01(\x05\x12\x13\n\x0bidentifiers\x18\x05 \x01(\x05\x12\x13\n\x0b\x65\x63u_version\x18\x06 \x01(\t\x12\x10\n\x08\x64id_data\x18\x07 \x03(\tB5\n$com.nextev.cvs_proto.protobuf.customB\rDTCStatusUnit')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_DTCSTATUSRESP_DTCEXTDATA = _descriptor.Descriptor(
  name='DTCExtData',
  full_name='DTCStatusResp.DTCExtData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecu_no', full_name='DTCStatusResp.DTCExtData.ecu_no', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dtc_no', full_name='DTCStatusResp.DTCExtData.dtc_no', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='occ_counter', full_name='DTCStatusResp.DTCExtData.occ_counter', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='occ_ts', full_name='DTCStatusResp.DTCExtData.occ_ts', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='odo_val', full_name='DTCStatusResp.DTCExtData.odo_val', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lv_batt_vol', full_name='DTCStatusResp.DTCExtData.lv_batt_vol', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='veh_speed', full_name='DTCStatusResp.DTCExtData.veh_speed', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='DTCStatusResp.DTCExtData.status', index=7,
      number=8, type=5, cpp_type=1, label=1,
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
  serialized_start=222,
  serialized_end=376,
)

_DTCSTATUSRESP_CLRDTCSTATUS = _descriptor.Descriptor(
  name='ClrDTCStatus',
  full_name='DTCStatusResp.ClrDTCStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecu_no', full_name='DTCStatusResp.ClrDTCStatus.ecu_no', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='DTCStatusResp.ClrDTCStatus.status', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=378,
  serialized_end=424,
)

_DTCSTATUSRESP_DTCSTATUS = _descriptor.Descriptor(
  name='DTCStatus',
  full_name='DTCStatusResp.DTCStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecu_no', full_name='DTCStatusResp.DTCStatus.ecu_no', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dtc_no', full_name='DTCStatusResp.DTCStatus.dtc_no', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='DTCStatusResp.DTCStatus.status', index=2,
      number=3, type=5, cpp_type=1, label=1,
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
  serialized_start=426,
  serialized_end=485,
)

_DTCSTATUSRESP_DTCSNAPSHOT = _descriptor.Descriptor(
  name='DTCSnapshot',
  full_name='DTCStatusResp.DTCSnapshot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ecu_no', full_name='DTCStatusResp.DTCSnapshot.ecu_no', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dtc_no', full_name='DTCStatusResp.DTCSnapshot.dtc_no', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='DTCStatusResp.DTCSnapshot.status', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='record_no', full_name='DTCStatusResp.DTCSnapshot.record_no', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='identifiers', full_name='DTCStatusResp.DTCSnapshot.identifiers', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ecu_version', full_name='DTCStatusResp.DTCSnapshot.ecu_version', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='did_data', full_name='DTCStatusResp.DTCSnapshot.did_data', index=6,
      number=7, type=9, cpp_type=9, label=3,
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
  serialized_start=488,
  serialized_end=628,
)

_DTCSTATUSRESP = _descriptor.Descriptor(
  name='DTCStatusResp',
  full_name='DTCStatusResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='dtcs', full_name='DTCStatusResp.dtcs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dtc_ext_data', full_name='DTCStatusResp.dtc_ext_data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='clr_dtc', full_name='DTCStatusResp.clr_dtc', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dtc_snapshot', full_name='DTCStatusResp.dtc_snapshot', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DTCSTATUSRESP_DTCEXTDATA, _DTCSTATUSRESP_CLRDTCSTATUS, _DTCSTATUSRESP_DTCSTATUS, _DTCSTATUSRESP_DTCSNAPSHOT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=19,
  serialized_end=628,
)

_DTCSTATUSRESP_DTCEXTDATA.containing_type = _DTCSTATUSRESP
_DTCSTATUSRESP_CLRDTCSTATUS.containing_type = _DTCSTATUSRESP
_DTCSTATUSRESP_DTCSTATUS.containing_type = _DTCSTATUSRESP
_DTCSTATUSRESP_DTCSNAPSHOT.containing_type = _DTCSTATUSRESP
_DTCSTATUSRESP.fields_by_name['dtcs'].message_type = _DTCSTATUSRESP_DTCSTATUS
_DTCSTATUSRESP.fields_by_name['dtc_ext_data'].message_type = _DTCSTATUSRESP_DTCEXTDATA
_DTCSTATUSRESP.fields_by_name['clr_dtc'].message_type = _DTCSTATUSRESP_CLRDTCSTATUS
_DTCSTATUSRESP.fields_by_name['dtc_snapshot'].message_type = _DTCSTATUSRESP_DTCSNAPSHOT
DESCRIPTOR.message_types_by_name['DTCStatusResp'] = _DTCSTATUSRESP

DTCStatusResp = _reflection.GeneratedProtocolMessageType('DTCStatusResp', (_message.Message,), dict(

  DTCExtData = _reflection.GeneratedProtocolMessageType('DTCExtData', (_message.Message,), dict(
    DESCRIPTOR = _DTCSTATUSRESP_DTCEXTDATA,
    __module__ = 'dtc_resp_pb2'
    # @@protoc_insertion_point(class_scope:DTCStatusResp.DTCExtData)
    ))
  ,

  ClrDTCStatus = _reflection.GeneratedProtocolMessageType('ClrDTCStatus', (_message.Message,), dict(
    DESCRIPTOR = _DTCSTATUSRESP_CLRDTCSTATUS,
    __module__ = 'dtc_resp_pb2'
    # @@protoc_insertion_point(class_scope:DTCStatusResp.ClrDTCStatus)
    ))
  ,

  DTCStatus = _reflection.GeneratedProtocolMessageType('DTCStatus', (_message.Message,), dict(
    DESCRIPTOR = _DTCSTATUSRESP_DTCSTATUS,
    __module__ = 'dtc_resp_pb2'
    # @@protoc_insertion_point(class_scope:DTCStatusResp.DTCStatus)
    ))
  ,

  DTCSnapshot = _reflection.GeneratedProtocolMessageType('DTCSnapshot', (_message.Message,), dict(
    DESCRIPTOR = _DTCSTATUSRESP_DTCSNAPSHOT,
    __module__ = 'dtc_resp_pb2'
    # @@protoc_insertion_point(class_scope:DTCStatusResp.DTCSnapshot)
    ))
  ,
  DESCRIPTOR = _DTCSTATUSRESP,
  __module__ = 'dtc_resp_pb2'
  # @@protoc_insertion_point(class_scope:DTCStatusResp)
  ))
_sym_db.RegisterMessage(DTCStatusResp)
_sym_db.RegisterMessage(DTCStatusResp.DTCExtData)
_sym_db.RegisterMessage(DTCStatusResp.ClrDTCStatus)
_sym_db.RegisterMessage(DTCStatusResp.DTCStatus)
_sym_db.RegisterMessage(DTCStatusResp.DTCSnapshot)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.customB\rDTCStatusUnit'))
# @@protoc_insertion_point(module_scope)