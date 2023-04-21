#!/usr/bin/env python3
from typing import List
from abc import ABC

from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Duplicate_Services_Manager(ABC):

    def __init__(self, aaop_list : List[AAOP], service_type : str):
        self.aaop_list = aaop_list
        self.service_type = service_type

    def process_multiples_action_All(self):
        return self.aaop_list # nothing to do here as of now

    def process_multiples_action_Fail(self):
        this_request = error_Request()
        this_request.options = {}
        this_request.options['disallowed_multiples'] = 'Multiples of a service are requested, but multiples are not allowed.'
        this_request.options['the_relevant_service'] = self.service_type
        this_aaop = AAOP(Dictionary_Name='error', 
                The_AAO=this_request,
                AAO_Type='Error')
        this_aaop_list = [] 
        this_aaop_list.append(this_aaop) 
        return this_aaop_list

    def process_multiples_action_Merge(self):
        """ Eventually, this should actually check if multiple requests can be merged.  
        For now, I'm in a hurry, so multiples that cannot coexist will all fail.  
        Please be specific with service requests. BLF """
        return self.process_multiples_action_Fail()


    def process_conflicted_merge(self):
        pass



