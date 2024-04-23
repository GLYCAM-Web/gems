#!/usr/bin/env python3
import os

from pydantic import constr, Field
from pydantic.typing import Literal as pyLiteral

from gemsModules.project.main_api import Project
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class GlycomimeticsProject(Project):
    """Glycomimetics Project class"""

    title: str = "Initial Glycomimetics Project"
    parent_entity: str = "complex"
    app: str = "glycomimetics"
    requested_service: str = ""
    entity_id: str = "complex/glycomimetics"
    requesting_agent: str = "tester"
    u_uuid: constr(max_length=36) = " "
    sim_length: constr(max_length=5) = "100"

    # TODO: Update from mdaas inputs
    has_input_files: bool = True
    input_type: constr(max_length=25) = "Amber-prmtop & inpcrd"
    parm7_file_name: constr(max_length=255) = "DGlcpa1-OH.parm7"
    rst7_file_name: constr(max_length=255) = "DGlcpa1-OH.rst7"

    # TODO: convert to glycomimetics protocols
    metadataPath: str = "/programs/gems/External/GM_Utils/metadata"  # /moeties etc.

    def add_temporary_info(self):
        ic = InstanceConfig()

        self.project_dir: str = os.path.join(
            ic.get_filesystem_path("Glycomimetics"), self.pUUID
        )
