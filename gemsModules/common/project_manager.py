#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.main_api_entity import Entity
from gemsModules.project.main_api import Project

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