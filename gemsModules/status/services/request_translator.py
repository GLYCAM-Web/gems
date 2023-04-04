#!/usr/bin/env python3
from typing import Union, List

from gemsModules.status.main_api import Status_Transaction
from gemsModules.status.main_api import Status_API
from gemsModules.status.main_api import Status_Entity

from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.common.action_associated_objects import AAOP

class JSON_to_Service_Request_translator():
    """ Inspect the incoming JSON object to figure out which services need 
        to be run.  Bundle these into a service request package tree.
    """

    def __init__(self, transaction: Delegator_Transaction):
        self.transaction = transaction
        self.aaop_list = []

    def process(self):
        self.copy_explicit_services()
        self.add_implicit_services()
        return self.get_aaop_list()

    def copy_explicit_services(self):
        if self.transaction.inputs.entity.services.__root__ is not None:
            the_root = self.transaction.inputs.entity.services.__root__ 
            for supplied_name in the_root:
                service_request = the_root[supplied_name]
                this_aaop = AAOP(Dictionary_Name=supplied_name, The_AAO=service_request)
                print(this_aaop)
                self.aaop_list.append(this_aaop)
   
    def add_implicit_services(self):
        pass

    def get_aaop_list(self):
        return self.aaop_list


class Manage_Raw_Services_Package_List():

    def __init__(self, aaop_list : List[AAOP]):
        #self.aaop_list = aaop.list
        pass
        
    def sort_services_by_type(self):
        pass

    def manage_duplicate_services(self):
        pass 

class Request_to_task_input_translator():
    pass