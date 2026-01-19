from dataclasses import dataclass
import traceback
import grpc
import concurrent.futures as futures
import logging
import os
import subprocess

from typing import Optional
from subprocess import PIPE

import protos.minimal_pb2 as stub
import protos.minimal_pb2_grpc

log = logging.getLogger(__name__)


class MinServicer(protos.minimal_pb2_grpc.UnaryServicer):
    def GetServerResponse(self, request, context):
        log.info("TESTCONN server has been called.")

        response = stub.MessageResponse(stdout="No response.")
        GEMSHOME = os.environ.get("GEMSHOME")
        if GEMSHOME == None:
            log.error("GEMSHOME is not set.")
            response = stub.MessageResponse(stdout="GemsHomeNotSet")
        else:
            try:
                p = subprocess.Popen(
                    f"{GEMSHOME}/bin/delegate",
                    stdin=PIPE,
                    stdout=PIPE,
                    stderr=PIPE,
                    shell=False,
                )

                log.debug(f"Request: {request}")
                (stdout, stderr) = p.communicate(input=request.message.encode("utf-8"))

                if p.returncode != 0 or stderr:
                    response = stub.MessageResponse(
                        stdout=stdout.decode("utf-8").replace('"', ""),
                        stderr=stderr.decode("utf-8").replace('"', ""),
                        exitCode=p.returncode,
                        errorType="Error",
                    )
                else:
                    log.debug(f"Succesfully received response: {stdout}")
                    response = stub.MessageResponse(
                        stdout.decode("utf-8").replace('"', "")
                    )
            except Exception as error:
                response = stub.MessageResponse(
                    stdout="No response.",
                    exitCode=1,
                    errorType="Exception",
                    exception=traceback.format_exc(),
                )

        return response


def create_server(port=51151):
    pool = futures.ThreadPoolExecutor(max_workers=10)
    server = grpc.server(pool)

    server.add_insecure_port(f"[::]:{port}")

    protos.minimal_pb2_grpc.add_UnaryServicer_to_server(MinServicer(), server)

    return pool, server


def main(port=51151):
    logging.basicConfig(level=logging.DEBUG)

    pool, server = create_server(port)

    try:
        server.start()
        log.info("TESTCONN server started.")
        server.wait_for_termination()
    except KeyboardInterrupt:
        log.info("Stopping TESTCONN server...")
    finally:
        server.stop(0)
        pool.shutdown(wait=True)


if __name__ == "__main__":
    main()
