#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.project_manager import Project_Manager

from gemsModules.mmservice.mdaas.main_api import MDaaS_Entity
from gemsModules.mmservice.mdaas.main_api_project import MdProject

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class mdaas_Project_Manager(Project_Manager):

    def process(self) -> MdProject:
        self.response_project = MdProject()
        self.instantiate_response_project()
        return self.response_project

    def instantiate_response_project(self) -> MdProject:
        self.response_project.add_temporary_info()

    def fill_response_project_from_incoming_project(self):
        pass

    def fill_response_project_from_response_entity(self):
        pass


def testme() -> MdProject :
    the_entity=MDaaS_Entity(type="MDaaS")
    the_project=MdProject()
    the_manager=mdaas_Project_Manager(entity=the_entity, project=the_project)
    return the_manager.instantiate_new_project()

if __name__ == "__main__":
    project=testme()
    print(project.json(indent=2))
