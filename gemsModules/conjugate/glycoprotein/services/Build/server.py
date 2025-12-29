#!/usr/bin/env python3
from pydantic import validate_arguments
from gemsModules.logging.logger import Set_Up_Logging 

from ...services.Build.api import BuildService_Request, BuildService_Response

from .logic import execute
log = Set_Up_Logging(__name__)


def Serve(service : BuildService_Request) -> BuildService_Response:
    log.debug(f"GpB/Build serving service request: {service=}")
    response = BuildService_Response()
    
    response.outputs, the_notices = execute(service.inputs, service.options)
    response.notices.extend(the_notices)
    
    return response

    
