#!/usr/bin/env python3
import os
from pathlib import Path

# from gemsModules.complex.glycomimetics.tasks import batchcompute
from .api import ProjectManagement_Inputs, ProjectManagement_Outputs, PM_Resource
#from ...tasks import set_up_build_directory

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
    project_dir = Path(inputs.projectDir)
    if os.path.exists(project_dir / "outputs"):
        log.debug(f"GpB/ProjectManagement: project directory already exists: {inputs.projectDir}, skipping creation.")
    else:
        log.debug(f"GpB/ProjectManagement: about to create project directory: {inputs.projectDir}")
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(project_dir / "outputs", exist_ok=True)
        status_log_path = project_dir / "status.log"
                # Now lets touch the status.log file
        if not status_log_path.exists():
            log.debug(f"GpB/ProjectManagement: creating status.log file at {status_log_path}")
            status_log_path.touch()  # Create the status log file if it does not exist
        
        log.debug("GpB/ProjectManagement: about to copy resources to project dir")
        log.debug(f"GpB/ProjectManagement: resources: {inputs.resources}")
        # Copy all PM_Resources to the output directory.
        resources_to_replace_by_role = {}
        for resource in inputs.resources:
            new_resource = resource.copy_to(project_dir)
            if new_resource.resourceRole == "protein-file":
                # also create a symbolic link to the protein file at top-level
                protein_link = project_dir / "OriginalInput.pdb"
                if not protein_link.exists():
                    log.debug(f"GpB/ProjectManagement: creating symbolic link for protein file: {protein_link}")
                    if resource.locationType == "filesystem-path-unix":
                        protein_link.symlink_to(new_resource.payload)
                        with open(status_log_path, 'a') as f:
                            f.write(f"Default PDB file at {protein_link}\n")
                    else:
                        log.warning(f"GpB/ProjectManagement: Cannot create symbolic link for protein file, unsupported location type: {resource.locationType}")
                resources_to_replace_by_role[new_resource.resourceRole] = new_resource
            elif new_resource.resourceRole == "glycan-mappings":
                pass
            
        for role, resource in resources_to_replace_by_role.items():
            # pop the original resource from the inputs.resources
            inputs.resources.remove_resource_by_role(role)
            # and add the new resource to the service outputs
            service_outputs.resources.add_resource(resource)
            
        with open(status_log_path, 'a') as f:
            f.write("Project directory initialized,n")
            
    return service_outputs
