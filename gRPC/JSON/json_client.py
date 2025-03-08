import logging

import grpc
import os

import json_pb2
import json_pb2_grpc

class JSONClient():
    def __init__(self, json):
        self.json = json
        self.response = self.run()

    def run(self):

        with grpc.insecure_channel(os.getenv('GRPC_DELEGATOR_HOST') + ':' + os.getenv('GRPC_DELEGATOR_PORT')) as channel:
        # with grpc.insecure_channel('localhost:50051') as channel:
            stub = json_pb2_grpc.JSONStub(channel)
            response = stub.JSON_Delegator(json_pb2.JSONRequest(input=self.json))
            #print("json_client returning a response: \n" + str(response) )
        return response


if __name__ == '__main__':
    logging.basicConfig()
    json_client = JSONClient(json="{ \"hello\": \"hello world!\" }")
    print(json_client.response)
