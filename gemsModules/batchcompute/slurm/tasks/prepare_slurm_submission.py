#!/usr/bin/env python3

import os
import socket

from gemsModules.systemoperations.instance_config import InstanceConfig

from ..slurm_director_settings import Known_Slurm_Submission_Builders

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def update_job_from_instance_config(SlurmJobDict):
    """Update the SlurmJobDict with context-specific sbatch arguments from the InstanceConfig."""
    ic = InstanceConfig()

    ic_args = ic.get_keyed_arguments(
        "sbatch_arguments", context=SlurmJobDict["context"]
    )

    SlurmJobDict.update(ic_args)


def localize_working_directory(thisSlurmJobInfo):
    """Update the working directory in the SlurmJobInfo object with the context-specific filesystem path."""
    thisSlurmJobInfo.incoming_dict["workingDirectory"] = os.path.join(
        InstanceConfig().get_filesystem_path(thisSlurmJobInfo.incoming_dict["context"]),
        thisSlurmJobInfo.incoming_dict["pUUID"],
    )

    return thisSlurmJobInfo


# TODO: This is deeply coupled with systemoperations.instance_config.InstanceConfig / instance_config.json
def create_contextual_slurm_submission_script(thisSlurmJobInfo):
    """Create a slurm submission script with context-specific sbatch arguments using the InstanceConfig."""

    # TODO: Part of decoupling batchcompute and making it a separate Entity
    # involves creating a proper transaction. we shoudn't just modify the incoming_dict.
    SlurmJobDict = thisSlurmJobInfo.incoming_dict

    update_job_from_instance_config(SlurmJobDict)
    localize_working_directory(thisSlurmJobInfo)

    # TODO: Depending on what entity is calling this, we may need to rename the submission script.
    SlurmJobDict["slurm_runscript_name"] = "slurm_submit.sh"

    # instead of passing working directory, pass pUUID only and get base mdcluster path
    # # also this will need to have specialized function for contexts in the future. (md cluster path is only for MDaaS-RunMD)
    SlurmJobDict["slurm_runscript_name"] = os.path.join(
        SlurmJobDict["workingDirectory"],
        SlurmJobDict["slurm_runscript_name"],
    )

    SlurmJobDict["sbatchArgument"] = (
        os.path.join(
            SlurmJobDict["workingDirectory"],
            SlurmJobDict["sbatchArgument"],
        )
        + "\n"
    )

    log.debug("Slurm runscript path: " + SlurmJobDict["slurm_runscript_name"] + "\n")
    if os.path.exists(SlurmJobDict["slurm_runscript_name"]):
        log.debug("Found existing Slurm runscript.  Refusing to clobber.")
        return
    else:
        log.debug("Will generate a new Slurm runscript.")
        log.debug("About to create runscript on %s", socket.gethostname())
        log.debug("SlurmJobDict: " + str(SlurmJobDict))

    # We generate the slurm submission script here, but each entity may have different requirements.
    # We had to wait until batchcompute/slurm ensured we were on the appropriate host to perform this, which is why we now
    # must use Entity-specific functions to generate the script from batch compute.
    #
    # This is currently parallel to the Delegator's redirector_settings.py
    if SlurmJobDict["context"] in Known_Slurm_Submission_Builders:
        Known_Slurm_Submission_Builders[SlurmJobDict["context"]](SlurmJobDict)


def seek_correct_host(jsonObjectString, context):
    """Using gRPC, try to reroute the request to the correct host given a context, usually the current one."""
    from gemsModules.networkconnections.grpc import slurm_grpc_submit, RpcError

    addresses = InstanceConfig().get_possible_hosts_for_context(
        context, with_slurmport=True
    )

    failed = False
    tried = []
    response = None
    while len(addresses):
        h, p = addresses.pop().split(":")
        try:
            response = slurm_grpc_submit(jsonObjectString, host=h, port=p)
            failed = False
            break
        except RpcError:
            failed = True
            log.warning(
                "Failed to submit to %s:%s. Trying next host in list.",
                h,
                p,
                exc_info=True,
            )
        finally:
            tried.append(h)

    if failed:
        log.error(
            "All attempts to make a SLURM submission over gRPC failed. servers tried: %s",
            tried,
        )

    return response
