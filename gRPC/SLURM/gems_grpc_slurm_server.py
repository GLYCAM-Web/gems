"""The Python implementation of the GemsGrpcSlurmReceiver server."""

from concurrent import futures
import time
import logging

import grpc
import os,sys,subprocess,signal
from subprocess import *

import gems_grpc_slurm_pb2
import gems_grpc_slurm_pb2_grpc

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
print("Hello from gems_grpc_slurm_server.py")

class GemsGrpcSlurmReceiver(gems_grpc_slurm_pb2_grpc.GemsGrpcSlurmServicer):

    def GemsGrpcSlurmReceiver(self, request, context):
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        GemsPath = os.environ.get('GEMSHOME')
        if GemsPath == None:
            theResponse=JSON_Error_Response('GemsHomeNotSet')
            return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=theResponse)

        os.environ['GEMS_DEBUG_VERBOSITY']='-1'
        jobsubmissioncommand = GemsPath+"/bin/slurmreceive"
        try:
            p = subprocess.Popen(jobsubmissioncommand, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False) 
            theStdin=request.input.encode('utf-8')
            (outputhere,errorshere) = p.communicate(input=theStdin)
            # Check to see if there were any errors, either by exit code or existence of stderr
            theErrorReturned=None
            if p.returncode == -11 or p.returncode == 139:
                theErrorReturned='CaughtSegFault'
            elif p.returncode != 0 :
                theErrorReturned='UnknownError'
            elif errorshere :
                theErrorReturned='HaveStderr'
            # If there was an error, return an error report
            if theErrorReturned is not None:
                theResponse=JSON_Error_Response(theErrorReturned,p.returncode,str(outputhere),str(errorshere),None)
                sys.stderr.write("For date-time stamp: " + dt_string)
                sys.stderr.write("For this submission: "  + jobsubmissioncommand) 
                sys.stderr.write("This is the result: "  + theResponse)
                return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=theResponse)
        # If even that failed, still send something back
        except Exception as error:
            sys.stderr.write("For date-time stamp: " + dt_string)
            sys.stderr.write("Caught exception:  "  + str(error))
            theResponse=JSON_Error_Response('CaughtException',None,None,None,str(error))
            return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=theResponse)
        # If no errors detected, return the standard output
        return gems_grpc_slurm_pb2.GemsGrpcSlurmResponse(output=outputhere)

def serve():
    print("Starting to serve Slurm via GRPC.")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gems_grpc_slurm_pb2_grpc.add_GemsGrpcSlurmServicer_to_server(GemsGrpcSlurmReceiver(), server)
    # server.add_insecure_port(os.environ.get('GEMS_GRPC_SLURM_HOST') + ':' + os.environ.get('GEMS_GRPC_SLURM_PORT'))
    # server.add_insecure_port('[::]:50505')
    # TODO  Add capability for a secure port
    thePort=os.environ.get('GEMS_GRPC_SLURM_PORT')
    if thePort is None:
        print("The GEMS_GRPC_SLURM_PORT is not set.  Exiting.")
        sys.exit(1)
    server.add_insecure_port('[::]:' + thePort)
    server.start()
    try:
        while True:
            print("Starting sleepytime.")
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt")
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


