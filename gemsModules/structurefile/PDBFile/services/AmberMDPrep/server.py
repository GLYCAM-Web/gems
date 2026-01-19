#!/usr/bin/env python3
from gemsModules.structurefile.PDBFile.services.AmberMDPrep.api import (
    AmberMDPrep_Request,
    AmberMDPrep_Response,
)

from gemsModules.systemoperations.filesystem_ops import separate_path_and_filename

from gemsModules.structurefile.PDBFile.services.AmberMDPrep.logic import execute

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(service: AmberMDPrep_Request) -> AmberMDPrep_Response:
    """Execute the service request"""

    # TODO: Prepare the directory/project with implicit services.
    response = AmberMDPrep_Response()
    response.outputs = execute(service.inputs)

    log.debug(f"AmberMDPrep prepare_pdb_Response: {response}")
    return response
