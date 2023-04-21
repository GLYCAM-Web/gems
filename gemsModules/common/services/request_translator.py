#!/usr/bin/env python3
from typing import Union, List, Protocol, Dict
from abc import ABC, abstractmethod
import uuid

from gemsModules.common.main_api import Transaction
from gemsModules.common.main_api_resources import Resource
from gemsModules.common.main_api_procedural_options import Procedural_Options
from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Implied_Services_Inputs(Protocol):
    inputs : Union[Dict,Resource] 
    procedural_options : Procedural_Options
    options : Dict[str,str]

class JSON_to_Service_Request_translator(ABC):
    """ Inspect the incoming JSON object to figure out which services need 
        to be run.  Bundle these into a service request package list.
    """

    def __init__(self, transaction: Transaction):
        self.transaction = transaction
        self.aaop_list : List[AAOP] = []

    def process(self):
        if self.transaction.inputs.entity.services.__root__ is None:
            self.add_default_services()
        else: 
            self.copy_explicit_services()
        self.add_implicit_services()
        return self.get_aaop_list()

    def copy_explicit_services(self):
        if self.transaction.inputs.entity.services.__root__ is not None:
            the_root = self.transaction.inputs.entity.services.__root__ 
            for supplied_name in the_root:
                service_request = the_root[supplied_name]
                this_aaop = AAOP(Dictionary_Name=supplied_name, 
                        ID_String=uuid.uuid4(),
                        The_AAO=service_request,
                        AAO_Type=service_request.typename)
                self.aaop_list.append(this_aaop)

    @abstractmethod
    def add_default_services(self) -> List[AAOP]:
        pass

    @abstractmethod
    def add_implicit_services(self, 
            implied_services_inputs : Implied_Services_Inputs) -> List[AAOP]:
        pass

    def get_aaop_list(self):
        return self.aaop_list

