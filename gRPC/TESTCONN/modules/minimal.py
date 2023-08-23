import logging
import os
import traceback

from subprocess import PIPE, Popen


from protos import minimal_pb2, minimal_pb2_grpc
from modules.base import SimpleGRPCClient, SimpleGRPCServer

log = logging.getLogger(__name__)


class MinServer(SimpleGRPCServer):
    PB_GRPC_MODULE = minimal_pb2_grpc

    class Servicer(PB_GRPC_MODULE.UnaryServicer):
        def GetServerResponse(self, request, context):
            log.debug(f"{self.__class__.__name__}.GetServerResponse has been called.")
            request = bytes.fromhex(request.message)

            response = "No response."

            GEMSHOME = os.environ.get("GEMSHOME")
            if GEMSHOME == None:
                log.error("GEMSHOME is not set.")
                response = "GemsHomeNotSet"
            else:
                try:
                    p = Popen(
                        ["echo", f"{request.decode('utf-8')}"],
                        stdin=PIPE,
                        stdout=PIPE,
                        stderr=PIPE,
                        shell=False,
                    )

                    (stdout, stderr) = p.communicate(input=request)

                    if p.returncode != 0 or stderr:
                        response = stderr.decode("utf-8").replace('"', "")
                    else:
                        response = stdout.decode("utf-8").replace('"', "")

                except Exception:
                    response = f"{traceback.format_exc()}"

            return minimal_pb2.MessageResponse(message=bytes(response, "utf-8").hex())


class MinClient(SimpleGRPCClient):
    PB_MODULE = minimal_pb2
    STUB_TYPE = minimal_pb2_grpc.UnaryStub

    def get_response(self, request):
        log.debug(f"{self.__class__.__name__}.get_response has been called.")
        request = bytes(request, "utf-8").hex()

        # We might be able to automate this, but "GetServerResponse" and "Message" are arbitrary - part of the protobuf definition.
        response = self.stub.GetServerResponse(self.protobuf.Message(message=request))
        response = bytes.fromhex(response.message).decode("utf-8")
        response = response.replace("\n", "")
        return response
