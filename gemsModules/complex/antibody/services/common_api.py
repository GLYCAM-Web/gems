#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union, Any

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
        "Antibody", "Ligand"
    ] = Field(
        ...,
        title="Resource Role",
        description="PDB file roles associated with Antibody.",
    )
    payload: Any = Field(
        None,
        description="The thing that is described by the location and format.",
    )