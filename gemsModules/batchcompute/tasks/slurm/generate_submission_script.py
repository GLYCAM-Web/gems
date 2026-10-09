#!/usr/bin/env python3

import os
import socket

from gemsModules.configuration.main_api import session_instance_config

from .slurm_director_settings import Known_Slurm_Submission_Builders

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def update_job_from_instance_config(SlurmJobDict):
    """Update the SlurmJobDict with context-specific sbatch arguments from the InstanceConfig."""
    ic_args = session_instance_config.get_batch_computing_arguments_for_context(
        SlurmJobDict.get("context", "")
    )
    for k, v in ic_args.items():
        if k not in SlurmJobDict or not SlurmJobDict[k]:
            SlurmJobDict[k] = v


def localize_working_directory(thisSlurmJobInfo):
    """Update the working directory in the SlurmJobInfo object with the context-specific filesystem path."""
    current_wd = thisSlurmJobInfo.incoming_dict.get("workingDirectory")
    if current_wd and os.path.exists(current_wd):
        return thisSlurmJobInfo

    ctx = thisSlurmJobInfo.incoming_dict.get("context", "")
    ic_path = session_instance_config.get_filesystem_path_by_service_ID(ctx)
    if ic_path and thisSlurmJobInfo.incoming_dict.get("pUUID"):
        thisSlurmJobInfo.incoming_dict["workingDirectory"] = os.path.join(
            ic_path,
            thisSlurmJobInfo.incoming_dict["pUUID"],
        )

    return thisSlurmJobInfo


def execute(thisSlurmJobInfo):
    """Create a slurm submission script with context-specific sbatch arguments using the InstanceConfig."""
    SlurmJobDict = thisSlurmJobInfo.incoming_dict

    update_job_from_instance_config(SlurmJobDict)
    localize_working_directory(thisSlurmJobInfo)

    SlurmJobDict["slurm_runscript_name"] = "slurm_submit.sh"

    SlurmJobDict["slurm_runscript_name"] = os.path.join(
        SlurmJobDict["workingDirectory"],
        SlurmJobDict["slurm_runscript_name"],
    )

    if "sbatchArgument" in SlurmJobDict and SlurmJobDict["sbatchArgument"]:
        log.debug("Prepending workdir to main sbatch command")
        if not SlurmJobDict["sbatchArgument"].startswith(SlurmJobDict["workingDirectory"]):
            SlurmJobDict["sbatchArgument"] = (
                os.path.join(
                    SlurmJobDict["workingDirectory"],
                    SlurmJobDict["sbatchArgument"],
                )
                + "\n"
            )
        else:
            if not SlurmJobDict["sbatchArgument"].endswith("\n"):
                SlurmJobDict["sbatchArgument"] += "\n"

    log.debug("Slurm runscript path: " + SlurmJobDict["slurm_runscript_name"] + "\n")
    if os.path.exists(SlurmJobDict["slurm_runscript_name"]):
        log.debug("Found existing Slurm runscript. Refusing to clobber.")
        return
    else:
        log.debug("Will generate a new Slurm runscript.")
        log.debug("About to create runscript on %s", socket.gethostname())
        log.debug("SlurmJobDict: " + str(SlurmJobDict))

    if SlurmJobDict["context"] in Known_Slurm_Submission_Builders:
        log.debug("About to create main submission script...")
        Known_Slurm_Submission_Builders[SlurmJobDict["context"]](SlurmJobDict)
