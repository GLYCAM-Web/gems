#!/usr/bin/env python3
import os
from pathlib import Path

from gemsModules.common.main_api_resources import Resource, Resources
from .api import ProjectManagement_Inputs, ProjectManagement_Outputs, PM_Resource, PM_Output_Resources
from ...tasks import download_pdb_from_rcsb_by_id

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def make_resources_project_specific(inputs_resources: Resources, output_resources: Resources, project_dir: str, uploads_path: str, status_log_path: Path) -> Resources:
    """ Updates the resources to be project-specific by copying them to the project directory.
    
    Also handles specific resource roles behaviour.
    """
    while input_resource := inputs_resources.pop():
        if input_resource.resourceRole == "protein-file":
            # Copy the resource to the project directory
            project_resource = input_resource.copy_to(Path(project_dir))
            protein_link = Path(project_dir) / "OriginalInput.pdb"
            if not protein_link.exists():
                log.debug(f"GpB/ProjectManagement: creating symbolic link for protein file: {protein_link}")
                if project_resource.locationType == "filesystem-path-unix":
                    protein_link.symlink_to(project_resource.payload)
                    
                    # Log the creation of the symbolic link
                    with open(status_log_path, 'a') as f:
                        f.write(f"Default PDB file at {protein_link}\n")
                else:
                    log.error(f"GpB/ProjectManagement: Cannot create symbolic link for protein file, unsupported location type: {project_resource.locationType}")
            else:
                log.debug(f"GpB/ProjectManagement: symbolic link for protein file already exists: {protein_link}")
            output_resources.add_resource(project_resource)
            
        elif input_resource.resourceRole == "rcsb-id":
            log.debug("Creating PDB file and resource from RCSB ID resource.")
            # Need to update it for protein-file
            download_path = download_pdb_from_rcsb_by_id.execute(
                pdb_id=input_resource.payload,
                output_dir=Path(uploads_path),
                compressed=False
            )
            
            # Create a new resource for the downloaded file
            project_resource = Resource(
                payload=download_path,
                resourceFormat="PDB",
                resourceRole="protein-file",
                locationType="filesystem-path-unix"
            )
            inputs_resources.add_resource(project_resource)
        else:
            log.warning(f"GpB/ProjectManagement: Unhandled resource role: {input_resource.resourceRole}")
        

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
        make_resources_project_specific(inputs.resources, service_outputs.resources, inputs.projectDir, inputs.uploadsPath, status_log_path)
        
        # Log the initialization of the project directory
        log.debug(f"GpB/ProjectManagement: project directory initialized at {project_dir}")
        with open(status_log_path, 'a') as f:
            f.write("Project directory initialized\n")
            
    return service_outputs
