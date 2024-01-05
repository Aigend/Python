# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: driving_behaviour_msg.proto

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
  name='driving_behaviour_msg.proto',
  package='',
  serialized_pb=_b('\n\x1b\x64riving_behaviour_msg.proto\"\xc7\x01\n\x15\x44rivingBehaviourEvent\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x05\x12\x11\n\tsample_ts\x18\x03 \x01(\x04\x12\x32\n\tbehaviour\x18\x04 \x03(\x0e\x32\x1f.DrivingBehaviourEvent.Behavior\"J\n\x08\x42\x65havior\x12\x0e\n\nSHARP_TURN\x10\x00\x12\x16\n\x12RAPID_DECELERATION\x10\x01\x12\x16\n\x12RAPID_ACCELERATION\x10\x02\x42?\n$com.nextev.cvs_proto.protobuf.eventsB\x17\x44rivingBehaviourMessage')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_DRIVINGBEHAVIOUREVENT_BEHAVIOR = _descriptor.EnumDescriptor(
  name='Behavior',
  full_name='DrivingBehaviourEvent.Behavior',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SHARP_TURN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RAPID_DECELERATION', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RAPID_ACCELERATION', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=157,
  serialized_end=231,
)
_sym_db.RegisterEnumDescriptor(_DRIVINGBEHAVIOUREVENT_BEHAVIOR)


_DRIVINGBEHAVIOUREVENT = _descriptor.Descriptor(
  name='DrivingBehaviourEvent',
  full_name='DrivingBehaviourEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='DrivingBehaviourEvent.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='DrivingBehaviourEvent.version', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sample_ts', full_name='DrivingBehaviourEvent.sample_ts', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='behaviour', full_name='DrivingBehaviourEvent.behaviour', index=3,
      number=4, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DRIVINGBEHAVIOUREVENT_BEHAVIOR,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=231,
)

_DRIVINGBEHAVIOUREVENT.fields_by_name['behaviour'].enum_type = _DRIVINGBEHAVIOUREVENT_BEHAVIOR
_DRIVINGBEHAVIOUREVENT_BEHAVIOR.containing_type = _DRIVINGBEHAVIOUREVENT
DESCRIPTOR.message_types_by_name['DrivingBehaviourEvent'] = _DRIVINGBEHAVIOUREVENT

DrivingBehaviourEvent = _reflection.GeneratedProtocolMessageType('DrivingBehaviourEvent', (_message.Message,), dict(
  DESCRIPTOR = _DRIVINGBEHAVIOUREVENT,
  __module__ = 'driving_behaviour_msg_pb2'
  # @@protoc_insertion_point(class_scope:DrivingBehaviourEvent)
  ))
_sym_db.RegisterMessage(DrivingBehaviourEvent)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n$com.nextev.cvs_proto.protobuf.eventsB\027DrivingBehaviourMessage'))
# @@protoc_insertion_point(module_scope)
