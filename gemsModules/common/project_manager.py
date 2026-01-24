#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.main_api_entity import Entity
from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Project_Manager(ABC):
    def __init__(self, entity: Entity, incoming_project: Project = None):
        self.incoming_entity = entity
        self.incoming_project = incoming_project
        self.response_project = None

    def process(self) -> Project:
        self.response_project = Project()
        self.fill_response_project_from_incoming_project()
        self.fill_response_project_from_response_entity(responseProject=None, responseEntity=None)
        return self.response_project

#    @abstractmethod
    def fill_response_project_from_incoming_project(self):
        self.response_project = self.incoming_project.copy(deep=True)

#    @abstractmethod
#    def fill_response_project_from_response_entity(self, responseProject: Project, responseEntity: Entity):
#    @abstractmethod
    def fill_response_project_from_response_entity(self, responseProject, responseEntity):
    ##  I hope that the following is not true.
    ##  To use this in an entity without making changes to it, you need to declare the method like the following.
    ##  Note especially where the declaration requires local class types. Here, the example is from the PDBFile
    ##  entity inside the structurefile parent. It is important to return the correct type of project.
    #   def fill_response_project_from_response_entity(self, responseProject: PDBFile_Project, responseEntity: PDBFile_Entity):
    #       return super().fill_response_project_from_response_entity(responseProject=responseProject,responseEntity=responseEntity)
        return responseProject


class common_Project_Manager(Project_Manager):
    def fill_response_project_from_incoming_project(self):
        if self.incoming_project is not None:
            self.response_project = self.incoming_project

    def fill_response_project_from_response_entity(self, responseProject: Project, responseEntity: Entity):
        pass
