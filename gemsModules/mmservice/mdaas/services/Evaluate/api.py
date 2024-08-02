#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Union, Optional

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
    pUUID: Optional[str] = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    projectDir: Optional[str] = Field(
        None,
        title="Project Directory",
        description="Full path to project directory",
    )
    resources: Resources = Field(
        title="Resources",
        description="List of resources to copy to project directory",
        default_factory=Resources,
    )
    protocolFilesPath: Optional[str] = Field(
        None,
        title="Protocol Files Path",
        description="Full path to protocol files directory",
    )
    outputDirPath: Optional[str] = Field(
        None,
        title="Output Directory Path",
        description="Full path to output directory",
    )
    sim_length: Optional[str] = Field(
        None,
        title="Simulation Length",
        description="Length of simulation in ns",
    )

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
