#!/usr/bin/env python3
from typing import Union, List

from gemsModules.delegator.main_api import Delegator_Transaction
from gemsModules.delegator.main_api import Delegator_API
from gemsModules.delegator.main_api import Delegator_Entity
from gemsModules.common.action_associated_objects import AAOP

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

def translate_incoming_JSON_into_a_service_request_package_tree(
        transaction : Delegator_Transaction
        ) ->  (str, Union[str, List[AAOP]]):
    """ Inspect the incoming JSON object to figure out which services need 
        to be run.  Bundle these into a service request package tree.
    """
#    if transaction.inputs.entity.services.__root__ is None:
#        print("It is none!")
#        print(transaction.inputs.entity.services)
#    else: 
#        print("It is not none")
#        print(transaction.inputs.entity.services)

    aaop_list = []
    # First, add any explicit Service Requests
    if transaction.inputs.entity.services.__root__ is not None:
        the_root = transaction.inputs.entity.services.__root__ 
        for supplied_name in the_root:
            service_request = the_root[supplied_name]
            this_aaop = AAOP(Dictionary_Name=supplied_name, The_AAO=service_request)
            print(this_aaop)
            aaop_list.append(this_aaop)

    # See if there are duplicates and if duplicates are allowed

    # Next scan the implicit service info


template_API = Delegator_API.construct(entity=Delegator_Entity.construct(entityType='Delegator'))
#self.outputs = self.get_API_type(self).construct(entity=Entity.construct(entityType=settings_main.WhoIAm))


#JSON_to_Service_Request_mapping={
#        template_API.entity.inputs['cake'] : "yay"
#        }


class JSON_to_Service_Request_translator():
    pass



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
    translate_incoming_JSON_into_a_service_request_package_tree(this_transaction)


#this_transaction = Delegator_Transaction()
#this_transaction.process_incoming_string(in_string=json_input_for_plain_explicit_test)
#translate_incoming_JSON_into_a_service_request_package_tree(this_transaction)
