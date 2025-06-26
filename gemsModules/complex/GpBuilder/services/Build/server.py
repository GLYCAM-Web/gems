#!/usr/bin/env python3
from gemsModules.logging.logger import Set_Up_Logging 

from ...services.Build.api import BuildService_Request, BuildService_Response
from ...tasks import run_gpbuilder
from ...main_api_project import GpBuilderProject

from .logic import execute
log = Set_Up_Logging(__name__)


def Serve(service : BuildService_Request) -> BuildService_Response:
    log.debug(f"GpB/Build serving service request: {service=}")
    response = BuildService_Response()
    
    response.outputs, response.notices = execute(service.inputs, service.options)
    
    return response

    
