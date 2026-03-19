#!/usr/bin/env python3
import os

from pydantic import BaseModel, constr, Field
from pydantic.typing import Literal as PyLiteral
from typing import Literal, Any

from gemsModules.project.main_api import Project
#from gemsModules.deprecated.instance_config.main import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

class AntibodyExecutionHostData(BaseModel):
    ## These indicate paths are on the execution host
    external_stacks_path : str = Field(
            "" ,
            description = "Path to software stacks that are not just binaries (gems, amber, etc.)"
            )
    binary_dependencies_path : str = Field(
            "",
            description = "Path to standard binary dependencies, e.g., VMD."
            )
    aad2_docker_version : str = Field(
            "",
            description = "in the external_stacks_path, look for AAD2_Docker_v{aad2_docker_version}."
            )
    aad2_docker_home : str = Field(
            "",
            description = "If unset: {external_stacks_path}/AAD2_Docker_v{aad2_docker_version}."
            )
    aad2_cli_bin_path : str = Field(
            "",
            description = "if unset: {external_stacks_path}/AAD2_Docker_v{aad2_docker_version}/image/AAD2/bin."
            )
    aad2_image_name : str = Field(
            "",
            description = "The name for the AAD2 docker image."
            )
    aad2_image_tag : str = Field(
            "",
            description = "The tag for the AAD2 docker image."
            )
    aad2_image_file_path : str = Field(
            "",
            description = "The full path to the AAD2 docker image files."
            )
    vmd_home : str = Field(
            "",
            description = "The full path to the VMD binary."
            )
    vmd_lib : str = Field(
            "",
            description = "The full path to the VMD library directory."
            )



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



