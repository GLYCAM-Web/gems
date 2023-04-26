#!/usr/bin/env python3
from typing import Dict, Callable
from gemsModules.common.services.error.server import Serve as serve_error
from gemsModules.common.services.list_services.server import Serve as serve_list_services
from gemsModules.common.services.marco.server import Serve as serve_marco
from gemsModules.common.services.status.server import Serve as serve_status

from gemsModules.delegator.services.known_entities.server import Serve as serve_known_entities

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

service_modules : Dict[str, Callable] = {
    'Error' : serve_error,
    'KnownEntities' : serve_known_entities,
    'ListServices': serve_list_services, 
    'Marco': serve_marco, 
    'Status': serve_status
    }
