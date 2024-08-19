#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Union, Optional

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.mmservice.mdaas.main_api_common import (
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
    protocolFilesPath: Optional[str] = Field(
        None,
        title="Protocol Files Path",
        description="Full path to protocol files directory",
    )
    sim_length: Optional[str] = Field(
        None,
        title="Simulation Length",
        description="Length of simulation in ns",
    )
    
    resources: Resources = Field(
        title="Resources",
        description="List of resources to copy to project directory",
        default_factory=Resources,
    )

class Evaluate_Outputs(BaseModel):
    timeEstimateHours: Optional[float] = Field(
        None,
        title="Time Estimate Hours",
        description="Estimated time to run in hours",
    )
    
    resources: Resources = Field(
        title="Resources",
        description="List of resources to copy to project directory",
        default_factory=Resources,
    )


class Evaluate_Request(MDaaS_Service_Request):
    typename: str = Field("Evaluate", alias="type")
    # the following must be redefined in a child class
    inputs: Evaluate_Inputs = Evaluate_Inputs()


class Evaluate_Response(MDaaS_Service_Response):
    typename: str = Field("Evaluate", alias="type")
    outputs: Evaluate_Outputs = Evaluate_Outputs()
