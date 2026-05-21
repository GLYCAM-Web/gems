#!/usr/bin/env python3
from typing import List, Callable

from gemsModules.common.services.duplicate_requests import Duplicate_Requests_Manager


from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Batchcompute_Duplicate_Requests_Manager(Duplicate_Requests_Manager):

    def get_available_services(self) -> List[str]:
        from gemsModules.batchcompute.tasks import get_services_list
        return get_services_list.execute()

    def get_duplicates_manager(self, service : str) -> Callable:
        from gemsModules.batchcompute.services.settings.duplicates_modules import module_loader
        return module_loader(service)
        
