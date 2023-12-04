"""The Python implementation of the GemsGrpcSlurmReceiver server."""

import os, sys, subprocess, json, asyncio

from concurrent import futures
from subprocess import *

import grpc
import gems_grpc_slurm_pb2, gems_grpc_slurm_pb2_grpc

from grpc_health.v1 import health_pb2, health_pb2_grpc


from gemsModules.logging.logger import new_concurrent_logger

# in production this is causing problems. TODO: separate logging files per server.
# log = Set_Up_Logging(__name__)
# because this gets called by grpc we need to make sure to open a fresh file handler. for a logger

log = new_concurrent_logger(__name__, force_dirty=True)

MAX_RETRIES = 5
CHECK_INTERVAL = 5


# Combined dictionary
briefs = {
    "GemsHomeNotSet": (1, "Unable to read or set a usable GEMSHOME."),
    "PythonPathHasNoGemsModules": (2, "Unable to find gemsModules in the PYTHON_PATH."),
    "IncorrectNumberOfArgs": (3, "The number of command-line arguments is incorrect."),
    "UnknownError": (4, "There was an unknown fatal error."),
    "NotAFile": (
        5,
        "The name specified on the command line does not reference a file.",
    ),
    "NotAJSONObject": (6, "The input supplied is not a JSON objct."),
    "CaughtSegFault": (7, "A subprocess generated a segmentation fault."),
    "CaughtException": (8, "Caught an exception internally to the script."),
    "HaveStderr": (
        9,
        "Process returned 0 as exit status, but also returned standard error.",
    ),
}


def JSON_Error_Response(theBrief, theExitCode, theStdout, theStderr, theExceptionError):
    errorcode, message = briefs[theBrief]

    error_response = {
        "entity": {
            "type": "GRPC",
            "responses": [
                {
                    "Error": {
                        "respondingService": "GemsGrpcSlurmReceiver",
                        "notice": {
                            "type": "Exit",
                            "code": str(errorcode),
                            "brief": theBrief,
                            "message": message,
                        },
                        "options": {
                            "osExitCode": str(theExitCode) if theExitCode else "None",
                            "theStandardError": theStderr or "None",
                            "theStandardOutput": theStdout or "None",
                            "theExceptionError": theExceptionError or "None",
                        },
                    }
                }
            ],
        }
    }

    return json.dumps(error_response)


ONE_DAY_IN_SECONDS = 60 * 60 * 24
log.info("Hello from gems_grpc_slurm_server.py")


class GemsGrpcSlurmReceiver(gems_grpc_slurm_pb2_grpc.GemsGrpcSlurmServicer):
    def GemsGrpcSlurmReceiver(self, request, context):
        print(f"Inside GemsGrpcSlurmReceiver method {context}")
        from datetime import datetime

        log.info("gRPC Slurm server has been called.")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        GemsPath = os.environ.get("GEMSHOME")
        if GemsPath == None:
            theResponse = JSON_Error_Response("GemsHomeNotSet")
            return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=theResponse)

        log.debug("The request input is >>>" + request.input + "<<<")
        log.debug("GEMSHOME is >>>" + GemsPath + "<<<")
        os.environ["GEMS_DEBUG_VERBOSITY"] = "-1"
        jobsubmissioncommand = GemsPath + "/bin/slurmreceive"
        try:
            print("About to run the subprocess with command:", jobsubmissioncommand)
            p = subprocess.Popen(
                jobsubmissioncommand, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False
            )
            theStdin = request.input.encode("utf-8")
            print("The stdin is:", theStdin)
            (outputhere, errorshere) = p.communicate(input=theStdin)
            print(
                f"process results: {theStdin=} {outputhere=} {errorshere=} {p.returncode=}"
            )

            # Check to see if there were any errors, either by exit code or existence of stderr
            theErrorReturned = None
            if p.returncode == -11 or p.returncode == 139:
                log.error("gRPC Slurm server caught a segfault.")
                theErrorReturned = "CaughtSegFault"
            elif p.returncode == 129:
                log.error("Common services not found")
                theErrorReturned = "CommonServicesNotFound"
            elif p.returncode != 0:
                theErrorReturned = "UnknownError"
                log.error("gRPC Slurm server caught an unknown error.")
            elif errorshere:
                theErrorReturned = "HaveStderr"
                log.error(
                    "gRPC Slurm server found output to STDERR despite a zero exit code."
                )
            # If there was an error, return an error report
            if theErrorReturned is not None:
                print("Got an error ", theErrorReturned)
                theResponse = JSON_Error_Response(
                    theErrorReturned,
                    p.returncode,
                    str(outputhere),
                    str(errorshere),
                    None,
                )
                log.error("For date-time stamp: " + dt_string)
                log.error("For this submission: " + jobsubmissioncommand)
                log.error("This is the result: " + theResponse)
                return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=theResponse)
        # If even that failed, still send something back
        except Exception as error:
            print(error)
            log.error("For date-time stamp: " + dt_string)
            log.error(
                "Caught exception while trying to run the subprocess:  " + str(error)
            )
            theResponse = JSON_Error_Response(
                "CaughtException", None, None, None, str(error)
            )
            print("trying to respond with error")
            return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=theResponse)
        # If no errors detected, return the standard output
        return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=outputhere)


async def serve():
    print("serving")
    log.info("Starting to serve Slurm via GRPC.")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gems_grpc_slurm_pb2_grpc.add_GemsGrpcSlurmServicer_to_server(
        GemsGrpcSlurmReceiver(), server
    )
    # TODO  Add capability for a secure port
    thePort = os.environ.get("GEMS_GRPC_SLURM_PORT")
    if thePort is None:
        log.error("The GEMS_GRPC_SLURM_PORT is not set.  Exiting.")
        sys.exit(1)
    server.add_insecure_port("[::]:" + thePort)
    server.start()
    print(f"Server started on port: {thePort}")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        log.info("Caught keyboard interrupt")
        server.stop(0)


async def check_server_health(health_stub, max_retries, check_interval):
    retries = 0
    while retries < max_retries:
        try:
            response = await health_stub.Check(
                health_pb2.HealthCheckRequest(service="")
            )
            if response.status == health_pb2.HealthCheckResponse.SERVING:
                print("Server is healthy")
                retries = 0  # Reset the retry counter if the server is healthy
            else:
                print("Server is not healthy")
                retries += 1
        except Exception as e:
            print(f"Health check failed: {e}")
            retries += 1

        await asyncio.sleep(check_interval)

    raise Exception("Server has been unhealthy for too long, initiating restart...")


async def main():
    while True:
        # Setup the gRPC channel and stub for health checking
        channel = grpc.insecure_channel("localhost:66666")
        health_stub = health_pb2_grpc.HealthStub(channel)

        # Start the server and health checker
        serve_task = asyncio.create_task(serve())
        health_check_task = asyncio.create_task(
            check_server_health(health_stub, MAX_RETRIES, CHECK_INTERVAL)
        )

        try:
            await asyncio.gather(serve_task, health_check_task)
        except health_check_task.exception() as e:
            print(f"Restarting server due to health check failure: {e}")

        print("Restarting serve function...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt received, exiting.")
        sys.exit(0)
