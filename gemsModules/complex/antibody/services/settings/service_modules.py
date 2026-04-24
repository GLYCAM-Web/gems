#!/usr/bin/env python3
from typing import Dict, Callable
from gemsModules.common.services.error.server import Serve as serve_error
from gemsModules.common.services.list_services.server import (
    Serve as serve_list_services,
)
from gemsModules.common.services.marco.server import Serve as serve_marco

from gemsModules.complex.antibody.services.ProjectManagement.server import Serve as serve_ProjectManagement
from gemsModules.complex.antibody.services.Evaluate.server import Serve as serve_evaluate
from gemsModules.complex.antibody.services.Analyze.server import Serve as serve_validate
from gemsModules.complex.antibody.services.Build.server import Serve as serve_build
from gemsModules.complex.antibody.services.Status.server import Serve as serve_status

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


service_modules: Dict[str, Callable] = {
    "Error": serve_error,
    "ListServices": serve_list_services,
    "Marco": serve_marco,
    "Status": serve_status,
    "Evaluate": serve_evaluate,
    "Build": serve_build,
    "Analyze": serve_validate,
    "ProjectManagement": serve_ProjectManagement,
}
