# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import gems_grpc_slurm_pb2 as gems__grpc__slurm__pb2


class GemsGrpcSlurmStub(object):
    """The JSON service definition."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GemsGrpcSlurmReceiver = channel.unary_unary(
            "/GemsGrpcSlurm.GemsGrpcSlurm/GemsGrpcSlurmReceiver",
            request_serializer=gems__grpc__slurm__pb2.GemsGrpcSlurmRequest.SerializeToString,
            response_deserializer=gems__grpc__slurm__pb2.GemsGrpcSlurmResponse.FromString,
        )


class GemsGrpcSlurmServicer(object):
    """The JSON service definition."""

    def GemsGrpcSlurmReceiver(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_GemsGrpcSlurmServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GemsGrpcSlurmReceiver": grpc.unary_unary_rpc_method_handler(
            servicer.GemsGrpcSlurmReceiver,
            request_deserializer=gems__grpc__slurm__pb2.GemsGrpcSlurmRequest.FromString,
            response_serializer=gems__grpc__slurm__pb2.GemsGrpcSlurmResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "GemsGrpcSlurm.GemsGrpcSlurm", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class GemsGrpcSlurm(object):
    """The JSON service definition."""

    @staticmethod
    def GemsGrpcSlurmReceiver(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/GemsGrpcSlurm.GemsGrpcSlurm/GemsGrpcSlurmReceiver",
            gems__grpc__slurm__pb2.GemsGrpcSlurmRequest.SerializeToString,
            gems__grpc__slurm__pb2.GemsGrpcSlurmResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
