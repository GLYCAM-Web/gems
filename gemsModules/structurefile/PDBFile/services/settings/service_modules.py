#!/usr/bin/env python3
from typing import Dict, Callable
from gemsModules.common.services.error.server import Serve as serve_error
from gemsModules.common.services.list_services.server import (
    Serve as serve_list_services,
)
from gemsModules.common.services.marco.server import Serve as serve_marco
from gemsModules.common.services.status.server import Serve as serve_status

from gemsModules.structurefile.PDBFile.services.AmberMDPrep.server import (
    Serve as serve_prepare_pdb,
)

from gemsModules.structurefile.PDBFile.services.ProjectManagement.server import (
    Serve as serve_project_management,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

service_modules: Dict[str, Callable] = {
    "Error": serve_error,
    "ListServices": serve_list_services,
    "Marco": serve_marco,
    "Status": serve_status,
    "AmberMDPrep": serve_prepare_pdb,
    "ProjectManagement": serve_project_management,
}
