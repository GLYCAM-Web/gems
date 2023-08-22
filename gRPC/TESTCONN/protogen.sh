!/usr/bin/env bash

BASE="${GEMSHOME}/gRPC/TESTCONN"
PROTO="${BASE}/protos/${2:-$1}.proto"

python -m grpc_tools.protoc -I=$BASE --grpc_python_out=$BASE/protos --python_out=$BASE/protos $PROTO

if [ $? -eq 0 ]; then
    echo "protogen.sh: protoc succeeded for ${PROTO}"
else
    echo "protogen.sh: protoc failed"
fi
