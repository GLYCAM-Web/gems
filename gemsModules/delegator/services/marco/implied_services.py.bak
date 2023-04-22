#!/usr/bin/env python3
from typing import Union, List, Protocol
import uuid

from gemsModules.delegator.main_api import Delegator_Transaction
from gemsModules.delegator.services.marco.api import marco_Request
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
                        ID_String=uuid.uuid4(),
                        The_AAO=service_request,
                        AAO_Type=service_request.typename)
#                print(this_aaop)
                self.aaop_list.append(this_aaop)
   
    def add_implicit_services(self):

        if self.transaction.inputs.entity.services.__root__ is None:
            service_request = marco_Request()
            this_aaop = AAOP(Dictionary_Name='implied_marco', 
                    ID_String=uuid.uuid4(),
                    The_AAO=service_request,
                    AAO_Type='Marco')
#            print(this_aaop)
            self.aaop_list.append(this_aaop)

        if self.transaction.inputs.entity.inputs is not None:  
#            print("it is not none")
            this_dict = self.transaction.inputs.entity.inputs
#            print("here is the dict")
#            print(this_dict)
            if 'cake' in this_dict.keys() or 'color' in this_dict.keys() :
#                print("found cake or color")
                service_request = marco_Request()
                service_request.options = {}
                if 'cake' in self.transaction.inputs.entity.inputs.keys() :
                    service_request.options["cake"]=self.transaction.inputs.entity.inputs["cake"]
                if 'color' in self.transaction.inputs.entity.inputs.keys() :
                    service_request.options["color"]=self.transaction.inputs.entity.inputs["color"]
                this_aaop = AAOP(Dictionary_Name='implied_cake_marco', 
                        ID_String=uuid.uuid4(),
                        The_AAO=service_request,
                        AAO_Type='Marco')
#                print(this_aaop)
                self.aaop_list.append(this_aaop)

    def get_aaop_list(self):
        return self.aaop_list


class Raw_Services_Package_List_Manager():

    from gemsModules.delegator.services.error.api import error_Request
    from gemsModules.delegator.services.settings import Multiples_Action
    from gemsModules.delegator.services.settings import Request_Conflict_Action

    def __init__(self, aaop_list : List[AAOP]):
        self.aaop_list = aaop_list
        from gemsModules.delegator.tasks import get_services_list
        self.available_services = get_services_list.execute()



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
            this_request = error_Request()
            this_request.options = {}
            this_request.options['unknown_services'] = 'Unknown services found in the request.'
            this_request.options['the_unknown_services'] = str(unknown_services)
            this_aaop = AAOP(Dictionary_Name='error', 
                    The_AAO=this_request,
                    AAO_Type='Error')
            self.aaop_list.append(this_aaop)
            

    def manage_duplicate_services(self):
        duplicates : Dict[str,List[AAOP]] = {}
        for service_type in self.available_services :
            duplicates[service_type] = self.get_all_of_type_in_AAOP_list(AAO_Type=service_type)
            if len(duplicates[service_type]) > 1 :
                dup_man = Duplicate_Services_Manager(aaop_list = duplicates[service_type], service_type = service_type)



class Duplicate_Services_Manager():

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
    the_aaop_list = translator.process()
    print("here is each item in the aaop list")
    for item in the_aaop_list :
        print(item)


