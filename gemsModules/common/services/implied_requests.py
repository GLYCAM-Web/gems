#!/usr/bin/env python3
from typing import Union, List, Protocol, Dict
from abc import ABC, abstractmethod

from gemsModules.common.main_api_resources import Resource
from gemsModules.common.main_api_procedural_options import Procedural_Options
from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


class Implied_Services_Inputs(Protocol):
    inputs : Union[Dict,Resource] 
    procedural_options : Procedural_Options
    options : Dict[str,str]


class Implicit_Service_Request_Manager(ABC):
    """ Inspect the incoming JSON object to figure out which services need 
        to be run.  Bundle these into a service request package list.
    """

    @abstractmethod
    def add_implicit_services(self, 
            implied_services_inputs : Implied_Services_Inputs) -> List[AAOP]:
        pass

    def get_aaop_list(self):
        return self.aaop_list

