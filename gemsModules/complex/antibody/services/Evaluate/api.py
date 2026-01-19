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
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Evaluate_input_Resource(Resource):
    pass


class Evaluate_output_Resource(Resource):
    pass


class Evaluate_Input_Resources(Resources):
    __root__: List[
        Union[PDB_File_Resource, Evaluate_input_Resource, Evaluate_output_Resource]
    ] = None


class Evaluate_Output_Resources(Resources):
    __root__: List[Union[Evaluate_input_Resource, Evaluate_output_Resource]] = None


class Evaluate_Inputs(BaseModel):
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

    # Evaluate's real request always needs an input PDB, should we be able to instantiate it blank?
    # resources: Evaluate_Input_Resources = Evaluate_Input_Resources()
    resources: Resources = Resources()


class Evaluate_Outputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    resources: Evaluate_Output_Resources = Evaluate_Output_Resources()


class Evaluate_Request(Antibody_Service_Request):
    typename: str = Field("Evaluate", alias="type")
    inputs: Evaluate_Inputs = Evaluate_Inputs()


class Evaluate_Response(Antibody_Service_Response):
    typename: str = Field("Evaluate", alias="type")
    outputs: Evaluate_Outputs = Evaluate_Outputs()

if __name__ == "__main__":
    # generate a blank request
    thisRequest = Evaluate_Request()
    with open("Blank_Evaluate_Request-git-ignore-me.json", "w") as f:
        f.write(thisRequest.json(indent=2))
