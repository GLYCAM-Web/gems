#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List, Optional, Union

from gemsModules.common.main_api_resources import Resource, Resources


from gemsModules.complex.gpbuilder.main_api import (
    GpBuilder_Service_Request,
    GpBuilder_Service_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Build_Inputs(BaseModel):
    pUUID: str = Field()

    pdb_file: str = Field(
        None,
        title="PDB File",
        description="PDB file to be used for building the system",
    )
    
    # TODO: Bad name: describes the structure of the glyco protein and the method of it's construction
    gpbuilder_config_file: str = Field(
        None,
        title="GPBuilder Configuration File",
        description="Contains build configuration and residues to glycosylate with with GLYCAM Condensed Sequences."
    )