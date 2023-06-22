#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.project_manager import Project_Manager

from gemsModules.structurefile.PDB.main_api import AmberMDPrep_Entity
from gemsModules.structurefile.PDB.main_api_project import PDBProject

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Project_Manager(Project_Manager):
    def process(self) -> PDBProject:
        self.instantiate_response_project()
        return self.response_project

    def instantiate_response_project(self) -> PDBProject:
        # self.fill_response_project_from_incoming_project()
        self.response_project = PDBProject()
        self.response_project.add_temporary_info()

        return self.response_project

    @staticmethod
    def instantiate_new_project() -> PDBProject:
        """This is a static method that returns a new project."""
        project = PDBProject()
        project.add_temporary_info()
        return project

    def fill_response_project_from_incoming_project(self):
        # if self.incoming_project is not None:
        #    self.response_project = AmberMDPrepProject(**self.incoming_project.dict())
        pass

    def fill_response_project_from_response_entity(self):
        # find inputs in entity and put them in project
        # find outputs in entity and put them in project

        # self.response_project = AmberMDPrepProject(**self.incoming_entity.inputs)
        pass


def testme() -> PDBProject:
    the_entity = AmberMDPrep_Entity(type="AmberMDPrep")
    the_project = PDBProject()
    the_manager = AmberMDPrep_Project_Manager(
        entity=the_entity, incoming_project=the_project
    )
    return the_manager.process()


if __name__ == "__main__":
    proj = testme()
    print(proj.json(indent=2))
