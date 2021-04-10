# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ball_launcher.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ball_launcher.proto',
  package='ball_launcher',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x13\x62\x61ll_launcher.proto\x12\rball_launcher\"\x99\x02\n\x07Request\x12\x33\n\x07request\x18\x01 \x02(\x0e\x32\".ball_launcher.Request.RequestType\x12+\n\x05state\x18\x02 \x01(\x0b\x32\x1c.ball_launcher.Request.State\x1a}\n\x05State\x12\x10\n\x03phi\x18\x01 \x01(\x02:\x03\x30.5\x12\x12\n\x05theta\x18\x02 \x01(\x02:\x03\x30.5\x12\x19\n\x0etop_left_motor\x18\x03 \x01(\x02:\x01\x30\x12\x1a\n\x0ftop_right_motor\x18\x04 \x01(\x02:\x01\x30\x12\x17\n\x0c\x62ottom_motor\x18\x05 \x01(\x02:\x01\x30\"-\n\x0bRequestType\x12\r\n\tSET_STATE\x10\x00\x12\x0f\n\x0bLAUNCH_BALL\x10\x01')
)



_REQUEST_REQUESTTYPE = _descriptor.EnumDescriptor(
  name='RequestType',
  full_name='ball_launcher.Request.RequestType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SET_STATE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LAUNCH_BALL', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=275,
  serialized_end=320,
)
_sym_db.RegisterEnumDescriptor(_REQUEST_REQUESTTYPE)


_REQUEST_STATE = _descriptor.Descriptor(
  name='State',
  full_name='ball_launcher.Request.State',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='phi', full_name='ball_launcher.Request.State.phi', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='theta', full_name='ball_launcher.Request.State.theta', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='top_left_motor', full_name='ball_launcher.Request.State.top_left_motor', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='top_right_motor', full_name='ball_launcher.Request.State.top_right_motor', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bottom_motor', full_name='ball_launcher.Request.State.bottom_motor', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=148,
  serialized_end=273,
)

_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='ball_launcher.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request', full_name='ball_launcher.Request.request', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='state', full_name='ball_launcher.Request.state', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_REQUEST_STATE, ],
  enum_types=[
    _REQUEST_REQUESTTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=320,
)

_REQUEST_STATE.containing_type = _REQUEST
_REQUEST.fields_by_name['request'].enum_type = _REQUEST_REQUESTTYPE
_REQUEST.fields_by_name['state'].message_type = _REQUEST_STATE
_REQUEST_REQUESTTYPE.containing_type = _REQUEST
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(

  State = _reflection.GeneratedProtocolMessageType('State', (_message.Message,), dict(
    DESCRIPTOR = _REQUEST_STATE,
    __module__ = 'ball_launcher_pb2'
    # @@protoc_insertion_point(class_scope:ball_launcher.Request.State)
    ))
  ,
  DESCRIPTOR = _REQUEST,
  __module__ = 'ball_launcher_pb2'
  # @@protoc_insertion_point(class_scope:ball_launcher.Request)
  ))
_sym_db.RegisterMessage(Request)
_sym_db.RegisterMessage(Request.State)


# @@protoc_insertion_point(module_scope)
