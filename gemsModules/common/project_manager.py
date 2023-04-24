#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.main_api_entity import Entity
from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Project_Manager(ABC):
    
    def __init__(self, entity : Entity, project : Project = None):
        self.response_entity = entity
        self.incoming_project = project

    def process(self) -> Project:
        self.response_project = Project()
        self.fill_response_project_from_incoming_project()
        self.fill_response_project_from_response_entity()
        return self.response_project

    @abstractmethod
    def fill_response_project_from_incoming_project(self):
        pass

    @abstractmethod
    def fill_response_project_from_response_entity(self):
        pass

class common_Project_Manager(Project_Manager):
        
        def __init__(self, entity : Entity, project : Project = None):
            super().__init__(entity, project)
    
        def fill_response_project_from_incoming_project(self):
            if self.incoming_project is not None:
                self.response_project = self.incoming_project
    
        def fill_response_project_from_response_entity(self):
            pass