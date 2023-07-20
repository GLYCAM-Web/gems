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


class AmberMDPrep_input_Resource(Resource):
    """Need to write validators."""

    ## Works now:
    ##
    ## locationType = filepath
    ##
    ## resourceFormat = amber_parm7 | amber_rst7 | md_path | max_hours
    ##
    ## payload = string containing a /path/to/file  |  integer (number of hours)
    ##
    ## options = none currently read
    ##
    pass


class AmberMDPrep_output_Resource(Resource):
    """Need to write validators."""

    ## Works now:
    ##
    ## locationType = filepath
    ##
    ## resourceFormat = amber_parm7 | amber_rst7 | amber_nc | amber_mdcrd | amber_mdout | zipfile
    ##
    ## payload = string containing a /path/to/file
    ##
    ## notices = these will surely happen
    ##
    pass


class AmberMDPrep_Resources(Resources):
    __root__: list[
        Union[AmberMDPrep_input_Resource, AmberMDPrep_output_Resource]
    ] = None


class AmberMDPrep_Inputs(BaseModel):
    pdb_file: str = Field(
        # Note: This should be a required field, but the way Request instantiates an empty Inputs disallows this.
        ...,
        title="Amber Parm7",
        description="Name of Amber PDB file",
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
        title="Output Directory Path",
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
        title="Output Directory Path",
        description="Path to output directory",
    )
    resources: AmberMDPrep_Resources = AmberMDPrep_Resources()


class AmberMDPrep_Request(PDBFile_Service_Request):
    typename: str = Field("AmberMDPrep", alias="type")
    # the following must be redefined in a child class
    inputs: AmberMDPrep_Inputs = None


class AmberMDPrep_Response(PDBFile_Service_Response):
    typename: str = Field("AmberMDPrep", alias="type")
    outputs: AmberMDPrep_Outputs = AmberMDPrep_Outputs()
