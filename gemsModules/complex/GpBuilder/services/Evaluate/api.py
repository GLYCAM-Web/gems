#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing   import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.complex.GpBuilder.main_api_common import GpBuilder_Service_Request, GpBuilder_Service_Response

from gemsModules.logging.logger import Set_Up_Logging 


log = Set_Up_Logging(__name__)


class EvaluateService_input_Resource(Resource):
    """ Need to write validators. """
    pass

class EvaluateService_output_Resource(Resource):
    """ Need to write validators. """
    pass

class EvaluateService_Resources(Resources):
    __root__ : List[Union[EvaluateService_input_Resource, EvaluateService_output_Resource]] = Field(default_factory=list)

    
class EvaluateService_Inputs(BaseModel):
    pUUID: Optional[str] = Field(
        None,
        title="Project UUID",
        description="UUID for this GpBuilder Project, assigned automatically by GEMS",
    )
    projectDir: str = Field(
        None,
        title="Project Directory",
        description="Full path to the project directory",
    )
    
    protein_file: str = Field(..., description="Path to the protein PDB file")
    
    # TODO: Could this be generalized to an Inputs superclass? Internally we should be manipulating resources, not inputs.
    resources : Optional[EvaluateService_Resources] = Field(
        title='Resources',
        description='Resources for Build',
        default_factory=EvaluateService_Resources
    )
    
    
class EvaluateService_Outputs(BaseModel) :
    message : str = Field(
        "",
        title='Evaluate response',
        description='A nice message to return.',
    )
    resources : Optional[EvaluateService_Resources] = Field(
        title='Resources',
        description='Resources for Build',
        default_factory=EvaluateService_Resources
    )


class EvaluateService_Request(GpBuilder_Service_Request) :
    typename : str  = Field(
        "Build",  
        alias='type'
    )
    # the following must be redefined in a child class
    inputs: EvaluateService_Inputs = Field(
        ...,
        title='Inputs',
        description='Inputs for Build'
    )


class EvaluateService_Response(GpBuilder_Service_Response) :
    typename : str  = Field(
        "Build",   
        alias='type'
    )
    outputs : EvaluateService_Outputs = EvaluateService_Outputs()
