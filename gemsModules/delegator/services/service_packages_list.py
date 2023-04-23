#!/usr/bin/env python3
from typing import List, Callable
from gemsModules.common.services.service_packages_list import Services_Package_List_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class delegator_Services_Package_List_Manager(Services_Package_List_Manager):

    def get_available_services(self) -> List[str]:
        from gemsModules.delegator.tasks import get_services_list
        self.available_services = get_services_list.execute()
        return self.available_services

    # def get_service_module(self, service_type: str) -> Callable:
    #     from gemsModules.delegator.services.known_entities.servicer import Serve as known_entity_Serve
    #     pass