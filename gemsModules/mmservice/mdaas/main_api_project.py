#!/usr/bin/env python3
import os
import socket

from pydantic import constr, Field
from pydantic.typing import Literal as pyLiteral

from gemsModules.project.main_api import Project
from gemsModules.systemoperations.instance_ops import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class MdProject(Project):
    """This is a very hacky version for proof of concept.  This is not intended for use in production."""

    title: str = "very hacky initial MDaaS service"
    parent_entity: str = "mmservice"
    app: str = "md"
    requested_service: str = "mdaas"
    entity_id: str = "MDaaS"
    service_id: str = "RunMD"
    # filesystem_path unset to find out where defaults come from. TODO/N: We should consider the nature of setting defaults here.
    filesystem_path: str = "/website/userdata"
    service_dir: str = "mmservice"
    requesting_agent: str = "tester"
    has_input_files: bool = True
    system_phase: constr(max_length=25) = "In solvent"
    input_type: constr(max_length=25) = "Amber-prmtop & inpcrd"
    parm7_file_name: constr(max_length=255) = "DGlcpa1-OH.parm7"
    rst7_file_name: constr(max_length=255) = "DGlcpa1-OH.rst7"
    u_uuid: constr(max_length=36) = " "
    sim_length: constr(max_length=5) = "100"
    notify: bool = False
    # TODO: Currently ignored by set_up_run_md_directory.
    upload_path: constr(max_length=255) = "/programs/gems/tests/temp-inputs/mdinput"

    project_type: pyLiteral["md"] = Field("md", title="Type", alias="type")

    # TODO need protocol file in mdproject
    protocolFilesPath: str = "/programs/gems/External/MD_Utils/protocols/RoeProtocol"

    def add_temporary_info(self):
        # This is assuming an MDaaS-RunMD Context, in swarm needs to be:
        # self.compute_cluster_filesystem_path = None or "/cluster/thoreau/scratch2/thoreau-web"
        # and the metal thoreau config should be:
        # self.compute_cluster_filesystem_path = "/scratch2/thoreau-web"
        ic = InstanceConfig()

        fs_path = os.path.join(
            str(ic.get_md_filesystem_path()),
            self.pUUID,
        )
        log.debug(f"md_project location: {fs_path}")

        self.project_dir: str = fs_path
        self.logs_dir: str = os.path.join(self.project_dir, "logs")
        self.site_mode: str = "proof-of-concept"
        self.versions_file_path: str = os.path.join(self.project_dir, "VERSIONS.sh")
