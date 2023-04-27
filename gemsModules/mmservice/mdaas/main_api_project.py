#!/usr/bin/env python3
from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class MdProject(Project):
    system_phase : constr(max_length=25) = "In solvent"
    input_type : constr(max_length=25) = "Amber-prmtop & inpcrd"
    prmtop_file_name : constr(max_length=255) = " "
    inpcrd_file_name : constr(max_length=255) = " "
    u_uuid : constr(max_length=36) = " "
    sim_length : constr(max_length=5) = '100'
    notify : bool =True
    upload_path : constr(max_length=255)  = " "
    
    project_type : Literal['md'] = Field(  
            'md',
            title='Type',
            alias='type'
            )

