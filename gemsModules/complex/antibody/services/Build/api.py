#!/usr/bin/env python3
from pydantic import BaseModel, Field, root_validator
from typing import List, Optional, Union

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.common.code_utils import GemsStrEnum
from gemsModules.common.main_api_notices import Notices

from gemsModules.complex.antibody.main_api import (
    Antibody_Service_Request,
    Antibody_Service_Response,
)
from gemsModules.complex.antibody.services.common_api import (
    PDB_File_Resource,
    Moiety_Library_Names,
    Position_Modification_Options,
    Modification_Position,  # TODO: We really should be using Position_Modification_Options, temp integration
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Build_input_Resource(Resource):
    pass


class Build_output_Resource(Resource):
    pass


class Build_Input_Resources(Resources):
    __root__: List[
        Union[PDB_File_Resource, Build_input_Resource, Build_output_Resource]
    ] = None


class Build_Output_Resources(Resources):
    __root__: List[Union[Build_input_Resource, Build_output_Resource]] = None


class Build_Inputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )

    # TODO: make sure to update resources with this payload if provided this way
    antibody_path: Optional[str] = Field(
        None,
        title="Antibody Path",
        description="Antibody PDB file",
    )
    ligand_path: Optional[str] = Field(
        None,
        title="Ligand Path",
        description="Ligand PDB file",
    )

    # Build's real request always needs an input PDB, should we be able to instantiate it blank?
    # resources: Build_Input_Resources = Build_Input_Resources()
    resources: Resources = Resources()


class Build_Outputs(BaseModel):
    # TODO/Q: Should this be here?
    Available_Libraries: List[str] = Field(
        default_factory=Moiety_Library_Names.get_json_list,
        title="Available Libraries",
        description="List of available libraries",
    )
    Condensed_Sequence: Optional[str] = Field(
        None,
        title="Condensed Sequence",
        description="GLYCAM condensed sequence representing the ligand in the protein co-complex",
    )
    Available_Modification_Options: Optional[List[Modification_Position]] = Field(
        default_factory=list,
        title="Available Modification Options",
        description="List of available modification options",
    )
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
    resources: Build_Output_Resources = Build_Output_Resources()


class Build_Request(Antibody_Service_Request):
    typename: str = Field("Build", alias="type")
    inputs: Build_Inputs = Build_Inputs()


class Build_Response(Antibody_Service_Response):
    typename: str = Field("Build", alias="type")
    outputs: Build_Outputs = Build_Outputs()

if __name__ == "__main__":
    # generate a blank request
    thisRequest = Build_Request()
    with open("Blank_Build_Request-git-ignore-me.json", "w") as f:
        f.write(thisRequest.json(indent=2))
