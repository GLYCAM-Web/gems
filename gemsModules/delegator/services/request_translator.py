#!/usr/bin/env python3
from typing import Union, List

from gemsModules.delegator.main_api import Delegator_Transaction
from gemsModules.delegator.services.marco.api import marco_Request
from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class JSON_to_Service_Request_translator():
    """ Inspect the incoming JSON object to figure out which services need 
        to be run.  Bundle these into a service request package list.
    """

    def __init__(self, transaction: Delegator_Transaction):
        self.transaction = transaction
        self.aaop_list : List[AAOP] = []
        from gemsModules.delegator.tasks import get_services_list
        self.available_services = get_services_list.execute()

    def process(self):
        self.copy_explicit_services()
        self.add_implicit_services()
        return self.get_aaop_list()

    def copy_explicit_services(self):
        if self.transaction.inputs.entity.services.__root__ is not None:
            the_root = self.transaction.inputs.entity.services.__root__ 
            for supplied_name in the_root:
                service_request = the_root[supplied_name]
                this_aaop = AAOP(Dictionary_Name=supplied_name, 
                        The_AAO=service_request,
                        AAO_Type=service_request.typename)
                print(this_aaop)
                self.aaop_list.append(this_aaop)
   
    def add_implicit_services(self):

        if self.transaction.inputs.entity.services.__root__ is None:
            service_request = marco_Request()
            this_aaop = AAOP(Dictionary_Name='implied_marco', 
                    The_AAO=service_request,
                    AAO_Type='Marco')
            print(this_aaop)
            self.aaop_list.append(this_aaop)

        if self.inputs.entity.inputs is not None:  
            if Union[ 'cake', 'color' ] in self.inputs.entity.inputs.keys() :
                service_request = marco_Request()
                service_request.options = {}
                if 'cake' in self.inputs.entity.inputs.keys() :
                    service_request.options["cake"]=self.inputs.entity.inputs["cake"]
                if 'color' in self.inputs.entity.inputs.keys() :
                    service_request.options["color"]=self.inputs.entity.inputs["color"]
                this_aaop = AAOP(Dictionary_Name='cake_marco', 
                        The_AAO=service_request
                        AAO_Type='Marco')
                print(this_aaop)
                self.aaop_list.append(this_aaop)

    def get_aaop_list(self):
        return self.aaop_list


class Manage_Raw_Services_Package_List():


    def __init__(self, aaop_list : List[AAOP]):
        self.aaop_list = aaop_list


    def get_all_of_type_in_AAOP_list(self, AAO_Type : str):
        aaop_type_list : List[AAOP] = []
        for item in self.aaop_list:
            if item.AAO_Type == AAO_Type :
                aaop_type_list.append(item)
        return aaop_type_list


    def manage_unknown_services(self):
        unknown_services : List[str]  = []
        for item in self.aaop_list :
            if item.AAO_Type not in Union [ self.available_services, 'Error' ] :
                unknown_services.append(item.AAO_Type)
                self.aaop_list.remove(item)
        if len(unknown_services) != 0 :
            from gemsModules.delegator.services.error.api import error_Request
            this_request = error_Request()
            this_request.options = {}
            this_request.options['unknown_services'] = 'Unknown services found in the request.'
            this_request.options['the_unknown_services'] = str(unknown_services)
            this_aaop = AAOP(Dictionary_Name='error', 
                    The_AAO=this_request
                    AAO_Type='Error')
            self.aaop_list.append(this_aaop)
            

    def manage_duplicate_services(self):
        for service_type in self.available_services :
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


