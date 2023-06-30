#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod

from gemsModules.common.project_manager import Project_Manager

from gemsModules.structurefile.PDB.main_api import PDB_Entity
from gemsModules.structurefile.PDB.main_api_project import PDB_Project

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDB_Project_Manager(Project_Manager):
    def process(self) -> PDB_Project:
        self.instantiate_response_project()
        return self.response_project

    def instantiate_response_project(self) -> PDB_Project:
        # self.fill_response_project_from_incoming_project()
        self.response_project = PDB_Project()
        self.response_project.add_temporary_info()

        return self.response_project

    @staticmethod
    def instantiate_new_project() -> PDB_Project:
        """This is a static method that returns a new project."""
        project = PDB_Project()
        project.add_temporary_info()
        return project

    def fill_response_project_from_incoming_project(self):
        if self.incoming_project is not None:
            self.response_project = PDB_Project(**self.incoming_project.dict())

    def fill_response_project_from_response_entity(self):
        self.response_project = PDB_Project()
        self.response_project.inputs = self.incoming_entity.inputs
        self.response_project.outputs = self.incoming_entity.outputs


def testme() -> PDB_Project:
    the_entity = PDB_Entity(type="PDB")
    the_project = PDB_Project()
    the_manager = PDB_Project_Manager(entity=the_entity, incoming_project=the_project)
    return the_manager.process()


if __name__ == "__main__":
    proj = testme()
    print(proj.json(indent=2))
