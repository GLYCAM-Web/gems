#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Union

from gemsModules.common.main_api_resources import Resource, Resources

from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.complex.glycomimetics.main_api import (
    Glycomimetics_Service_Request,
    Glycomimetics_Service_Response,
)

from gemsModules.complex.glycomimetics.services.common_api import (
    PDB_File_Resource,
    Moiety_Library_Names,
    Position_Modification_Options,
    Modification_Position
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


class Build_Input_Resources(Resources):
    __root__: List[
        Union[PDB_File_Resource, Build_input_Resource, Build_output_Resource]
    ] = None


class Build_Output_Resources(Resources):
    __root__: List[Union[Build_input_Resource, Build_output_Resource]] = None


# TODO: update descriptions
class Build_Options(BaseModel):
    """Options for controlling the build's exection."""

    Interval: int = Field(
        30,
        title="Interval",
        description="Interval",
    )
    NumThreads: int = Field(
        1,
        title="Number of Threads",
        description="Number of Threads",
    )
    OutputPath: str = Field(
        "output",
        title="Output Path",
        description="Output Path",
    )
    LogFile: str = Field(
        "sample.log",
        title="Log File",
        description="Log file filename",
    )


class Build_Inputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )

    Available_Libraries: List[str] = (
        Moiety_Library_Names.get_json_list()
    )  # might need syntax adjustment
    Selected_Modification_Options: Position_Modification_Options = None

    complex_PDB_Filename: str = None
    # Until we have the workflow down, the correct location for these is unclear.
    # For the moment, I'm assuming that they get made during the Evaluate step.
    receptor_PDB_Filename: str = None
    ligand_PDB_Filename: str = None

    #    coComplex: str = Field(
    #        None,
    #        title="Complex",
    #        description="Complex to build",
    #    )
    buildOptions: Build_Options = Build_Options()

    # TODO: Fix the complications
    # resources: Build_Input_Resources = Build_Input_Resources()
    resources: Resources = Resources()


# it will be hard to specify this before the workflow is well specified
class Build_Outputs(BaseModel):
    pUUID: str = Field(
        None,
        title="Project UUID",
        description="UUID of Project",
    )
    projectDir: str = Field(
        None,
        title="Output Directory Path",
        description="Path to output directory",
    )
    resources: Build_Output_Resources = Build_Output_Resources()


class Build_Selected_Positions_Request(Glycomimetics_Service_Request):
    typename: str = Field("Build_Selected_Positions", alias="type")
    # the following must be redefined in a child class
    inputs: Build_Inputs = Build_Inputs()


class Build_Selected_Positions_Response(Glycomimetics_Service_Response):
    typename: str = Field("Build_Selected_Positions", alias="type")
    outputs: Build_Outputs = Build_Outputs()


if __name__ == "__main__":
    # very simple request to demonstrate:
    request = Build_Selected_Positions_Request(
        inputs=Build_Inputs(
            Available_Libraries=[""],
            Selected_Modification_Options=Position_Modification_Options(
                Position=Modification_Position(
                    Residue_Identifier="1",
                    Residue_Name="GLY",
                    Chain_Identifier="A",
                    Attachment_Atom="N",
                    Replaced_Atom="O"
                ),
                Libraries=[Moiety_Library_Names.aldehydes, Moiety_Library_Names.ketones, Moiety_Library_Names.sulfonyl_halides]
            ),
            buildOptions=Build_Options(
                Interval=30,
                NumThreads=1,
                OutputPath="output",
                LogFile="sample.log",
            ),
            resources=Resources(
                __root__=[
                    PDB_File_Resource(
                        locationType="Path",
                        resourceFormat="PDB-unknown",
                        resourceRole="Complex_Input",
                        payload="/path/to/file",
                    ),
                    Build_input_Resource(
                        locationType="File",
                        resourceFormat="PDB-unknown",
                        payload="/path/to/file",
                    ),
                    Build_output_Resource(
                        locationType="File",
                        resourceFormat="PDB-unknown",
                        payload="/path/to/file",
                    ),
                ]
            ),
        )
    )
    # dump to file
    with open("build_selected_positions_request-git-ignore-me.json", "w") as f:
        f.write(request.json(indent=2))