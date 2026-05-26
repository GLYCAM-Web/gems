#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.batchcompute.main_api import Batchcompute_Entity
from gemsModules.batchcompute.main_api_project import Batchcompute_Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)



class Batchcompute_Request_Data_Filler(Request_Data_Filler):

        # self.aaop_list = aaop_list
        # self.entity = entity
        # self.project = project

## See:  configuration/main_api.py

    # No data to fill here.
    def process(self, transaction) -> List[AAOP]:
        for aaop in self.aaop_list:
            if aaop.Dictionary_Name=='SubmitJob':
                from gemsModules.batchcompute.services.SubmitJob import api
                this_Project : Batchcompute_Project = self.project
                aaop.The_AAO.inputs.pUUID=this_Project.pUUID

        return self.aaop_list
