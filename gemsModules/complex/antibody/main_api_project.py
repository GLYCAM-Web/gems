#!/usr/bin/env python3
import os

from pydantic import constr, Field
from pydantic.typing import Literal as PyLiteral
from typing import Literal, Any

from gemsModules.project.main_api import Project
#from gemsModules.deprecated.instance_config.main import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AntibodyProject(Project):
    """Antibody Project class"""

    ## These are required by the code that does the docking
    protein: constr(max_length=255) = ""
    ligand: constr(max_length=255) = ""
    input_type: constr(max_length=255) =  "AutoDock extended PDB (chemical/pdbqt) & application/json"

    ## These indicate where the code and its dependencies are
    external_stacks_path : str = ""
    aad2_docker_version : str = ""
    aad2_docker_path : str = ""
    binary_dependencies_path : str = ""
    


    def __init__(self, **data : Any):
        super().__init__(**data)
        self.has_input_files = False
        self.project_type = 'ad'
        self.parent_entity = "Complex"
        self.entity_id = "antibody"
        self.service_id = "ad"
        self.title = "Automated Antibody-Glycan Docking Project"
        self.app = "AntibodyDocking"
#        self.requesting_agent = "" ## This probably does not need to be set.
        self.setFilesystemPath(noClobber=False)
        self.setUploadsPath(noClobber=False)
        self.setServiceDir(noClobber=False)
        self.setProjectDir(noClobber=False)
        self.setVersionsFilePath(noClobber=False)
        self.logs_dir = str(os.path.join(self.project_dir, "logs"))


