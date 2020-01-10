#!/usr/bin/env python3
import gemsModules
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
import traceback
from gemsModules.batchcompute.slurm.dataio import *

def submit(thisSlurmJobInfo):
    import os, sys, subprocess, signal
    from subprocess import Popen

    if 'sbatchArgument' not in thisSlurmJobInfo.incoming_dict.keys():
        return "SLURM submit cannot find sbatch submission arguments."

    if thisSlurmJobInfo.incoming_dict['workingDirectory'] is not None:
        try:
            os.chdir(thisSlurmJobInfo.incoming_dict['workingDirectory'])
        except Exception as error:
            print("Was unable to change to the working directory.")
            print("Error type: " + str(type(error)))
            print(traceback.format_exc())
            return "Was unable to change to the working directory."
#    print("The current directory is:  " + os.getcwd() )
    try:
        print ("In func submit(), incoming dict sbatchArg is: " + thisSlurmJobInfo.incoming_dict['sbatchArgument'] + "\n")
        p = subprocess.Popen( [ 'sbatch', thisSlurmJobInfo.incoming_dict['sbatchArgument'] ] ,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (outputhere,errorshere) = p.communicate()
        if p.returncode != 0 :
            print ("Sbatch stdout is: " + str(outputhere) + "\n") #Yao's printing statement
            return "SLURM submit got non-zero exit upon attempt to submit."
        else:
            return str(outputhere)
    except Exception as error:
        print("Was unable to submit the job.")
        print("Error type: " + str(type(error)))
        print(traceback.format_exc())
        return "Was unable to submit the job."

def writeSlurmSubmissionScript(path, jsonObjectString):
    import sys
    try:
        script = open(path, "w")
    except Exception as error:
        print("Cannnot write slurm run script. Aborting")
        sys.exit(1)

    script.write("#!/bin/bash" + "\n")
    script.write("#SBATCH --chdir=" + jsonObjectString["workingDirectory"] + "\n")
    script.write("#SBATCH --error=slurm_%x-%A.err" + "\n")
    script.write("#SBATCH --get-user-env" + "\n")
    script.write("#SBATCH --job-name=" + jsonObjectString["name"] + "\n")
    script.write("#SBATCH --nodes=1" + "\n")
    script.write("#SBATCH --output=slurm_%x-%A.out" + "\n")
    script.write("#SBATCH --partition=" + jsonObjectString["partition"] + "\n")
    script.write("#SBATCH --tasks-per-node=1" + "\n")
    script.write("#SBATCH --uid=" + jsonObjectString["user"] + "\n")
    script.write("\n")
    script.write("bash " + jsonObjectString["sbatchArgument"] + "\n")

def manageIncomingString(jsonObjectString):
    """
    TODO write me a docstring
    """
    import os, sys, socket

    if verbosity > 0 :
        print("~~~\nbatchcompute.slurm receive.py submit() was called.\n~~~")
    if verbosity > 1 :
        print("incoming jsonObjectString: \n" + jsonObjectString)

    # Make a new SlurmJobInfo object for holding I/O information.
    thisSlurmJobInfo=SlurmJobInfo(jsonObjectString)
    thisSlurmJobInfo.parseIncomingString()

    # Figure out whether we need to send this to a different machine
    useGRPC=True
    thePort=os.environ.get('GEMS_GRPC_SLURM_PORT')
    print("the port is: " + thePort)
    if thePort is None:
        print("cant find grpc slurm submission port. using localhost")
        useGRPC=False
    theHost=os.environ.get('GEMS_GRPC_SLURM_HOST')
    print("the host is: " + theHost)
    if theHost is None:
        print("cant find grpc slurm submission host. using localhost")
        useGRPC=False
    else:
        localHost = socket.gethostname()
        print("the local host is: " + localHost)
        if theHost == localHost:
            useGRPC=False

    slurm_runscript_path = jsonObjectString["workingDirectory"] + "/slurm_submit.sh" 
    writeSlurmSubmissionScript(slurm_runscript_path, jsonObjectString)

    if useGRPC:
        gemsPath = os.environ.get('GEMSHOME')
        if gemsPath is None:
            return "Cannot determine GEMSHOME."
        sys.path.append(gemsPath + "/gRPC/SLURM")
        import grpc 
        import gems_grpc_slurm_client

        submission = gems_grpc_slurm_client.GemsGrpcSlurmClient(json=jsonObjectString)
        return submission.response
    else:
        theResponse = submit(thisSlurmJobInfo)
        if theResponse is None:
            print("Got none response")
        else:
            return theResponse


def main():
    import importlib.util, os, sys
    #from importlib import util
    if importlib.util.find_spec("gemsModules") is None:
        this_dir, this_filename = os.path.split(__file__)
        sys.path.append(this_dir + "/../../")
        if importlib.util.find_spec("common") is None:
          print("I cannot find the Common Servicer.  No clue what to do. Exiting")
          sys.exit(1)
        else:
          from common import utils
    else:
        from gemsModules.common import utils
    jsonObjectString=utils.JSON_From_Command_Line(sys.argv)
    try:
        thisSlurmJobInfo=manageIncomingString(jsonObjectString)
    except Exception as error:
        print("\nThe Slurm Job info string manager captured an error.")
        print("Error type: " + str(type(error)))
        print(traceback.format_exc())
        ##TODO: see about exploring this error and returning more info. Temp solution for now.
    try:
        submit(thisSlurmJobInfo)
    except Exception as error:
        print("\nThe Slurm Job sumbit module captured an error.")
        print("Error type: " + str(type(error)))
        print(traceback.format_exc())
  
  
    print("\ndelegator is returning this: \n" +  responseObjectString)


if __name__ == "__main__":
    main()

