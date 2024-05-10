#!/usr/bin/env python3
from pydantic import validate_arguments

from .api import Validate_Request, Validate_Response
from .logic import execute
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


@validate_arguments
def Serve(service: Validate_Request) -> Validate_Response:
    log.info("Serve called")
    log.info(f"service: {service}")

    log.debug(f"service.inputs: {service.inputs}")
    results = execute(service.inputs)

    return Validate_Response(outputs=results)
