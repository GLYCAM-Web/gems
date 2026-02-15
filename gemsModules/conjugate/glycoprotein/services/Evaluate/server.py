#!/usr/bin/env python3
from gemsModules.logging.logger import Set_Up_Logging 

from ...services.Evaluate.api import EvaluateService_Request, EvaluateService_Response
from ...tasks import generate_input_file, run_gpbuilder
from ...main_api_project import GlycoProteinProject

from .logic import execute
log = Set_Up_Logging(__name__)


def Serve(service : EvaluateService_Request) -> EvaluateService_Response:
    log.info("Serve for service Evaluate in GlycoProtein is called")
    log.debug(f"GP/Evaluate serving service request: {service=}")
    response = EvaluateService_Response()
    
    response.outputs, response.notices = execute(service.inputs, service.options)

    
    return response

    
