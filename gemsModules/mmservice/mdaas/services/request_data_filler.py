#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler
from gemsModules.common.main_api_resources import Resource

from gemsModules.mmservice.mdaas.main_api import MDaaS_Entity
from gemsModules.mmservice.mdaas.main_api_project import MdProject

from gemsModules.mmservice.mdaas.services.run_md import run_md_api
from gemsModules.mmservice.mdaas.services.ProjectManagement import api as pm_api
from gemsModules.mmservice.mdaas.services.Evaluate import api as evaluate_api

from gemsModules.common.code_utils import find_aaop_by_id

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class mdaas_Request_Data_Filler(Request_Data_Filler):
    # self.aaop_list = aaop_list
    # self.entity = entity
    # self.project = project

    # No data to fill here.
    def process(self) -> list[AAOP]:
        """Fill in any data required in the service request aaop_list."""
        
        # TODO: Ordering and workflow manager compatibility
        for i, aaop in enumerate(reversed(self.aaop_list)):
            log.debug(f"i: {i}, {aaop.AAO_Type=}")

            # TODO: Use the settings.KnownServices dict to map AAO_Type to fillers.
            if aaop.AAO_Type == "RunMD":
                self.__fill_run_md_aaop(i, aaop)
            elif aaop.AAO_Type == "ProjectManagement":
                self.__fill_projman_aaop(i, aaop)
            elif aaop.AAO_Type == "Evaluate":
                self.__fill_evaluate_aaop(i, aaop)

        return self.aaop_list

    def __fill_run_md_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        # TODO/N: This doesn't make much sense as the RunMD service takes a parm7 and rst7 as inputs,
        # but we don't even use run_md_Inputs in the API. See implied translator todos.
        #
        # N: Resources will not be available in RunMD.logic.execute() unless we add them here.
        # This design implementation differs from the GM Entity's current conceptualization, which always has resources.
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        aaop.The_AAO.inputs.outputDirPath = self.response_project.project_dir
        aaop.The_AAO.inputs.protocolFilesPath = self.response_project.protocolFilesPath

        log.debug(f"RUNMD AAOP {aaop}")
        if aaop.The_AAO.inputs.parameter_topology_file is not None:
            parm7 = Resource(
                payload=aaop.The_AAO.inputs.parameter_topology_file,
                resourceFormat="AMBER-7-prmtop",
                resourceRole="parameter-topology",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(parm7)
        if aaop.The_AAO.inputs.input_coordinate_file is not None:
            rst7 = Resource(
                payload=aaop.The_AAO.inputs.input_coordinate_file,
                resourceFormat="AMBER-7-restart",
                resourceRole="input-coordinate",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(rst7)
        if aaop.The_AAO.inputs.unminimized_gas_file is not None:
            gas = Resource(
                payload=aaop.The_AAO.inputs.unminimized_gas_file,
                resourceFormat="AMBER-7-prmtop",
                resourceRole="unminimized-gas",
                locationType="filesystem-path-unix"
            )
            aaop.The_AAO.inputs.resources.add_resource(gas)
            
        log.debug(f"RUNMD AAOP FILLED: {aaop}")
        return self.aaop_list

    # TODO: PDBFile and MDaaS PM data fillers are very similar, can we generalize them?
    def __fill_projman_aaop(self, i: int, aaop: AAOP):        
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        aaop.The_AAO.inputs.projectDir = self.response_project.project_dir
        aaop.The_AAO.inputs.protocolFilesPath = self.response_project.protocolFilesPath
        aaop.The_AAO.inputs.outputDirPath = self.response_project.project_dir
        aaop.The_AAO.inputs.sim_length = self.response_project.sim_length

        # Add the input request as a json file resource.
        input_json = Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "input.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)
        

        # TODO/FIX: Could be more generic/lifted.
        # Are we certain that RunMD will always have all resources filled first?
        if aaop.Requester is not None:
            log.debug(f"MDaaS/ProjectManagement requester: {aaop.Requester}")
            requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester) 
            log.debug(f"resources: {requester_aaop.The_AAO.inputs.resources}")
            for resource in requester_aaop.The_AAO.inputs.resources:
                aaop.The_AAO.inputs.resources.add_resource(resource)

    def __fill_evaluate_aaop(self, i: int, aaop: AAOP):
        aaop.The_AAO.inputs.pUUID = self.response_project.pUUID
        aaop.The_AAO.inputs.projectDir = self.response_project.project_dir
        aaop.The_AAO.inputs.protocolFilesPath = self.response_project.protocolFilesPath
        aaop.The_AAO.inputs.outputDirPath = self.response_project.project_dir
        aaop.The_AAO.inputs.sim_length = self.response_project.sim_length

        if aaop.Requester is not None:
            requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester)
            for resource in requester_aaop.The_AAO.inputs.resources:
                aaop.The_AAO.inputs.resources.add_resource(resource)
                
