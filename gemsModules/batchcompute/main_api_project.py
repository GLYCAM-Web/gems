#!/usr/bin/env python3
from typing import Literal
import os

from pydantic import constr, Field

from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Batchcompute_Project(Project):
    """ batchcompute project. """

    ## These entries are all parts of a JSON object, so use JSON types, e.g., str rather than Path, etc.
    def __init__(self, **data : Any):
        super().__init__(**data)
        self.has_input_files = True
        self.project_type = "bc" # This is the same as service_id, and is used in the deprecated code as such
        self.parent_entity = "Batchcompute" # This is the name of the top directory gemsModule if this is a subModule (initial letter captialized)
                                # Otherwise it is the name of the gemsModule directory for the Entity (initial letter capitalized)
        self.entity_id = "batchcompute" # Do not include the parent directory here - lowercase
        self.service_id = "bc" # This becomes the subdirectory output paths (like cb, gp, ad, gm, pdb, etc)
                                                        # & is used for lookup in instance config
        self.title = "batchcompute project"
        self.app = "Batchcompute" # first letter capitalized or Pascal case
        # self.requesting_agent = "" # Website, command line, sideload, etc. - should be set by requesting agent
                                     # but can be filled in or overridden if used for security or sanity reasons
        self.requested_service = "SubmitJob"

        # Redefine the following as needed
        self.site_mode = "proof-of-concept"
        self.setFilesystemPath(noClobber=False)
        self.setUploadsPath(noClobber=False)
        self.setServiceDir(noClobber=False)
        self.setProjectDir(noClobber=False)
        self.setVersionsFilePath(noClobber=False)
        self.logs_dir = str(os.path.join(self.project_dir, "logs"))
        self.compute_cluster_filesystem_path = self.project_dir

## If the following are universally used, add them to the main Project class
#
#u_uuid : constr(max_length=36) = " "
#notify : bool = False
   
## This is defined in Project, so not redefining it here
#
#project_type : Literal['batchcompute'] = Field(  
#        'batchcompute',
#        title='Type',
#        alias='type'
#        )
        

## These are added automatically unless specified by the user
#
#filesystem_path : str = "/some/path/"
#service_dir : str = "SubmitJob_dir"
#uploads_path : constr(max_length=255)  = "" # Set automatically from 
#    def add   temporary   info(self): 
#        self.project_dir : str = os.path.join(self.filesystem_path,
#                self.service_dir,
#                self.project_type,
#                self.pUUID)
