#!/usr/bin/env python3
from gemsModules.complex.antibody.services.ProjectManagement.api import (
    ProjectManagement_Request,
    ProjectManagement_Response,
)

from gemsModules.systemoperations.filesystem_ops import separate_path_and_filename

# from gemsModules.complex.antibody.tasks import set_up_build_directory
# from gemsModules.complex.antibody.tasks import initiate_build
from gemsModules.common.main_api_notices import Notices
from gemsModules.complex.antibody.services.ProjectManagement.logic import execute
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def Serve(service: ProjectManagement_Request) -> ProjectManagement_Response:
    response = ProjectManagement_Response()
    service_notices = Notices()
    response.outputs = execute(service.inputs, service_notices=service_notices)
    if service_notices:
        response.notices.extend(service_notices)
    if response.outputs and hasattr(response.outputs, "notices") and response.outputs.notices:
        response.notices.extend(response.outputs.notices)

    log.debug(f"ProjectManagement prepare_pdb_Response: {response}")
    return response
