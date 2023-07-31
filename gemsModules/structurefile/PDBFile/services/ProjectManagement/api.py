#!/usr/bin/env python3
# import from typing first, in case you want to import pydantic.typing
from typing import Optional, Union
import uuid
from pydantic import BaseModel, Field
from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.structurefile.PDBFile.main_api import (
    PDBFile_Service_Request,
    PDBFile_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class ProjectManagement_input_Resource(Resource):
    """Need to write validators."""

    pass


class ProjectManagement_output_Resource(Resource):
    """Need to write validators."""

    pass


class ProjectManagement_Resources(Resources):
    __root__: list[
        Union[ProjectManagement_input_Resource, ProjectManagement_output_Resource]
    ] = None


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
    use_serial: bool = Field(
        False,
        title="Use Serial",
        description="Should we force the GEMS code to run in serial?",
    )
    resources: Resources = Resources()


class ProjectManagement_Outputs(BaseModel):
    ppinfo: str = Field(
        None,
        title="Preprocessing Information",
        description="ProjectManagement's preprocessing information",
    )
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


class ProjectManagement_AAOP(AAOP):
    def __init__(self, name=None, request=True):
        if name is None:
            name = "ProjectManagement"
        if request:
            name = f"{name}_Request"
        else:
            name = f"{name}_Response"

        if request:
            aao = ProjectManagement_Request()
        else:
            aao = ProjectManagement_Response()

        super().__init__(
            AAO_Type="ProjectManagement",
            The_AAO=aao,
            ID_String=uuid.uuid4(),
            Dictionary_Name=name,
        )
