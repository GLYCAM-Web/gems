#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.request_data_filler import Request_Data_Filler

from gemsModules.TEMPLATE.main_api import Template_Entity
from gemsModules.TEMPLATE.main_api_project import TemplateProject

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class template_Request_Data_Filler(Request_Data_Filler):

        # self.aaop_list = aaop_list
        # self.entity = entity
        # self.project = project

    # No data to fill here.
    def process(self) -> List[AAOP]:
        for aaop in self.aaop_list:
            if aaop.Dictionary_Name=='template_service':
                from gemsModules.template.services.template_service import api
                this_Project : TemplateProject = self.project
                aaop.The_AAO.inputs.pUUID=this_Project.pUUID

        return self.aaop_list
