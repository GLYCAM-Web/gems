#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.main_api_entity import Entity
from gemsModules.project.main_api import Project
from gemsModules.common.project_manager import Project_Manager

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class delegator_Project_Manager(Project_Manager):

    def process(self) -> Project:
        return None

    def fill_response_project_from_incoming_project(self):
        return None

    def fill_response_project_from_response_entity(self):
        return None

