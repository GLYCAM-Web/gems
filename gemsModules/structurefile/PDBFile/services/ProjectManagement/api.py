#!/usr/bin/env python3
# import from typing first, in case you want to import pydantic.typing
from pathlib import Path
from typing_extensions import Literal, Optional
from pydantic import BaseModel, Field

from gemsModules.logging.logger import Set_Up_Logging

from gemsModules.structurefile.PDBFile.main_api import (
    PDBFile_Service_Request,
    PDBFile_Service_Response,
)
from gemsModules.structurefile.PDBFile.services.ProjectManagement.resources import (
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


class ProjectManagement_Outputs(BaseModel):
    outputFilePath: str = Field(
        None,
        title="Output File Path",
        description="Full path to output file",
    )
    resources: ProjectManagement_Resources = ProjectManagement_Resources()


class ProjectManagement_Request(PDBFile_Service_Request):
    typename: str = Field("ProjectManagement", alias="type")
    # Cannot Make a PM request without inputs.
    inputs: ProjectManagement_Inputs = ProjectManagement_Inputs()


class ProjectManagement_Response(PDBFile_Service_Response):
    typename: str = Field("ProjectManagement", alias="type")
    outputs: ProjectManagement_Outputs = ProjectManagement_Outputs()
