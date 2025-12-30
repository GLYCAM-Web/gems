#!/usr/bin/env python3
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

# TODO: Replace with PM_Resource
from gemsModules.common.main_api_resources import Resource

from gemsModules.conjugate.glycoprotein.main_api import Gpbuilder_Entity
from gemsModules.conjugate.glycoprotein.main_api_project import GpBuilderProject

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Gpbuilder_Request_Data_Filler(Request_Data_Filler):
    def process(self) -> List[AAOP]:        
        this_Project : GpBuilderProject = self.response_project
        
        log.debug(f"GpB/Request_Data_Filler now filling data for the request.")
        log.debug(f"GpB/Request_Data_Filler: {this_Project.project_dir=}")
        # We fill in the data in reverse, as dependents are at the end of the list.
        for i, aaop in enumerate(reversed(self.aaop_list)):
            log.debug(f"GpB/Request_Data_Filler: {i}: {aaop.AAO_Type=}")
            
            if aaop.AAO_Type=='Build':
                if aaop.The_AAO.inputs.pUUID is None:
                    aaop.The_AAO.inputs.pUUID = this_Project.pUUID
                else:
                    # if the pUUID is already set, we assume it's from a previous Evaluation request.
                    this_Project.pUUID = aaop.The_AAO.inputs.pUUID
                    this_Project.add_temporary_info()
                    
                # copy inputs to resources
                self.__fill_build_input_resources(aaop, this_Project.project_dir)
            elif aaop.AAO_Type=='Evaluate':
                aaop.The_AAO.inputs.pUUID = this_Project.pUUID
                
                self.__fill_evaluate_input_resources(aaop)
            elif aaop.AAO_Type=='ProjectManagement':
                aaop.The_AAO.inputs.pUUID = this_Project.pUUID
                aaop.The_AAO.inputs.projectDir = this_Project.project_dir
                
                self.__fill_projectman_input_resources(aaop)
                # copy resources from requester
                self.fill_resources_from_requester_if_exists(aaop, deep_copy=True)
            elif aaop.AAO_Type=='Status':
                if aaop.The_AAO.inputs.pUUID is None:
                    log.error("GpB/Request_Data_Filler: Status service requires pUUID to be set.")
                    raise ValueError("GpB/Request_Data_Filler: Status service requires pUUID to be set.")
                else:
                    this_Project.pUUID = aaop.The_AAO.inputs.pUUID
                    this_Project.add_temporary_info()
                    aaop.The_AAO.inputs.projectDir = this_Project.project_dir
            
            log.debug(f"GpB/Request_Data_Filler filled: {aaop.The_AAO.inputs=}")
        
        return self.aaop_list

    def __fill_build_input_resources(self, aaop: AAOP, project_dir: str):
        log.debug(f" Filling build input resources for {aaop=}")
        if aaop.The_AAO.inputs.protein_file not in (None, ""):
            log.debug(f"Protein file found in inputs: {aaop.The_AAO.inputs.protein_file}")
            # if the protein file is set, we add it as a resource
            protein = Resource(
                payload=aaop.The_AAO.inputs.protein_file,
                resourceFormat="PDB",
                resourceRole="protein-file",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(protein)
        else:
            # This is assuming that build doesn't require a protein file to be set in inputs for v1. TODO: Be more explicit in handling protein file 
            log.debug(f"Protein file not set in inputs, trying to find OriginalInput.pdb in project directory {project_dir}.")
            # try to grab from the project dir by seeing what OriginalInput.pdb points to
            default_pdb = Path(project_dir) / "OriginalInput.pdb"
            if default_pdb.exists():
                # resolve the symlink to get the actual file
                if default_pdb.is_symlink():
                    default_pdb = default_pdb.resolve()
                log.debug(f"OriginalInput.pdb found at {default_pdb}, setting as protein file.")
                protein = Resource(
                    payload=default_pdb,
                    resourceFormat="PDB",
                    resourceRole="protein-file",
                    locationType="filesystem-path-unix"
                )
                aaop.The_AAO.inputs.resources.add_resource(protein)
                aaop.The_AAO.inputs.protein_file = str(default_pdb)
                log.debug(f"Set protein file to {aaop.The_AAO.inputs.protein_file} from OriginalInput.pdb.")
            else:
                log.warning(f"OriginalInput.pdb not found in project directory {project_dir}, protein file will not be set.")
        if aaop.The_AAO.inputs.glycan_mappings is not None:
            mappings = Resource(
                payload=aaop.The_AAO.inputs.glycan_mappings,
                resourceFormat="python-dict",
                resourceRole="glycan-mappings",
                locationType="Payload"
            )
            aaop.The_AAO.inputs.resources.add_resource(mappings)

    def __fill_evaluate_input_resources(self, aaop: AAOP):
        log.debug(f" Filling evaluate input resources for {aaop=}")
        
        rcsb_id = aaop.The_AAO.inputs.rcsb_id
        if rcsb_id:
            rcsb_id = rcsb_id.strip().lower()
        
        given_protein_file = aaop.The_AAO.inputs.protein_file
        
        if given_protein_file is None and rcsb_id is None:
            log.warning("Neither protein_file nor rcsb_id is set in inputs, no protein file will be set in resources.")
        else:
            log.warning("Both protein_file and rcsb_id are set in inputs, keeping RCSB ID and updating protein_file.")

        if rcsb_id:
            log.debug(f"RCSB ID found in inputs: {rcsb_id}")
            # if the rcsb_id is set, we assume the protein file will be downloaded later
            aaop.The_AAO.inputs.resources.add_resource(
                Resource(
                    payload=rcsb_id,
                    resourceFormat="RCSB-ID",
                    resourceRole="rcsb-id",
                    locationType="Payload"
                )
            )
            given_protein_file = None
            
        if given_protein_file:
            log.debug(f"Protein file found in inputs: {given_protein_file}")
            aaop.The_AAO.inputs.resources.add_resource(
                Resource(
                    payload=given_protein_file,
                    resourceFormat="PDB",
                    resourceRole="protein-file",
                    locationType="filesystem-path-unix"
                )
            )


        
        
    def __fill_projectman_input_resources(self, aaop: AAOP):
        log.debug(f" Filling project management input resources for {aaop=}")

        input_json = Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "request.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)
