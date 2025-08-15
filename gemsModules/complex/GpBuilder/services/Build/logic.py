from typing import Optional
from pydantic import validate_arguments
from pathlib import Path

from gemsModules.common.main_api_notices import Notices
from gemsModules.common.main_api_resources import Resource
from gemsModules.logging.logger import Set_Up_Logging

from .api import Build_Inputs, Build_Outputs, BuildOptions
from ...main_api_project import GpBuilderProject
from ...tasks import run_gpbuilder, generate_input_file, archive_project

log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Build_Inputs, options: BuildOptions) -> tuple[Build_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Build_Outputs()
    service_notices = Notices()

    # TODO: Handle this more gracefully.
    if not inputs.pUUID:
        service_notices.addNotice(
            Brief="pUUID missing",
            Scope="Service",
            Messenger="GpBuilder",
            Type="Error",
            Code="400",
            Message="pUUID missing, current project not found"
        )
        log.error("pUUID missing, cannot execute GpBuilder.")
        return service_outputs, service_notices

    job_dir = GpBuilderProject.get_project_dir_from_pUUID(inputs.pUUID)
    status_log_path = job_dir / "status.log"
    
    log.debug(f"workdir: {job_dir}")
    if not job_dir:
        service_notices.addNotice(
            Brief="Project not found",
            Scope="Service",
            Messenger="GpBuilder",
            Type="Error",
            Code="400",
            Message="Project not found",
        )
        log.error("Project not found, cannot execute GpBuilder.")
        return service_outputs, service_notices

    # generate the input file for GpBuilder
    input_file = Path(job_dir) / "the_input.txt"
    
    generate_input_file.execute(input_file, inputs, options)
    service_outputs.resources.append(Resource(
        locationType="filesystem-path-unix",
        resourceRole="gpbuilder-input-file",
        resourceFormat="text/plain",
        payload=job_dir / "the_input.txt"
    ))
    with open(status_log_path, "a") as status_out:
        status_out.write(f"GpB Input file created.\n")

    # TODO: Write status.log with "GpBuilder finished with: Success|Failure" afterwards or make this a backgrounded process.
    # If backgrounded, write "Submitted".
    failed = run_gpbuilder.execute_gpb(job_dir, inputs.pUUID)
    if failed:
        service_notices.addNotice(
            Brief="GpBuilder execution failed",
            Scope="Service",
            Messenger="GpBuilder",
            Type="Error",
            Code="500",
            Message="GpBuilder execution failed.",
        )
        log.error("GpBuilder execution failed.")
    else:
        service_notices.addNotice(
            Brief="GpBuilder running",
            Scope="Service",
            Messenger="GpBuilder",
            Type="Info",
            Code="200",
            Message="GpBuilder execution started.",
        )
        log.debug("GpBuilder execution started, see project logs for details.")
  
        # archive_project.execute(job_dir, inputs.pUUID)
        # log.debug(f"Project {inputs.pUUID} just archived.")
    
        # This is redundant for now, but when GpB is no longer blocking we will need to write this with the background task.
        # with open(status_log_path, "a") as status_out:
        #    status_out.write("All complete\n")
                
    return service_outputs, service_notices