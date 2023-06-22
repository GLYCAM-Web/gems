import os

from pydantic import typing, constr, Field

from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBProject(Project):
    """A project for storing information about an AmberMDPrep project.

    Right now, this only can use the PreparePDB service.

    """

    title: str = "very hacky initial AmberMDPrep service"
    parent_entity: str = "structurefile"
    app: str = "mdprep"
    requested_service: str = "AmberMDPrep"
    entity_id: str = "PDB"
    service_id: str = "AmberMDPrep"
    filesystem_path: str = "/website/userdata/"
    service_dir: str = ""
    requesting_agent: str = "tester"
    has_input_files: bool = True
    system_phase: constr(max_length=25) = "In solvent"
    input_type: constr(max_length=25) = "pdb"
    pdb_file_name: constr(max_length=255) = "016.AmberMDPrep.4mbzEdit.pdb"
    u_uuid: constr(max_length=36) = " "
    notify: bool = False
    upload_path: constr(max_length=255) = "/website/TESTS/PDB/"

    project_type: typing.Literal["pdb"] = Field("pdb", title="Type", alias="type")

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
