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


class Build_input_Resource(Resource):
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


class Build_output_Resource(Resource):
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


class Build_Resources(Resources):
    __root__: List[Union[Build_input_Resource, Build_output_Resource]] = None


# TODO: update descriptions
class Build_Options(BaseModel):
    """Options for controlling the build's exection."""

    Interval: int = Field(
        30,
        title="Interval",
        description="Interval",
    )


class Build_Inputs(BaseModel):
    coComplex: str = Field(
        None,
        title="Complex",
        description="Complex to build",
    )
    moietyMetadata: str = Field(
        None,
        title="Moiety Metadata PDBQT",
        description="Metadata for moiety",
    )
    buildOptions: Build_Options = Build_Options()
    resources: Build_Resources = Build_Resources()


class Build_Outputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    # outputDirPath: str = Field(
    #     None,
    #     title="Output Directory Path",
    #     description="Path to output directory",
    # )
    resources: Build_Resources = Build_Resources()


class Build_Request(Glycomimetics_Service_Request):
    typename: str = Field("Build", alias="type")
    # the following must be redefined in a child class
    inputs: Build_Inputs = Build_Inputs()


class Build_Response(Glycomimetics_Service_Response):
    typename: str = Field("Build", alias="type")
    outputs: Build_Outputs = Build_Outputs()
