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


class AmberMDPrep_input_Resource(Resource):
    """Need to write validators."""

    pass


class AmberMDPrep_output_Resource(Resource):
    """Need to write validators."""

    pass


class AmberMDPrep_Resources(Resources):
    __root__: list[
        Union[AmberMDPrep_input_Resource, AmberMDPrep_output_Resource]
    ] = None


class AmberMDPrep_Inputs(BaseModel):
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


class AmberMDPrep_Outputs(BaseModel):
    ppinfo: str = Field(
        None,
        title="Preprocessing Information",
        description="AmberMDPrep's preprocessing information",
    )
    outputFilePath: str = Field(
        None,
        title="Output File Path",
        description="Full path to output file",
    )
    resources: AmberMDPrep_Resources = AmberMDPrep_Resources()


class AmberMDPrep_Request(PDBFile_Service_Request):
    typename: str = Field("AmberMDPrep", alias="type")
    # the following must be redefined in a child class
    inputs: AmberMDPrep_Inputs = None


class AmberMDPrep_Response(PDBFile_Service_Response):
    typename: str = Field("AmberMDPrep", alias="type")
    outputs: AmberMDPrep_Outputs = AmberMDPrep_Outputs()
