#!/usr/bin/env python3
import os
from typing import Protocol, Dict, Optional
from pydantic import BaseModel

from gemsModules.structurefile.PDBFile.tasks import prepare_pdb
from gemsModules.structurefile.PDBFile.services.AmberMDPrep.api import (
    AmberMDPrep_Inputs,
    AmberMDPrep_Outputs,
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


def execute(inputs: AmberMDPrep_Inputs) -> AmberMDPrep_Outputs:
    """Executes the service."""
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = AmberMDPrep_Outputs()
    # The who_I_am must be set in the options.

    # TODO: should this always execute? I think what makes sense is for it to conditionally
    # execute on an AAO_Type of "prepare_pdb" which is only known to the PDB.AmberMDPrep service.
    output = prepare_pdb.execute(
        os.path.join(inputs.inputFilePath, inputs.pdb_file),
        os.path.join(inputs.outputFilePath, inputs.outputFileName),
    )

    # NOTE/TODO: using serviceOutputs doubles up the keys.
    return output
