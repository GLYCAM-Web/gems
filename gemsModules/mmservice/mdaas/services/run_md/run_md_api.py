#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Optional, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.mmservice.mdaas.main_api_common import (
    MDaaS_Service_Request,
    MDaaS_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class run_md_Inputs(BaseModel):
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
    protocolFilesPath: str = Field(
        None,
        title="Protocol files directory",
        description="Path to where the protocol files are stored",
    )
    control_script: str = Field(
        "Run_Protocol.bash",
        title="Control Script",
        description="Name of the script used to run the protocol",
    )
    
    # Explicit inputs; copied to resources for internal use.
    parameter_topology_file: str = Field(
        None,
        alias="parameter-topology-file",
    )
    input_coordinate_file: str = Field(
        None,
        alias="input-coordinate-file",
    )
    unminimized_gas_file: str = Field(
        None,
        alias="unminimized-gas-file",
    )
    
    # Options
    sim_length: Optional[str] = Field(
        None,
        title="Simulation Length",
        description="Length of simulation in ns",
    )
    use_serial: bool = Field(
        False,
        title="Use Serial",
        description="Should we force the GEMS code to run in serial?",
    )
    
    resources: Resources = Field(
        title="Resources",
        description="List of input resources",
        default_factory=Resources,
    )
    
    
class run_md_Outputs(BaseModel):
    projectDir: str = Field(
        None,
        title="Output Directory Path",
        description="Path to output directory",
    )
    resources: Resources = Field(
        title="Resources",
        description="List of resources to copy to project directory",
        default_factory=Resources,
    )

class run_md_Request(MDaaS_Service_Request):
    typename: str = Field("RunMD", alias="type")
    # the following must be redefined in a child class
    inputs: run_md_Inputs = run_md_Inputs()


class run_md_Response(MDaaS_Service_Response):
    typename: str = Field("RunMD", alias="type")
    outputs: run_md_Outputs = run_md_Outputs()
