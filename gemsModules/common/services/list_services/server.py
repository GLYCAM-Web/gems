#!/usr/bin/env python3
from gemsModules.common.main_api_services import Service_Request, Service_Response
from gemsModules.common.main_api_notices import Notices

# from gemsModules.common.services.error.logic import error
from gemsModules.common.tasks.get_services_list import (
    execute as get_services_list,
)
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(request: Service_Request) -> Service_Response:
    log.info("The marco server was called.")
    response = Service_Response()
    if request.typename != "ListServices":
        response.typename = request.typename
        response.outputs = {
            "message": "Incorrect typename sent to ListServices Servicer."
        }
        response.notices = Notices()
        response.notices.addDefaultNotice(
            Brief="InvalidInput", Messenger="ListServices Sevicer"
        )
    else:
        response.typename = "ListServices"
        response.outputs = get_services_list()
    return response
