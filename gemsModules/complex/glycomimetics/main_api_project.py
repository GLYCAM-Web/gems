#!/usr/bin/env python3
import os

from pydantic import constr, Field
from pydantic.typing import Literal as PyLiteral
from typing import Literal, Any

from gemsModules.project.main_api import Project
from gemsModules.deprecated.instance_config.main import InstanceConfig

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class GlycomimeticsProject(Project):
    """Glycomimetics Project class"""
    # TODO: Better names, also, snake_case --- Done 2026-02-13 BLFoley
    #complex: constr(max_length=255) = "Complex.pdb"
    #receptor: constr(max_length=255) = "Receptor.pdb"
    #ligand: constr(max_length=255) = "Ligand.pdb"
    complexFile: str = Field(  
        "Complex.pdb", title="PDB file containing the protein-glycan complex", alias="complex", max_length=255
    )
    receptorFile: str = Field(  
        "Receptor.pdb", title="PDB file containing the receptor protein", alias="receptor", max_length=255
    )
    ligandFile: str = Field(  
        "Ligand.pdb", title="PDB file containing the glycan", alias="ligand", max_length=255
    )
    input_type: constr(max_length=255) = "AutoDock extended PDB (chemical/pdbqt) & application/json"
    gm_utils_version: str = Field(  
        "", title="Glycomimetics software version", max_length=255
    )

    # protocolFilesPath: constr(max_length=255) = "/website/programs/gems/External/GM_Utils/protocols"
    # TODO: convert to glycomimetics protocols
    metadataPath: constr(max_length=255) = (
        "/programs/gems/External/GM_Utils/metadata"  # /moeties etc.
    )

    def __init__(self, **data : Any):
        super().__init__(**data)
        #
        # Removing the following redefinition of the field in the Project class
        # self.project_type: PyLiteral["gm"] = Field("gm", title="Type", alias="type")
        # Instead, just initializing it as desired
        self.project_type = 'gm'
        #
        self.has_input_files = False
        self.parent_entity = "Complex"
        self.entity_id = "glycomimetics"
        self.service_id = "gm"
        self.title = "Initial Glycomimetics Project"
        self.app = "Glycomimetics"
        self.requesting_agent = ""
        self.requested_service = "Build"
        self.setFilesystemPath(noClobber=False)
        self.setUploadsPath(noClobber=False)
        self.setServiceDir(noClobber=False)
        self.setProjectDir(noClobber=False)
        self.setVersionsFilePath(noClobber=False)
        self.logs_dir = str(os.path.join(self.project_dir, "logs"))



## Some former contents of this class
#    title: str = "Initial Glycomimetics Project"
#    parent_entity: str = "Complex"
#    app: str = "Glycomimetics"
#    requested_service: str = ""
#    project_type: PyLiteral["gm"] = Field("gm", title="Type", alias="type")
#    entity_id: str = "glycomimetics"
#    service_id: constr(max_length=25) = ""  # what should this be?
#    gm_utils_version: str = ""
#    requesting_agent: str = "tester"
#    input_type: constr(max_length=25) = (
#        "AutoDock extended PDB (chemical/pdbqt) & application/json"
#    )
#
#    pUUID: constr(max_length=36) = ""
#    project_dir: constr(max_length=255) = ""
#
#    # TODO: Better names, also, snake_case
#    complex: constr(max_length=255) = "Complex.pdb"
#    receptor: constr(max_length=255) = "Receptor.pdb"
#    ligand: constr(max_length=255) = "Ligand.pdb"
#
#    # protocolFilesPath: constr(max_length=255) = "/website/programs/gems/External/GM_Utils/protocols"
#
#    # TODO: convert to glycomimetics protocols
#    metadataPath: constr(max_length=255) = (
#        "/programs/gems/External/GM_Utils/metadata"  # /moeties etc.
#    )
#
