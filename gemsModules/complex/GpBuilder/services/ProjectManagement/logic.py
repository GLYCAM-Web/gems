#!/usr/bin/env python3
import os
from pathlib import Path

# from gemsModules.complex.glycomimetics.tasks import batchcompute
from gemsModules.common.main_api_resources import Resource, Resources
from .api import ProjectManagement_Inputs, ProjectManagement_Outputs, PM_Resource, PM_Output_Resources
#from ...tasks import set_up_build_directory

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def handle_protein_file_resource(resource, project_dir: Path, status_log_path: Path):
    # Create a constant symbolic link to this Build's protein file at top-level
    protein_link = project_dir / "OriginalInput.pdb"
    if not protein_link.exists():
        log.debug(f"GpB/ProjectManagement: creating symbolic link for protein file: {protein_link}")
        if resource.locationType == "filesystem-path-unix":
            protein_link.symlink_to(resource.payload)
            
            # Log the creation of the symbolic link
            with open(status_log_path, 'a') as f:
                f.write(f"Default PDB file at {protein_link}\n")
        else:
            log.warning(f"GpB/ProjectManagement: Cannot create symbolic link for protein file, unsupported location type: {resource.locationType}")
            log.error(f"Unsupported location type for protein file: {resource.locationType}")
    
    
def make_resources_project_specific(inputs_resources: Resources, output_resources: Resources, project_dir: Path, status_log_path: Path) -> Resources:
    """ Updates the resources to be project-specific by copying them to the project directory.
    
    Also handles specific resource roles behaviour.
    """
    
    updated_resources = {}
    updated_service_resources = PM_Output_Resources()
    
    for input_resource in inputs_resources:
        if input_resource.resourceRole == "protein-file":
            # Copy the resource to the project directory
            project_resource = input_resource.copy_to(project_dir)
            
            handle_protein_file_resource(project_resource, project_dir, status_log_path)
            
            # update the resources
            this_role = project_resource.resourceRole
            if this_role in updated_resources:
                log.warning(f"GpB/ProjectManagement: Multiple protein files found, replacing existing one for role: {this_role}")        
                log.debug(f"The resource was: {updated_resources[this_role]=}")
            updated_resources[this_role] = input_resource, project_resource
            log.debug(f"GpB/ProjectManagement: Updated resource for role {this_role}: {updated_resources[this_role]}")
        elif input_resource.resourceRole == "rcsb-id":
            # Need to update it for protein-file
            pass
        
    # Remove the original resources from inputs.resources now that we're done iterating them.
    # Also add the new resources to the updated_service_resources.
    for role, (input_resource, project_resource) in updated_resources.items():
        # pop the original resource from the inputs.resources
        # inputs.resources.remove_resource_by_role(role)
        inputs_resources.remove(input_resource)
        updated_service_resources.add_resource(project_resource)
    
    output_resources.extend(updated_service_resources)


def execute(inputs: ProjectManagement_Inputs) -> ProjectManagement_Outputs:
    """Executes the service."""
    log.debug(f"serviceInputs: {inputs}")

    service_outputs = ProjectManagement_Outputs()
    service_outputs.resources.add_resource(
        PM_Resource(
            payload=inputs.projectDir,
            resourceFormat="string",
            resourceRole="project-directory",
            locationType="filesystem-path-unix"
        )
    )
    
    project_dir = Path(inputs.projectDir)
    if os.path.exists(project_dir / "outputs"):
        log.debug(f"GpB/ProjectManagement: project directory already exists: {inputs.projectDir}, skipping creation.")
    else:
        # Setup project directory.
        log.debug(f"GpB/ProjectManagement: about to create project directory: {inputs.projectDir}")
        os.makedirs(project_dir / "outputs")
        
        # Create a status log file in the project directory.
        status_log_path = project_dir / "status.log"
        status_log_path.touch()
               
        # Update the project directory with resources and add them to the service output resources.
        log.debug("GpB/ProjectManagement: about to manage and copy input resources to project dir")
        log.debug(f"GpB/ProjectManagement: resources: {inputs.resources}")
        make_resources_project_specific(inputs.resources, service_outputs.resources, project_dir, status_log_path)
        
        # Log the initialization of the project directory
        log.debug(f"GpB/ProjectManagement: project directory initialized at {project_dir}")
        with open(status_log_path, 'a') as f:
            f.write("Project directory initialized\n")
            
    return service_outputs
