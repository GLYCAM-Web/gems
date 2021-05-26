"""The Python implementation of the GemsGrpcSlurmReceiver server."""

from concurrent import futures
import time
import logging  ## this might not be necessary - maybe used by gRPC?

import grpc
import os,sys,subprocess,signal
from subprocess import *

import gems_grpc_slurm_pb2
import gems_grpc_slurm_pb2_grpc

from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


brief_to_code = {
    'GemsHomeNotSet' :              1 ,
    'PythonPathHasNoGemsModules' :  2 ,
    'IncorrectNumberOfArgs' :       3 ,
    'UnknownError' :                4 ,
    'NotAFile' :                    5 ,
    'NotAJSONObject' :              6 ,
    'CaughtSegFault' :              7 ,
    'CaughtException' :             8 ,
    'HaveStderr' :                  9
}
code_to_message = {
    1 : 'Unable to read or set a usable GEMSHOME.',
    2 : 'Unable to find gemsModules in the PYTHON_PATH.',
    3 : 'The number of command-line arguments is incorrect.',
    4 : 'There was an unknown fatal error.',
    5 : 'The name specified on the command line does not reference a file.',
    6 : 'The input supplied is not a JSON objct.' ,
    7 : 'A subprocess generated a segmentation fault.',
    8 : 'Caught an exception internally to the script.',
    9 : 'Process returned 0 as exit status, but also returned standard error.'
}

def JSON_Error_Response(theBrief,theExitCode,theStdout,theStderr,theExceptionError):
    whoIAm='GemsGrpcSlurmReceiver'
    errorcode=brief_to_code[theBrief]
    if not theExitCode:
        theExitCode='None'
    if theExitCode is None:
        theExitCode='None'
    if not theStderr :
        theStderr='None'
    if theStderr is None:
        theStderr='None'
    if not theStdout :
        theStdout='None'
    if theStdout is None :
        theStdout='None'
    if not theExceptionError :
        theExceptionError='None'
    if theExceptionError is None :
        theExceptionError='None'
    # Build the JSON object to return if there is an error
    thereturn = "{ \"entity\" : { \"type\": \"GRPC\", \"responses\" : \
[{ \"Error\" : { \"respondingService\" : \"" + whoIAm + "\",\
\"notice\" : { \"type\" : \"Exit\",\
\"code\" : \"" + str(errorcode) + "\",\
\"brief\" : \"" + theBrief + "\",\
\"message\" : \"" + str(code_to_message[errorcode]) + "\"\
} \"options\" : {\
\"osExitCode\" : \"" + str(theExitCode)  + "\", \
\"theStandardError\": \"" + theStderr  + "\" \
\"theStandardOutput\": \"" + theStdout  + "\" \
\"theExceptionError\": \"" + theExceptionError  + "\" \
} } } ] } }"

    return thereturn

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
log.info("Hello from gems_grpc_slurm_server.py")

class GemsGrpcSlurmReceiver(gems_grpc_slurm_pb2_grpc.GemsGrpcSlurmServicer):

    def GemsGrpcSlurmReceiver(self, request, context):
        from datetime import datetime
        log.info("gRPC Slurm server has been called.")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        GemsPath = os.environ.get('GEMSHOME')
        if GemsPath == None:
            theResponse=JSON_Error_Response('GemsHomeNotSet')
            return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=theResponse)

        log.debug("The request input is >>>"+request.input+"<<<")
        log.debug("GEMSHOME is >>>"+GemsPath+"<<<")
        os.environ['GEMS_DEBUG_VERBOSITY']='-1'
        jobsubmissioncommand = GemsPath+"/bin/slurmreceive"
        try:
            p = subprocess.Popen(jobsubmissioncommand, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False) 
            theStdin=request.input.encode('utf-8')
            (outputhere,errorshere) = p.communicate(input=theStdin)
            # Check to see if there were any errors, either by exit code or existence of stderr
            theErrorReturned=None
            if p.returncode == -11 or p.returncode == 139:
                log.error("gRPC Slurm server caught a segfault.")
                theErrorReturned='CaughtSegFault'
            elif p.returncode != 0 :
                theErrorReturned='UnknownError'
                log.error("gRPC Slurm server caught an unknown error.")
            elif errorshere :
                theErrorReturned='HaveStderr'
                log.error("gRPC Slurm server found output to STDERR despite a zero exit code.")
            # If there was an error, return an error report
            if theErrorReturned is not None:
                theResponse=JSON_Error_Response(theErrorReturned,p.returncode,str(outputhere),str(errorshere),None)
                log.error("For date-time stamp: " + dt_string)
                log.error("For this submission: "  + jobsubmissioncommand) 
                log.error("This is the result: "  + theResponse)
                return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=theResponse)
        # If even that failed, still send something back
        except Exception as error:
            log.error("For date-time stamp: " + dt_string)
            log.error("Caught exception while trying to run the subprocess:  "  + str(error))
            theResponse=JSON_Error_Response('CaughtException',None,None,None,str(error))
            return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=theResponse)
        # If no errors detected, return the standard output
        return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=outputhere)

def serve():
    log.info("Starting to serve Slurm via GRPC.")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gems_grpc_slurm_pb2_grpc.add_GemsGrpcSlurmServicer_to_server(GemsGrpcSlurmReceiver(), server)
    # TODO  Add capability for a secure port
    thePort=os.environ.get('GEMS_GRPC_SLURM_PORT')
    if thePort is None:
        log.error("The GEMS_GRPC_SLURM_PORT is not set.  Exiting.")
        sys.exit(1)
    server.add_insecure_port('[::]:' + thePort)
    server.start()
    try:
        while True:
            log.info("Starting sleepytime.")
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        log.info("Caught keyboard interrupt")
        server.stop(0)

if __name__ == '__main__':
    # logging.basicConfig()
    try:
        print("About to call serve.")
        serve()
    except Exception as error:
        print("gems_grpc_slurm_server.py main/serve caught an error.")
        print(str(error))
    finally:
        print("Cleaning up and shutting down.")
        sys.exit(1) ## TODO:  change this number to something reasonable


