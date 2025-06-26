from pydantic import validate_arguments

from gemsModules.common.main_api_notices import Notices
from .api import Build_Inputs, Build_Outputs, BuildOptions
from ...main_api_project import GpBuilderProject
from ...tasks import run_gpbuilder
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Build_Inputs, options: BuildOptions) -> tuple[Build_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Build_Outputs()
    service_notices = Notices()

    workdir = GpBuilderProject.get_project_dir_from_pUUID(inputs.pUUID)
    log.debug(f"workdir: {workdir}")
    if not workdir:
        service_notices.addNotice(
            Brief="Project not found",
            Scope="Service",
            Messenger="GpBuilder",
            Type="Error",
            Code="400",
            Message="Project not found",
        )
        return service_outputs, service_notices

    job_dir = GpBuilderProject.get_project_dir_from_pUUID(inputs.pUUID)
    run_gpbuilder.execute_gpb(job_dir / "the_input.txt", job_dir)
    log.debug(f"GPB run completed.")
    # TODO: archive afterwards
    # archive_project.execute(job_dir, inputs.pUUID)
    
    return service_outputs, service_notices