#!/usr/bin/env python3
from pydantic import constr, Field
from pydantic.typing import Literal as pyLiteral

from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class TemplateProject(Project):
    """ Template project for making new entities. """
    title : str = "Teplate project"
    parent_entity : str = ""
    app : str = "template"
    requested_service : str = "template"
    entity_id : str = "Template"
    service_id : str = "TemplateService"
    filesystem_path : str = "/some/path/"
    service_dir : str = "template_dir"
    requesting_agent : str = "templater"
    has_input_files : bool = True
    u_uuid : constr(max_length=36) = " "
    notify : bool = False
    upload_path : constr(max_length=255)  = "/path/to/template_dir"
    
    project_type : pyLiteral['template'] = Field(  
            'template',
            title='Type',
            alias='type'
            )

