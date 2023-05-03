#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing   import List, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.TEMPLATE.main_api import Template_Service_Request, Template_Service_Response

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

class template_service_input_Resource(Resource):
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

class template_service_output_Resource(Resource):
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

class template_service_Resources(Resources):
    __root__ : List[Union[template_service_input_Resource, template_service_output_Resource]] = None


class template_service_Inputs(BaseModel) :
    pUUID : str = Field(
        None,
        title='Project UUID',
        description='UUID of Project',
    )
    resources : template_service_Resources = template_service_Resources()
    
    
class template_service_Outputs(BaseModel) :
    message : str = Field(
        None,
        title='Template response',
        description='A nice message to return.',
    )
    resources : template_service_Resources = template_service_Resources()


class template_service_Request(Template_Service_Request) :
    typename : str  = Field(
        "TemplateService",   
        alias='type'
    )
    # the following must be redefined in a child class
    inputs : template_service_Inputs = template_service_Inputs()

class template_service_Response(Template_Service_Response) :
    typename : str  = Field(
        "TemplateService",   
        alias='type'
    )
    outputs : template_service_Outputs = template_service_Outputs()
