#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod
from pathlib import Path

from gemsModules.common.project_manager import Project_Manager

from gemsModules.complex.antibody.main_api import Antibody_Entity
from gemsModules.complex.antibody.main_api_project import AntibodyProject

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Antibody_Project_Manager(Project_Manager):

    def process(self) -> AntibodyProject:
        log.info("Project management for Antibody_Project_Manager is begun")

        # If there is incoming info, use that. Else, make an incoming project.
        if self.incoming_project is not None:
            incomingUUID = get_pUUID_from_incoming_project()
            if incomingUUID is not None:
                 self.incoming_project.pUUID = foundUUID
            self.incoming_project.setProjectDir(noClobber=False)
            self.incoming_project.logs_dir = str(os.path.join(self.incoming_project.project_dir, "logs"))
        else:
            self.incoming_project = AntibodyProject()

        # Try to create specified directories as needed and complain if they are not specified
        if self.incoming_project.project_dir not in (None, "") :
            check_make_directory(Dir_Path=self.incoming_project.project_dir)
        else:
            log.error("Project directory not specified")
        if self.incoming_project.uploads_path not in (None, "") :
            check_make_directory(Dir_Path=self.incoming_project.uploads_path)
        else:
            log.error("Uploads path not specified")
        if self.incoming_project.logs_dir not in (None, "") :
            check_make_directory(Dir_Path=self.incoming_project.logs_dir)
        else:
            log.error("Logging directory for the project is not specified")

        # Generate the response project from the incoming project
        self.fill_response_project_from_incoming_project()
        log.debug("The incoming project is:")
        log.debug(self.incoming_project.json(indent=2))
        log.debug("The response project is:")
        log.debug(self.response_project.json(indent=2))
        return self.response_project

    # TODO: can probably be generalized and just pass the Project type.
    def fill_response_project_from_response_entity(self, responseProject: AntibodyProject, responseEntity: Antibody_Entity):
        self.response_project = responseProject
        for response in responseEntity.responses.__root__.values():
            if response.typename == "Status" :
                self.response_project.status = response.outputs.status
        return self.response_project

    ## This is only used for the unit test for this file
    @staticmethod
    def instantiate_new_project() -> AntibodyProject:
        """This is a static method that returns a new project."""
        project = AntibodyProject()
        project.add_filesystem_info()
        return project


##############################
#### Old code
##############################
#        ###### 
#        ###### Old process
#        ###### 
#        ## log.debug("Antibody_Project_Manager.process")
#        ## log.debug("incoming_entity: %s", self.incoming_entity)
#        ## log.debug("incoming_project: %s", self.incoming_project)
#        #
#        #self.instantiate_response_project()
#        ## Broken: TODO/fixme: But useful for correcting Build.project_dir when it should come from Evaluation.project_dir.
#        ## self.fill_response_project_from_incoming_project()
#        #self.fill_response_project_from_response_entity()
#        #
#        #return self.response_project
#        ####### 
#        ####### 
#        ####### 
#
# Should no longer be needed
#    def instantiate_response_project(self) -> AntibodyProject:
#        self.response_project = self.instantiate_new_project()
#
#        return self.response_project
#        if self.incoming_project is not None:
#            # need to combine instead of create new
#            # self.response_project = AntibodyProject(**self.incoming_project.dict())
#            if self.response_project is None:
#                self.response_project = self.instantiate_new_project()
#
#            for key, value in self.incoming_project.dict().items():
#                if key in self.response_project.dict().keys():
#                    self.response_project.dict()[key] = value
#                else:
#                    log.warning("Key %s not in response project", key)
#

####
#### This test has not been tested and probably will not work
####
def testme() -> AntibodyProject:
    the_entity = Antibody_Entity(type="AntibodyDocking")
    the_project = AntibodyProject() 
    the_manager = Antibody_Project_Manager(
        entity=the_entity, incoming_project=the_project
    )
    return the_manager.instantiate_new_project()


if __name__ == "__main__":
    project = testme()
    print(project.json(indent=2))
