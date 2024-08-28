#!/usr/bin/env python3
import os
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

# from gemsModules.complex.glycomimetics.tasks import batchcompute
from .api import ProjectManagement_Inputs, ProjectManagement_Outputs, PM_Resource

from gemsModules.complex.glycomimetics.tasks import set_up_build_directory

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(inputs: ProjectManagement_Inputs) -> ProjectManagement_Outputs:
    """Executes the service."""
    log.debug(f"serviceInputs: {inputs}")

    service_outputs = ProjectManagement_Outputs()
    service_outputs.resources.add_resource(
        PM_Resource(
            payload=inputs.projectDir,
            resourceFormat="string",
            resourceRole="ProjectDirectory",
        )
    )
    
    # Setup project directory, TODO: Taskify
    log.debug("GM/ProjectManagement: about to create project directory")
    os.makedirs(inputs.projectDir, exist_ok=True)
    
    log.debug("GM/ProjectManagement: about to copy resources to project dir")
    log.debug(f"GM/ProjectManagement: resources: {inputs.resources}")
    # Copy all PM_Resources to the output directory.
    for resource in inputs.resources:
        # TODO: Typify and copy all PM_Resources to the output directory appropriately.
        # if isinstance(resource, PM_Resource):
        file_resource = resource.copy_to(inputs.projectDir)
        
        # If it's main pdb, symlink it to projectDir/Receptor.pdb 
        # TODO/Q: Should it be Receptor and not CoComplex? # Yao's Evaluation likes sugars.
        if resource.resourceRole == "Receptor":
            # TODO: use the GM project's `complex` field for this.
            os.symlink(file_resource.payload, os.path.join(inputs.projectDir, "Receptor.pdb"))
        service_outputs.resources.add_resource(file_resource)

    # # TODO: we can use PM_Resource.copy_to to copy the files to the output directory.
    # service_outputs.resources = ProjectManagement_Resources(resources=resources)

    return service_outputs
