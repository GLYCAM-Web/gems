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
        
    # Run External/AAD2/0.configure/setup_AD_directory, then update ad2config
    #GEMSHOME = os.environ.get("GEMSHOME")/External/AAD2
    # TODO: use GW_DOMAIN to change test/actual/dev
    subprocess.run([f"/programs/website_aad2/test/AAD2_Docker/image/AAD2/0.configure/setup_AD_Directory"], cwd=inputs.projectDir)

    # move ad2config.example to ad2config and modify it
    shutil.move(f"{inputs.projectDir}/ad2config.example", f"{inputs.projectDir}/ad2config")
    replacements = {
        "Antibody_File_Name": antibody_name,
        "Glycan_File_Name": ligand_name,
        #"CONTAINER_NAME_PREFIX": f"{inputs.pUUID[:6]}-antibody-docking",
        "CONTAINER_NAME_PREFIX": "",
        "Computing_Mode": "Batch",
        "Use_Docker": "True",
        "AD2_Docking_Batch_Script": "submit_docking_to_slurm_with_docker.bash",
        "AD2_Docking_Local_Script": "gwconfig"
        # "GLYCAM_FLEXIBILITY": "Partial",
    }
    replace_bash_variable_in_file(f"{inputs.projectDir}/ad2config", replacements)
    
    # remove AD2_Random_Seeds=.*EOF from ad2config
    with open(f"{inputs.projectDir}/ad2config", "r") as f:
        lines = f.readlines()
    with open(f"{inputs.projectDir}/ad2config", "w") as f:
        for line in lines:
            if "AD2_Random_Seeds" not in line:
                f.write(line)
            else:
                break
            
    # Create ad2cliconfig (different from AD2config) Note: Not needed for AD to run
    # create_ad2cliconfig.execute(inputs.projectDir)
    
    # Move ad2dockerconfig.example to ad2dockerconfig and update it approriately
    shutil.move(f"{inputs.projectDir}/ad2dockerconfig.example", f"{inputs.projectDir}/ad2dockerconfig")

    with open("/programs/website_aad2/test/AAD2_Docker/settings.bash", "r") as f:
        ad2dockerconfig = f.readlines()
        # export AAD2_IMAGE_NAME="antibody-docking"
        # export AAD2_TAG_NAME="2025-03-05-09-36-blf
        for line in ad2dockerconfig:
            if "AAD2_IMAGE_NAME" in line:
                image_name = line.split("=")[1].strip().strip('"')
            if "AAD2_TAG_NAME" in line:
                tag_name = line.split("=")[1].strip().strip('"')

    replacements = {
        "Image": f"{image_name}:{tag_name}",
        "AAD2_DOCKER_HOME": "/programs/website_aad2/test/AAD2_Docker",
    }
    replace_bash_variable_in_file(f"{inputs.projectDir}/ad2dockerconfig", replacements)
    
    # gwconfig from /programs/gems/External/GW_Stack_for_AAD2/gwconfig.example
    gwconfig_example = f"/programs/website_aad2/test/GW_Stack_for_AAD2/gwconfig.example"
    gwconfig = f"{inputs.projectDir}/gwconfig"
    shutil.copy(gwconfig_example, gwconfig)
    replacements = {
        "pUUID": inputs.pUUID,
        "DOCKING_REPLICA_CPUS": "56",
    }
    replace_bash_variable_in_file(gwconfig, replacements)
    
    # slurm_submit_docking /programs/gems/External/GW_Stack_for_AAD2/submit_docking_to_slurm_with_docker.bash
    slurm_submit_docking = f"/programs/website_aad2/test/GW_Stack_for_AAD2/submit_docking_to_slurm_with_docker.bash"
    actual_submit_docking = shutil.copy(slurm_submit_docking, inputs.projectDir)
    # change #SBATCH --cpus-per-task=${DOCKING_REPLICA_CPUS}
    # to #SBATCH --cpus-per-task=56
    with open(actual_submit_docking, "r") as f:
        lines = f.readlines()
    with open(actual_submit_docking, "w") as f:
        for line in lines:
            if "#SBATCH --cpus-per-task=${DOCKING_REPLICA_CPUS}" in line:
                f.write("#SBATCH --cpus-per-task=56\n")
            else:
                f.write(line)

    
    # # TODO: we can use PM_Resource.copy_to to copy the files to the output directory.
    # service_outputs.resources = ProjectManagement_Resources(resources=resources)

    return service_outputs
