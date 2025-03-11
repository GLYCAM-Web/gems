#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler
from gemsModules.common.main_api_resources import Resource

from gemsModules.complex.antibody.main_api import Antibody_Entity
from gemsModules.complex.antibody.main_api_project import AntibodyProject

from .ProjectManagement import api as pm_api
from .Evaluate import api as evaluate_api
from .Build import api as build_api
from .Analyze import api as analyze_api

from gemsModules.common.code_utils import find_aaop_by_id

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Antibody_Request_Data_Filler(Request_Data_Filler):
    def process(self) -> list[AAOP]:
        """Fill in any data required in the service request aaop_list."""
        
        # We will fill all AAOPs in order, ensuring PM aaop exists before we depend on project paths.
        update_proj_dirs = []
        do_proj_dir_update = False
        for i, aaop in enumerate(self.aaop_list):
            log.debug(f"i: {i}, {aaop.AAO_Type}={aaop}")

            if aaop.AAO_Type == "Build":
                self.__fill_build_aaop(i, aaop)
                update_proj_dirs.append(aaop)
            elif aaop.AAO_Type == "ProjectManagement":
                self.__fill_projman_aaop(i, aaop)
                do_proj_dir_update = True
            elif aaop.AAO_Type == "Evaluate":
                self.__fill_evaluate_aaop(i, aaop)
                update_proj_dirs.append(aaop)
            elif aaop.AAO_Type == "Analyze":
                self.__fill_analyze_aaop(i, aaop)
                update_proj_dirs.append(aaop)
            else:
                log.warning(f"AD/RequestDataFiller: I don't know how to data fill for {aaop.AAO_Type}")

        if not do_proj_dir_update:
            log.warning("AD/RequestDataFiller: No ProjectManagement AAOP found to update project directories.")
            log.warning("This WILL cause problems with the service execution.")
        else:   
            self.__post_process_fill(update_proj_dirs)

        return self.aaop_list

    def __post_process_fill(self, update_proj_dirs: List[AAOP]):
        # TODO/FIX: Hack, but easiest/cheapest way to get all project resources to have the project_dir prepended.
        roles_to_find = ["Antibody", "Ligand"]
        for aaop in update_proj_dirs:
            log.debug(f"AD/RequestDataFiller: Prepending project_dir to resources for {aaop.AAO_Type}")
            for r in aaop.The_AAO.inputs.resources:
                if not roles_to_find:
                    return True
                if (
                    r.resourceRole in roles_to_find
                    and r.locationType == "filesystem-path-unix"
                ):
                    # extract filename from payload
                    r.payload = str(Path(self.response_project.project_dir) / Path(r.payload).name)
                    log.debug(
                        f"AD/RequestDataFiller: {r.resourceRole} prepended project_dir to Receptor payload: {r.payload}"
                    )
                    
                    roles_to_find.remove(r.resourceRole)
                    break
        
        if roles_to_find:
            log.warning(f"AD/RequestDataFiller: Could not find resources for roles: {roles_to_find}")
        return False

    def __fill_projman_aaop(self, i: int, aaop: AAOP):
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        aaop.The_AAO.inputs.projectDir = self.response_project.project_dir

        # Add the resources to copy to the project output directory by the Project Management service.
        # TODO: copy parm7/rst7 this way.
        input_json = pm_api.PM_Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "request.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)

        # TODO: need to handle the case of direct inputs that are not resources.
        self.fill_resources_from_requester_if_exists(aaop, deep_copy=True)

    def __fill_evaluate_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        
        # TODO: need to handle the case of direct inputs that are not resources.
        if not self.fill_resources_from_requester_if_exists(aaop):
            self.__fill_input_pdb_resources(aaop)
        
        self.__fill_pdb_inputs_from_resources(aaop)
        # Add the resources to copy to the project output directory by the Project Management service.

    def __fill_build_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        # Do not fill this, we read it later.
        # aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
  
        if not self.fill_resources_from_requester_if_exists(aaop):
            self.__fill_input_pdb_resources(aaop)
        
        self.__fill_pdb_inputs_from_resources(aaop)

        return self.aaop_list
    
    def __fill_analyze_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        pass 
            
    def __fill_input_pdb_resources(self, aaop):
        if aaop.AAO_Type not in ["Build", "Evaluate"]:
            log.warning(f"AD/RequestDataFiller.fill_input_resources: I don't know how to fill input resources for {aaop.AAO_Type}")
            return
        
        antibody_filename = aaop.The_AAO.inputs.antibody_path
        ligand_filename = aaop.The_AAO.inputs.ligand_path

        if antibody_filename:
            pdb = Resource(
                payload=antibody_filename,
                resourceFormat="chemical/pdb",
                resourceRole="Antibody",
                locationType="filesystem-path-unix",
            )
            aaop.The_AAO.inputs.resources.add_resource(pdb)
        if ligand_filename:
            pdb = Resource(
                payload=ligand_filename,
                resourceFormat="chemical/pdb",
                resourceRole="Ligand",
                locationType="filesystem-path-unix",
            )
            aaop.The_AAO.inputs.resources.add_resource(pdb)
            
    def __fill_pdb_inputs_from_resources(self, aaop):
        if aaop.AAO_Type not in ["Build", "Evaluate"]:
            log.warning(f"AD/RequestDataFiller.fill_inputs_from_resources: I don't know how to fill inputs from resources for {aaop.AAO_Type}")
            return
        
        for resource in aaop.The_AAO.inputs.resources:
            if resource.resourceRole == "Antibody":
                aaop.The_AAO.inputs.antibody_path = resource.payload
            elif resource.resourceRole == "Ligand":
                aaop.The_AAO.inputs.ligand_path = resource.payload
            else:
                log.warning(f"AD/RequestDataFiller.fill_inputs_from_resources: I don't know how to fill input from resource {resource.resourceRole}")
