#!/usr/bin/env python3
import gemsModules
from gemsModules import common
from gemsModules.common.services import *
from gemsModules.common.transaction import * # might need whole file...
import traceback
from gemsModules.batchcompute.slurm.dataio import *
from gemsModules.common.loggingConfig import *

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

def submit(thisSlurmJobInfo):
    log.debug("submit() was called.\n")
    import os, sys, subprocess, signal
    from subprocess import Popen

    if 'sbatchArgument' not in thisSlurmJobInfo.incoming_dict.keys():
        return "SLURM submit cannot find sbatch submission arguments."

    if thisSlurmJobInfo.incoming_dict['workingDirectory'] is not None:
        try:
            os.chdir(thisSlurmJobInfo.incoming_dict['workingDirectory'])
        except Exception as error:
            log.error("Was unable to change to the working directory.")
            log.error("Error type: " + str(type(error)))
            log.error(traceback.format_exc())
            return "Was unable to change to the working directory."
    log.debug("The current directory is:  " + os.getcwd() )
    try:
        log.debug ("In func submit(), incoming dict sbatchArg is: " + thisSlurmJobInfo.incoming_dict['sbatchArgument'] + "\n")
        p = subprocess.Popen( [ 'sbatch', thisSlurmJobInfo.incoming_dict["slurm_runscript_name"] ] ,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (outputhere,errorshere) = p.communicate()
        if p.returncode != 0 :
            return "SLURM submit got non-zero exit upon attempt to submit."
        else:
            log.debug("outputhere in raw form: " + str(outputhere))
            theOutput=outputhere.decode("utf-8")
            log.debug("outputhere stripped: " + theOutput)
            return theOutput
    except Exception as error:
        log.error("Was unable to submit the job.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        return "Was unable to submit the job."

def writeSlurmSubmissionScript(path, thisSlurmJobInfo):
    import sys
    try:
        script = open(path, "w")
    except Exception as error:
        log.error("Cannnot write slurm run script. Aborting")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        sys.exit(1)

    incoming_dict = thisSlurmJobInfo.incoming_dict

    script.write("#!/bin/bash" + "\n")
    script.write("#SBATCH --chdir=" + incoming_dict["workingDirectory"] + "\n")
    script.write("#SBATCH --error=slurm_%x-%A.err" + "\n")
    script.write("#SBATCH --get-user-env" + "\n")
    script.write("#SBATCH --job-name=" + incoming_dict["name"] + "\n")
    script.write("#SBATCH --nodes=1" + "\n")
    script.write("#SBATCH --output=slurm_%x-%A.out" + "\n")
    script.write("#SBATCH --partition=" + incoming_dict["partition"] + "\n")
    script.write("#SBATCH --tasks-per-node=1" + "\n")
    script.write("#SBATCH --uid=" + incoming_dict["user"] + "\n")
    script.write("\n")
    script.write("bash " + incoming_dict["sbatchArgument"] + "\n")

def manageIncomingString(jsonObjectString):
    """
    TODO write me a docstring
    """
    import os, sys, socket

    log.info("manageIncomingString() was called.\n")
    log.debug("incoming jsonObjectString: \n" + jsonObjectString)

    # Make a new SlurmJobInfo object for holding I/O information.
    thisSlurmJobInfo=SlurmJobInfo(jsonObjectString)
    thisSlurmJobInfo.parseIncomingString()

    # Figure out whether we need to send this to a different machine
    useGRPC=True
    thePort=os.environ.get('GEMS_GRPC_SLURM_PORT')
    log.debug("the port is: " + thePort)
    if thePort is None:
        log.debug("cant find grpc slurm submission port. using localhost")
        useGRPC=False
    theHost=os.environ.get('GEMS_GRPC_SLURM_HOST')
    log.debug("the host is: " + theHost)
    if theHost is None:
        log.debug("cant find grpc slurm submission host. using localhost")
        useGRPC=False
    else:
        localHost = socket.gethostname()
        log.debug("the local host is: " + localHost)
        if theHost == localHost:
            useGRPC=False
    thisSlurmJobInfo.incoming_dict["slurm_runscript_name"] = "slurm_submit.sh"
    slurm_runscript_path = thisSlurmJobInfo.incoming_dict["workingDirectory"] + "/" + thisSlurmJobInfo.incoming_dict["slurm_runscript_name"]
    log.debug ("Slurm runscript path: " + slurm_runscript_path + "\n")
    writeSlurmSubmissionScript(slurm_runscript_path, thisSlurmJobInfo)

    log.debug("useGRPC: " + str(useGRPC))
    if useGRPC:
        gemsPath = os.environ.get('GEMSHOME')
        if gemsPath is None:
            return "Cannot determine GEMSHOME."
        sys.path.append(gemsPath + "/gRPC/SLURM")
        import grpc
        import gems_grpc_slurm_client

        log.debug("submitting to gems_grpc_slurm_client.")
        submission = gems_grpc_slurm_client.GemsGrpcSlurmClient(json=jsonObjectString)
        return submission.response

    else:
        log.debug("not using grpc.")
        theResponse = submit(thisSlurmJobInfo)
        if theResponse is None:
            log.error("Got none response")
            ##TODO: return a proper error response
        else:
            thisSlurmJobInfo.copyJobinfoInToOut()
            thisSlurmJobInfo.addSbatchResponseToJobinfoOut(theResponse)
            log.debug("The outgoing dictionary is: \n")
            log.debug(str(thisSlurmJobInfo.outgoing_dict))
            log.debug("\n")
            return thisSlurmJobInfo.outgoing_dict


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

