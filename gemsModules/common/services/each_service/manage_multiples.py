#!/usr/bin/env python3
from typing import List
from abc import ABC, abstractmethod

from gemsModules.common.action_associated_objects import AAOP
from gemsModules.common.main_api_services import Service_Request

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Multiples_Manager(ABC):

    def __init__(self, aaop_list : List[AAOP]):
        self.incoming_aaop_list = aaop_list
        self.processed_aaop_list : List[AAOP] = []

    @abstractmethod
    def process_multiples(self) -> List[AAOP]:
        pass

    def process_multiples_action_All(self):
        self.processed_aaop_list=self.incoming_aaop_list # nothing to do here as of now

    def process_multiples_action_First(self):
        self.processed_aaop_list.append(self.incoming_aaop_list[0]) # nothing to do here as of now

    def process_multiples_action_Last(self):
        self.processed_aaop_list.append(self.incoming_aaop_list[-1]) # nothing to do here as of now

    def process_multiples_action_Fail(self):
        this_request = Service_Request(typename='Error')
        this_request.options = {}
        this_request.options['disallowed_multiples'] = 'Multiples of a service are requested, but multiples are not allowed.'
        this_request.options['the_relevant_service'] = self.service_type
        this_aaop = AAOP(Dictionary_Name='Error', 
                The_AAO=this_request,
                AAO_Type='Error')
        self.processed_aaop_list.append(this_aaop) 

    def process_multiples_action_Merge(self):
        """ This should be overridden if used, but it's not an abstract method.
        """
        raise NotImplementedError



