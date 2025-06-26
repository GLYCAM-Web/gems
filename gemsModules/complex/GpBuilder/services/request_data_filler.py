#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

# TODO: Replace with PM_Resource
from gemsModules.common.main_api_resources import Resource

from gemsModules.complex.GpBuilder.main_api import Gpbuilder_Entity
from gemsModules.complex.GpBuilder.main_api_project import GpBuilderProject

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
                aaop.The_AAO.inputs.pUUID = this_Project.pUUID
                
                # copy inputs to resources
                self.__fill_build_input_resources(aaop)
            elif aaop.AAO_Type=='Evaluate':
                aaop.The_AAO.inputs.pUUID = this_Project.pUUID
                
                self.__fill_evaluate_input_resources(aaop)
            elif aaop.AAO_Type=='ProjectManagement':
                aaop.The_AAO.inputs.pUUID = this_Project.pUUID
                aaop.The_AAO.inputs.projectDir = this_Project.project_dir
                
                self.__fill_projectman_input_resources(aaop)
                # copy resources from requester
                self.fill_resources_from_requester_if_exists(aaop, deep_copy=True)
            
            log.debug(f"GpB/Request_Data_Filler filled: {aaop.The_AAO.inputs=}")
        
        return self.aaop_list

    def __fill_build_input_resources(self, aaop: AAOP):
        log.debug(f" Filling build input resources for {aaop=}")
        if aaop.The_AAO.inputs.protein_file is not None:
            protein = Resource(
                payload=aaop.The_AAO.inputs.protein_file,
                resourceFormat="PDB",
                resourceRole="protein-file",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(protein)
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
        if aaop.The_AAO.inputs.protein_file is not None:
            protein = Resource(
                payload=aaop.The_AAO.inputs.protein_file,
                resourceFormat="PDB",
                resourceRole="protein-file",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(protein)
        
    def __fill_projectman_input_resources(self, aaop: AAOP):
        log.debug(f" Filling project management input resources for {aaop=}")

        input_json = Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "request.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)