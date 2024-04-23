#!/usr/bin/env python3
from gemsModules.common.main_api_services import Service_Request, Service_Response

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(service: Service_Request) -> Service_Response:
    log.info("Serve called")
    log.info(f"service: {service}")
    return Service_Response(
        status="Success", message="Glycomimetics Serve not implemented"
    )
