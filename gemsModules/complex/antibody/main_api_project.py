#!/usr/bin/env python3
import os

from pydantic import constr, Field
from typing import Literal

from gemsModules.project.main_api import Project
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AntibodyProject(Project):
    """Antibody Project class"""

    title: str = "Initial Antibody Project"
    parent_entity: str = "complex"
    app: str = "ad"
    requested_service: str = ""
    project_type: Literal["ad"] = Field("ad", title="Type", alias="type")
    entity_id: str = "complex/antibody"
    service_id: constr(max_length=25) = ""  # what should this be?
    gm_utils_version: str = ""
    requesting_agent: str = "tester"
    input_type: constr(max_length=25) = (
        "AutoDock extended PDB (chemical/pdbqt) & application/json"
    )

    pUUID: constr(max_length=36) = ""
    project_dir: constr(max_length=255) = ""

    # TODO: Better names, also, snake_case
    protein: constr(max_length=255) = "protein.pdb"
    ligand: constr(max_length=255) = "ligand.pdb"


    def add_temporary_info(self):
        ic = InstanceConfig()

        # this could probably be generalized.
        self.project_dir: str = os.path.join(
            ic.get_filesystem_path("AntibodyDocking"), self.pUUID
        )
