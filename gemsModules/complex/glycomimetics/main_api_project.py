#!/usr/bin/env python3
import os

from pydantic import constr, Field
from typing import Literal

from gemsModules.project.main_api import Project
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class GlycomimeticsProject(Project):
    """Glycomimetics Project class"""

    title: str = "Initial Glycomimetics Project"
    parent_entity: str = "complex"
    app: str = "gm"
    requested_service: str = ""
    project_type: Literal["gm"] = Field("gm", title="Type", alias="type")
    entity_id: str = "complex/glycomimetics"
    service_id: constr(max_length=25) = ""  # what should this be?
    gm_utils_version: str = ""
    requesting_agent: str = "tester"
    input_type: constr(max_length=25) = (
        "AutoDock extended PDB (chemical/pdbqt) & application/json"
    )

    pUUID: constr(max_length=36) = ""
    project_dir: constr(max_length=255) = ""

    # TODO: Better names, also, snake_case
    complex: constr(max_length=255) = "Complex.pdb"
    receptor: constr(max_length=255) = "Receptor.pdb"
    ligand: constr(max_length=255) = "Ligand.pdb"

    # protocolFilesPath: constr(max_length=255) = "/website/programs/gems/External/GM_Utils/protocols"

    # TODO: convert to glycomimetics protocols
    metadataPath: constr(max_length=255) = (
        "/programs/gems/External/GM_Utils/metadata"  # /moeties etc.
    )

    def add_temporary_info(self):
        ic = InstanceConfig()

        # this could probably be generalized.
        self.project_dir: str = os.path.join(
            ic.get_filesystem_path("Glycomimetics"), self.pUUID
        )
