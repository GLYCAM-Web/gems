#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.mmservice.mdaas.main_api import MDaaS_Entity
from gemsModules.mmservice.mdaas.main_api_project import MdProject

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class mdaas_Request_Data_Filler(Request_Data_Filler):
    # self.aaop_list = aaop_list
    # self.entity = entity
    # self.project = project

    # No data to fill here.
    def process(self) -> List[AAOP]:
        for aaop in self.aaop_list:
            if aaop.AAO_Type == "RunMD":
                from gemsModules.mmservice.mdaas.services.run_md import api

                this_Project: MdProject = self.response_project
                log.debug("REQUEST_DATA_FILLER: run_md")
                aaop.The_AAO.inputs = api.run_md_Inputs()
                aaop.The_AAO.inputs.amber_parm7 = this_Project.parm7_file_name
                aaop.The_AAO.inputs.amber_rst7 = this_Project.rst7_file_name
                aaop.The_AAO.inputs.pUUID = this_Project.pUUID
                aaop.The_AAO.inputs.outputDirPath = this_Project.project_dir
                aaop.The_AAO.inputs.protocolFilesPath = (
                    "/programs/gems/tests/temp-inputs/RoeProtocol/"
                )
                aaop.The_AAO.inputs.inputFilesPath = this_Project.upload_path

        return self.aaop_list
