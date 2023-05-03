#!/usr/bin/env python3
from gemsModules.TEMPLATE.services.template_service.api import template_service_Request, template_service_Response

from gemsModules.TEMPLATE.tasks import say_something_nice

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(service : template_service_Request) -> template_service_Response:

    message = say_something_nice.execute()
    response = template_service_Response()
    response.outputs.message = message
    return response

    
