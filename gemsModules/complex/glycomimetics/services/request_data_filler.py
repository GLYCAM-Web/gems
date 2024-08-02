#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.complex.glycomimetics.main_api import Glycomimetics_Entity
from gemsModules.complex.glycomimetics.main_api_project import GlycomimeticsProject

from gemsModules.complex.glycomimetics.services.Build_Selected_Positions import api as build_api
from gemsModules.complex.glycomimetics.services.ProjectManagement import api as pm_api

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
        for i, aaop in enumerate(self.aaop_list):
            log.debug(f"i: {i}, {aaop.AAO_Type=}")

            if aaop.AAO_Type == "RunMD":
                self.__fill_build_aaop(i, aaop)
            elif aaop.AAO_Type == "ProjectManagement":
                self.__fill_projman_aaop(i, aaop)

        return self.aaop_list

    def __fill_build_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        # Please note, if you need values from response_project, make sure they are initialized appropriately by project manager.
        aaop.The_AAO.inputs = build_api.build_Inputs(
            pUUID=self.response_project.pUUID,
            outputDirPath=self.response_project.project_dir,
        )

        return self.aaop_list

    def __fill_projman_aaop(self, i: int, aaop: AAOP):
        aaop.The_AAO.inputs = pm_api.ProjectManagement_Inputs(
            pUUID=self.response_project.pUUID,
            projectDir=self.response_project.project_dir,
            outputDirPath=self.response_project.project_dir,
        )

        # Add the resources to copy to the project output directory by the Project Management service.
        # TODO: copy parm7/rst7 this way.
        input_json = pm_api.PM_Resource(
            payload=self.transaction.incoming_string,
            resourceFormat="json",
            locationType="Payload",
            options={"filename": "input.json"},
        )
        aaop.The_AAO.inputs.resources.add_resource(input_json)

        # if aaop.Requester is not None:
        #     # If we were using an AAOP_Tree we could use aaop_tree.get_aaop_by_id(aaop.Requester)
        #     requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester)
        #     log.debug("Found requester aaop[%s]", requester_aaop)
        #     log.debug(
        #         "for aaop_list[%s], %s",
        #         i, requester_aaop.The_AAO.inputs,
        #     )
        # else:
        #     log.debug(
        #         "No requester found for aaop_list[%s], PM service request will not have a pdb file resource.", i,
        #     )

        log.debug(
            "\tFinished building ProjectManagement_Inputs, aaop_list[%s].inputs filled with %s",
            i,
            self.aaop_list[i].The_AAO.inputs,
        )
