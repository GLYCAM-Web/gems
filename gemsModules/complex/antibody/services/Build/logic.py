#!/usr/bin/env python3
from pydantic import validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.logging.logger import Set_Up_Logging

from ...main_api_project import AntibodyProject
from ...tasks import run_ad_build, update_build_options

from .api import Build_Inputs, Build_Outputs


log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Build_Inputs, options: dict) -> tuple[Build_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Build_Outputs()
    service_notices = Notices()

    if inputs.pUUID is None:
        service_notices.addNotice(
            Brief="pUUID not provided",
            Scope="Service",
            Messenger="AntibodyDocking",
            Type="Error",
            Code="400",
            Message="Project could not be found without an input pUUID to the Build service",
        )
        return service_outputs, service_notices
    
    workdir = AntibodyProject.get_project_dir_from_pUUID(inputs.pUUID)
    log.debug(f"workdir: {workdir}")
    
    # As we pass the options to build, must update them rather than initializing with PM.
    update_build_options.execute(options, workdir)
    
    results = run_ad_build.execute(workdir)
    if results.returncode:
        service_notices.addNotice(
            Brief="Build Failed",
            Scope="Service",
            Messenger="AntibodyDocking",
            Type="Error",
            Code="500",
            Message=f"Build Failed: {results.stderr}",
        )
        return service_outputs, service_notices
    
    if not len(service_notices):
        service_notices.addNotice(
            Brief="Build Successful",
            Scope="Service",
            Messenger="AntibodyDocking",
            Type="Info",
            Code="600",
            Message="Build Successful",
        )

    log.debug(f"service_outputs: {service_outputs}")
    log.debug(f"service_notices: {service_notices}")
    return service_outputs, service_notices
