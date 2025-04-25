#!/usr/bin/env python3
from gemsModules.complex.GpBuilder.services.Build.api import BuildService_Request, BuildService_Response

from gemsModules.complex.GpBuilder.tasks import generate_input_file, run_gpbuilder

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(service : BuildService_Request) -> BuildService_Response:
    response = BuildService_Response()
    
    
    # TODO: Should be done by an implied ProjectManagementRequest
    job_dir = "/programs/gems/testGpBuilder-git-ignore-me"
    generate_input_file.execute(job_dir, service.inputs, service.options)
    
    return response

    
