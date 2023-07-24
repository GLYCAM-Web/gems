#!/usr/bin/env python3
# import from typing first, in case you want to import pydantic.typing
from typing import Optional, Union
from pydantic import BaseModel, Field
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
    pdb_file: str = Field(
        # Note: This should be a required field, but the way Request instantiates an empty Inputs disallows this.
        ...,
        title="PDB File",
        description="Name of PDB file to preprocess.",
    )
    outputFileName: Optional[str] = Field(
        None,
        title="Output file name",
        description="Name of output file",
    )
    pUUID: Optional[str] = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    outputFilePath: Optional[str] = Field(
        None,  # "/website/TESTS/ambermdprep/ambermdprep_test_files/output_dir",
        title="Output File Path",
        description="Path to output directory",
    )

    inputFilePath: Optional[str] = Field(
        None,  # "/website/TESTS/ambermdprep/test_files",
        title="Input Files Directory Path",
        description="Path to whhere the input files are stored",
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
    # the following must be redefined in a child class
    inputs: ProjectManagement_Inputs = None


class ProjectManagement_Response(PDBFile_Service_Response):
    typename: str = Field("ProjectManagement", alias="type")
    outputs: ProjectManagement_Outputs = ProjectManagement_Outputs()
