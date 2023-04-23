#!/usr/bin/env python3
from typing import List
from abc import ABC, abstractmethod

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_entity import Entity
from gemsModules.common.services.explicit_requests import Explicit_Service_Request_Manager
from gemsModules.common.services.service_packages_list import Services_Package_List_Manager
from gemsModules.common.services.implied_requests import Implicit_Services_Request_Manager 
from gemsModules.common.services.default_requests import Default_Service_Request_Manager
from gemsModules.common.services.duplicate_requests import Duplicate_Requests_Manager
from gemsModules.common.services.request_data_filler import Request_Data_Filler
from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Request_Manager(ABC):
    
    def __init__(self, entity : Entity, project : Project):
        self.entity = entity
        self.project = project

    def process(self) -> List[AAOP]:
        self.set_explicit_aaops()
        self.remove_unknown_services()
        self.gather_implicit_services()
        self.aaop_list = self.managed_explicit_aaops + self.implicit_aaops
        self.manage_duplicates()
        if self.aaop_list == []:
            self.aaop_list = self.get_default_aaops()
        self.fill_request_data_needs()
        return self.aaop_list

    def set_explicit_aaops(self):
        explicit_manager = Explicit_Service_Request_Manager(entity=self.entity)
        self.explicit_aaops : List[AAOP] = explicit_manager.process()

    @abstractmethod
    def remove_unknown_services(self):
        unknown_manager = Services_Package_List_Manager(aaop_list=self.explicit_aaops)
        self.managed_explicit_aaops : List[AAOP] = unknown_manager.manage_unknown_services()

    @abstractmethod
    def gather_implicit_services(self): 
        implicit_manager = Implicit_Services_Request_Manager(input_object = self.entity)
        self.implicit_aaops : List[AAOP] = implicit_manager.process()

    @abstractmethod
    def manage_duplicates(self):
        duplicate_manager = Duplicate_Requests_Manager(aaop_list=self.aaop_list)
        self.return_aaop_list : List[AAOP] = duplicate_manager.process()

    @abstractmethod
    def get_default_aaops(self) -> List[AAOP]:
        default_manager = Default_Service_Request_Manager()
        self.default_aaops : List[AAOP] = default_manager.get_default_services_aaops()
        return self.default_aaops
    
    @abstractmethod
    def fill_request_data_needs(self):
        data_filler = Request_Data_Filler(aaop_list=self.aaop_list, entity=self.entity, project=self.project)
        self.aaop_list = data_filler.process()