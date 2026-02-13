import os
from typing import Any

from pydantic import typing, constr, Field

from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Project(Project):
    """A project for storing information about an AmberMDPrep project.

    Right now, this only can use the PreparePDB service.

    """
    pdb_filename: constr(max_length=255) = "016.AmberMDPrep.4mbzEdit.pdb"
    input_type: constr(max_length=25) = "pdb"
    notify: bool = True

    def __init__(self, **data : Any):
        super().__init__(**data)
        self.has_input_files = True
        self.project_type = 'pdb'
        self.parent_entity = "structurefile"
        self.entity_id = "glycoprotein"
        self.service_id = "pdb"
        self.title = "very hacky initial AmberMDPrep service"
        self.app = "mdprep"
        self.requesting_agent = ""
        self.requested_service = "AmberMDPrep"
        self.uploads_path = "/website/TESTS/pdb/"

    def add_filesystem_info(self):
        self.setFilesystemPath(noClobber=False)
        self.setUploadsPath(noClobber=False)
        self.setServiceDir(noClobber=False)
        self.setProjectDir(noClobber=False)
        self.setVersionsFilePath(noClobber=False)
        self.logs_dir: str = os.path.join(self.project_dir, "logs")
        self.site_mode: str = "proof-of-concept"
        self.versions_file_path: str = os.path.join(self.project_dir, "VERSIONS.sh")

    # One day, this should inject REMARK cards providing provenance for the altered PDB file
    def add_pdb_info(self):
        pass


#    def add    temporary    info(self):  ## Keeping in case this pattern is somehow different from the above
#        self.project_dir: str = os.path.join(
#            self.filesystem_path,
#            self.parent_entity,
#            self.service_dir,
#            self.project_type,
#            self.pUUID,
#        )
#        # self.compute_cluster_filesystem_path: str = self.project_dir
