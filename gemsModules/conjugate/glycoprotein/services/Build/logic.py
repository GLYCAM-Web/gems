from typing import Optional
from pydantic import validate_arguments
from pathlib import Path

from gemsModules.common.main_api_notices import Notices
from gemsModules.common.main_api_resources import Resource
from gemsModules.logging.logger import Set_Up_Logging

from .api import Build_Inputs, Build_Outputs, BuildOptions
from ...main_api_project import GlycoProteinProject
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
            Messenger="GlycoProtein",
            Type="Error",
            Code="400",
            Message="pUUID missing, current project not found"
        )
        log.error("pUUID missing, cannot execute GlycoProtein.")
        return service_outputs, service_notices

#  This should be part of inputs:Build_Inputs already
#    job_dir = GlycoProteinProject.get_project_dir_from_pUUID(inputs.pUUID)
    job_dir = inputs.projectDir
    status_log_path = job_dir + "/status.log"
    
    log.debug(f"workdir: {job_dir}")
    if not job_dir:
        service_notices.addNotice(
            Brief="Project not found",
            Scope="Service",
            Messenger="GlycoProtein",
            Type="Error",
            Code="400",
            Message="Project not found",
        )
        log.error("Project not found, cannot execute GlycoProtein.")
        return service_outputs, service_notices

    # generate the input file for GlycoProtein
    input_file = job_dir + "/the_input.txt"
    
    generate_input_file.execute(input_file, inputs, options)
    service_outputs.resources.append(Resource(
        locationType="filesystem-path-unix",
        resourceRole="gpbuilder-input-file",
        resourceFormat="text/plain",
        payload=str(input_file),
    ))
    with open(status_log_path, "a") as status_out:
        status_out.write(f"GP Input file created.\n")

    # TODO: Write status.log with "GlycoProtein finished with: Success|Failure" afterwards or make this a backgrounded process.
    # If backgrounded, write "Submitted".
    failed = run_gpbuilder.execute_gpb(job_dir, inputs.pUUID)
    if failed:
        service_notices.addNotice(
            Brief="GlycoProtein execution failed",
            Scope="Service",
            Messenger="GlycoProtein",
            Type="Error",
            Code="500",
            Message="GlycoProtein execution failed.",
        )
        log.error("GlycoProtein execution failed.")
        with open(status_log_path, "a") as status_out:
            status_out.write("GlycoProtein execution failed.\n")
    else:
        service_notices.addNotice(
            Brief="GlycoProtein running",
            Scope="Service",
            Messenger="GlycoProtein",
            Type="Info",
            Code="200",
            Message="GlycoProtein execution started.",
        )
        log.debug("GlycoProtein execution started, see project logs for details.")
        # The start_build.sh writes this to the status.log, so we don't need to do it here.
        # with open(status_log_path, "a") as status_out:
        #     status_out.write("GlycoProtein execution started.\n")

                
    return service_outputs, service_notices
