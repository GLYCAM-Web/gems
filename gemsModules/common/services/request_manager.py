#!/usr/bin/env python3
from typing import List
from abc import ABC, abstractmethod

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_entity import Entity
from gemsModules.common.services.explicit_requests import Explicit_Service_Request_Manager
from gemsModules.common.services.service_packages_list import Services_Package_List_Utilities
from gemsModules.common.services.implied_requests import common_Implied_Services_Request_Manager 
from gemsModules.common.services.default_requests import common_Default_Service_Request_Manager
from gemsModules.common.services.duplicate_requests import common_Duplicate_Requests_Manager
from gemsModules.common.services.request_data_filler import common_Request_Data_Filler
from gemsModules.common.services.settings import Available_Services
from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Request_Manager(ABC):
    
    def __init__(self, entity : Entity, project : Project):
        self.entity = entity
        self.project = project
        self.explicit_aaops : List[AAOP] = []
        self.aaop_list : List[AAOP] = []
        self.set_local_modules()

    @abstractmethod
    def set_local_modules(self):
        self.explicit_manager = Explicit_Service_Request_Manager(entity=self.entity)
        self.unknown_manager = Services_Package_List_Utilities(aaop_list=self.explicit_aaops)
        self.implied_manager = common_Implied_Services_Request_Manager(input_object = self.entity)
        self.duplicate_manager = common_Duplicate_Requests_Manager(aaop_list=self.aaop_list)
        self.default_manager = common_Default_Service_Request_Manager()
        self.data_filler = common_Request_Data_Filler(aaop_list=self.aaop_list, entity=self.entity, project=self.project)
        self.available_services = Available_Services.get_list()

    def process(self) -> List[AAOP]:
        log.debug("Processing request for entity")
        log.debug("about to set explicit aaops")
        print("the entity is: ", self.entity)
        self.set_explicit_aaops()
        log.debug("about to remove unknown services")
        self.remove_unknown_services()
        log.debug("about to gather implicit services")
        self.gather_implicit_services()
        self.aaop_list = self.managed_explicit_aaops + self.implicit_aaops
        log.debug("about to manage duplicates")
        self.manage_duplicates()
        if self.aaop_list == []:
            self.aaop_list = self.get_default_aaops()
        log.debug("about to fill request data needs")
        self.fill_request_data_needs()
        return self.aaop_list

    def set_explicit_aaops(self):
        self.explicit_aaops : List[AAOP] = self.explicit_manager.process()

    def remove_unknown_services(self):
        self.managed_explicit_aaops : List[AAOP] = self.unknown_manager.manage_unknown_services(available_services=self.available_services)

    def gather_implicit_services(self): 
        self.implicit_aaops : List[AAOP] = self.implied_manager.process()

    def manage_duplicates(self):
        self.return_aaop_list : List[AAOP] = self.duplicate_manager.process()

    def get_default_aaops(self) -> List[AAOP]:
        self.default_aaops : List[AAOP] = self.default_manager.get_default_services_aaops()
        return self.default_aaops
    
    def fill_request_data_needs(self):
        self.aaop_list = self.data_filler.process()


class common_Request_Manager(Request_Manager):
        
        def set_local_modules(self):
            super().set_local_modules()