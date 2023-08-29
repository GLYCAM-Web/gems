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

    service_outputs.outputDirPath = inputs.outputDirPath

    # TODO: use resources to copy all input files to the output directory.
    for resource in inputs.resources:
        if isinstance(resource, PM_Resource):
            resource.copy_to(inputs.outputDirPath)

    # # TODO: we can use PM_Resource.copy_to to copy the files to the output directory.
    # service_outputs.resources = ProjectManagement_Resources(resources=resources)

    return service_outputs
