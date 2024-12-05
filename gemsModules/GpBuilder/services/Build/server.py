#!/usr/bin/env python3
from gemsModules.GpBuilder.services.Build.api import BuildService_Request, BuildService_Response

from gemsModules.GpBuilder.tasks import say_something_nice

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(service : BuildService_Request) -> BuildService_Response:

    message = say_something_nice.execute()
    response = BuildService_Response()
    response.outputs.message = message
    return response

    
