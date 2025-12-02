#!/usr/bin/python3.9

import sys
import os
import json
import subprocess

import traceback
from gemsModules.deprecated.common.loggingConfig import *

from gemsModules.logging.logger import new_concurrent_logger

log = new_concurrent_logger(__name__)


def batch_compute_delegation(incoming_json_dict):
    # For right now, slurm in the only agent for batch compute to call.
    from gemsModules.deprecated.batchcompute.slurm import receive as slurm_receive
    from gemsModules.deprecated.batchcompute import runLocally

    #slurm_basic_submission_json = {}
    #workdir = incoming_json_dict["workingDirectory"]
    #sbatch_argument = incoming_json_dict["sbatchArgument"]

    minimal_json_dict = incoming_json_dict
    output_str = json.dumps(minimal_json_dict)

    useSLURM = True
    thePort = os.environ.get("GEMS_GRPC_SLURM_PORT")
    log.debug("the port is: " + str(thePort))
    if thePort is None:
        log.debug("cant find grpc slurm submission port. using localhost")
        useSLURM = False
    theHost = os.environ.get("GEMS_GRPC_SLURM_HOST")
    log.debug("the host is: " + str(theHost))
    if theHost is None:
        log.debug("cant find grpc slurm submission host. using localhost")
        useSLURM = False


    if useSLURM: 
        slurm_receive.manageIncomingString(output_str)
    else: 
        #workdir = incoming_json_dict["workingDirectory"]
        #sbatch_argument = incoming_json_dict["sbatchArgument"]
        runLocally.manageIncomingString(output_str)



if __name__ == "__main__":
    batch_compute(sys.argv[1])
