#!/usr/bin/env python3
import os
from gemsModules.mmservice.mdaas.services.ProjectManagement.api import (
    ProjectManagement_Inputs,
    ProjectManagement_Outputs,
)

from gemsModules.mmservice.mdaas.tasks import set_up_run_md_directory

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(inputs: ProjectManagement_Inputs) -> ProjectManagement_Outputs:
    """Executes the service."""
    log.debug(f"serviceInputs: {inputs}")

    service_outputs = ProjectManagement_Outputs()

    # create output directory TODO: setup before copy_to or after?
    os.makedirs(inputs.outputDirPath, exist_ok=True)

    amber_parm7, amber_rst7 = None, None
    # We can do this because MDaaS's RDF fills in the input Resources from RunMD.
    # TODO: There are other notes on this. Rather than use requester, implied translator can be
    # used to copy inputs from entity to both services.
    for resource in inputs.resources:
        # Copy all Resources to the output directory.
        resource.copy_to(inputs.outputDirPath)

        if resource.resourceFormat == "AMBER-7-prmtop":
            amber_parm7 = inputs.outputDirPath + "/" + resource.filename
        if resource.resourceFormat == "AMBER-7-restart":
            amber_rst7 = inputs.outputDirPath + "/" + resource.filename

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

    # TODO: taskify
    # lets also update sim_length in the protocol here. We're given inputs.sim_length in ns, but must calculate the nstlim stepcount.
    sim_length = float(inputs.sim_length)
    nstlim = int(sim_length * 500000)  # 500k because dt=0.002
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

    return service_outputs
