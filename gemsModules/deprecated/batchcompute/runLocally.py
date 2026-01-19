#!/usr/bin/env python3
import gemsModules.deprecated
from gemsModules.deprecated import common
from gemsModules.deprecated.common.services import *
from gemsModules.deprecated.common.transaction import *  # might need whole file...
import traceback
from gemsModules.deprecated.common.loggingConfig import *

from gemsModules.logging.logger import new_concurrent_logger

log = new_concurrent_logger(__name__)


def runJob(incoming_json_dict):
    log.debug("runJob() was called.\n")
    import os, sys, subprocess, signal
    from subprocess import Popen

    workdir = incoming_json_dict["workingDirectory"]
    sbatch_argument = incoming_json_dict["sbatchArgument"]

    if "sbatchArgument" not in incoming_json_dict.keys():
        return "Local submit cannot find submission directive ('sbatchArgument')."

    if incoming_json_dict["workingDirectory"] is not None:
        try:
            os.chdir(incoming_json_dict["workingDirectory"])
        except Exception as error:
            log.error("Was unable to change to the working directory.")
            log.error("Error type: " + str(type(error)))
            log.error(traceback.format_exc())
            return "Was unable to change to the working directory."
    log.debug("The current directory is:  " + os.getcwd())
    try:
        log.debug(
            "In func submit(), incoming dict sbatchArg is: "
            + incoming_json_dict["sbatchArgument"]
            + "\n"
        )
        p = subprocess.Popen(
            [incoming_json_dict["sbatchArgument"]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        (outputhere, errorshere) = p.communicate()
        if p.returncode != 0:
            return "Local submit got non-zero exit upon attempt to run job."
        else:
            log.debug("outputhere in raw form: " + str(outputhere))
            theOutput = outputhere.decode("utf-8")
            log.debug("outputhere stripped: " + theOutput)
            return theOutput
    except Exception as error:
        log.error("Was unable to submit the job.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
        return "Was unable to submit the job."


def manageIncomingString(jsonObjectString):
    """
    TODO write me a docstring
    """
    import os, sys, socket

    log.info("manageIncomingString() was called.\n")
    log.debug("incoming jsonObjectString: \n" + jsonObjectString)

    job_dict = json.loads(jsonObjectString)

    theResponse = runJob(job_dict)
    if theResponse is None:
        log.error("Got none response")
        ##TODO: return a proper error response
    else:
        log.debug("The outgoing dictionary is: \n")
        log.debug(str(theResponse))
        log.debug("\n")
        return theResponse


