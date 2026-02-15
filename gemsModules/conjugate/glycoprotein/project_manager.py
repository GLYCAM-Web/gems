#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.project_manager import Project_Manager

from gemsModules.conjugate.glycoprotein.main_api import GlycoProtein_Entity
from gemsModules.conjugate.glycoprotein.main_api_project import GlycoProteinProject

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class GlycoProtein_Project_Manager(Project_Manager):

    def process(self) -> GlycoProteinProject:
        log.info("Project management for GlycoProtein_Project_Manager is begun")
        #self.instantiate_response_project()
        if self.incoming_project is not None:
            self.response_project = self.fill_response_project_from_incoming_project()
        else: 
            self.response_project = GlycoProteinProject()
        return self.response_project

#    def instantiate_response_project(self) -> GlycoProteinProject:
#        self.response_project = GlycoProteinProject()
#        self.response_project.add_filesystem_info()

#    def fill_response_project_from_incoming_project(self):
#        pass

    # This happens at the very end of the transaction's processing
    def fill_response_project_from_response_entity(self, responseProject: GlycoProteinProject, responseEntity: GlycoProtein_Entity):
        log.info("Final fill of response project for GlycoProtein_Project_Manager is begun")
        self.response_project = responseProject
        for response in responseEntity.responses.__root__.values():
            if response.typename == "Status" :
                self.response_project.status = response.outputs.status
        return self.response_project



def testme() -> GlycoProteinProject :
    the_entity=GlycoProtein_Entity(type="GlycoProtein")
    the_project=GlycoProteinProject()
    the_manager=GlycoProtein_Project_Manager(entity=the_entity, project=the_project)
    return the_manager.instantiate_new_project()

if __name__ == "__main__":
    project=testme()
    print(project.json(indent=2))
