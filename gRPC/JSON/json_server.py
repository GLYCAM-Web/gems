"""The Python implementation of the GRPC JSON_Delegator server."""

from concurrent import futures
import time

import grpc
import os,sys,subprocess
from subprocess import *

import json
import json_pb2
import json_pb2_grpc

from gemsModules.logging.logger import new_concurrent_logger
log = new_concurrent_logger(__name__, force_dirty=True)

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
    8 : 'Caught an exception internally to the script..',
    9 : 'Process returned 0 as exit status, but also returned standard error.'
}

def JSON_Error_Response(theBrief,theExitCode,theStdout,theStderr,theExceptionError):
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
[{ \"Error\" : { \"respondingService\" : \"JSONServer\",\
\"notice\" : { \"type\" : \"Exit\",\
\"code\" : \"" + str(errorcode) + "\",\
\"brief\" : \"" + theBrief + "\",\
\"message\" : \"" + str(code_to_message[errorcode]) + "\"\
}, \"options\" : {\
\"osExitCode\" : \"" + str(theExitCode)  + "\", \
\"theStandardError\": " + json.dumps(theStderr)  + ", \
\"theStandardOutput\": " + json.dumps(theStdout)  + ", \
\"theExceptionError\": \"" + theExceptionError  + "\" \
} } } ] } }"

    return thereturn

print("Hello from json_server.py")

class JSON_Delegator(json_pb2_grpc.JSONServicer):

    def JSON_Delegator(self, request, context):
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        GemsPath = os.environ.get('GEMSHOME')
        if GemsPath == None:
            theResponse=JSON_Error_Response('GemsHomeNotSet')
            return json_pb2.JSONResponse(output=theResponse)

        os.environ['GEMS_DEBUG_VERBOSITY']='-1'
        jobsubmissioncommand = GemsPath+"/bin/delegate"
        try:
            print("Hello from json_server.py JSON_Delegator() 1000")
            #start = time.time()
            theStdin=request.input.encode('utf-8')
            p = subprocess.run(jobsubmissioncommand, input=theStdin, capture_output=True, shell=False) 
            #end1 = time.time()
            outputhere = p.stdout
            errorshere = p.stderr
            #end2 = time.time()
            #print(end1 - start)
            #print(end2 - start)
            # Check to see if there were any errors, either by exit code or existence of stderr
            theErrorReturned=None
            if p.returncode == -11 or p.returncode == 139:
                theErrorReturned='CaughtSegFault'
            elif p.returncode != 0 :
                theErrorReturned='UnknownError'
            elif errorshere :
                theErrorReturned='HaveStderr'
            else :
                pass 
            # If there was an error, return an error report
            if theErrorReturned is not None:
                theResponse=JSON_Error_Response(theErrorReturned,p.returncode,str(outputhere),str(errorshere),None)
                print("For date-time stamp: " + dt_string)
                print("For this submission: "  + jobsubmissioncommand) 
                print("With this input: "  + request.input) 
                print("This is the result: "  + theResponse)
                return json_pb2.JSONResponse(output=theResponse)
        # If even that failed, still send something back
        except Exception as error:
            print("For date-time stamp: " + dt_string)
            print("Caught exception:  "  + str(error))
            theResponse=JSON_Error_Response('CaughtException',None,None,None,str(error))
            return json_pb2.JSONResponse(output=theResponse)
        # If no errors detected, return the standard output
        return json_pb2.JSONResponse(output=outputhere)

def serve():
    print("Starting to serve JSON API as GRPC.")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    json_pb2_grpc.add_JSONServicer_to_server(JSON_Delegator(), server)
    # server.add_insecure_port(os.getenv('GRPC_DELEGATOR_HOST') + ':' + os.getenv('GRPC_DELEGATOR_PORT'))
    thePort = os.getenv('GRPC_DELEGATOR_PORT')
    if thePort is None:
        thePort = '50051'
        log.debug("The gRPC/JSON server port is not defined.  Using default port 50051.")

    server.add_insecure_port(f'[::]:{thePort}')
    server.start()
    print(f"Server started on port: {thePort}")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Caught keyboard interrupt")
        server.stop(0)

if __name__ == '__main__':
    # logging.basicConfig()
    try:
        print("About to call serve.")
        serve()
    except Exception as error:
        print("json_server.py main/serve caught an error.")
        print(str(error))
    finally:
        print("Cleaning up and shutting down.")
        sys.exit(1) ## TODO:  change this number to something reasonable


