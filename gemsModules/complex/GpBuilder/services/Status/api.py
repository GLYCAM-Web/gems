#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing   import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.complex.GpBuilder.main_api_common import GpBuilder_Service_Request, GpBuilder_Service_Response

from gemsModules.logging.logger import Set_Up_Logging 


log = Set_Up_Logging(__name__)


class StatusService_input_Resource(Resource):
    """ Need to write validators. """
    pass

class StatusService_output_Resource(Resource):
    """ Need to write validators. """
    pass

class StatusService_Resources(Resources):
    __root__ : List[Union[StatusService_input_Resource, StatusService_output_Resource]] = Field(default_factory=list)


class Status_Options(BaseModel):
    """ Options for the Status service. """
    pass


class Status_Inputs(BaseModel):
    pUUID: Optional[str] = Field(
        None,
        title="Project UUID",
        description="UUID for this GpBuilder Project, assigned automatically by GEMS",
    )
    

class Status_Outputs(BaseModel):
    status: str = Field("")


class StatusService_Request(GpBuilder_Service_Request) :
    typename : str  = Field(
        "Status",  
        alias='type'
    )
    # the following must be redefined in a child class
    inputs: Status_Inputs = Field(
        ...,
        title='Inputs',
        description='Inputs for Build'
    )


class StatusService_Response(GpBuilder_Service_Response) :
    typename : str  = Field(
        "Status",   
        alias='type'
    )
    outputs : Status_Outputs = Status_Outputs()
