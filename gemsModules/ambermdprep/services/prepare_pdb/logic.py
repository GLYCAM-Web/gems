#!/usr/bin/env python3
import os
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.ambermdprep.tasks import prepare_pdb
from gemsModules.ambermdprep.services.prepare_pdb.api import (
    prepare_pdb_Inputs,
    prepare_pdb_Outputs,
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


class serviceInputs(BaseModel):
    """Allows a Service_Request to be used as input"""

    inputs: requestInputs = requestInputs()
    options: Dict[str, str]


class serviceOutputs(BaseModel):
    outputs: responseOutputs = responseOutputs()


def execute(inputs: prepare_pdb_Inputs) -> prepare_pdb_Outputs:
    """Executes the service."""
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = prepare_pdb_Outputs()
    # The who_I_am must be set in the options.

    output = prepare_pdb.execute(
        os.path.join(inputs.inputFilesPath, inputs.pdb_file),
        os.path.join(inputs.outputDirPath, inputs.pdb_file),
    )

    # NOTE/TODO: using serviceOutputs doubles up the keys.
    return output
