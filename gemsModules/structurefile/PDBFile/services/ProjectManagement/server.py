#!/usr/bin/env python3
from gemsModules.structurefile.PDBFile.services.ProjectManagement.api import (
    ProjectManagement_Request,
    ProjectManagement_Response,
)

from gemsModules.systemoperations.filesystem_ops import separate_path_and_filename

# from gemsModules.mmservice.mdaas.tasks import set_up_run_md_directory
# from gemsModules.mmservice.mdaas.tasks import initiate_build
from gemsModules.structurefile.PDBFile.services.ProjectManagement.logic import execute
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(service: ProjectManagement_Request) -> ProjectManagement_Response:
    response = ProjectManagement_Response()
    response.outputs = execute(service.inputs)

    log.debug(f"ProjectManagement prepare_pdb_Response: {response}")
    return response
