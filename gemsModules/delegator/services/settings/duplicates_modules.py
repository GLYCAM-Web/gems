from typing import Dict, Callable

from gemsModules.delegator.services.list_services.manage_multiples import list_services_Multiples_Manager
from gemsModules.delegator.services.known_entities.manage_multiples import known_entities_Multiples_Manager 
from gemsModules.delegator.services.marco.manage_multiples import marco_Multiples_Manager 
from gemsModules.delegator.services.status.manage_multiples import status_Multiples_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

duplicates_modules : Dict[str, Callable] = {
    'KnownEntities': known_entities_Multiples_Manager,
    'ListServices': list_services_Multiples_Manager, 
    'Marco': marco_Multiples_Manager, 
    'Status': status_Multiples_Manager
    }
