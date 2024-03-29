# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: instant_status_msg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import door_status_pb2
import driving_data_pb2
import alarm_signal_pb2
import hvac_status_pb2
import light_status_pb2
import occupant_status_pb2
import signal_status_pb2
import soc_status_pb2
import tyre_status_pb2
import window_status_pb2
import alarm_data_pb2
import driving_motor_pb2
import extremum_data_pb2
import position_status_pb2
import vehicle_status_pb2
import bms_status_pb2
import can_msg_pb2
import trip_status_pb2
import body_status_pb2
import can_signal_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='instant_status_msg.proto',
  package='',
  serialized_pb=_b('\n\x18instant_status_msg.proto\x1a\x11\x64oor_status.proto\x1a\x12\x64riving_data.proto\x1a\x12\x61larm_signal.proto\x1a\x11hvac_status.proto\x1a\x12light_status.proto\x1a\x15occupant_status.proto\x1a\x13signal_status.proto\x1a\x10soc_status.proto\x1a\x11tyre_status.proto\x1a\x13window_status.proto\x1a\x10\x61larm_data.proto\x1a\x13\x64riving_motor.proto\x1a\x13\x65xtremum_data.proto\x1a\x15position_status.proto\x1a\x14vehicle_status.proto\x1a\x10\x62ms_status.proto\x1a\rcan_msg.proto\x1a\x11trip_status.proto\x1a\x11\x62ody_status.proto\x1a\x10\x63\x61n_signal.proto\"\xb6\x08\n\x11InstantStatusResp\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nrequest_id\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\x05\x12\x0e\n\x06icc_id\x18\x04 \x01(\t\x12\x34\n\x0csample_point\x18\x05 \x01(\x0b\x32\x1e.InstantStatusResp.SamplePoint\x12\x11\n\tsample_ts\x18\x06 \x01(\x04\x12\x16\n\x0e\x63onfig_version\x18\x07 \x01(\t\x12\x19\n\x11signallib_version\x18\x08 \x01(\t\x1a\xe3\x06\n\x0bSamplePoint\x12\x11\n\tsample_ts\x18\x01 \x01(\x04\x12 \n\x0b\x64oor_status\x18\x02 \x01(\x0b\x32\x0b.DoorStatus\x12\"\n\x0c\x64riving_data\x18\x03 \x01(\x0b\x32\x0c.DrivingData\x12\"\n\x0c\x61larm_signal\x18\x04 \x01(\x0b\x32\x0c.AlarmSignal\x12 \n\x0bhvac_status\x18\x05 \x01(\x0b\x32\x0b.HVACStatus\x12\"\n\x0clight_status\x18\x06 \x01(\x0b\x32\x0c.LightStatus\x12(\n\x0foccupant_status\x18\x07 \x01(\x0b\x32\x0f.OccupantStatus\x12$\n\rsignal_status\x18\x08 \x01(\x0b\x32\r.SignalStatus\x12\x1e\n\nsoc_status\x18\t \x01(\x0b\x32\n.SOCStatus\x12&\n\x0evehicle_status\x18\n \x01(\x0b\x32\x0e.VehicleStatus\x12 \n\x0btyre_status\x18\x0b \x01(\x0b\x32\x0b.TyreStatus\x12$\n\rwindow_status\x18\x0c \x01(\x0b\x32\r.WindowStatus\x12\x1e\n\nalarm_data\x18\r \x01(\x0b\x32\n.AlarmData\x12$\n\rdriving_motor\x18\x0e \x01(\x0b\x32\r.DrivingMotor\x12$\n\rextremum_data\x18\x0f \x01(\x0b\x32\r.ExtremumData\x12(\n\x0fposition_status\x18\x10 \x01(\x0b\x32\x0f.PositionStatus\x12;\n\x14\x62\x61ttery_package_info\x18\x11 \x01(\x0b\x32\x1d.SOCStatus.BatteryPackageInfo\x12\x1e\n\nbms_status\x18\x12 \x01(\x0b\x32\n.BmsStatus\x12.\n\rcharging_info\x18\x13 \x01(\x0b\x32\x17.SOCStatus.ChargingInfo\x12\x18\n\x07\x63\x61n_msg\x18\x14 \x01(\x0b\x32\x07.CanMsg\x12\x10\n\x08\x65vm_flag\x18\x15 \x01(\x08\x12 \n\x0btrip_status\x18\x16 \x01(\x0b\x32\x0b.TripStatus\x12 \n\x0b\x62ody_status\x18\x17 \x01(\x0b\x32\x0b.BodyStatus\x12\x1e\n\ncan_signal\x18\x18 \x01(\x0b\x32\n.CanSignalB<\n$com.nextev.cvs_proto.protobuf.eventsB\x14InstantStatusMessage')
  ,
  dependencies=[door_status_pb2.DESCRIPTOR,driving_data_pb2.DESCRIPTOR,alarm_signal_pb2.DESCRIPTOR,hvac_status_pb2.DESCRIPTOR,light_status_pb2.DESCRIPTOR,occupant_status_pb2.DESCRIPTOR,signal_status_pb2.DESCRIPTOR,soc_status_pb2.DESCRIPTOR,tyre_status_pb2.DESCRIPTOR,window_status_pb2.DESCRIPTOR,alarm_data_pb2.DESCRIPTOR,driving_motor_pb2.DESCRIPTOR,extremum_data_pb2.DESCRIPTOR,position_status_pb2.DESCRIPTOR,vehicle_status_pb2.DESCRIPTOR,bms_status_pb2.DESCRIPTOR,can_msg_pb2.DESCRIPTOR,trip_status_pb2.DESCRIPTOR,body_status_pb2.DESCRIPTOR,can_signal_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_INSTANTSTATUSRESP_SAMPLEPOINT = _descriptor.Descriptor(
  name='SamplePoint',
  full_name='InstantStatusResp.SamplePoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sample_ts', full_name='InstantStatusResp.SamplePoint.sample_ts', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='door_status', full_name='InstantStatusResp.SamplePoint.door_status', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='driving_data', full_name='InstantStatusResp.SamplePoint.driving_data', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='alarm_signal', full_name='InstantStatusResp.SamplePoint.alarm_signal', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hvac_status', full_name='InstantStatusResp.SamplePoint.hvac_status', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='light_status', full_name='InstantStatusResp.SamplePoint.light_status', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='occupant_status', full_name='InstantStatusResp.SamplePoint.occupant_status', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signal_status', full_name='InstantStatusResp.SamplePoint.signal_status', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='soc_status', full_name='InstantStatusResp.SamplePoint.soc_status', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='vehicle_status', full_name='InstantStatusResp.SamplePoint.vehicle_status', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tyre_status', full_name='InstantStatusResp.SamplePoint.tyre_status', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='window_status', full_name='InstantStatusResp.SamplePoint.window_status', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='alarm_data', full_name='InstantStatusResp.SamplePoint.alarm_data', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='driving_motor', full_name='InstantStatusResp.SamplePoint.driving_motor', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='extremum_data', full_name='InstantStatusResp.SamplePoint.extremum_data', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='position_status', full_name='InstantStatusResp.SamplePoint.position_status', index=15,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='battery_package_info', full_name='InstantStatusResp.SamplePoint.battery_package_info', index=16,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bms_status', full_name='InstantStatusResp.SamplePoint.bms_status', index=17,
      number=18, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='charging_info', full_name='InstantStatusResp.SamplePoint.charging_info', index=18,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='can_msg', full_name='InstantStatusResp.SamplePoint.can_msg', index=19,
      number=20, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='evm_flag', full_name='InstantStatusResp.SamplePoint.evm_flag', index=20,
      number=21, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trip_status', full_name='InstantStatusResp.SamplePoint.trip_status', index=21,
      number=22, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='body_status', full_name='InstantStatusResp.SamplePoint.body_status', index=22,
      number=23, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='can_signal', full_name='InstantStatusResp.SamplePoint.can_signal', index=23,
      number=24, type=11, cpp_type=10, label=1,
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
  serialized_start=634,
  serialized_end=1501,
)

_INSTANTSTATUSRESP = _descriptor.Descriptor(
  name='InstantStatusResp',
  full_name='InstantStatusResp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='InstantStatusResp.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request_id', full_name='InstantStatusResp.request_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='InstantStatusResp.version', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='icc_id', full_name='InstantStatusResp.icc_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sample_point', full_name='InstantStatusResp.sample_point', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sample_ts', full_name='InstantStatusResp.sample_ts', index=5,
      number=6, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='config_version', full_name='InstantStatusResp.config_version', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signallib_version', full_name='InstantStatusResp.signallib_version', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_INSTANTSTATUSRESP_SAMPLEPOINT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=423,
  serialized_end=1501,
)

_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['door_status'].message_type = door_status_pb2._DOORSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['driving_data'].message_type = driving_data_pb2._DRIVINGDATA
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['alarm_signal'].message_type = alarm_signal_pb2._ALARMSIGNAL
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['hvac_status'].message_type = hvac_status_pb2._HVACSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['light_status'].message_type = light_status_pb2._LIGHTSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['occupant_status'].message_type = occupant_status_pb2._OCCUPANTSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['signal_status'].message_type = signal_status_pb2._SIGNALSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['soc_status'].message_type = soc_status_pb2._SOCSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['vehicle_status'].message_type = vehicle_status_pb2._VEHICLESTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['tyre_status'].message_type = tyre_status_pb2._TYRESTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['window_status'].message_type = window_status_pb2._WINDOWSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['alarm_data'].message_type = alarm_data_pb2._ALARMDATA
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['driving_motor'].message_type = driving_motor_pb2._DRIVINGMOTOR
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['extremum_data'].message_type = extremum_data_pb2._EXTREMUMDATA
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['position_status'].message_type = position_status_pb2._POSITIONSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['battery_package_info'].message_type = soc_status_pb2._SOCSTATUS_BATTERYPACKAGEINFO
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['bms_status'].message_type = bms_status_pb2._BMSSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['charging_info'].message_type = soc_status_pb2._SOCSTATUS_CHARGINGINFO
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['can_msg'].message_type = can_msg_pb2._CANMSG
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['trip_status'].message_type = trip_status_pb2._TRIPSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['body_status'].message_type = body_status_pb2._BODYSTATUS
_INSTANTSTATUSRESP_SAMPLEPOINT.fields_by_name['can_signal'].message_type = can_signal_pb2._CANSIGNAL
_INSTANTSTATUSRESP_SAMPLEPOINT.containing_type = _INSTANTSTATUSRESP
_INSTANTSTATUSRESP.fields_by_name['sample_point'].message_type = _INSTANTSTATUSRESP_SAMPLEPOINT
DESCRIPTOR.message_types_by_name['InstantStatusResp'] = _INSTANTSTATUSRESP

InstantStatusResp = _reflection.GeneratedProtocolMessageType('InstantStatusResp', (_message.Message,), dict(

  SamplePoint = _reflection.GeneratedProtocolMessageType('SamplePoint', (_message.Message,), dict(
    DESCRIPTOR = _INSTANTSTATUSRESP_SAMPLEPOINT,
    __module__ = 'instant_status_msg_pb2'
    # @@protoc_insertion_point(class_scope:InstantStatusResp.SamplePoint)
    ))
  ,
  DESCRIPTOR = _INSTANTSTATUSRESP,
  __module__ = 'instant_status_msg_pb2'
  # @@protoc_insertion_point(class_scope:InstantStatusResp)
  ))
_sym_db.RegisterMessage(InstantStatusResp)
_sym_db.RegisterMessage(InstantStatusResp.SamplePoint)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.eventsB\024InstantStatusMessage'))
# @@protoc_insertion_point(module_scope)
