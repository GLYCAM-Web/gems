#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
from gemsModules.mmservice.mdaas.services.ProjectManagement.api import (
    ProjectManagement_Inputs,
    ProjectManagement_Outputs,
)

from gemsModules.mmservice.mdaas.tasks import set_up_run_md_directory, update_10_produ_in_sim_length

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(inputs: ProjectManagement_Inputs) -> ProjectManagement_Outputs:
    """Executes the service."""
    log.debug(f"Beginning MDaaS ProjectManagement")
    log.debug(f"Got resources: {inputs.resources}")
    service_outputs = ProjectManagement_Outputs()

    # create project/output directory TODO: setup before copy_to or after?
    os.makedirs(inputs.outputDirPath, exist_ok=True)

    amber_parm7, amber_rst7, unmin_gas = None, None, None

    for resource in inputs.resources:
        # Copy all Resources to the output directory.
        copy = False

        if resource.resourceRole == "parameter-topology":
            amber_parm7 = resource.filename
            copy = True
        if resource.resourceRole == "input-coordinate":
            amber_rst7 = resource.filename
            copy = True
        if resource.resourceRole == "unminimized-gas":
            log.debug(f"unminimized-gas: {resource.filename}")
            unmin_gas = resource.filename
            copy = True

        if copy:
            resource.copy_to(inputs.outputDirPath)

    if not amber_parm7 or not amber_rst7:
        raise ValueError(f"Missing required AMBER-7-prmtop or AMBER-7-restart resource. got {amber_parm7=} {amber_rst7=} {unmin_gas=}")
        
    # Set up the run directory.
    set_up_run_md_directory.execute(
        protocol_files_dir=inputs.protocolFilesPath,
        output_dir_path=inputs.outputDirPath,
        # TODO: Right now, the uploads dir path is obtained from a default MDProject.
        parm7_real_name=amber_parm7,
        rst7_real_name=amber_rst7,
    )

    # Update the production.in file with the simulation length from the request
    update_10_produ_in_sim_length.execute(inputs.outputDirPath, inputs.sim_length)

    # update service outputs
    service_outputs.outputDirPath = inputs.outputDirPath

    return service_outputs
