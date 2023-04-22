#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.main_api_entity import Entity
from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Explicit_Service_Request_Manager():
    """ Inspect the incoming JSON object to figure out which services need 
        to be run.  Bundle these into a service request package list.
    """

    def __init__(self, entity: Entity):
        self.entity = entity
        self.aaop_list : List[AAOP] = []

    def process(self):
        if self.entity.services.__root__ is None:
            return []
        else: 
            self.copy_explicit_services()
            return self.get_aaop_list()

    def copy_explicit_services(self):
        if self.entity.services.__root__ is not None:
            the_root = self.entity.services.__root__ 
            for supplied_name in the_root:
                service_request = the_root[supplied_name]
                this_aaop = AAOP(Dictionary_Name=supplied_name, 
                        ID_String=uuid.uuid4(),
                        The_AAO=service_request,
                        AAO_Type=service_request.typename)
                self.aaop_list.append(this_aaop)


    def get_aaop_list(self):
        return self.aaop_list
    