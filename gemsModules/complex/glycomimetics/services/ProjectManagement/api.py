#!/usr/bin/env python3
# import from typing first, in case you want to import pydantic.typing
from pathlib import Path
from typing_extensions import Literal, Optional
from pydantic import BaseModel, Field

from gemsModules.logging.logger import Set_Up_Logging

from gemsModules.complex.glycomimetics.main_api import (
    Glycomimetics_Service_Request,
    Glycomimetics_Service_Response,
)

from gemsModules.complex.glycomimetics.services.ProjectManagement.resources import (
    ProjectManagement_Resources,
    PM_Resource,
)


log = Set_Up_Logging(__name__)


class ProjectManagement_Inputs(BaseModel):
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
    resources: list[PM_Resource] = Field(
        title="Resources",
        description="List of resources to copy to project directory",
        default_factory=list,
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
    inputFilesPath: Optional[str] = Field(
        None,
        title="Input Files Path",
        description="Full path to input files directory",
    )
    amber_parm7: Optional[str] = Field(
        None,
        title="Amber Parm7",
        description="Name of Amber Parm7 file",
    )
    amber_rst7: Optional[str] = Field(
        None,
        title="Amber Rst7",
        description="Name of Amber Rst7 file",
    )
    sim_length: Optional[str] = Field(
        None,
        title="Simulation Length",
        description="Length of simulation in ns",
    )


class ProjectManagement_Outputs(BaseModel):
    outputDirPath: str = Field(
        None,
        title="Output File Path",
        description="Full path to output file",
    )
    resources: ProjectManagement_Resources = ProjectManagement_Resources()


# PM Requests should be based in common.Request, in my mind.
class ProjectManagement_Request(Glycomimetics_Service_Request):
    typename: str = Field("ProjectManagement", alias="type")
    # Cannot Make a PM request without inputs.
    inputs: ProjectManagement_Inputs = ProjectManagement_Inputs()


class ProjectManagement_Response(Glycomimetics_Service_Response):
    typename: str = Field("ProjectManagement", alias="type")
    outputs: ProjectManagement_Outputs = ProjectManagement_Outputs()
