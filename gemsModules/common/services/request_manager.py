#!/usr/bin/env python3
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_entity import Entity
from gemsModules.common.services.explicit_requests import Explicit_Service_Request_Manager
from gemsModules.common.services.service_packages_list import Services_Package_List_Manager
from gemsModules.common.services.implied_requests import Implicit_Services_Request_Manager 
from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Request_Manager():
    
    def __init__(self, entity : Entity, project : Project):
        self.entity = entity
        self.project = project

    def process(self):
        self.set_explicit_aaops()
        self.remove_unknown_services()
        self.gather_implicit_services()

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

    
