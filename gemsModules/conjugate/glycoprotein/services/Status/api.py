#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing   import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.conjugate.glycoprotein.main_api_common import GlycoProtein_Service_Request, GpBuilder_Service_Response

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
        description="UUID for this GlycoProtein Project, assigned automatically by GEMS",
    )
    projectDir: Optional[str] = Field(
        None,
        title="Project Directory",
        description="Directory where the GlycoProtein project is located (auto-filled)",
    )
    

class Status_Outputs(BaseModel):
    status: str = Field("")


class StatusService_Request(GlycoProtein_Service_Request) :
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


class StatusService_Response(GlycoProtein_Service_Response) :
    typename : str  = Field(
        "Status",   
        alias='type'
    )
    outputs : Status_Outputs = Status_Outputs()
