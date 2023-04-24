#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_entity import Entity
from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Request_Data_Filler(ABC):
    
    def __init__(self, aaop_list : List[AAOP], entity : Entity, project : Project):
        self.aaop_list = aaop_list
        self.entity = entity
        self.project = project

    @abstractmethod
    def process(self) -> List[AAOP]:
        pass
        

class common_Request_Data_Filler(Request_Data_Filler):
        
    def process(self) -> List[AAOP]:
        log.debug("common_Request_Data_Filler.process() called.")
        return self.aaop_list