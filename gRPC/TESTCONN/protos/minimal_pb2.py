# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minimal.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rminimal.proto\x12\x07minimal\"\x1a\n\x07Message\x12\x0f\n\x07message\x18\x01 \x01(\t\"\"\n\x0fMessageResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2J\n\x05Unary\x12\x41\n\x11GetServerResponse\x12\x10.minimal.Message\x1a\x18.minimal.MessageResponse\"\x00\x62\x06proto3')



_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_MESSAGERESPONSE = DESCRIPTOR.message_types_by_name['MessageResponse']
Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'minimal_pb2'
  # @@protoc_insertion_point(class_scope:minimal.Message)
  })
_sym_db.RegisterMessage(Message)

MessageResponse = _reflection.GeneratedProtocolMessageType('MessageResponse', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGERESPONSE,
  '__module__' : 'minimal_pb2'
  # @@protoc_insertion_point(class_scope:minimal.MessageResponse)
  })
_sym_db.RegisterMessage(MessageResponse)

_UNARY = DESCRIPTOR.services_by_name['Unary']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGE._serialized_start=26
  _MESSAGE._serialized_end=52
  _MESSAGERESPONSE._serialized_start=54
  _MESSAGERESPONSE._serialized_end=88
  _UNARY._serialized_start=90
  _UNARY._serialized_end=164
# @@protoc_insertion_point(module_scope)
