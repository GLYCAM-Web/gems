#!/usr/bin/env python3
import random
from pydantic import BaseModel, Field
from typing   import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.complex.GpBuilder.main_api_common import GpBuilder_Service_Request, GpBuilder_Service_Response

from gemsModules.logging.logger import Set_Up_Logging 


log = Set_Up_Logging(__name__)


class BuildService_input_Resource(Resource):
    """ Need to write validators. """
    pass

class BuildService_output_Resource(Resource):
    """ Need to write validators. """
    pass

class BuildService_Resources(Resources):
    __root__ : List[Union[BuildService_input_Resource, BuildService_output_Resource]] = Field(default_factory=list)


# TODO: To structurefile/common_api.py? 
# TODO: Needs to be Evaluate/Glycosites.
class GlycanMapping(BaseModel):
    residue: str
    sequence: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, list) and len(v) == 2:
            return cls(residue=v[0], sequence=v[1])
        return v
    

class BuildOptions(BaseModel):
    number_of_samples: Optional[int] = Field(2, ge=1, description="Number of output structures")
    persist_cycles: Optional[int] = Field(5, ge=1, description="Number of persist cycles")
    seed: Optional[int] = Field(default=random.randint(0,1e9), description="Random seed for reproducibility")
    
    
class Build_Inputs(BaseModel):
    pUUID: Optional[str] = Field(
        None,
        title="Project UUID",
        description="UUID for this GpBuilder Project, assigned automatically by GEMS",
    )
    
    protein_file: Optional[str] = Field(..., description="Path to the protein PDB file")
    glycan_mappings: List[GlycanMapping] = Field(
        ..., description="List of residue to glycan sequence mappings"
    )
    
    # TODO: Could this be generalized to an Inputs superclass? Internally we should be manipulating resources, not inputs.
    resources : Optional[BuildService_Resources] = Field(
        title='Resources',
        description='Resources for Build',
        default_factory=BuildService_Resources
    )
    
    
class Build_Outputs(BaseModel) :
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


class BuildService_Request(GpBuilder_Service_Request) :
    typename : str  = Field(
        "Build",  
        alias='type'
    )
    # the following must be redefined in a child class
    inputs: Build_Inputs = Field(
        ...,
        title='Inputs',
        description='Inputs for Build'
    )
    options: Optional[BuildOptions] = Field(
        default_factory=BuildOptions,
        title='Options',
    )


class BuildService_Response(GpBuilder_Service_Response) :
    typename : str  = Field(
        "Build",   
        alias='type'
    )
    outputs : Build_Outputs = Build_Outputs()
