import logging
import os
import traceback

from subprocess import PIPE, Popen


from protos import minimal_pb2, minimal_pb2_grpc
from modules.base import SimpleGRPCClient, SimpleGRPCServer

log = logging.getLogger(__name__)


class MinServer(SimpleGRPCServer):
    def add_servicer(self):
        minimal_pb2_grpc.add_UnaryServicer_to_server(self.Servicer(), self.server)

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

    def send_request(self, request):
        log.debug(f"Querying {self.host} with {request}...")
        response = self.get_response(request)
        log.debug(f"Response: {response}")
        return response

    def get_response(self, request):
        return self.stub.GetServerResponse(self.protobuf.Message(message=request))
