#!/usr/bin/env python3
## Possibly this should be in gemsModules/project.

from abc import ABC, abstractmethod
import os

from gemsModules.common.project_manager import Project_Manager

from gemsModules.structurefile.PDBFile.main_api import PDBFile_Entity
from gemsModules.structurefile.PDBFile.main_api_project import PDBFile_Project

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Project_Manager(Project_Manager):
    def process(self) -> PDBFile_Project:
        self.instantiate_response_project()
        return self.response_project

    def instantiate_response_project(self) -> PDBFile_Project:
        self.response_project = PDBFile_Project()
        self.response_project.add_temporary_info()
        return self.response_project

    @staticmethod
    def instantiate_new_project() -> PDBFile_Project:
        """This is a static method that returns a new project."""
        project = PDBFile_Project()
        project.add_temporary_info()
        return project

    def fill_response_project_from_incoming_project(self):
        if self.incoming_project is not None:
            self.response_project = PDBFile_Project(**self.incoming_project.dict())

    def fill_response_project_from_response_entity(self):
        self.response_project = PDBFile_Project()
        self.response_project.inputs = self.incoming_entity.inputs
        self.response_project.outputs = self.incoming_entity.outputs


def testme() -> PDBFile_Project:
    the_entity = PDBFile_Entity(type="PDB")
    the_project = PDBFile_Project()
    the_manager = PDBFile_Project_Manager(
        entity=the_entity, incoming_project=the_project
    )
    return the_manager.process()


if __name__ == "__main__":
    proj = testme()
    print(proj.json(indent=2))
