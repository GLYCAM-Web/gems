#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.mmservice.mdaas.main_api import (
    MDaaS_Service_Request,
    MDaaS_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

class PDBResource(Resource):
    resourceFormat = "PDB"

class InputPDBResource(Resource):
    resourceRole = "Input"

class Evaluate_Inputs(BaseModel):
    resources: list[PDBResource]


class Evaluate_Outputs(BaseModel):
    outputDirPath: str = Field(
        None,
        title="Output Directory Path",
        description="Path to output directory",
    )
    resources: Resources = Resources()


class Evaluate_Request(MDaaS_Service_Request):
    typename: str = Field("RunMD", alias="type")
    # the following must be redefined in a child class
    inputs: Evaluate_Inputs = Evaluate_Inputs()


class Evaluate_Response(MDaaS_Service_Response):
    typename: str = Field("RunMD", alias="type")
    outputs: Evaluate_Outputs = Evaluate_Outputs()
