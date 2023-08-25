#!/usr/bin/env python3
from gemsModules.mmservice.mdaas.services.run_md.run_md_api import (
    run_md_Request,
    run_md_Response,
)


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(service_request: run_md_Request) -> run_md_Response:
    # needs to access after data filler, but is it?
    log.debug("SERVE: run_md")

    response = run_md_Response()
    response.outputs.outputDirPath = service_request.inputs.outputDirPath
    return response
