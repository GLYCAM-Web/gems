#!/usr/bin/env python3
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.mmservice.mdaas.tasks import initiate_build
from gemsModules.mmservice.mdaas.services.run_md.run_md_api import (
    run_md_Inputs,
    run_md_Outputs,
)
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def execute(inputs: run_md_Inputs) -> run_md_Outputs:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = run_md_Outputs()

    ic = InstanceConfig()

    #

    return service_outputs
