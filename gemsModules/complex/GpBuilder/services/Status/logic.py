#!/usr/bin/env python3
from typing import Optional
from pydantic import validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.logging.logger import Set_Up_Logging

from .api import Status_Inputs, Status_Outputs, Status_Options


log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Status_Inputs, options: Optional[Status_Options]) -> tuple[Status_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Status_Outputs()
    service_notices = Notices()
    
    status_file = inputs.projectDir + "/status.txt"
    status_greps = { "Build finished": "All complete", "Build finished with errors": "with errors"}
    try:
        with open(status_file, 'r') as f:
            status_content = f.read()
            for key, value in status_greps.items():
                if value in status_content:
                    service_outputs.status = key
                    log.info(f"Status found: {key}")
                    break
            else:
                service_outputs.status = "No status found"
                log.warning("No status found in the status file.")
    except FileNotFoundError:
        service_outputs.status = "Status file not found"
        log.error(f"Status file not found: {status_file}")
    return service_outputs, service_notices
