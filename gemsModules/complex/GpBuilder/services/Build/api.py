#!/usr/bin/env python3
import random
from pydantic import BaseModel, Field
from typing   import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.complex.GpBuilder.main_api_common import GpBuilder_Service_Request, GpBuilder_Service_Response
from gemsModules.complex.GpBuilder.services.Evaluate.api import Glycosite

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
    Chain: str
    ResidueNumber: str
    Sequence: str
    SequenceContext: Optional[str] = Field("", description="Sequence context around the glycan mapping, if given")
    InsertionCode: Optional[str] = Field("", description="Insertion code, if any")
    Tags: Optional[str] = Field("", description="Tags associated with the glycan mapping, if given")
    
UINT64_MAX = 2**64 - 1 # sys.maxsize is platform-dependent, so we use a fixed value for UINT64_MAX
class BuildOptions(BaseModel):
    number_of_samples: Optional[int] = Field(
        1, ge=0, description="Number of structure samples to create in addition to the default structure"
    )
    persist_cycles: Optional[int] = Field(
        5, ge=1, description="How long the algorithm persists in looking for a solution with a lower number of overlaps"
    )
    rng_seed: Optional[int] = Field(
        default_factory=lambda: random.randint(0, UINT64_MAX),  # Use a random seed by default
        ge=0, le=UINT64_MAX,
        description="Random number generator seed for reproducibility"
    )
    overlap_rejection_threshold: Optional[float] = Field(
        0.0, ge=0.0, description="LJ repulsive potential threshold for glycan atoms; samples exceeding this are rejected"
    )
    prepare_for_md: Optional[bool] = Field(
        False, 
        description="Prepare for MD simulation (creates OFF files for each output structure)"
    )
    use_initial_glycosite_residue_conformation: Optional[bool] = Field(
        False, description="Preserve chi1 and chi2 angles of protein-glycan linkages according to their initial shape"
    )
    move_overlapping_sidechains: Optional[bool] = Field(
        False, description="Adjust protein sidechains if it reduces glycan overlap or increases glycan shape range"
    )
    delete_unresolvable_glycosites: Optional[bool] = Field(
        False, description="Delete glycans in samples exceeding overlap threshold to produce structures with no overlaps"
    )
    
    
class Build_Inputs(BaseModel):
    pUUID: Optional[str] = Field(
        None,
        title="Project UUID",
        description="UUID for this GpBuilder Project, assigned automatically by GEMS",
    )
    
    protein_file: Optional[str] = Field("", description="Path to the protein PDB file")
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
    outputs : Build_Outputs = Field(default_factory=Build_Outputs, title='Outputs')
