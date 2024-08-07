#!/usr/bin/env python3
from typing import List
import uuid

from gemsModules.common.main_api_entity import Entity
from gemsModules.common.main_api_services import Service_Request
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
        log.debug("In Explicit_Service_Request_Manager, process")
        if self.entity.services.__root__ is None:
            log.debug("In Explicit_Service_Request_Manager, process, no services")
            return []
        else: 
            self.copy_explicit_services()
            the_aaop_list=self.get_aaop_list()
            log.debug("In Explicit_Service_Request_Manager, process, returning aaop list:")
            for item in the_aaop_list:
                log.debug(item)
            return the_aaop_list

    def copy_explicit_services(self):
        the_root = self.entity.services.__root__ 
        log.debug("In Explicit_Service_Request_Manager, copy_explicit_services")
        log.debug("the_root is: ")
        log.debug(the_root)
        for supplied_name in the_root:
            log.debug("the supplied name is: " + supplied_name)
            service_request: Service_Request = self.validate_service_request(the_root[supplied_name].copy(deep=True))
            log.debug("the service request is: ")
            log.debug(service_request)
            this_aaop = AAOP(Dictionary_Name=supplied_name, 
                    ID_String=uuid.uuid4(),
                    The_AAO=service_request,
                    AAO_Type=service_request.typename)
            log.debug("the aaop is: ")
            log.debug(this_aaop)
            log.debug("done printing the aaop")
            self.aaop_list.append(this_aaop)

    def validate_service_request(self, service_request):
        return service_request


    def get_aaop_list(self):
        return self.aaop_list
    