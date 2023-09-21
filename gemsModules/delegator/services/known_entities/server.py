#!/usr/bin/env python3
from gemsModules.common.main_api_services import Service_Request, Service_Response
from gemsModules.common.main_api_notices import Notices

from gemsModules.delegator.tasks.get_known_entities import (
    execute as get_known_entities,
)
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(request: Service_Request) -> Service_Response:
    log.info("The KnownEntities server was called.")
    response = Service_Response()

    response.typename = request.typename
    response.outputs = {"message": get_known_entities()}
    response.notices = Notices()

    return response
