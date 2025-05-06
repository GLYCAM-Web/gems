#!/usr/bin/env python3
import os
from pydantic import constr, Field
from typing import Literal

from gemsModules.project.main_api import Project
from gemsModules.systemoperations.instance_config import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Gpbuilder_Project(Project):
    """ GpBuilder project for making new entities. """
    title : str = "GpBuilder project"
    parent_entity : str = ""
    app : str = "GpBuilder"
    requested_service : str = "Build"
    entity_id : str = "GpBuilder"
    service_id : str = "Build"
    filesystem_path : str = "/some/path/"
    service_dir : str = "Build_dir"
    requesting_agent : str = ""
    has_input_files : bool = True
    u_uuid : constr(max_length=36) = " "
    notify : bool = False
    upload_path : constr(max_length=255)  = "/path/to/Build_dir"
    
    project_type : Literal['GpBuilder'] = Field(  
            'GpBuilder',
            title='Type',
            alias='type'
            )

    def add_temporary_info(self): 
        ic = InstanceConfig()
        self.project_dir : str = os.path.join(
            ic.get_filesystem_path(app="GpBuilder"), self.pUUID
        )
