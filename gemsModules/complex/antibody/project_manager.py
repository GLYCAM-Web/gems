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
        # log.debug("Antibody_Project_Manager.process")
        # log.debug("incoming_entity: %s", self.incoming_entity)
        # log.debug("incoming_project: %s", self.incoming_project)
        
        self.instantiate_response_project()
        # Broken: TODO/fixme: But useful for correcting Build.project_dir when it should come from Evaluation.project_dir.
        # self.fill_response_project_from_incoming_project()
        self.fill_response_project_from_response_entity()

        return self.response_project

    def instantiate_response_project(self) -> AntibodyProject:
        self.response_project = self.instantiate_new_project()

        return self.response_project

    @staticmethod
    def instantiate_new_project() -> AntibodyProject:
        """This is a static method that returns a new project."""
        project = AntibodyProject()
        project.add_temporary_info()
        return project

    # TODO: can probably be generalized and just pass the Project type.
    def fill_response_project_from_incoming_project(self, responseProject: AntibodyProject, responseEntity: Antibody_Entity):
        self.response_project = responseProject
        for response in responseEntity.responses.__root__.values():
            if response.typename == "Status" :
                self.response_project.status = response.outputs.status
        return self.response_project

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

    def fill_response_project_from_response_entity(self):
        log.debug("fill_response_project_from_response_entity %s", self.incoming_entity)
        ...


def testme() -> AntibodyProject:
    the_entity = Antibody_Entity(type="AntibodyDocking")
    the_project = Antibody_Entity()
    the_manager = Antibody_Project_Manager(
        entity=the_entity, incoming_project=the_project
    )
    return the_manager.instantiate_new_project()


if __name__ == "__main__":
    project = testme()
    print(project.json(indent=2))
