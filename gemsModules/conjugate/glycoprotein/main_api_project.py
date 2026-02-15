#!/usr/bin/env python3
from pydantic import constr, Field
from pydantic.typing import Literal as PyLiteral
from typing import Any
from pathlib import Path
import os

from gemsModules.project.main_api import Project
#from gemsModules.deprecated.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class GlycoProteinProject(Project):
    """ GlycoProtein project for making new entities. """
    pdb_project_pUUID : constr(max_length=36)=""
    status : constr(max_length=10)="submitted"
    gpbuilder_input_file: constr(max_length=255) = "the_input.txt"
    input_type  = "PDB (chemical/pdb) & Glycan Mappings (application/json)"

    def __init__(self, **data : Any):
        super().__init__(**data)
        self.has_input_files = True
        self.project_type = 'gp'
        self.parent_entity = "Conjugate"
        self.entity_id = "glycoprotein"
        self.service_id = "gp" # used for lookup in the instance config file
        self.title = "GlycoProtein project"
        self.app = "GlycoProtein"
        self.setFilesystemPath(noClobber=False)
        self.setUploadsPath(noClobber=False)
        self.setServiceDir(noClobber=False)
        self.setProjectDir(noClobber=False)
        self.setVersionsFilePath(noClobber=False)
        self.logs_dir = str(os.path.join(self.project_dir, "logs"))

