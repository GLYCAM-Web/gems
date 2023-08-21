from abc import abstractmethod, ABC
import json
import logging
import argparse
from pathlib import Path
import sys

from typing import Literal
import grpc
import os

import protos.minimal_pb2
import protos.minimal_pb2_grpc

log = logging.getLogger(__name__)


class GRPCClient(ABC):
    STUB_TYPE = None
    PB_MODULE = None

    def __init__(self, host):
        self.host = host

        self._stub = None
        self._pb_module = None
        self._channel = None

    @property
    def protobuf(self):
        return self.PB_MODULE

    @property
    def stub(self):
        if self._stub is None:
            self._stub = self.STUB_TYPE(self.channel)
        return self._stub

    @property
    def channel(self):
        if self._channel is None:
            self._channel = grpc.insecure_channel(self.host)
        return self._channel

    def close(self):
        if self._channel is not None:
            self._channel.close()
            self._channel = None

    @abstractmethod
    def send_request(self, request):
        pass

    @abstractmethod
    def get_response(self, request):
        pass


class MinClient(GRPCClient):
    STUB_TYPE = protos.minimal_pb2_grpc.UnaryStub
    PB_MODULE = protos.minimal_pb2

    def send_request(self, request):
        log.debug(f"Querying {self.host} with {request}...")
        response = self.get_response(request)
        log.debug(f"Response: {response}")
        return response

    def get_response(self, request):
        return self.stub.GetServerResponse(self.protobuf.Message(message=request))


# Useful for TESTDELEGATOR
def init_argshost_from_env(args):
    # example hosts:
    # $GRPC_DELEGATOR_HOST:$GRPC_DELEGATOR_PORT
    # $GEMS_GRPC_SLURM_HOST:$GEMS_GRPC_SLURM_PORT
    try:
        slurm_host = (
            f"{os.getenv('GEMS_GRPC_SLURM_HOST')}:{os.getenv('GEMS_GRPC_SLURM_PORT')}"
        )
    except TypeError:
        log.warning("This container is not configured to use GEMS_GRPC_SLURM_HOST.")
        slurm_host = None

    try:
        delegator_host = (
            f"{os.getenv('GRPC_DELEGATOR_HOST')}:{os.getenv('GRPC_DELEGATOR_PORT')}"
        )
    except TypeError:
        log.warning("This container is not configured to use GRPC_DELEGATOR_HOST.")
        delegator_host = None

    # If we don't use a special keyword, it will just pass through the "host:port"
    if args.host == "delegator":
        args.host = delegator_host
    elif args.host == "slurm":
        args.host = slurm_host
    elif args.host == "conntest":
        args.host = f"{os.getenv('GRPC_DELEGATOR_HOST')}:51151"

    if args.host is None:
        raise ValueError("No valid host provided.")

    return args


def argparser():
    # takes host / port and json_request_path OR json stdin
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--host",
        type=str,
        default="localhost:51151",
        help="The host to connect to. Can be a docker container label or a host:port string.",
    )
    parser.add_argument(
        "--json",
        type=str,
        default='{ "hello": "hello world!" }',
        help="The JSON to send to the server. Can be a path to a file or a stdin string.",
    )

    args = parser.parse_args()
    args = init_argshost_from_env(args)

    # If no json provided, check stdin
    if args.json is None:
        args.json = sys.stdin.read()
    elif Path(args.json).exists():
        with open(args.json, "r") as f:
            args.json = f.read()

    if args.json is None:
        raise ValueError("No JSON provided.")

    return args


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = argparser()

    log.debug("The JsonClient is going to attempt contacting: %s", args.host)
    client = MinClient(host=args.host)

    response = client.query(request=args.json)

    log.debug(f"Response:\n{response}")


if __name__ == "__main__":
    main()
