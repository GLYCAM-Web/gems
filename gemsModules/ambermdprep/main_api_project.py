import os

from pydantic import typing, constr, Field

from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrepProject(Project):
    """A project for storing information about an AmberMDPrep project.

    Right now, this only offers the PreparePDB service.

    """

    title: str = "very hacky initial AmberMDPrep service"
    parent_entity: str = "ambermdprep"
    app: str = "md"
    requested_service: str = "ambermdprep"
    entity_id: str = "AmberMDPrep"
    service_id: str = "PreparePDB"
    filesystem_path: str = "/website/userdata/"
    service_dir: str = "prepare_pdb"
    requesting_agent: str = "tester"
    has_input_files: bool = True
    system_phase: constr(max_length=25) = "In solvent"
    input_type: constr(max_length=25) = "pdb"
    pdb_file_name: constr(max_length=255) = "016.AmberMDPrep.4mbzEdit.pdb"
    u_uuid: constr(max_length=36) = " "
    notify: bool = False
    upload_path: constr(
        max_length=255
    ) = "/website/userdata/prepare_pdb/016.AmberMDPrep.4mbzEdit.pdb"

    project_type: typing.Literal["md"] = Field("md", title="Type", alias="type")

    def add_temporary_info(self):
        self.project_dir: str = os.path.join(
            self.filesystem_path, self.service_dir, self.project_type, self.pUUID
        )
        self.compute_cluster_filesystem_path: str = self.project_dir
        self.logs_dir: str = os.path.join(self.project_dir, "logs")
        self.site_mode: str = "proof-of-concept"
        self.versions_file_path: str = os.path.join(self.project_dir, "VERSIONS.sh")

    def add_pdb_info(self):
        pass
