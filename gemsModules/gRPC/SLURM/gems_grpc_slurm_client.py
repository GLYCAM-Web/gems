import logging

import grpc
import os

import gems_grpc_slurm_pb2
import gems_grpc_slurm_pb2_grpc

class GemsGrpcSlurmClient():
    def __init__(self, json):
        self.json = json
        self.response = self.run()

    def run(self):

        with grpc.insecure_channel(os.getenv('GEMS_GRPC_SLURM_HOST') + ':' + os.getenv('GEMS_GRPC_SLURM_PORT')) as channel:
        # with grpc.insecure_channel('localhost:50505') as channel:
            stub = gems_grpc_slurm_pb2_grpc.GemsGrpcSlurmStub(channel)
            response = stub.GemsGrpcSlurmReceiver(gems_grpc_slurm_pb2.GemsGrpcSlurmRequest(input=self.json))
            #print("json_client returning a response: \n" + str(response) )
        return response


if __name__ == '__main__':
    logging.basicConfig()
    gems_grpc_slurm_client = GemsGrpcSlurmClient(json="{ \"hello\": \"hello world!\" }")
    print(gems_grpc_slurm_client.response)
