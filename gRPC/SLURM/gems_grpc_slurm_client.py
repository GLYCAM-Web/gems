import logging

import grpc
import os, sys

import gems_grpc_slurm_pb2
import gems_grpc_slurm_pb2_grpc

from gemsModules.logging.logger import new_concurrent_logger

log = new_concurrent_logger(__name__)


class GemsGrpcSlurmClient:
    def __init__(self, json, host=None, port=None):
        self.json = json
        self.response = self.run(theHost=host, thePort=port)

    def run(self, theHost=None, thePort=None):
        log.info("gRPC Slurm client called.\n")

        # So that run still behaves as expected for anything still using json_client.run() without args:
        if theHost is None:
            theHost = os.environ.get("GEMS_GRPC_SLURM_HOST")
            log.debug("the host is:  " + theHost)
            if theHost is None:
                log.error("The gRPC/SLURM server host is not defined.  Exiting.")
                sys.exit(1)
        if thePort is None:
            thePort = os.environ.get("GEMS_GRPC_SLURM_PORT")
            log.debug("the port is:  " + thePort)
            if theHost is None:
                log.error("The gRPC/SLURM server port is not defined.  Exiting.")
                sys.exit(1)

        hostport = theHost + ":" + thePort
        log.debug("hostport is >>>" + hostport + "<<<")
        with grpc.insecure_channel(hostport) as channel:
            stub = gems_grpc_slurm_pb2_grpc.GemsGrpcSlurmStub(channel)
            log.debug("Attempting to send %s over %s", self.json, hostport)
            response = stub.GemsGrpcSlurmReceiver(
                gems_grpc_slurm_pb2.GemsGrpcSlurmRequest(input=self.json)
            )
            log.debug(
                "gems_grpc_slurm_client returns this response: \n" + str(response)
            )
        return response


if __name__ == "__main__":
    logging.basicConfig()
    gems_grpc_slurm_client = GemsGrpcSlurmClient(json='{ "hello": "hello world!" }')
    print(gems_grpc_slurm_client)
