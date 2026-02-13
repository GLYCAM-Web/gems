#!/usr/bin/env python3
from typing import Literal
import os

from pydantic import constr, Field

from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class {{cookiecutter.gems_module}}_Project(Project):
    """ {{cookiecutter.gems_module}} project for making new entities. """

    def __init__(self, **data : Any):
        super().__init__(**data)
        self.has_input_files = True
        self.project_type = "" # This is often set to the same string as service_id
        self.parent_entity = "" # This is the name of the top directory gemsModule if this is a subModule
        self.entity_id = "{{cookiecutter.gems_module}}" # Do not include the parent directory here
        self.service_id = "{{cookiecutter.service_id}}" # this is the subdirectory in the output path (like cb, gp, ad, gm, pdb, etc)
        self.title = "{{cookiecutter.gems_module}} project"
        self.app = "{{cookiecutter.entity_name}}"
        self.requesting_agent = "" # Website, command line, sideload, etc.
        self.requested_service = "{{cookiecutter.service_name}}"
        self.site_mode = "proof-of-concept"

        ## If the following are universally used, add them to the main Project class
        #
        #u_uuid : constr(max_length=36) = " "
        #notify : bool = False
   
        ## This is defined in Project, so not redefining it here
        #
        #project_type : Literal['{{cookiecutter.gems_module}}'] = Field(  
        #        '{{cookiecutter.gems_module}}',
        #        title='Type',
        #        alias='type'
        #        )

    def add_filesystem_info(self):
        self.setFilesystemPath(noClobber=False)
        self.setUploadsPath(noClobber=False)
        self.setServiceDir(noClobber=False)
        self.setProjectDir(noClobber=False)
        self.setVersionsFilePath(noClobber=False)
        self.logs_dir = os.path.join(self.project_dir, "logs")
        self.versions_file_path = os.path.join(self.project_dir, "VERSIONS.sh")
        self.compute_cluster_filesystem_path = self.project_dir


## These are added automatically unless specified by the user
#
#filesystem_path : str = "/some/path/"
#service_dir : str = "{{cookiecutter.service_name}}_dir"
#uploads_path : constr(max_length=255)  = "" # Set automatically from 
#    def add   temporary   info(self): 
#        self.project_dir : str = os.path.join(self.filesystem_path,
#                self.service_dir,
#                self.project_type,
#                self.pUUID)
