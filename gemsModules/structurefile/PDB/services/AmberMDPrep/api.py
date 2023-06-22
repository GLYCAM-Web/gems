#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.structurefile.PDB.main_api import (
    AmberMDPrep_Service_Request,
    AmberMDPrep_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class prepare_pdb_input_Resource(Resource):
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


class prepare_pdb_output_Resource(Resource):
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


class prepare_pdb_Resources(Resources):
    __root__: List[
        Union[prepare_pdb_input_Resource, prepare_pdb_output_Resource]
    ] = None


class prepare_pdb_Inputs(BaseModel):
    pdb_file: str = Field(
        None,
        title="Amber Parm7",
        description="Name of Amber PDB file",
    )

    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    outputDirPath: str = Field(
        "/website/TESTS/ambermdprep/ambermdprep_test_files/output_dir",
        title="Output Directory Path",
        description="Path to output directory",
    )
    inputFilesPath: str = Field(
        "/website/TESTS/ambermdprep/test_files",
        title="Input Files Directory Path",
        description="Path to whhere the input files are stored",
    )
    use_serial: bool = Field(
        False,
        title="Use Serial",
        description="Should we force the GEMS code to run in serial?",
    )
    resources: Resources = Resources()


class prepare_pdb_Outputs(BaseModel):
    message: str = Field(
        None,
        title="Message",
        description="Message from the service",
    )
    outputDirPath: str = Field(
        None,
        title="Output Directory Path",
        description="Path to output directory",
    )
    resources: prepare_pdb_Resources = prepare_pdb_Resources()


class prepare_pdb_Request(AmberMDPrep_Service_Request):
    typename: str = Field("AmberMDPrep", alias="type")
    # the following must be redefined in a child class
    inputs: prepare_pdb_Inputs = prepare_pdb_Inputs()


class prepare_pdb_Response(AmberMDPrep_Service_Response):
    typename: str = Field("AmberMDPrep", alias="type")
    outputs: prepare_pdb_Outputs = prepare_pdb_Outputs()
