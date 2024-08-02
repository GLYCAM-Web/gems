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
    log.debug("Beginning MDaaS ProjectManagement")

    service_outputs = ProjectManagement_Outputs()

    # create project/output directory TODO: setup before copy_to or after?
    os.makedirs(inputs.outputDirPath, exist_ok=True)

    amber_parm7, amber_rst7 = None, None

    ug_resource_parent = None  # Part of hack below, TODO: REMOVE
    for resource in inputs.resources:
        # Hack to resolve the unminimized-gas.parm7 file from the parent sequence project.
        if (
            resource.locationType == "filesystem-path-unix"
            and resource.resourceFormat == "AMBER-7-prmtop"
            and ug_resource_parent is None
        ):
            log.debug(f"resource.payload: {resource.payload}")
            ug_resource_parent = Path(resource.payload).parent

        # Copy all Resources to the output directory.
        resource.copy_to(inputs.outputDirPath)

        if resource.resourceFormat == "AMBER-7-prmtop":
            amber_parm7 = inputs.outputDirPath + "/" + resource.filename
        if resource.resourceFormat == "AMBER-7-restart":
            amber_rst7 = inputs.outputDirPath + "/" + resource.filename

    # TODO/PRIORITY: should be it's own resource:
    # This MUST be a temporary hack and could be replaced with an API change including a specified min-gas Resource.
    # To implement this properly, we must update these scripts, at a minimum:
    # request_data_filler, PM.execute(this file), set_up_run_md_directory, and project_manager.
    if ug_resource_parent:
        ug_path = ug_resource_parent / "unminimized-gas.parm7"
        # this file isn't actually necessary for MDaaS, but tasks/set_up_run_md_directory used by the RunMD service
        # will symlink it if it exists in the MD Project.
        if ug_path.exists():
            # copy unminimized-gas.parm7 to outputDirPath, to be symlinked by tasks/set_up_run_md_directory.
            shutil.copy(ug_path, inputs.outputDirPath)
    else:
        log.warning("We were not able to resolve the unminimized-gas.parm7 file, likely because a filesystem-path-unix resource was not used and this is not currently supported.")
        log.warning("MDInput.parm7 will not be symlinked.")

    if not amber_parm7 or not amber_rst7:
        raise ValueError("Missing required AMBER-7-prmtop or AMBER-7-restart resource.")

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
