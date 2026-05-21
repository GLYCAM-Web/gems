#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.project_manager import Project_Manager

from gemsModules.batchcompute.main_api import Batchcompute_Entity
from gemsModules.batchcompute.main_api_project import Batchcompute_Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Batchcompute_Project_Manager(Project_Manager):

    def process(self) -> Batchcompute_Project:
        self.response_project = Batchcompute_Project()
        self.instantiate_response_project()
        return self.response_project

    def instantiate_response_project(self) -> Batchcompute_Project:
        self.response_project.add_filesystem_info()

    ## Override this method if you want to copy the incoming project to the response project.
    def fill_response_project_from_incoming_project(self):
        pass

    ## This maintains project type and does not make any changes to the project.
    ## Override this method if you need to add information from the responses objects
    ## to the response project 
    def fill_response_project_from_response_entity(self, 
            responseProject: Batchcompute_Project, 
            responseEntity:  Batchcompute_Entity):
            return super().fill_response_project_from_response_entity(
                    responseProject=responseProject,
                    responseEntity=responseEntity)


def testme() -> Batchcompute_Project :
    the_entity=Batchcompute_Entity(type="batchcompute")
    the_project=Batchcompute_Project()
    the_manager=Batchcompute_Project_Manager(entity=the_entity, project=the_project)
    return the_manager.instantiate_new_project()

if __name__ == "__main__":
    project=testme()
    print(project.json(indent=2))
