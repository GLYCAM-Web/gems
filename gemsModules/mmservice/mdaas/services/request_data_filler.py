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
        this_Project: MdProject = self.response_project
        log.debug("REQUEST_DATA_FILLER: run_md\nproject: %s", this_Project)
        aaop.The_AAO.inputs = run_md_api.run_md_Inputs()
        aaop.The_AAO.inputs.amber_parm7 = this_Project.parm7_file_name
        aaop.The_AAO.inputs.amber_rst7 = this_Project.rst7_file_name
        aaop.The_AAO.inputs.pUUID = this_Project.pUUID
        aaop.The_AAO.inputs.outputDirPath = this_Project.project_dir
        aaop.The_AAO.inputs.protocolFilesPath = "/programs/gems/tests/temp-inputs/RoeProtocol"  # this_Project.protocolFilesPath trying to avoid modifying the current mdaas request
        aaop.The_AAO.inputs.inputFilesPath = this_Project.upload_path

        return self.aaop_list

    def __fill_projman_aaop(self, i: int, aaop: AAOP):
        # Fill in the project management service request
        aaop.The_AAO.inputs = pm_api.ProjectManagement_Inputs(
            pUUID=self.response_project.pUUID,
            projectDir=self.response_project.project_dir,
            protocolFilesPath="/programs/gems/tests/temp-inputs/RoeProtocol",  # this_Project.protocolFilesPath trying to avoid modifying the current mdaas request # TODO: no protocol files for MDaaS project currently.
            outputDirPath=self.response_project.project_dir,
            inputFilesPath=self.response_project.upload_path,
            amber_parm7=self.response_project.parm7_file_name,
            amber_rst7=self.response_project.rst7_file_name,
        )

        # Add the resources to copy to the project management service request
        input_json = pm_api.PM_Resource.from_payload(
            self.transaction.incoming_string, "input", "json"
        )
        aaop.The_AAO.inputs.resources.append(input_json)

        # Lets try to get inputs from the requesting AAOP for ProjectManagement
        if aaop.Requester is not None:
            # If we were using an AAOP_Tree we could use aaop_tree.get_aaop_by_id(aaop.Requester)
            requester_aaop = find_aaop_by_id(self.aaop_list, aaop.Requester)
            log.debug(
                "Found requester aaop[%s] for aaop_list[%s], %s",
                requester_aaop,
                i,
                requester_aaop.The_AAO.inputs,
            )
            # we don't use run_md_Inputs because they may not have been filled in yet.
            # input_parm7 = pm_api.PM_Resource(
            #     name=Path(
            #         requester_aaop.The_AAO.inputs["parameter-topology-file"]
            #     ).stem,
            #     res_format="parm7",
            #     location=str(requester_aaop.The_AAO.inputs["parameter-topology-file"]),
            #     locationType="File",
            # )

            # input_rst7 = pm_api.PM_Resource(
            #     name=Path(
            #         requester_aaop.The_AAO.inputs["input-coordinate-file"].location
            #     ).stem,
            #     res_format="rst7",
            #     location=str(
            #         requester_aaop.The_AAO.inputs["input-coordinate-file"].location
            #     ),
            #

            # TODO: These double up run_md inputs in a strange way, probably don't need MDaaS PM inputs to include these.
            input_parm7 = requester_aaop.The_AAO.inputs["parameter-topology-file"]
            input_rst7 = requester_aaop.The_AAO.inputs["input-coordinate-file"]
            log.debug(
                "Adding MDaaS resources to ProjectManagement_Inputs:\n\t%s and %s",
                input_parm7,
                input_rst7,
            )
            aaop.The_AAO.inputs.resources.append(input_parm7)
            aaop.The_AAO.inputs.resources.append(input_rst7)

            # TODO: also fill the protocol files path properly, (not a static string)
        else:
            log.debug(
                "No requester found for aaop_list[%s], PM service request will not have a pdb file resource.",
                i,
            )

        log.debug(
            "\tFinished building ProjectManagement_Inputs, aaop_list[%s].inputs filled with %s",
            i,
            self.aaop_list[i].The_AAO.inputs,
        )