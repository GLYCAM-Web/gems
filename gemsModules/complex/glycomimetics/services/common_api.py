#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Literal, Union, Any

from gemsModules.common.main_api_resources import Resource
from gemsModules.common.code_utils import GemsStrEnum

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDB_File_Resource(Resource):
    typename: Literal["PdbFile"] = Field(
        "PdbFile",
        alias="type",
        title="PDB File Resource Type",
        description="The name of the type of Resource.",
    )
    locationType: Literal["RCSB_ID", "Path", "Payload", "URL"] = Field(
        "Path",
        title="Location Type",
        description="Where the PDB File can be found.",
    )
    resourceFormat: Literal["PDB-strict", "PDB-unknown", "PDB-variant"] = Field(
        "PDB-unknown",
        title="Resource Format",
        description="Supported formats will vary with each Entity.",
    )
    resourceRole: Literal[
        "Complex_Input", "Glycomimetics_Output", "Ligand", "Receptor"
    ] = Field(
        ...,
        title="Resource Role",
        description="PDB file roles associated with Glycomimetics.",
    )
    payload: Any = Field(
        None,
        description="The thing that is described by the location and format.",
    )


class Moiety_Library_Names(GemsStrEnum):
    """List of R-group libraries specified at this position."""

    aldehydes = "Aldehydes"
    sulfonyl_halides = "Sulfonyl_Halides"
    ketones = "Ketones"


class Modification_Position(BaseModel):
    Residue_Identifier: str = Field(
        ...,
        description="The residue identifier, typically an integer followed occasionally by a letter.",
    )
    Attachment_Atom: str = Field(
        ..., description="The atom in the residue to which the mods will be attached."
    )
    Replaced_Atom: str = Field(
        ...,
        description="The atom in the residue that will be replaced by the modification.",
    )


class Position_Modification_Options(BaseModel):
    Position: Modification_Position = ...
    Libraries: List[Moiety_Library_Names] = []


# 		- Evaluation:
# 			- If included, these are the libraries available at this position.  Must be a subset of All R Group Libraries
# 			- If not included, then this position can use any of the available libraries specified above.
# 		- Build Position
# 			- If not included, all available libraries will be used.
# 			- If included, only the specified libraries will be used
