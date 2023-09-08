#!/usr/bin/env python3
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.mmservice.mdaas.tasks import initiate_build
from gemsModules.mmservice.mdaas.services.run_md.run_md_api import (
    run_md_Inputs,
    run_md_Outputs,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


## These are a little redundant in this simple example.
class requestInputs(BaseModel):
    """Defines the inputs to the service."""

    entity: str = None
    who_I_am: str = None


class responseOutputs(BaseModel):
    """Defines the outputs from the service."""

    message: str = None
    info: Optional[str] = None


class serviceInputs(Protocol):
    """Allows a Service_Request to be used as input"""

    inputs: requestInputs = requestInputs()
    options: Dict[str, str]


class serviceOutputs(BaseModel):
    outputs: responseOutputs = responseOutputs()


class cakeInputs:
    cake: bool = False
    color: str = None


def execute(inputs: run_md_Inputs) -> serviceOutputs:
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = run_md_Outputs()

    initiate_build.execute(
        pUUID=inputs.pUUID,
        outputDirPath=inputs.outputDirPath,
        use_serial=True,
    )
    return service_outputs
