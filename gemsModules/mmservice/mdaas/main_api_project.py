#!/usr/bin/env python3
import os
import socket

from pydantic import constr, Field
from pydantic.typing import Literal as PyLiteral

from gemsModules.project.main_api import Project
from gemsModules.deprecated.instance_config.main import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class MdProject(Project):
    """This is a very hacky version for proof of concept.  This is not intended for use in production."""

    title: str = "very hacky initial MDaaS service"
    parent_entity: str = "mmservice"
    app: str = "MDaaS"
    requested_service: str = "mdaas"
    entity_id: str = "md"
    service_id: str = "md"
    ## service_id: str = "RunMD" ## this was breaking things
    # filesystem_path unset to find out where defaults come from. TODO/N: We should consider the nature of setting defaults here.
    # filesystem_path: str = "/website/userdata"
    ##  Defaults are managed in the parent class (Project) and are set using 'add_filesystem_info()'.
    filesystem_path: str = ""
    service_dir: str = "mmservice"
    requesting_agent: str = "tester"
    has_input_files: bool = True
    system_phase: constr(max_length=25) = "In solvent"
    input_type: constr(max_length=25) = "Amber-prmtop & inpcrd"
    parm7_file_name: constr(max_length=255) = "DGlcpa1-OH.parm7"
    rst7_file_name: constr(max_length=255) = "DGlcpa1-OH.rst7"
    unsolvated_parm7_file_name: constr(max_length=255) = "unminimized-gas.parm7"
    u_uuid: constr(max_length=36) = " "
    sim_length: constr(max_length=5) = "100"
    notify: bool = False
    # TODO: Currently ignored by set_up_run_md_directory.
    #upload_path: constr(max_length=255) = "/programs/gems/tests/temp-inputs/mdinput" 
    ##    Why is it this directory? It should not be inside gems.
    upload_path: constr(max_length=255) = ""

    project_type: PyLiteral["md"] = Field("md", title="Type", alias="type")

    # TODO need protocol file in mdproject
    protocolFilesPath: str = "/programs/gems/External/MD_Utils/protocols/RoeProtocol"

    ## temporary? (BLF 2026-01-24)
    def add_temporary_info(self):
        #ic = InstanceConfig()
        #self.versions_file_path: str = os.path.join(self.project_dir, "VERSIONS.sh")
        #self.project_dir: str = os.path.join(
        #    ic.get_filesystem_path(app="MDaaS-RunMD"), self.pUUID
        #)

        self.add_filesystem_info()
        log.debug(f"MdProject location: {self.project_dir}")

        self.logs_dir: str = os.path.join(self.project_dir, "logs")
        self.site_mode: str = "proof-of-concept"

    ## TODO figure out a kind way to make this generic for all methods, even those 
    ##      that do not have all these features.
    def add_filesystem_info(self):
        self.setFilesystemPath(noClobber=False)
        self.setUploadsPath(noClobber=False)
        self.setServiceDir(noClobber=False)
        self.setProjectDir(noClobber=False)
        self.setVersionsFilePath(noClobber=False)

