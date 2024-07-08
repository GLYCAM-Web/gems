#!/usr/bin/env python3
from pydantic import BaseModel, Field, root_validator
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

    # Evaluate's real request always needs an input PDB, should we be able to instantiate it blank?
    resources: Evaluate_Input_Resources = Evaluate_Input_Resources()


class Evaluate_Outputs(BaseModel):
    Available_Libraries: List[str] = (
        Moiety_Library_Names.get_json_list()
    )  # might need syntax adjustment
    Available_Modification_Options: Position_Modification_Options = None
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
    inputs: Evaluate_Inputs = Evaluate_Inputs()


class Evaluate_Response(Glycomimetics_Service_Response):
    typename: str = Field("Evaluate", alias="type")
    outputs: Evaluate_Outputs = Evaluate_Outputs()


if __name__ == "__main__":
    # generate a blank request
    thisRequest = Evaluate_Request()
    with open("Blank_Evaluate_Request.json", "w") as f:
        f.write(thisRequest.json(indent=2))
