from pydantic import validate_arguments
from pathlib import Path

from gemsModules.common.main_api_notices import Notices
from gemsModules.common.main_api_resources import Resource
from gemsModules.logging.logger import Set_Up_Logging

from .api import Build_Inputs, Build_Outputs, BuildOptions
from ...main_api_project import GpBuilderProject
from ...tasks import run_gpbuilder, generate_input_file

log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Build_Inputs, options: BuildOptions) -> tuple[Build_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Build_Outputs()
    service_notices = Notices()

    job_dir = GpBuilderProject.get_project_dir_from_pUUID(inputs.pUUID)
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

    # TODO: Write status.log with "GpBuilder finished with: Success|Failure" afterwards or make this a backgrounded process.
    # If backgrounded, write "Submitted".
    failed = run_gpbuilder.execute_gpb(job_dir / "the_input.txt", job_dir)
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
    log.debug(f"GPB run completed.")
    
    # TODO: archive afterwards - this could probably be PM's job in a future version.
    # TODO: write status.log with "Archival complete"
    # archive_project.execute(job_dir, inputs.pUUID)
    
    # TODO: write status.log with "All complete"
    return service_outputs, service_notices