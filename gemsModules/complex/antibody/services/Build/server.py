#!/usr/bin/env python3
# from gemsModules.common.main_api_services import Service_Request, Service_Response
from .api import Build_Request, Build_Response
from .api import Build_Inputs
from .logic import execute

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def Serve(service: Build_Request) -> Build_Response:
    log.info("Serve called")
    log.info(f"service: {service}")
    log.debug(f"Build service.inputs: {service.inputs}")
    service_response = Build_Response()

    service_response.outputs, service_notices = execute(service.inputs)
    service_response.notices.extend(service_notices)
    
    return service_response
