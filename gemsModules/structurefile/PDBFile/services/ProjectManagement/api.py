#!/usr/bin/env python3
# import from typing first, in case you want to import pydantic.typing
from pathlib import Path
from typing import Literal, Optional
from pydantic import BaseModel, Field

from gemsModules.common.main_api_resources import Resources

from gemsModules.structurefile.PDBFile.main_api import (
    PDBFile_Service_Request,
    PDBFile_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging


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
    resources: Resources = Field(
        title="Resources",
        description="List of resources to copy to project directory",
        default_factory=Resources,
    )


class ProjectManagement_Outputs(BaseModel):
    outputFilePath: str = Field(
        None,
        title="Output File Path",
        description="Full path to output file",
    )
    resources: Resources = Field(
        title="Resources",
        description="List of resources to copy to project directory",
        default_factory=Resources,
    )


class ProjectManagement_Request(PDBFile_Service_Request):
    typename: str = Field("ProjectManagement", alias="type")
    # Cannot Make a PM request without inputs.
    inputs: ProjectManagement_Inputs = ProjectManagement_Inputs()


class ProjectManagement_Response(PDBFile_Service_Response):
    typename: str = Field("ProjectManagement", alias="type")
    outputs: ProjectManagement_Outputs = ProjectManagement_Outputs()
