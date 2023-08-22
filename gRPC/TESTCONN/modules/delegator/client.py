import json
import logging
import argparse
from pathlib import Path
import sys

from typing import Literal
import grpc
import os

import json_pb2
import json_pb2_grpc

log = logging.getLogger(__name__)


class JSONClient:
    def __init__(self, host=None, json=None):
        # Compatibility for how JSONClient is already used by json_api.submit, which assumes GRPC_DELEGATOR and no host argument.
        # Otherwise host can be a required positional argument and the argparser would handle this default.
        if os.getenv("GRPC_DELEGATOR_HOST") is not None and host is None:
            host = (
                f"{os.getenv('GRPC_DELEGATOR_HOST')}:{os.getenv('GRPC_DELEGATOR_PORT')}"
            )

        self.host = host
        self.json = json
        self.response = None

        if json is not None:
            self.response = self.run()

    def run(self, json=None, host=None):
        host = host or self.host
        json = json or self.json
        log.debug(f"Using {host} for JSON client.\n\nRequest:\n{json}\n\n")
        with grpc.insecure_channel(host) as channel:
            stub = json_pb2_grpc.JSONStub(channel)
            response = stub.JSON_Delegator(json_pb2.JSONRequest(input=json))
        return response


def argparser():
    # takes host / port and json_request_path OR json stdin
    parser = argparse.ArgumentParser()

    # example hosts:
    # $GRPC_DELEGATOR_HOST:$GRPC_DELEGATOR_PORT
    # $GEMS_GRPC_SLURM_HOST:$GEMS_GRPC_SLURM_PORT
    # Some default hosts to use if we can
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

    # can be "delegator" or "slurm" or "host:port" where host is a docker container label on the same network
    parser.add_argument("--host", type=str, default=delegator_host)

    # Can be a jsonstr or a path to a json file
    parser.add_argument("--json", type=str, default='{ "hello": "hello world!" }')

    args = parser.parse_args()

    # If we don't use a special keyword, it will just pass through the "host:port"
    if args.host == "delegator":
        args.host = delegator_host
    elif args.host == "slurm":
        args.host = slurm_host
    elif args.host == "gg":
        args.host = f"{os.getenv('GRPC_DELEGATOR_HOST')}:51151"

    if args.host is None:
        raise ValueError("No valid host provided.")
    log.debug("The JsonClient is going to attempt contacting: %s", args.host)

    # If no json provided, check stdin
    if args.json is None:
        args.json = sys.stdin.read()

    # Check if the given json argument is a path, if not, just assume it's a json string. (we do nothing)
    if Path(args.json).exists():
        with open(args.json, "r") as f:
            args.json = f.read()

    if args.json is None:
        raise ValueError("No JSON provided.")

    return args


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = argparser()

    json_client = JSONClient(host=args.host, json=args.json)

    response = json.loads(json_client.response.output)
    log.debug(f"Response:\n{json.dumps(response['entity'], indent=2)}\n\n")


if __name__ == "__main__":
    main()
