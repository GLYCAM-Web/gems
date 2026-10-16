#!/usr/bin/env python3
from pydantic import BaseModel, Field, root_validator
from typing import List, Optional, Union

from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.common.code_utils import GemsStrEnum
from gemsModules.common.main_api_notices import Notices

from gemsModules.complex.antibody.main_api_common import (
    Antibody_Service_Request,
    Antibody_Service_Response,
)
from gemsModules.complex.antibody.services.common_api import (
    PDB_File_Resource,
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
    projectDir: Optional[str] = Field(
        None,
        title="Project Directory",
        description="Full path to project directory",
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
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    resources: Build_Output_Resources = Build_Output_Resources()

# Note: check that the numbers correspond as needed for pydantic and for AbD
class Build_Flexibilities(GemsStrEnum):
    rigid = "rigid"
    partial = "partial"
    flexible = "flexible"


class Build_Options(BaseModel):
    flexibility: Build_Flexibilities = Field(
        Build_Flexibilities.partial,
        description="How much of the ligand should be flexible?",
        alias="Glycan_Flexibility",
    )
    count: int = Field(
        5,
        description="How many replicas/experiments to perform.",
        alias="Number_of_Replicas",
    )

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def normalize_keys(cls, values):
        if isinstance(values, dict):
            if "flexibility" in values and "Glycan_Flexibility" not in values:
                values["Glycan_Flexibility"] = values["flexibility"]
            if "count" in values and "Number_of_Replicas" not in values:
                values["Number_of_Replicas"] = values["count"]
            # Convert string counts to int if needed
            num_rep = values.get("Number_of_Replicas")
            if isinstance(num_rep, str) and num_rep.isdigit():
                values["Number_of_Replicas"] = int(num_rep)
            # Normalize flexibility value (e.g. Rigid -> rigid)
            flex_val = values.get("Glycan_Flexibility")
            if isinstance(flex_val, str):
                values["Glycan_Flexibility"] = flex_val.lower()
        return values


class Build_Request(Antibody_Service_Request):
    typename: str = Field("Build", alias="type")
    inputs: Build_Inputs = Build_Inputs()
    options: Optional[Union[Build_Options, dict]] = None


class Build_Response(Antibody_Service_Response):
    typename: str = Field("Build", alias="type")
    outputs: Build_Outputs = Build_Outputs()

if __name__ == "__main__":
    # generate a blank request
    thisRequest = Build_Request()
    with open("Blank_Build_Request-git-ignore-me.json", "w") as f:
        f.write(thisRequest.json(indent=2))
