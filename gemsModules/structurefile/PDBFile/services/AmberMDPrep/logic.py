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


def execute(inputs: AmberMDPrep_Inputs) -> AmberMDPrep_Outputs:
    """Executes the service."""
    log.debug(f"serviceInputs: {inputs}")
    service_outputs = AmberMDPrep_Outputs()
    # The who_I_am must be set in the options.

    in_file = os.path.join(inputs.inputFilePath, inputs.pdb_filename)
    out_file = os.path.join(inputs.outputFilePath, inputs.outputFileName)
    log.debug(f"AmberMDPrep: in_file: {in_file}, out_file: {out_file}")

    # TODO/Q: should this always execute? AmberMDPrep surely doesn't always prepare a PDB file?
    service_outputs.ppinfo = prepare_pdb.execute(in_file, out_file)

    return service_outputs
