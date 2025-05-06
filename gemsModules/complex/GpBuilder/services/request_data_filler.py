#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.complex.GpBuilder.main_api import Gpbuilder_Entity
from gemsModules.complex.GpBuilder.main_api_project import Gpbuilder_Project

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Gpbuilder_Request_Data_Filler(Request_Data_Filler):

        # self.aaop_list = aaop_list
        # self.entity = entity
        # self.project = project

    # No data to fill here.
    def process(self) -> List[AAOP]:        
        this_Project : Gpbuilder_Project = self.project
        
        log.debug(f"GpB/Request_Data_Filler now filling data for the request.")
        for aaop in self.aaop_list:
            if aaop.Dictionary_Name=='Build':
                aaop.The_AAO.inputs.pUUID=this_Project.pUUID
            elif aaop.Dictionary_Name=='ProjectManagement':
                log.debug(f"GpB/ProjectManagement AAOP {aaop}")
                aaop.The_AAO.inputs.projectDir = this_Project.project_dir
                aaop.The_AAO.inputs.pUUID=this_Project.pUUID

        return self.aaop_list
