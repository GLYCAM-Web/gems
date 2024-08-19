#!/usr/bin/env python3
# import from typing first, in case you want to import pydantic.typing
from pathlib import Path
from typing import Literal, Optional, Union
from pydantic import BaseModel, Field

from gemsModules.logging.logger import Set_Up_Logging

from ...main_api import Glycomimetics_Service_Request, Glycomimetics_Service_Response
from gemsModules.common.main_api_resources import Resource, Resources
from gemsModules.complex.glycomimetics.services.common_api import PDB_File_Resource

log = Set_Up_Logging(__name__)

class PM_Resource(Resource):
    pass

class PM_Input_Resource(PM_Resource):
    pass

class PM_Output_Resource(PM_Resource):
    pass

class PM_Input_Resources(Resources):
    __root__: Union[PDB_File_Resource, PM_Input_Resource, PM_Output_Resource] = Field(
        default_factory=list,
    )

class PM_Output_Resources(Resources):
    __root__: Union[PM_Input_Resource, PM_Output_Resource] = Field(
        default_factory=list,
    )

class ProjectManagement_Inputs(BaseModel):
    pUUID: Optional[str] = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    projectDir: str = Field(
        None,
        title="Output File Path",
        description="Full path to output file",
    )
    resources: Resources = Field(
        title="Resources",
        description="List of resources to copy to project directory",
        default_factory=Resources,
    )


class ProjectManagement_Outputs(BaseModel):
    resources: PM_Output_Resources = PM_Output_Resources()


# PM Requests should be based in common.Request, in my mind.
class ProjectManagement_Request(Glycomimetics_Service_Request):
    typename: str = Field("ProjectManagement", alias="type")
    # Cannot Make a PM request without inputs.
    inputs: ProjectManagement_Inputs = ProjectManagement_Inputs()


class ProjectManagement_Response(Glycomimetics_Service_Response):
    typename: str = Field("ProjectManagement", alias="type")
    outputs: ProjectManagement_Outputs = ProjectManagement_Outputs()
