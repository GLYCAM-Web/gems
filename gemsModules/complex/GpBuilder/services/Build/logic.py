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

    project_dir = GpBuilderProject.get_project_dir_from_pUUID(inputs.pUUID)
    status_log_path = project_dir / "status.log"
    
    log.debug(f"{project_dir=}")
    if not project_dir:
        service_notices.addNotice(
            Brief="Project not found",
            Scope="Service",
            Messenger="GpBuilder",
            Type="Error",
            Code="400",
            Message="Project not found",
        )
        return service_outputs, service_notices

    # generate the input file for GpBuilder
    input_file = project_dir / "the_input.txt"
    
    generate_input_file.execute(input_file, inputs, options)
    service_outputs.resources.append(Resource(
        locationType="filesystem-path-unix",
        resourceRole="gpbuilder-input-file",
        resourceFormat="text/plain",
        payload=str(input_file)
    ))
    with open(status_log_path, "a") as status_out:
        status_out.write(f"GEMS used GpBuilderTable to write the input file for GpBuilder.\n")

    # TODO: Write status.log with "GpBuilder finished with: Success|Failure" afterwards or make this a backgrounded process.
    # If backgrounded, write "Submitted".
    failed = run_gpbuilder.execute_gpb(input_file, project_dir)
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
        return service_outputs, service_notices
    else:
        log.debug("GpBuilder execution succeeded.")
    
    # TODO: archive afterwards - this could probably be PM's job in a future version. (Perhaps a request made by the background task to GEMS to archive the project?)
    # TODO: write status.log with "Archival complete"
    archive_project.execute(project_dir, inputs.pUUID)
    log.debug(f"Project {inputs.pUUID} archiving finished.")
 
    # TODO: This is redundant for now, but when GpB is no longer blocking we will need to write this with the background task.
    with open(status_log_path, "a") as status_out:
        status_out.write("All complete\n")
    
    return service_outputs, service_notices