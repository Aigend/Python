# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: alarm_signal.proto

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
  name='alarm_signal.proto',
  package='',
  serialized_pb=_b('\n\x12\x61larm_signal.proto\"\xd7\x01\n\x0b\x41larmSignal\x12*\n\nsignal_int\x18\x01 \x03(\x0b\x32\x16.AlarmSignal.SignalInt\x12.\n\x0csignal_float\x18\x02 \x03(\x0b\x32\x18.AlarmSignal.SignalFloat\x1a\x34\n\tSignalInt\x12\n\n\x02sn\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x11\x1a\x36\n\x0bSignalFloat\x12\n\n\x02sn\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x02\x42\x37\n$com.nextev.cvs_proto.protobuf.customB\x0f\x41larmSignalUnit')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_ALARMSIGNAL_SIGNALINT = _descriptor.Descriptor(
  name='SignalInt',
  full_name='AlarmSignal.SignalInt',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sn', full_name='AlarmSignal.SignalInt.sn', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='AlarmSignal.SignalInt.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='AlarmSignal.SignalInt.value', index=2,
      number=3, type=17, cpp_type=1, label=1,
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
  serialized_start=130,
  serialized_end=182,
)

_ALARMSIGNAL_SIGNALFLOAT = _descriptor.Descriptor(
  name='SignalFloat',
  full_name='AlarmSignal.SignalFloat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sn', full_name='AlarmSignal.SignalFloat.sn', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='AlarmSignal.SignalFloat.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='AlarmSignal.SignalFloat.value', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=184,
  serialized_end=238,
)

_ALARMSIGNAL = _descriptor.Descriptor(
  name='AlarmSignal',
  full_name='AlarmSignal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='signal_int', full_name='AlarmSignal.signal_int', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signal_float', full_name='AlarmSignal.signal_float', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_ALARMSIGNAL_SIGNALINT, _ALARMSIGNAL_SIGNALFLOAT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=238,
)

_ALARMSIGNAL_SIGNALINT.containing_type = _ALARMSIGNAL
_ALARMSIGNAL_SIGNALFLOAT.containing_type = _ALARMSIGNAL
_ALARMSIGNAL.fields_by_name['signal_int'].message_type = _ALARMSIGNAL_SIGNALINT
_ALARMSIGNAL.fields_by_name['signal_float'].message_type = _ALARMSIGNAL_SIGNALFLOAT
DESCRIPTOR.message_types_by_name['AlarmSignal'] = _ALARMSIGNAL

AlarmSignal = _reflection.GeneratedProtocolMessageType('AlarmSignal', (_message.Message,), dict(

  SignalInt = _reflection.GeneratedProtocolMessageType('SignalInt', (_message.Message,), dict(
    DESCRIPTOR = _ALARMSIGNAL_SIGNALINT,
    __module__ = 'alarm_signal_pb2'
    # @@protoc_insertion_point(class_scope:AlarmSignal.SignalInt)
    ))
  ,

  SignalFloat = _reflection.GeneratedProtocolMessageType('SignalFloat', (_message.Message,), dict(
    DESCRIPTOR = _ALARMSIGNAL_SIGNALFLOAT,
    __module__ = 'alarm_signal_pb2'
    # @@protoc_insertion_point(class_scope:AlarmSignal.SignalFloat)
    ))
  ,
  DESCRIPTOR = _ALARMSIGNAL,
  __module__ = 'alarm_signal_pb2'
  # @@protoc_insertion_point(class_scope:AlarmSignal)
  ))
_sym_db.RegisterMessage(AlarmSignal)
_sym_db.RegisterMessage(AlarmSignal.SignalInt)
_sym_db.RegisterMessage(AlarmSignal.SignalFloat)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.customB\017AlarmSignalUnit'))
# @@protoc_insertion_point(module_scope)