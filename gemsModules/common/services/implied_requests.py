#!/usr/bin/env python3
from typing import Union, List, Protocol, Dict, Callable
from abc import ABC, abstractmethod

from gemsModules.common.main_api_resources import Resource
from gemsModules.common.main_api_procedural_options import Procedural_Options
from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


# The following are the required inputs.  They are satisfied by an Entity.
# Using a protocol means that it need not be an Entity, but it must have
# the same attributes.
class Implied_Services_Inputs(Protocol):
    inputs : Union[Dict,Resource] 
    procedural_options : Procedural_Options
    options : Dict[str,str]


class Implied_Services_Request_Manager(ABC):
    """ Inspect the incoming JSON object to figure out which services need 
        to be run.  Bundle these into a service request package list.
    """

    def __init__(self, input_object : Implied_Services_Inputs):
        log.info("In Implied_Services_Request_Manager, init")
        self.aaop_list : List[AAOP] = []
        self.input_object = input_object

    @abstractmethod
    def get_available_services(self) -> List[str]:
        pass

    @abstractmethod
    def get_implicit_service_manager(self, service : str) -> Callable:
        pass

    def process(self) -> List[AAOP]:  
        """ Process the incoming JSON object to figure out which services 
            need to be run.  Bundle these into a service request package list.
        """
        log.debug("In Implied_Services_Request_Manager, process")
        for service in self.get_available_services():
            this_service_manager = self.get_implicit_service_manager(service)()
            log.debug("Processing the following service for implied requests: " + str(service))
            this_service_manager.process(input_object=self.input_object)
            self.aaop_list.extend(this_service_manager.get_aaop_list())
        return self.get_aaop_list()

    def get_aaop_list(self):
        return self.aaop_list


class common_Implied_Services_Request_Manager(Implied_Services_Request_Manager):

    def get_available_services(self) -> List[str]:
        return ["common"]
    
    def get_implicit_service_manager(self, service: str) -> Callable:
        pass
