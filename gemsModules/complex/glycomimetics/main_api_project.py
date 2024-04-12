#!/usr/bin/env python3
import os

from pydantic import constr, Field
from pydantic.typing import Literal as pyLiteral

from gemsModules.project.main_api import Project
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class GlycomimeticsProject(Project):
    """This is a very hacky version for proof of concept.  This is not intended for use in production."""

    title: str = "Initial Glycomimetics Project"
    parent_entity: str = "complex"
    app: str = "glycomimetics"
    requested_service: str = ""
    entity_id: str = "glycomimetics"
    service_id: str = ""
    # filesystem_path unset to find out where defaults come from. TODO/N: We should consider the nature of setting defaults here.
    filesystem_path: str = "/website/userdata"
    service_dir: str = "glycomimetics"
    requesting_agent: str = "tester"
    has_input_files: bool = True
    system_phase: constr(max_length=25) = "In solvent"
    input_type: constr(max_length=25) = "Amber-prmtop & inpcrd"
    # TODO: input files
    u_uuid: constr(max_length=36) = " "
    sim_length: constr(max_length=5) = "100"
    notify: bool = False

    # TODO: Is this necessary?
    upload_path: constr(max_length=255) = "/programs/gems/tests/temp-inputs/mdinput"
    # TODO: Update from mdaas inputs
    parm7_file_name: constr(max_length=255) = "DGlcpa1-OH.parm7"
    rst7_file_name: constr(max_length=255) = "DGlcpa1-OH.rst7"

    # TODO: kinda redundant given the parent_entity / app or entity_id / this class type
    project_type: pyLiteral["glyco"] = Field("glyco", title="Type", alias="type")

    # TODO: convert to glycomimetics protocols
    protocolFilesPath: str = "/programs/gems/External/MD_Utils/protocols/RoeProtocol"

    def add_temporary_info(self):
        ic = InstanceConfig()

        self.project_dir: str = os.path.join(ic.get_md_filesystem_path(), self.pUUID)
        # log.debug(f"GlycomimeticsProject location: {self.project_dir}")

        # self.logs_dir: str = os.path.join(self.project_dir, "logs")
        # self.site_mode: str = "proof-of-concept"
        # self.versions_file_path: str = os.path.join(self.project_dir, "VERSIONS.sh")
