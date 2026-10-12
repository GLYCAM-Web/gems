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

    def fill_response_project_from_incoming_project(self):
        if self.incoming_project is not None:
            self.response_project = self.incoming_project.copy(deep=True)

    def fill_response_project_from_response_entity(self, responseProject, responseEntity):
        ##  I hope that the following is not true.
        ##  To use this in an entity without making changes to it, you need to declare the method like the following.
        ##  Note especially where the declaration requires local class types. Here, the example is from the PDBFile
        ##  entity inside the structurefile parent. It is important to return the correct type of project.
        #   def fill_response_project_from_response_entity(self, responseProject: PDBFile_Project, responseEntity: PDBFile_Entity):
        #       return super().fill_response_project_from_response_entity(responseProject=responseProject,responseEntity=responseEntity)
        return responseProject

    def get_pUUID_from_incoming_project(self) -> str:
        if self.incoming_project is None or self.incoming_entity is None:
            return None
        if not self.incoming_entity.services or not self.incoming_entity.services.__root__:
            return None
        foundUUID = None
        serviceType = None
        for service in self.incoming_entity.services.__root__.values():
            inputs = getattr(service, "inputs", None)
            if inputs is None:
                continue
            puuid = None
            if hasattr(inputs, "pUUID"):
                puuid = inputs.pUUID
            elif isinstance(inputs, dict):
                puuid = inputs.get("pUUID")
            if puuid not in (None, ""):
                log.debug("Found pUUID in incoming request: %s", puuid)
                if foundUUID in (None, ""):
                    foundUUID = str(puuid)
                    serviceType = getattr(service, "typename", "Unknown")
                elif str(foundUUID) != str(puuid):
                    log.error("Conflicting pUUID values found in services. They are:")
                    log.error(f"service: {serviceType} - pUUID {foundUUID}")
                    log.error(f"service: {getattr(service, 'typename', 'Unknown')} - pUUID {puuid}")
                    raise ValueError("Service inputs have conflicting pUUIDs")
        return foundUUID



class common_Project_Manager(Project_Manager):
    def fill_response_project_from_incoming_project(self):
        if self.incoming_project is not None:
            self.response_project = self.incoming_project

    def fill_response_project_from_response_entity(self, responseProject: Project, responseEntity: Entity):
        pass
