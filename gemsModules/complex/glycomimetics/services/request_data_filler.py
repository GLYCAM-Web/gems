#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler
from gemsModules.common.main_api_resources import Resource

from gemsModules.complex.glycomimetics.main_api import Glycomimetics_Entity
from gemsModules.complex.glycomimetics.main_api_project import GlycomimeticsProject

from .Build_Selected_Positions import api as build_api
from .ProjectManagement import api as pm_api
from .Evaluate import api as evaluate_api
from .Validate import api as validate_api

from gemsModules.common.code_utils import find_aaop_by_id

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Glycomimetics_Request_Data_Filler(Request_Data_Filler):
    # self.aaop_list = aaop_list
    # self.entity = entity
    # self.project = project

    # No data to fill here.
    def process(self) -> list[AAOP]:
        """Fill in any data required in the service request aaop_list."""
        for i, aaop in enumerate(reversed(self.aaop_list)):
            log.debug(f"i: {i}, {aaop.AAO_Type}={aaop}")

            if aaop.AAO_Type == "Build_Selected_Positions":
                self.__fill_build_aaop(i, aaop)
            elif aaop.AAO_Type == "ProjectManagement":
                self.__fill_projman_aaop(i, aaop)
            elif aaop.AAO_Type == "Evaluate":
                self.__fill_evaluate_aaop(i, aaop)
            elif aaop.AAO_Type == "Validate":
                self.__fill_validate_aaop(i, aaop)

        return self.aaop_list

    def __fill_build_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        # Please note, if you need values from response_project, make sure they are initialized appropriately by project manager.
        
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        aaop.The_AAO.inputs.projectDir = self.response_project.project_dir
        aaop.The_AAO.inputs.outputDirPath = self.response_project.project_dir
        
        if aaop.The_AAO.inputs.complex_PDB_Filename is not None:
            pdb = Resource(
                payload=aaop.The_AAO.inputs.complex_PDB_Filename,
                resourceFormat="chemical/pdb",
                resourceRole="complex",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(pdb)
        if aaop.The_AAO.inputs.ligand_PDB_Filename is not None:
            pdb = Resource(
                payload=aaop.The_AAO.inputs.ligand_PDB_Filename,
                resourceFormat="chemical/pdb",
                resourceRole="ligand",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(pdb)
        if aaop.The_AAO.inputs.receptor_PDB_Filename is not None:
            pdb = Resource(
                payload=aaop.The_AAO.inputs.receptor_PDB_Filename,
                resourceFormat="chemical/pdb",
                resourceRole="receptor",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(pdb)
            
        return self.aaop_list

    def __fill_projman_aaop(self, i: int, aaop: AAOP):
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        aaop.The_AAO.inputs.projectDir = self.response_project.project_dir
        
        # Add the resources to copy to the project output directory by the Project Management service.
        # TODO: copy parm7/rst7 this way.
        input_json = pm_api.PM_Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "input.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)
        
        # TODO: need to handle the case of direct inputs that are not resources.
        self.fill_resources_from_requester_if_exists(aaop)

    def __fill_evaluate_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        
        # TODO: need to handle the case of direct inputs that are not resources.
        self.fill_resources_from_requester_if_exists(aaop)
        # Add the resources to copy to the project output directory by the Project Management service.
        
    def __fill_validate_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
                
        # TODO: need to handle the case of direct inputs that are not resources.
        self.fill_resources_from_requester_if_exists(aaop)