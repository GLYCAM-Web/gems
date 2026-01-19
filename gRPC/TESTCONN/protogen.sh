!/usr/bin/env bash

PROTONAME="${2:-$1}"
BASE="${GEMSHOME}/gRPC/TESTCONN"
PROTO="${BASE}/protos/definitions/${PROTONAME}.proto"

python -m grpc_tools.protoc -I=$BASE/protos/definitions --grpc_python_out=$BASE/protos --python_out=$BASE/protos $PROTO

if [ $? -eq 0 ]; then
    echo "protogen.sh: protoc succeeded for ${PROTO}"
    # due to the wayp rotoc works, it doesn't import proeprly, lets fix that by searching for "import ${PROTONAME}_pb2"
    # and replacing it with "from protos import ${PROTONAME}_pb2"
    sed -i "s/import ${PROTONAME}_pb2/from protos import ${PROTONAME}_pb2/g" "${BASE}/protos/${PROTONAME}_pb2_grpc.py"
else
    echo "protogen.sh: protoc failed"
fi
