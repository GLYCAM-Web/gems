import logging

import grpc
import os,sys

import gems_grpc_slurm_pb2
import gems_grpc_slurm_pb2_grpc

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class GemsGrpcSlurmClient():
    def __init__(self, json):
        self.json = json
        self.response = self.run()

    def run(self):

        log.info("gRPC Slurm client called.\n")
        theHost=os.environ.get('GEMS_GRPC_SLURM_HOST')
        log.debug("the host is:  " + theHost)
        if theHost is None:
            log.error("The gRPC/SLURM server host is not defined.  Exiting.")
            sys.exit(1)
        thePort=os.environ.get('GEMS_GRPC_SLURM_PORT')
        log.debug("the port is:  " + thePort)
        if theHost is None:
            log.error("The gRPC/SLURM server port is not defined.  Exiting.")
            sys.exit(1)
        
        hostport=theHost + ':' + thePort
        log.debug("hostport is >>>" + hostport + "<<<")
        with grpc.insecure_channel(hostport) as channel:
            stub = gems_grpc_slurm_pb2_grpc.GemsGrpcSlurmStub(channel)
            response = stub.GemsGrpcSlurmReceiver(gems_grpc_slurm_pb2.GemsGrpcSlurmRequest(input=self.json))
            log.debug("gems_grpc_slurm_client returns this response: \n" + str(response) )
        return response


if __name__ == '__main__':
    logging.basicConfig()
    gems_grpc_slurm_client = GemsGrpcSlurmClient(json="{ \"hello\": \"hello world!\" }")
    print(gems_grpc_slurm_client)
