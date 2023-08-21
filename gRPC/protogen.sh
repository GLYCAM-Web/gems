#!/usr/bin/env bash

BASE="${GEMSHOME}/gRPC/${1:-TESTCONN}/protos"
PROTO="${BASE}/${2:-1}.proto"

python -m grpc_tools.protoc -I=$BASE --grpc_python_out=$BASE --python_out=$BASE $PROTO

if [ $? -eq 0 ]; then
    echo "protogen.sh: protoc succeeded"
else
    echo "protogen.sh: protoc failed"
fi