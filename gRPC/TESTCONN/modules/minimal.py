import logging
import os
import traceback

from subprocess import PIPE, Popen


from protos import minimal_pb2, minimal_pb2_grpc
from modules.base import SimpleGRPCClient, SimpleGRPCServer

log = logging.getLogger(__name__)


class MinServer(SimpleGRPCServer):
    PB_GRPC_MODULE = minimal_pb2_grpc

    class Servicer(minimal_pb2_grpc.UnaryServicer):
        def GetServerResponse(self, request, context):
            log.debug(f"{self.__class__.__name__}'s gRPC Servicer has been called.")

            response = minimal_pb2.MessageResponse(message="No response.")

            GEMSHOME = os.environ.get("GEMSHOME")
            if GEMSHOME == None:
                log.error("GEMSHOME is not set.")
                response = minimal_pb2.MessageResponse(message="GemsHomeNotSet")
            else:
                try:
                    p = Popen(
                        # f"{GEMSHOME}/bin/delegate",
                        ["echo", f"{request.message}"],
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                        shell=False,
                    )

                    (stdout, stderr) = p.communicate(
                        input=request.message.encode("utf-8")
                    )

                    if p.returncode != 0 or stderr:
                        response = minimal_pb2.MessageResponse(
                            message=stderr.decode("utf-8").replace('"', "")
                        )
                    else:
                        response = minimal_pb2.MessageResponse(
                            message=stdout.decode("utf-8").replace('"', "")
                        )
                except Exception:
                    response = minimal_pb2.MessageResponse(
                        message=f"{traceback.format_exc()}"
                    )

            return response


class MinClient(SimpleGRPCClient):
    STUB_TYPE = minimal_pb2_grpc.UnaryStub
    PB_MODULE = minimal_pb2

    def get_response(self, request):
        # We might be able to automate this, but "GetServerResponse is arbitrary - part of the protobuf definition."
        return self.stub.GetServerResponse(self.protobuf.Message(message=request))
