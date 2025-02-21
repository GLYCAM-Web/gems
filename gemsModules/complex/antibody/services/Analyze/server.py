#!/usr/bin/env python3
from pydantic import validate_arguments

from .api import Analyze_Request, Analyze_Response, Analyze_Inputs, Analyze_Outputs
from .logic import execute
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


# Error
@validate_arguments
def Serve(service: Analyze_Request) -> Analyze_Response:
    log.info("Serve called")
    log.info(f"service: {service}")

    log.debug(f"service.inputs: {service.inputs}")

    # TODO: Pydantic should automatically do this...
    results, notices = execute(service.inputs)

    return Analyze_Response(outputs=results, notices=notices)
