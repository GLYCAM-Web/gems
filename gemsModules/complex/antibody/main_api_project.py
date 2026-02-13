#!/usr/bin/env python3
import os

from pydantic import constr, Field
from pydantic.typing import Literal as PyLiteral
from typing import Literal, Any

from gemsModules.project.main_api import Project
from gemsModules.deprecated.instance_config.main import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AntibodyProject(Project):
    """Antibody Project class"""
    # TODO: Better names, also, snake_case
    protein: constr(max_length=255) = ""
    ligand: constr(max_length=255) = ""
    input_type: constr(max_length=255) =  "AutoDock extended PDB (chemical/pdbqt) & application/json"

    def __init__(self, **data : Any):
        super().__init__(**data)
        self.has_input_files = False
        self.project_type = 'ad'
        self.parent_entity = "Complex"
        self.entity_id = "antibody"
        self.service_id = "ad"
        self.title = "Initial Antibody Project"
        self.app = "AntibodyDocking"
        self.requesting_agent = ""

    def add_filesystem_info(self):
        self.setFilesystemPath(noClobber=False)
        self.setUploadsPath(noClobber=False)
        self.setServiceDir(noClobber=False)
        self.setProjectDir(noClobber=False)
        self.setVersionsFilePath(noClobber=False)


