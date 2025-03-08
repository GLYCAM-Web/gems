import grpc
import os, sys

import json_pb2
import json_pb2_grpc

from gemsModules.logging.logger import new_concurrent_logger

log = new_concurrent_logger(__name__)


class JSONClient():
    def __init__(self, json, host=None, port=None):
        self.json = json
        self.response = self.run(theHost=host, thePort=port)

    def run(self, theHost=None, thePort=None):
        if theHost is None:
            theHost = os.getenv('GRPC_DELEGATOR_HOST')
            if theHost is None:
                log.error("The gRPC/JSON server host is not defined.  Exiting.")
                sys.exit(1)
        if thePort is None:
            thePort = os.getenv('GRPC_DELEGATOR_PORT')
            if theHost is None:
                log.error("The gRPC/JSON server port is not defined.  Exiting.")
                sys.exit(1)
                
        hostport = theHost + ":" + thePort
        log.debug("hostport is >>>" + hostport + "<<<")
        with grpc.insecure_channel(hostport) as channel:
            stub = json_pb2_grpc.JSONStub(channel)
            log.debug("Attempting to send %s over %s", self.json, hostport)
            response = stub.JSON_Delegator(json_pb2.JSONRequest(input=self.json))
            log.debug("json_client returns this response: \n" + str(response))
            
        return response


if __name__ == '__main__':
    logging.basicConfig()
    json_client = JSONClient(json="{ \"hello\": \"hello world!\" }")
    print(json_client.response)
