#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing   import List, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.{{cookiecutter.gems_module}}.main_api import {{cookiecutter.service_name}}_Service_Request, {{cookiecutter.service_name}}_Service_Response

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class {{cookiecutter.service_name}}Service_input_Resource(Resource):
    """ Need to write validators. """
    ## Works now:
    ##
    ## locationType = filepath
    ##
    ## resourceFormat = amber_parm7 | amber_rst7 | md_path | max_hours
    ##
    ## payload = string containing a /path/to/file  |  integer (number of hours)
    ##
    ## options = none currently read
    ##
    pass

class {{cookiecutter.service_name}}Service_output_Resource(Resource):
    """ Need to write validators. """
    ## Works now:
    ##
    ## locationType = filepath
    ##
    ## resourceFormat = amber_parm7 | amber_rst7 | amber_nc | amber_mdcrd | amber_mdout | zipfile
    ##
    ## payload = string containing a /path/to/file
    ##
    ## notices = these will surely happen
    ##
    pass

class {{cookiecutter.service_name}}Service_Resources(Resources):
    __root__ : List[Union[{{cookiecutter.service_name}}Service_input_Resource, {{cookiecutter.service_name}}Service_output_Resource]] = None


class {{cookiecutter.service_name}}Service_Inputs(BaseModel) :
    pUUID : str = Field(
        None,
        title='Project UUID',
        description='UUID of Project',
    )
    resources : {{cookiecutter.service_name}}Service_Resources = {{cookiecutter.service_name}}Service_Resources()
    
    
class {{cookiecutter.service_name}}Service_Outputs(BaseModel) :
    message : str = Field(
        None,
        title='{{cookiecutter.service_name}} response',
        description='A nice message to return.',
    )
    resources : {{cookiecutter.service_name}}Service_Resources = {{cookiecutter.service_name}}Service_Resources()


class {{cookiecutter.service_name}}Service_Request({{cookiecutter.service_name}}_Service_Request) :
    typename : str  = Field(
        "{{cookiecutter.service_name}}Service",   
        alias='type'
    )
    # the following must be redefined in a child class
    inputs : {{cookiecutter.service_name}}Service_Inputs = {{cookiecutter.service_name}}Service_Inputs()

class {{cookiecutter.service_name}}Service_Response({{cookiecutter.service_name}}_Service_Response) :
    typename : str  = Field(
        "{{cookiecutter.service_name}}Service",   
        alias='type'
    )
    outputs : {{cookiecutter.service_name}}Service_Outputs = {{cookiecutter.service_name}}Service_Outputs()
