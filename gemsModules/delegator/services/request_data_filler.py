#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_entity import Entity
from gemsModules.common.services.request_data_filler import Request_Data_Filler
from gemsModules.project.main_api import Project

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class delegator_Request_Data_Filler(Request_Data_Filler):
        
    # No data to fill here.
    def process(self) -> List[AAOP]:
        return self.aaop_list
