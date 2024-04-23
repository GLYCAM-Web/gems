#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.complex.glycomimetics.main_api import (
    Glycomimetics_Service_Request,
    Glycomimetics_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Analyze_input_Resource(Resource):
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


class Analyze_output_Resource(Resource):
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


class Analyze_Resources(Resources):
    __root__: List[Union[Analyze_input_Resource, Analyze_output_Resource]] = None


class Analyze_Inputs(BaseModel):
    amber_parm7: str = Field(
        None,
        title="Amber Parm7",
        description="Name of Amber Parm7 file",
    )
    amber_rst7: str = Field(
        None,
        title="Amber Rst7",
        description="Name of Amber Rst7 file",
    )
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    outputDirPath: str = Field(
        None,
        title="Output Directory Path",
        description="Path to output directory",
    )
    inputFilesPath: str = Field(
        None,
        title="Input Files Directory Path",
        description="Path to whhere the input files are stored",
    )
    protocolFilesPath: str = Field(
        None,
        title="Protocol files directory",
        description="Path to where the protocol files are stored",
    )
    use_serial: bool = Field(
        False,
        title="Use Serial",
        description="Should we force the GEMS code to run in serial?",
    )
    control_script: str = Field(
        "Run_Protocol.bash",
        title="Control Script",
        description="Name of the script used to run the protocol",
    )
    resources: Analyze_Resources = Analyze_Resources()


class Analyze_Outputs(BaseModel):
    outputDirPath: str = Field(
        None,
        title="Output Directory Path",
        description="Path to output directory",
    )
    resources: Analyze_Resources = Analyze_Resources()


class Analyze_Request(Glycomimetics_Service_Request):
    typename: str = Field("Analyze", alias="type")
    # the following must be redefined in a child class
    inputs: Analyze_Inputs = Analyze_Inputs()


class Analyze_Response(Glycomimetics_Service_Response):
    typename: str = Field("Analyze", alias="type")
    outputs: Analyze_Outputs = Analyze_Outputs()
