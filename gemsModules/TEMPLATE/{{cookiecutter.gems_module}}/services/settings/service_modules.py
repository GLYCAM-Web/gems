#!/usr/bin/env python3
from typing import Dict, Callable
from gemsModules.common.services.error.server import Serve as serve_error
from gemsModules.common.services.list_services.server import Serve as serve_list_services
from gemsModules.common.services.marco.server import Serve as serve_marco
from gemsModules.common.services.status.server import Serve as serve_status

from gemsModules.{{cookiecutter.gems_module}}.services.{{cookiecutter.service_name}}.server  import Serve as serve_{{cookiecutter.service_name}}

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

service_modules : Dict[str, Callable] = {
    'Error' : serve_error,
    'ListServices': serve_list_services, 
    'Marco': serve_marco, 
    'Status': serve_status,
    '{{cookiecutter.service_name}}' : serve_{{cookiecutter.service_name}}
    }
