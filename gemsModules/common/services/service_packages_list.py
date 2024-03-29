#!/usr/bin/env python3
from typing import Union, List

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.services.error.api import error_Request

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class Services_Package_List_Utilities():

    def __init__(self, aaop_list : List[AAOP]):
        self.aaop_list = aaop_list

    def get_all_of_type_in_AAOP_list(self, AAO_Type : str) -> List[AAOP]:
        aaop_type_list : List[AAOP] = []
        for item in self.aaop_list:
            if item.AAO_Type == AAO_Type :
                aaop_type_list.append(item)
        return aaop_type_list

    def manage_unknown_services(self, available_services : List[str]):
        unknown_services : List[str]  = []
        for item in self.aaop_list :
            if item.AAO_Type not in available_services :
                unknown_services.append(item.AAO_Type)
                self.aaop_list.remove(item)
        if len(unknown_services) != 0 :
            this_request = error_Request()
            this_request.options = {}
            this_request.options['unknown_services'] = 'Unknown services found in the request.'
            this_request.options['the_unknown_services'] = str(unknown_services)
            this_aaop = AAOP(Dictionary_Name='error', 
                    The_AAO=this_request,
                    AAO_Type='Error')
            self.aaop_list.append(this_aaop)
        return self.aaop_list

