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
        # TODO/FIX!:Please note, response_project is only the defaults here, right now.
        # TODO: Project manager still needs to fill out the project intelligently.
        this_Project: MdProject = self.response_project
        log.debug(
            "REQUEST_DATA_FILLER: run_md project: %s %s",
            self.response_project.parm7_file_name,
            self.response_project.rst7_file_name,
        )
        aaop.The_AAO.inputs = run_md_api.run_md_Inputs(
            # TODO: One would hope: But the project manager can't easily decode entity inputs.
            # (And probably shouldn't - but fill_response_project_* methods are tempting solutions.)
            # amber_parm7=this_Project.parm7_file_name,
            # amber_rst7=this_Project.rst7_file_name,
            # Hack: The project should have it's defaults overwritten if entity inputs were given.
            amber_parm7=aaop.The_AAO.inputs["parameter-topology-file"]["payload"],
            amber_rst7=aaop.The_AAO.inputs["input-coordinate-file"]["payload"],
            pUUID=this_Project.pUUID,
            outputDirPath=this_Project.project_dir,
            protocolFilesPath=this_Project.protocolFilesPath,
            # TODO: Probably needs to be set by procedural options/env
            inputFilesPath=this_Project.upload_path,
        )

        return self.aaop_list

    def __fill_projman_aaop(self, i: int, aaop: AAOP):
        log.debug(
            "REQUEST_DATA_FILLER: projman\nproject: %s %s",
            self.response_project.parm7_file_name,
            self.response_project.rst7_file_name,
        )

        aaop.The_AAO.inputs = pm_api.ProjectManagement_Inputs(
            pUUID=self.response_project.pUUID,
            projectDir=self.response_project.project_dir,
            protocolFilesPath=self.response_project.protocolFilesPath,  # this_Project.protocolFilesPath trying to avoid modifying the current mdaas request # TODO: no protocol files for MDaaS project currently.
            outputDirPath=self.response_project.project_dir,
            inputFilesPath=self.response_project.upload_path,
            # We will gather these from the requester's aaop.
            # amber_parm7=self.response_project.parm7_file_name,
            # amber_rst7=self.response_project.rst7_file_name,
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
            log.debug("Found requester aaop[%s]", requester_aaop)
            log.debug(
                "for aaop_list[%s], %s",
                i,
                requester_aaop.The_AAO.inputs,
            )

            # TODO/Q: I don't think run_md.json should specify anything more than the location
            # for the topology and coordinate files.
            # we don't use run_md_Inputs because they may not have been filled in yet.
            #
            # Crap... So we are using the valid inputs from the run_md service request
            # Which get filled/overwritten buy the fill_run_md_aaop method.
            # But they don't get filled appropriately... Should we be filling the
            # project itself before this?
            #
            # Ok, so fill response_project_from_response entity can handle this, so that the above response_project has valid inputs.
            # - But for the project manager to handle this, it needs to understand service requests.
            #
            # Ah, jeez.
            # These paths are relative to project.upload_path
            _parm7_path = requester_aaop.The_AAO.inputs["parameter-topology-file"][
                "payload"
            ]
            _rst7_path = requester_aaop.The_AAO.inputs["input-coordinate-file"][
                "payload"
            ]

            # input_parm7 = pm_api.PM_Resource(
            #     name=_parm7_path.stem,
            #     res_format="parm7",
            #     location=str(_parm7_path.parent),
            #     locationType="File",
            # )

            # input_rst7 = pm_api.PM_Resource(
            #     name=str(_rst7_path.stem),
            #     res_format="rst7",
            #     location=str(_rst7_path.parent),
            # )

            # log.debug(
            #     "Adding MDaaS resources to ProjectManagement_Inputs:\n\t%s and %s",
            #     input_parm7,
            #     input_rst7,
            # )
            # aaop.The_AAO.inputs.resources.append(input_parm7)
            # aaop.The_AAO.inputs.resources.append(input_rst7)

            aaop.The_AAO.inputs.amber_parm7 = str(_parm7_path)
            aaop.The_AAO.inputs.amber_rst7 = str(_rst7_path)

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
