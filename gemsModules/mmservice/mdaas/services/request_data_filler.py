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
        for i, aaop in enumerate(self.aaop_list):
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
        aaop.The_AAO.inputs = run_md_api.run_md_Inputs(
            pUUID=self.response_project.pUUID,
            outputDirPath=self.response_project.project_dir,
            protocolFilesPath=self.response_project.protocolFilesPath,
        )

        log.debug(f"RUNMD AAOP {aaop}")
        # Add the parameter-topology and restart files as resources.
        parm7 = Resource(
            payload=aaop,
            resourceFormat="AMBER-7-prmtop",
            resourceRole="parameter-topology-file",
            locationType="filesystem-path-unix",
        )

        return self.aaop_list

    # TODO: PDBFile and MDaaS PM data fillers are very similar, can we generalize them?
    def __fill_projman_aaop(self, i: int, aaop: AAOP):

        aaop.The_AAO.inputs = pm_api.ProjectManagement_Inputs(
            pUUID=self.response_project.pUUID,
            projectDir=self.response_project.project_dir,
            protocolFilesPath=self.response_project.protocolFilesPath,
            outputDirPath=self.response_project.project_dir,
            sim_length=self.response_project.sim_length,
        )

        # Add the input request as a json file resource.
        input_json = Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "input.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)

        # TODO/FIX: Could be more generic/lifted.
        if aaop.Requester is not None:
            requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester)
            for resource in requester_aaop.The_AAO.inputs.resources:
                aaop.The_AAO.inputs.resources.add_resource(resource)
    
        log.debug(
            "\tFinished building ProjectManagement_Inputs, aaop_list[%s].inputs filled with %s",
            i,
            self.aaop_list[i].The_AAO.inputs,
        )

    def __fill_evaluate_aaop(self, i: int, aaop: AAOP):
        # Same as in __fill_projman_aaop.

        aaop.The_AAO.inputs = evaluate_api.Evaluate_Inputs(
            pUUID=self.response_project.pUUID,
            projectDir=self.response_project.project_dir,
            protocolFilesPath=self.response_project.protocolFilesPath,
            outputDirPath=self.response_project.project_dir,
            sim_length=self.response_project.sim_length,
        )
        if aaop.Requester is not None:
            requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester)
            for resource in requester_aaop.The_AAO.inputs.resources:
                aaop.The_AAO.inputs.resources.add_resource(resource)