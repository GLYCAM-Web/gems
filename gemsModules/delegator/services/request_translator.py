#!/usr/bin/env python3
from typing import Union, List

from gemsModules.delegator.main_api import Delegator_Transaction
from gemsModules.delegator.main_api import Delegator_API
from gemsModules.delegator.main_api import Delegator_Entity
from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

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
        self.aaop_list = aaop.list

    def sort_services_by_type(self):
        pass

    def manage_duplicate_services(self):
        pass 

    # See if there are duplicates and if duplicates are allowed
    
    


#template_API = Delegator_API.construct(entity=Delegator_Entity.construct(entityType=WhoIAm))







class Request_to_task_input_translator():
    pass


json_input_for_plain_explicit_test='''{
 "entity" : {
    "type": "Delegator",
    "services" :
        { "Marco" :
                {
                        "type" : "Marco" 
                 
                }
        }
  }
}'''
json_input_for_cake_implicit_test='''{
 "entity" : {
    "type": "Delegator",
        "inputs" : {
            "cake" : "true",
            "color" : "pink"
        }
  }
}'''
json_input_for_cake_conflicting_test='''{
 "entity" : {
    "type": "Delegator",
        "inputs" : {
            "cake" : "true",
            "color" : "pink"
        },
        "services" :
        { "cakeMarco" :
                {
                        "type" : "Marco" ,
                        "options" : {
                                "cake" : "false",
                                "color" : "pink"
                        }

                }
        }
  }
}'''

for i in json_input_for_plain_explicit_test, json_input_for_cake_implicit_test, json_input_for_cake_conflicting_test :
    this_transaction = Delegator_Transaction()
    this_transaction.process_incoming_string(in_string=i)
    translator = JSON_to_Service_Request_translator(this_transaction)
    translator.copy_explicit_services()


