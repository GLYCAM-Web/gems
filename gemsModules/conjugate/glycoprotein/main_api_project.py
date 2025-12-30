#!/usr/bin/env python3
from pydantic import constr, Field
from pydantic.typing import Literal as PyLiteral
from typing import Literal
from pathlib import Path

from gemsModules.project.main_api import Project
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class GlycoProteinProject(Project):
    """ GlycoProtein project for making new entities. """
    title : str = "GlycoProtein project"
    parent_entity : str = ""
    app : str = "GlycoProtein"
    requested_service : str = "Build"
    project_type : PyLiteral["gp"] = Field("gp", title="Type", alias="type")
    entity_id : str = "conjugate.glycoprotein"
    service_id : str = ""
    requesting_agent : str = ""
    input_type : constr(max_length=25) = "PDB (chemical/pdb) & Glycan Mappings (application/json)"

    pUUID: constr(max_length=36) = ""
    project_dir: constr(max_length=255) = ""

    gpbuilder_input_file: constr(max_length=255) = "the_input.txt"
    
    def add_temporary_info(self): 
        self.project_dir : str = str(self.get_project_dir_from_pUUID(self.pUUID))

    @staticmethod
    def get_project_dir_from_pUUID(pUUID: str):
        return Path(
            InstanceConfig().get_filesystem_path(app="GlycoProtein"), pUUID
        )
