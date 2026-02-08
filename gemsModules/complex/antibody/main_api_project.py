#!/usr/bin/env python3
import os

from pydantic import constr, Field
from pydantic.typing import Literal as PyLiteral
from typing import Literal

from gemsModules.project.main_api import Project
from gemsModules.systemoperations.instance_config.main import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AntibodyProject(Project):
    """Antibody Project class"""

    title: str = "Initial Antibody Project"
    parent_entity: str = "Complex"
    app: str = "AntibodyDocking"
    requested_service: str = ""
    project_type: PyLiteral["ad"] = Field("ad", title="Type", alias="type")
    entity_id: str = "antibody"
    service_id: constr(max_length=25) = ""  # what should this be?
    gm_utils_version: str = ""
    requesting_agent: str = "tester"
    input_type: constr(max_length=25) = (
        "AutoDock extended PDB (chemical/pdbqt) & application/json"
    )

    pUUID: constr(max_length=36) = ""
    project_dir: constr(max_length=255) = ""

    # TODO: Better names, also, snake_case
    protein: constr(max_length=255) = ""
    ligand: constr(max_length=255) = ""

    @staticmethod
    def get_project_dir_from_pUUID(pUUID: str):
        return os.path.join(
            InstanceConfig().get_filesystem_path("AntibodyDocking"), pUUID
        )

    def add_temporary_info(self):
        self.project_dir: str = self.get_project_dir_from_pUUID(self.pUUID)
