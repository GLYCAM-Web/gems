#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing   import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.batchcompute.main_api_common import Batchcompute_Service_Request, Batchcompute_Service_Response

from gemsModules.logging.logger import Set_Up_Logging 


log = Set_Up_Logging(__name__)


class SubmitJobService_input_Resource(Resource):
    """ Need to write validators. """
    pass

class SubmitJobService_output_Resource(Resource):
    """ Need to write validators. """
    pass

class SubmitJobService_Resources(Resources):
    __root__ : List[Union[SubmitJobService_input_Resource, SubmitJobService_output_Resource]] = None


class SubmitJobService_Inputs(BaseModel) :
    pUUID : Optional[str] = Field(
        None,
        title='Project UUID',
        description='UUID of Project',
    )
    context: Optional[str] = Field(None, title='Context')
    workingDirectory: Optional[str] = Field(None, title='Working Directory')
    sbatchArgument: Optional[str] = Field(None, title='Sbatch Argument')
    name: Optional[str] = Field(None, title='Job Name')
    partition: Optional[str] = Field(None, title='Partition')
    user: Optional[str] = Field(None, title='User')
    resources : Optional[SubmitJobService_Resources] = Field(
        title='Resources',
        description='Resources for SubmitJob',
        default_factory=SubmitJobService_Resources
    )

    class Config:
        extra = "allow"
    
    
class SubmitJobService_Outputs(BaseModel) :
    message : str = Field(
        "",
        title='SubmitJob response',
        description='A nice message to return.',
    )
    resources : Optional[SubmitJobService_Resources] = Field(
        title='Resources',
        description='Resources for SubmitJob',
        default_factory=SubmitJobService_Resources
    )


class SubmitJobService_Request(Batchcompute_Service_Request) :
    typename : str  = Field(
        "SubmitJob",   
        alias='type'
    )
    # the following must be redefined in a child class
    inputs : SubmitJobService_Inputs = SubmitJobService_Inputs()

class SubmitJobService_Response(Batchcompute_Service_Response) :
    typename : str  = Field(
        "SubmitJob",   
        alias='type'
    )
    outputs : SubmitJobService_Outputs = SubmitJobService_Outputs()
