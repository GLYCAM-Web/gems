#!/usr/bin/env python3
from gemsModules.batchcompute.services.SubmitJob.api import SubmitJobService_Request, SubmitJobService_Response

from gemsModules.batchcompute.tasks import say_something_nice

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(service : SubmitJobService_Request) -> SubmitJobService_Response:

    message = say_something_nice.execute()
    response = SubmitJobService_Response()
    response.outputs.message = message
    return response

    
