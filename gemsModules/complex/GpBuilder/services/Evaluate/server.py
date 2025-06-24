#!/usr/bin/env python3
from gemsModules.complex.GpBuilder.services.Evaluate.api import EvaluateService_Request, EvaluateService_Response

from gemsModules.complex.GpBuilder.tasks import generate_input_file, run_gpbuilder

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(service : EvaluateService_Request) -> EvaluateService_Response:
    log.debug(f"GpB/Build serving service request: {service=}")
    response = EvaluateService_Response()
    
    
    # TODO: use ProjectManagementRequest's given project dir.
    job_dir = "/programs/gems/testGpBuilder-git-ignore-me"
    generate_input_file.execute(job_dir, service.inputs, service.options)
    
    return response

    
