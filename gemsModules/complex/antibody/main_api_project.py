#!/usr/bin/env python3
import os

from pydantic import constr
from typing import Any

from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

class AntibodyProject(Project):
    """Antibody Project class"""

    ## These are required by the code that does the docking
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
        self.title = "Automated Antibody-Glycan Docking Project"
        self.app = "AntibodyDocking"
        self.setFilesystemPath(noClobber=False)
        self.setUploadsPath(noClobber=False)
        self.setServiceDir(noClobber=False)
        self.setProjectDir(noClobber=False)
        self.setVersionsFilePath(noClobber=False)
        self.logs_dir = str(os.path.join(self.project_dir, "logs"))



