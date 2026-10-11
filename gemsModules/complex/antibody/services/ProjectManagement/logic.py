#!/usr/bin/env python3
import os
import subprocess
import shutil
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.systemoperations.filesystem_ops import replace_bash_variable_in_file
from gemsModules.systemoperations.environment_ops import get_site_version

# from gemsModules.complex.antibody.tasks import batchcompute
from gemsModules.complex.antibody.services.ProjectManagement.api import ProjectManagement_Inputs, ProjectManagement_Outputs, PM_Resource

from gemsModules.complex.antibody.tasks.create_configs import create_ad2config, create_gwconfig, create_vcconfig
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
    
    antibody_name, ligand_name = None, None
    for resource in inputs.resources:
        # TODO: Typify and copy all PM_Resources to the output directory appropriately.
        # if isinstance(resource, PM_Resource):
        file_resource = resource.copy_to(inputs.projectDir)
        
        # If it's the input pdb, symlink it at projectDir/Complex.pdb 
        if resource.resourceRole == "Antibody":
            antibody_name = os.path.relpath(file_resource.payload, inputs.projectDir)
            # target = os.path.join(inputs.projectDir, "protein.pdb") # AD default pdb name for Antibody
            # os.symlink(source, target)
        elif resource.resourceRole == "Ligand":
            ligand_name = os.path.relpath(file_resource.payload, inputs.projectDir)
            # target = os.path.join(inputs.projectDir, "ligand.pdb")
            # os.symlink(source, target)
        service_outputs.resources.add_resource(file_resource)
        
    # Note: AAD2 configuration from execution host settings
    site_version = get_site_version()
    create_vcconfig(inputs.projectDir+"/vcconfig")
    create_gwconfig(inputs.projectDir+"/gwconfig", inputs.pUUID)
    create_ad2config(inputs.projectDir+"/ad2config", antibody_name, ligand_name, siteversion=site_version)
    
    # Locate AAD2_Docker home
    aad2_docker_home = os.environ.get("AAD2_DOCKER_HOME")
    if not aad2_docker_home or not os.path.exists(aad2_docker_home):
        candidate_paths = [
            f"/programs/website_aad2/{site_version}/AAD2_Docker",
            "/home/lachele/WORK/AAD2_Docker",
        ]
        for cand in candidate_paths:
            if os.path.exists(cand):
                aad2_docker_home = cand
                break
    if not aad2_docker_home:
        aad2_docker_home = f"/programs/website_aad2/{site_version}/AAD2_Docker"

    image_name, tag_name = None, None
    settings_file = os.path.join(aad2_docker_home, "settings.bash")
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            for line in f:
                if "AAD2_IMAGE_NAME" in line and "=" in line:
                    image_name = line.split("=")[1].strip().strip('"\'')
                if "AAD2_TAG_NAME" in line and "=" in line:
                    tag_name = line.split("=")[1].strip().strip('"\'')

    replacements = {
        "AAD2_DOCKER_HOME": aad2_docker_home,
        "AAD2_CLI_BIN_PATH": os.path.join(aad2_docker_home, "image/AAD2/bin"),
    }
    if image_name and tag_name:
        replacements["Image"] = f"{image_name}:{tag_name}"
    replace_bash_variable_in_file(f"{inputs.projectDir}/ad2config", replacements)
    log.debug(f"The AD2 image is: '{image_name}:{tag_name}'")

    slurm_submit_docking = os.path.join(aad2_docker_home, "image/AAD2/bin/submit_docking_to_slurm_with_docker.bash")
    if os.path.exists(slurm_submit_docking):
        actual_submit_docking = shutil.copy(slurm_submit_docking, inputs.projectDir)
        if not os.path.exists(actual_submit_docking):
            log.warning(f"GM/ProjectManagement: Error copying {slurm_submit_docking} to {inputs.projectDir}")
    else:
        log.debug(f"slurm_submit_docking file not present on this host: {slurm_submit_docking}")

    return service_outputs
