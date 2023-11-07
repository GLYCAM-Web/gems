#!/usr/bin/env python3
import os
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

# from gemsModules.mmservice.mdaas.tasks import batchcompute
from gemsModules.mmservice.mdaas.services.ProjectManagement.api import (
    ProjectManagement_Inputs,
    ProjectManagement_Outputs,
)
from gemsModules.mmservice.mdaas.services.ProjectManagement.resources import (
    ProjectManagement_Resources,
    PM_Resource,
)

from gemsModules.mmservice.mdaas.tasks import set_up_run_md_directory

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(inputs: ProjectManagement_Inputs) -> ProjectManagement_Outputs:
    """Executes the service."""
    log.debug(f"serviceInputs: {inputs}")

    service_outputs = ProjectManagement_Outputs()

    set_up_run_md_directory.execute(
        protocol_files_dir=inputs.protocolFilesPath,
        output_dir_path=inputs.outputDirPath,
        # TODO: Right now, the uploads dir path is obtained from a default MDProject.
        uploads_dir_path=inputs.inputFilesPath,
        parm7_real_name=inputs.amber_parm7,
        rst7_real_name=inputs.amber_rst7,
    )

    # lets also update sim_length in the protocol here. We're given inputs.sim_length in ns, but must calculate the nstlim stepcount.
    sim_length = float(inputs.sim_length)
    nstlim = int(sim_length * 500000)  # 500k because dt=0.002
    # TODO: edit_amber_input_file() is not yet implemented.
    with open(inputs.outputDirPath + "/10.produ.in", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if "nstlim" in lines[i]:
                lines[i] = f"  nstlim = {nstlim},\n"
            if "ntwx" in lines[i]:
                lines[i] = f"  ntwx = {int(nstlim * 0.01)},\n"
            if "ntpr" in lines[i]:
                lines[i] = f"  ntpr = {int(nstlim * 0.01)},\n"
            if "ntwe" in lines[i]:
                lines[i] = f"  ntwe = {int(nstlim * 0.01)},\n"
            if "ntwr" in lines[i]:
                lines[i] = f"  ntwr = -{int(nstlim * 0.1)},\n"

    with open(inputs.outputDirPath + "/10.produ.in", "w") as f:
        f.writelines(lines)

    # update service outputs
    service_outputs.outputDirPath = inputs.outputDirPath

    # TODO: use resources to copy all input files to the output directory, such as parm7/rst7 as well.
    for resource in inputs.resources:
        # Copy all PM_Resources to the output directory.
        if isinstance(resource, PM_Resource):
            resource.copy_to(inputs.outputDirPath)

    # # TODO: we can use PM_Resource.copy_to to copy the files to the output directory.
    # service_outputs.resources = ProjectManagement_Resources(resources=resources)

    return service_outputs
