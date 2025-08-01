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

    return service_outputs, service_notices
