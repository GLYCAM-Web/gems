#!/usr/bin/env python3
from typing import Dict, Callable
from gemsModules.common.services.error.server import Serve as serve_error
from gemsModules.common.services.list_services.server import (
    Serve as serve_list_services,
)
from gemsModules.common.services.marco.server import Serve as serve_marco

from ..ProjectManagement.server import Serve as serve_ProjectManagement
from ..Evaluate.server import Serve as serve_evaluate
from ..Analyze.server import Serve as serve_validate
from ..Build.server import Serve as serve_build
from ..Status.server import Serve as serve_status

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
