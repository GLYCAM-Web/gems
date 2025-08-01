#!/usr/bin/env python3
from typing import Dict, Callable
from gemsModules.common.services.error.server import Serve as serve_error
from gemsModules.common.services.list_services.server import Serve as serve_list_services
from gemsModules.common.services.marco.server import Serve as serve_marco

from gemsModules.complex.GpBuilder.services.ProjectManagement.server import Serve as serve_pm
from gemsModules.complex.GpBuilder.services.Build.server  import Serve as serve_Build
from gemsModules.complex.GpBuilder.services.Evaluate.server import Serve as serve_evaluate
from gemsModules.complex.GpBuilder.services.Status.server import Serve as serve_status


service_modules : Dict[str, Callable] = {
    'Error' : serve_error,
    'ListServices': serve_list_services, 
    'Marco': serve_marco, 
    'ProjectManagement': serve_pm,
    'Evaluate': serve_evaluate,
    'Build' : serve_Build,
    'Status': serve_status,
}
