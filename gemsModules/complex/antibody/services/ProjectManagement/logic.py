#!/usr/bin/env python3
import os
import subprocess
import shutil
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.systemoperations.filesystem_ops import replace_bash_variable_in_file

# from gemsModules.complex.antibody.tasks import batchcompute
from .api import ProjectManagement_Inputs, ProjectManagement_Outputs, PM_Resource

from gemsModules.complex.antibody.tasks import create_ad2cliconfig

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
    log.debug(f"GM/ProjectManagement: about to create project directory: {inputs.projectDir}")
    os.makedirs(inputs.projectDir, exist_ok=True)
    
    log.debug("GM/ProjectManagement: about to copy resources to project dir")
    log.debug(f"GM/ProjectManagement: resources: {inputs.resources}")
    # Copy all PM_Resources to the output directory.
    for resource in inputs.resources:
        # TODO: Typify and copy all PM_Resources to the output directory appropriately.
        # if isinstance(resource, PM_Resource):
        file_resource = resource.copy_to(inputs.projectDir)
        
        # If it's the input pdb, symlink it at projectDir/Complex.pdb 
        if resource.resourceRole == "Antibody":
            source = os.path.relpath(file_resource.payload, inputs.projectDir)
            target = os.path.join(inputs.projectDir, "protein.pdb") # AD default pdb name for Antibody
            os.symlink(source, target)
        elif resource.resourceRole == "Ligand":
            source = os.path.relpath(file_resource.payload, inputs.projectDir)
            target = os.path.join(inputs.projectDir, "ligand.pdb")
            os.symlink(source, target)
        service_outputs.resources.add_resource(file_resource)
        
    # TODO: Run External/AAD2/0.configure/setup_AD_directory, then update ad2config
    GEMSHOME = os.environ.get("GEMSHOME")
    subprocess.run([f"{GEMSHOME}/External/AAD2/0.configure/setup_AD_Directory"], cwd=inputs.projectDir)

    # move ad2config.example to ad2config and modify it
    shutil.move(f"{inputs.projectDir}/ad2config.example", f"{inputs.projectDir}/ad2config")
    replacements = {
        "Antibody_File_Name": "protein.pdb",
        "Glycan_File_Name": "ligand.pdb",
    }
    replace_bash_variable_in_file(f"{inputs.projectDir}/ad2config", replacements)

    # Create ad2cliconfig (different from AD2config)
    create_ad2cliconfig.execute(inputs.projectDir)
    
    # Move ad2dockerconfig.example to ad2dockerconfig and update it approriately
    # TODO 
    
    # # TODO: we can use PM_Resource.copy_to to copy the files to the output directory.
    # service_outputs.resources = ProjectManagement_Resources(resources=resources)

    return service_outputs
