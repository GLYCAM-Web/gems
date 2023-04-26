#!/usr/bin/env python3
from typing import List, Callable
from abc import ABC, abstractmethod

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_entity import Entity
from gemsModules.common.services.explicit_requests import Explicit_Service_Request_Manager
from gemsModules.common.services.service_packages_list import Services_Package_List_Utilities
from gemsModules.common.services.implied_requests import common_Implied_Services_Request_Manager 
from gemsModules.common.services.default_requests import common_Default_Service_Request_Manager
from gemsModules.common.services.duplicate_requests import common_Duplicate_Requests_Manager
from gemsModules.common.services.request_data_filler import common_Request_Data_Filler
from gemsModules.common.services.settings.known_available import Available_Services
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
        self.explicit_manager_type : Callable = Explicit_Service_Request_Manager
        self.unknown_manager_type : Callable = Services_Package_List_Utilities
        self.implied_manager_type : Callable = common_Implied_Services_Request_Manager
        self.duplicate_manager_type : Callable = common_Duplicate_Requests_Manager
        self.default_manager_type : Callable = common_Default_Service_Request_Manager
        self.data_filler_type : Callable = common_Request_Data_Filler
        self.available_services : List[str]  = Available_Services.get_list()

    def process(self) -> List[AAOP]:
        log.debug("Processing request for entity")
        log.debug("about to set explicit aaops")
        self.set_explicit_aaops()
        log.debug("the explicit aaop list is: ")
        log.debug(self.explicit_aaops)
        log.debug("about to remove unknown services")
        self.remove_unknown_services()
        log.debug("the managed explicit aaop list is: ")
        log.debug(self.managed_explicit_aaops)
        log.debug("about to gather implicit services")
        self.gather_implicit_services()
        log.debug("the implicit aaop list is: ")
        log.debug(self.implicit_aaops)
        self.aaop_list = self.managed_explicit_aaops + self.implicit_aaops
        log.debug("the current aaop list is: ")
        log.debug(self.aaop_list)
        log.debug("about to manage duplicates")
        self.manage_duplicates()
        log.debug("the current aaop list is: ")
        log.debug(self.aaop_list)
        if self.aaop_list == []:
            self.aaop_list = self.get_default_aaops()
        log.debug("about to fill request data needs")
        self.fill_request_data_needs()
        log.debug("the current aaop list is: ")
        log.debug(self.aaop_list)
        return self.aaop_list

    def set_explicit_aaops(self):
        self.explicit_manager = self.explicit_manager_type(entity=self.entity)
        self.explicit_aaops : List[AAOP] = self.explicit_manager.process()

    def remove_unknown_services(self):
        self.unknown_manager=self.unknown_manager_type(aaop_list=self.explicit_aaops)
        self.managed_explicit_aaops : List[AAOP] = self.unknown_manager.manage_unknown_services(
            available_services=self.available_services)

    def gather_implicit_services(self): 
        self.implied_manager = self.implied_manager_type(input_object = self.entity)
        self.implicit_aaops : List[AAOP] = self.implied_manager.process()

    def manage_duplicates(self):
        self.duplicate_manager = self.duplicate_manager_type(aaop_list=self.aaop_list)
        self.return_aaop_list : List[AAOP] = self.duplicate_manager.process()

    def get_default_aaops(self) -> List[AAOP]:
        self.default_manager = self.default_manager_type()
        self.default_aaops : List[AAOP] = self.default_manager.get_default_services_aaops()
        return self.default_aaops
    
    def fill_request_data_needs(self):
        self.data_filler = self.data_filler_type(aaop_list=self.aaop_list, entity=self.entity, project=self.project)
        self.aaop_list = self.data_filler.process()


class common_Request_Manager(Request_Manager):
        
        def set_local_modules(self):
            super().set_local_modules()
