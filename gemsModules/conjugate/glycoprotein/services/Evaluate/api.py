#!/usr/bin/env python3
from pydantic import BaseModel, Field, validator
from typing   import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.conjugate.glycoprotein.main_api_common import GlycoProtein_Service_Request, GpBuilder_Service_Response

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


class Evaluate_Options(BaseModel):
    """ Options for the Evaluate service. """
    pass


class Evaluate_Inputs(BaseModel):
    pUUID: Optional[str] = Field(
        None,
        title="Project UUID",
        description="UUID for this GlycoProtein Project, assigned automatically by GEMS",
    )
    
    protein_file: Optional[str] = Field(None, description="Path to the protein PDB file")
    rcsb_id: Optional[str] = Field(
        None,
        title="RCSB ID",
        description="RCSB ID to sideload the protein structure",
    )
    
    # TODO: Could this be generalized to an Inputs superclass? Internally we should be manipulating resources, not inputs.
    resources : Optional[EvaluateService_Resources] = Field(
        title='Resources',
        description='Resources for Build',
        default_factory=EvaluateService_Resources
    )

    
# TODO: Belongs in main_api_common.py 
class Glycosite(BaseModel):
    """ Represents a glycosylation site in a protein structure. """
    Chain: str = Field(..., description="Chain identifier")
    ResidueNumber: str = Field(..., description="Residue number in the chain")
    InsertionCode: str = Field("", description="Insertion code, if any")
    SequenceContext: str = Field(..., description="Sequence context around the glycosylation site")
    Tags: str = Field("", description="Tags associated with the glycosylation site")
    
    
class Evaluate_Outputs(BaseModel) :
    csv_path: str = Field(
        None,
        title="CSV Path",
        description="CSV Data with possible glycosylation sites",
    )
    glycosites: List[Glycosite] = Field(
        default_factory=list,
        title="Glycosites",
        description="Possible sites for glycosylation"
    )
    resources : Optional[EvaluateService_Resources] = Field(
        title='Resources',
        description='Resources for Build',
        default_factory=EvaluateService_Resources
    )


class EvaluateService_Request(GlycoProtein_Service_Request) :
    typename : str  = Field(
        "Evaluate",  
        alias='type'
    )
    # the following must be redefined in a child class
    inputs: Evaluate_Inputs = Field(
        ...,
        title='Inputs',
        description='Inputs for Build'
    )


class EvaluateService_Response(GlycoProtein_Service_Response) :
    typename : str  = Field(
        "Evaluate",   
        alias='type'
    )
    outputs : Evaluate_Outputs = Evaluate_Outputs()
