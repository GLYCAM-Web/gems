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

    context = minimal_json_dict.get("context") or "MDaaS-RunMD"
    useSLURM = False
    try:
        from gemsModules.configuration.main_api import session_instance_config
        from gemsModules.networkconnections.grpc import is_GEMS_instance_for_SLURM_submission

        if is_GEMS_instance_for_SLURM_submission(context) or session_instance_config.get_possible_hosts_for_context(
            context, with_jsonport=True
        ):
            useSLURM = True
    except Exception as error:
        log.debug("Could not check instance_config for SLURM hosts: %s", error)

    if not useSLURM:
        thePort = os.environ.get("GEMS_GRPC_SLURM_PORT")
        theHost = os.environ.get("GEMS_GRPC_SLURM_HOST")
        if thePort is not None and theHost is not None:
            useSLURM = True

    if useSLURM:
        slurm_receive.manageIncomingString(output_str)
    else:
        runLocally.manageIncomingString(output_str)



if __name__ == "__main__":
    batch_compute(sys.argv[1])
