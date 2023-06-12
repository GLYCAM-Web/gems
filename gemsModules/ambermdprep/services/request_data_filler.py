#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.ambermdprep.main_api import AmberMDPrep_Entity
from gemsModules.mmservice.mdaas.main_api_project import MdProject

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Request_Data_Filler(Request_Data_Filler):
    # No data to fill here.
    def process(self) -> List[AAOP]:
        for aaop in self.aaop_list:
            if aaop.Dictionary_Name == "any_amber_prep":
                pass

        return self.aaop_list
