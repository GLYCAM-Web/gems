#!/usr/bin/env python3
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.explicit_requests import Explicit_Service_Request_Manager

from gemsModules.delegator.main_api import Delegator_Entity
from gemsModules.delegator.services.service_packages_list import delegator_Services_Package_List_Manager

from gemsModules.common.tasks import get_services_list

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Service_Manager():
    
    def __init__(self, entity : Delegator_Entity):
        self.entity = entity
        self.available_services = get_services_list.execute()


    def set_explicit_aaops(self):
        explicit_manager = Explicit_Service_Request_Manager(entity=self.entity)
        self.explicit_aaops = explicit_manager.process

    def remove_unknown_services(self):
        unknown_manager = delegator_Services_Package_List_Manager(aaop_list=self.explicit_aaops)
        self.managed_explicit_aaops = unknown_manager.manage_unknown_services()

    def gather_implicit_services(self): 
        for service in self.available_services :
            import the implicit manager for the service
            self.implicit_aaops = run that process

    
