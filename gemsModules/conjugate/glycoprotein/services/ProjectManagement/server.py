#!/usr/bin/env python3
# This line was originally the following:
from gemsModules.complex.glycomimetics.services.ProjectManagement.api import (
# I think the dependency should be on glycoprotein, not glycomimetics
#from gemsModules.conjugate.glycoprotein.services.ProjectManagement.api import (
    ProjectManagement_Request,
    ProjectManagement_Response,
)

from gemsModules.systemoperations.filesystem_ops import separate_path_and_filename

from gemsModules.conjugate.glycoprotein.services.ProjectManagement.logic import execute
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(service: ProjectManagement_Request) -> ProjectManagement_Response:
    log.debug(f"GP/ProjectManagement service: {service.inputs=}")
    response = ProjectManagement_Response()
    response.outputs = execute(service.inputs)

    log.debug(f"ProjectManagement prepare_pdb_Response: {response}")
    return response
