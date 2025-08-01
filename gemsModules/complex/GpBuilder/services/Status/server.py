#!/usr/bin/env python3
from gemsModules.logging.logger import Set_Up_Logging 

from ...services.Status.api import StatusService_Request, StatusService_Response
from ...tasks import generate_input_file, run_gpbuilder
from ...main_api_project import GpBuilderProject

from .logic import execute
log = Set_Up_Logging(__name__)


def Serve(service : StatusService_Request) -> StatusService_Response:
    log.debug(f"GpB/Status serving service request: {service=}")
    response = StatusService_Response()
    
    response.outputs, response.notices = execute(service.inputs, service.options)

    
    return response

    
