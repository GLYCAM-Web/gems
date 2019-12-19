import logging

import grpc
import os,sys

import gems_grpc_slurm_pb2
import gems_grpc_slurm_pb2_grpc

class GemsGrpcSlurmClient():
    def __init__(self, json):
        self.json = json
        self.response = self.run()

    def run(self):

        theHost=os.environ.get('GEMS_GRPC_SLURM_HOST')
        print("the host is:  " + theHost)
        if theHost is None:
            print("The gRPC/SLURM server host is not defined.  Exiting.")
            sys.exit(1)
        thePort=os.environ.get('GEMS_GRPC_SLURM_PORT')
        print("the port is:  " + thePort)
        if theHost is None:
            print("The gRPC/SLURM server port is not defined.  Exiting.")
            sys.exit(1)
        
        hostport=theHost + ':' + thePort
        print("hostport is >>>" + hostport + "<<<")
        #with grpc.insecure_channel(hostport) as channel:
        with grpc.insecure_channel('gw-slurm-head:50052') as channel:
            stub = gems_grpc_slurm_pb2_grpc.GemsGrpcSlurmStub(channel)
            response = stub.GemsGrpcSlurmReceiver(gems_grpc_slurm_pb2.GemsGrpcSlurmRequest(input=self.json))
            print("gems_grpc_slurm_client returns this response: \n" + str(response) )
        return response


if __name__ == '__main__':
    logging.basicConfig()
    gems_grpc_slurm_client = GemsGrpcSlurmClient(json="{ \"hello\": \"hello world!\" }")
    print(gems_grpc_slurm_client.response)
