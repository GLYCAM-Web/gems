#!/usr/bin/env python3
from .api import Build_Selected_Positions_Request, Build_Selected_Positions_Response
from .logic import execute 

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(service: Build_Selected_Positions_Request) -> Build_Selected_Positions_Response:
    log.info("Serve called")
    log.info(f"service: {service}")
    
    response = Build_Selected_Positions_Response()
    response.outputs = execute(service.inputs)
    
    return response
