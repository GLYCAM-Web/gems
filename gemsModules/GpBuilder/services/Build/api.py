#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing   import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.GpBuilder.main_api_common import Gpbuilder_Service_Request, GpBuilder_Service_Response

from gemsModules.logging.logger import Set_Up_Logging 


log = Set_Up_Logging(__name__)


class BuildService_input_Resource(Resource):
    """ Need to write validators. """
    pass

class BuildService_output_Resource(Resource):
    """ Need to write validators. """
    pass

class BuildService_Resources(Resources):
    __root__ : List[Union[BuildService_input_Resource, BuildService_output_Resource]] = None


class BuildService_Inputs(BaseModel) :
    pUUID : str = Field(
        None,
        title='Project UUID',
        description='UUID of Project',
    )
    resources : Optional[BuildService_Resources] = Field(
        title='Resources',
        description='Resources for Build',
        default_factory=BuildService_Resources
    )
    
    
class BuildService_Outputs(BaseModel) :
    message : str = Field(
        "",
        title='Build response',
        description='A nice message to return.',
    )
    resources : Optional[BuildService_Resources] = Field(
        title='Resources',
        description='Resources for Build',
        default_factory=BuildService_Resources
    )


class BuildService_Request(Gpbuilder_Service_Request) :
    typename : str  = Field(
        "Build",   
        alias='type'
    )
    # the following must be redefined in a child class
    inputs : BuildService_Inputs = BuildService_Inputs()

class BuildService_Response(GpBuilder_Service_Response) :
    typename : str  = Field(
        "Build",   
        alias='type'
    )
    outputs : BuildService_Outputs = BuildService_Outputs()
