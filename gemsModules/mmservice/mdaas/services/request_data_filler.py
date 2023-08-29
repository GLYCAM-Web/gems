#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.mmservice.mdaas.main_api import MDaaS_Entity
from gemsModules.mmservice.mdaas.main_api_project import MdProject

from gemsModules.mmservice.mdaas.services.run_md import run_md_api
from gemsModules.mmservice.mdaas.services.ProjectManagement import api as pm_api

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

            if aaop.AAO_Type == "RunMD":
                self.__fill_run_md_aaop(i, aaop)
            elif aaop.AAO_Type == "ProjectManagement":
                self.__fill_projman_aaop(i, aaop)

        return self.aaop_list

    def __fill_run_md_aaop(self, i: int, aaop: AAOP) -> List[AAOP]:
        # Please note, if you need values from response_project, make sure they are initialized appropriately by project manager.
        aaop.The_AAO.inputs = run_md_api.run_md_Inputs(
            amber_parm7=self.response_project.parm7_file_name,
            amber_rst7=self.response_project.rst7_file_name,
            pUUID=self.response_project.pUUID,
            outputDirPath=self.response_project.project_dir,
            protocolFilesPath=self.response_project.protocolFilesPath,
            # TODO: inputsFilePath is mostly ignored by setup_run_md_directory.
            # Possibly needs to be set by procedural options/env and/or doesn't make sense for GEMS to know about.
            inputFilesPath=self.response_project.upload_path,
        )

        return self.aaop_list

    def __fill_projman_aaop(self, i: int, aaop: AAOP):
        log.debug("REQUEST_DATA_FILLER: projman\nproject: %s %s", self.response_project)

        aaop.The_AAO.inputs = pm_api.ProjectManagement_Inputs(
            pUUID=self.response_project.pUUID,
            projectDir=self.response_project.project_dir,
            protocolFilesPath=self.response_project.protocolFilesPath,
            outputDirPath=self.response_project.project_dir,
            inputFilesPath=self.response_project.upload_path,
            amber_parm7=self.response_project.parm7_file_name,
            amber_rst7=self.response_project.rst7_file_name,
        )

        # Add the resources to copy to the project output directory by the Project Management service.
        input_json = pm_api.PM_Resource.from_payload(
            self.transaction.incoming_string, "input", "json"
        )
        aaop.The_AAO.inputs.resources.append(input_json)

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
