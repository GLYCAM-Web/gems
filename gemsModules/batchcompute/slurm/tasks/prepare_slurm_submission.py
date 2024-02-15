#!/usr/bin/env python3

import os
import socket
from gemsModules.mmservice.mdaas.tasks import create_slurm_submission

from gemsModules.networkconnections.grpc import slurm_grpc_submit, RpcError

from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


# TODO: This is deeply coupled with systemoperations.instance_config.InstanceConfig / instance_config.json
def create_contextual_slurm_submission_script(thisSlurmJobInfo):
    """Create a slurm submission script with context-specific sbatch arguments using the InstanceConfig."""
    SlurmJobDict = thisSlurmJobInfo.incoming_dict

    ic = InstanceConfig()
    ic_args = ic.get_keyed_arguments(
        "sbatch_arguments", context=SlurmJobDict["context"]
    )

    SlurmJobDict.update(ic_args)

    SlurmJobDict["slurm_runscript_name"] = "slurm_submit.sh"
    SlurmJobDict["workingDirectory"] = os.path.join(
        ic.get_md_filesystem_path(),
        SlurmJobDict["pUUID"],
    )
    # instead of passing working directory, pass pUUID only and get base mdcluster path # also this will need to have specialized function for contexts in the future. (md cluster path is only for MDaaS-RunMD)
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

    # In the future, We could possibly move this down to after we know if this is the correct host to submit on.
    log.debug("Slurm runscript path: " + SlurmJobDict["slurm_runscript_name"] + "\n")
    if os.path.exists(SlurmJobDict["slurm_runscript_name"]):
        log.debug("Found existing Slurm runscript.  Refusing to clobber.")
        return
    else:
        log.debug("Will generate a new Slurm runscript.")
        log.debug("About to create runscript on %s", socket.gethostname())
        log.debug("SlurmJobDict: " + str(SlurmJobDict))

    create_slurm_submission.execute(SlurmJobDict)


def seek_correct_host(jsonObjectString, context):
    """Using gRPC, try to reroute the request to the correct host given a context, usually the current one."""
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
        # maybe should be error?
        log.warning(
            "All attempts to make a SLURM submission over gRPC failed. servers tried: %s",
            tried,
        )

    return response
