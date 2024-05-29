#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Union

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.complex.glycomimetics.main_api import (
    Glycomimetics_Service_Request,
    Glycomimetics_Service_Response,
)
from gemsModules.complex.glycomimetics.services.common_api import (
        PDB_File_Resource, 
        Moiety_Library_Names,
        Position_Modification_Options,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Evaluate_input_Resource(Resource):
    """Need to write validators."""

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


class Evaluate_output_Resource(Resource):
    """Need to write validators."""

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


class Evaluate_Input_Resources(Resources):
    __root__: List[Union[
        PDB_File_Resource,
        Evaluate_input_Resource, 
        Evaluate_output_Resource
        ]] = None

class Evaluate_Output_Resources(Resources):
    __root__: List[Union[
        Evaluate_input_Resource, 
        Evaluate_output_Resource
        ]] = None


class Evaluate_Inputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    
    resources: Evaluate_Input_Resources = Evaluate_Input_Resources()


class Evaluate_Outputs(BaseModel):
    Available_Libraries : List[str] = Moiety_Library_Names.get_json_list()  # might need syntax adjustment
    Available_Modification_Options : Position_Modification_Options = None
    outputDirPath: str = Field(
        None,
        title="Output Directory Path",
        description="Path to output directory",
    )
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    resources: Evaluate_Output_Resources = Evaluate_Output_Resources()


class Evaluate_Request(Glycomimetics_Service_Request):
    typename: str = Field("Evaluate", alias="type")
    # the following must be redefined in a child class
    inputs: Evaluate_Inputs = Evaluate_Inputs()


class Evaluate_Response(Glycomimetics_Service_Response):
    typename: str = Field("Evaluate", alias="type")
    outputs: Evaluate_Outputs = Evaluate_Outputs()
