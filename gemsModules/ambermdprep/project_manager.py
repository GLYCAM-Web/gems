#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.project_manager import Project_Manager

from gemsModules.ambermdprep.main_api import AmberMDPrep_Entity
from gemsModules.ambermdprep.main_api_project import AmberMDPrepProject

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Project_Manager(Project_Manager):
    def process(self) -> AmberMDPrepProject:
        self.instantiate_response_project()
        return self.response_project

    def instantiate_response_project(self) -> AmberMDPrepProject:
        # self.fill_response_project_from_incoming_project()
        self.response_project = AmberMDPrepProject()
        self.response_project.add_temporary_info()

        return self.response_project

    @staticmethod
    def instantiate_new_project() -> AmberMDPrepProject:
        """This is a static method that returns a new project."""
        project = AmberMDPrepProject()
        project.add_temporary_info()
        return project

    def fill_response_project_from_incoming_project(self):
        if self.incoming_project is not None:
            self.response_project = AmberMDPrepProject(**self.incoming_project.dict())

    def fill_response_project_from_response_entity(self):
        # find inputs in entity and put them in project
        # find outputs in entity and put them in project

        self.response_project = AmberMDPrepProject(**self.incoming_entity.inputs)


def testme() -> AmberMDPrepProject:
    the_entity = AmberMDPrep_Entity(type="AmberMDPrep")
    the_project = AmberMDPrepProject()
    the_manager = AmberMDPrep_Project_Manager(
        entity=the_entity, incoming_project=the_project
    )
    return the_manager.process()


if __name__ == "__main__":
    project = testme()
    print(project.json(indent=2))
