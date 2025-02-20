#!/usr/bin/env python3
import os
from pathlib import Path
import sys
from typing import Protocol, Dict, Optional
from pydantic import BaseModel, validate_arguments

from gemsModules.common.main_api_notices import Notices
from gemsModules.systemoperations.instance_config import InstanceConfig
from gemsModules.logging.logger import Set_Up_Logging

from .api import Evaluate_Inputs, Evaluate_Outputs


log = Set_Up_Logging(__name__)


@validate_arguments
def execute(inputs: Evaluate_Inputs) -> tuple[Evaluate_Outputs, Notices]:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = Evaluate_Outputs()
    service_notices = Notices()

    # TODO: Call AD_Evaluate on thoreau here.

    if not len(service_notices):
        service_notices.addNotice(
            Brief="Evaluation Successful",
            Scope="Service",
            Messenger="AntibodyDocking",
            Type="Info",
            Code="600",
            Message="Evaluation Successful",
        )

    log.debug(f"service_outputs: {service_outputs}")
    log.debug(f"service_notices: {service_notices}")
    return service_outputs, service_notices
