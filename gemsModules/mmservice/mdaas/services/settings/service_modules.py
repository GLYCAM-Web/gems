#!/usr/bin/env python3
from typing import Dict, Callable
from gemsModules.common.services.error.server import Serve as serve_error
from gemsModules.common.services.list_services.server import (
    Serve as serve_list_services,
)
from gemsModules.common.services.marco.server import Serve as serve_marco
from gemsModules.common.services.status.server import Serve as serve_status
from gemsModules.mmservice.mdaas.services.run_md.server import Serve as serve_run_md
from gemsModules.mmservice.mdaas.services.ProjectManagement.server import (
    Serve as serve_ProjectManagement,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

service_modules: Dict[str, Callable] = {
    "Error": serve_error,
    "ListServices": serve_list_services,
    "Marco": serve_marco,
    "Status": serve_status,
    "RunMD": serve_run_md,
    "ProjectManagement": serve_ProjectManagement,
}
