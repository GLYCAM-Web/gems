#!/usr/bin/env python3
from gemsModules.mmservice.mdaas.services.Evaluate.api import Evaluate_Request, Evaluate_Response
from gemsModules.common.tasks import cake

from gemsModules.mmservice.mdaas.services.Evaluate.logic import execute

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)



def Serve(service_request: Evaluate_Request) -> Evaluate_Response:
    log.debug("SERVE: run_md")

    response = Evaluate_Response()
    response.outputs = execute(service_request.inputs)

    response.outputs.outputDirPath = service_request.inputs.outputDirPath
    return response
