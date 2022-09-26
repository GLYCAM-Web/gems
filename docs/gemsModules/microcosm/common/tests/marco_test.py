#!/usr/bin/env python3

## This is an early example of the workflow.
## Many things need to be moved to other places and such.
## But, it gives an overview of the workflow.

from docs.gemsModules.microcosm.common.main_api import Common_API, Transaction
from docs.gemsModules.microcosm.common.marco_servicer import Serve
from docs.gemsModules.microcosm.common.marco_data_translator import input_translator

json_Input = '''
{
    "entity": 
    { 
        "type": "CommonServicer", 
        "services": 
        { 
                "isAnybodyHome": 
                { 
                    "type": "Marco" 
                } 
        } 
    }, 
    "prettyPrint" : true 
    }
'''

## Since Transaction is an ABC, it can't be instantiated.
## So we have to create a subclass.
class local_Transaction (Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
       return Common_API

this_Transaction = local_Transaction()
this_Transaction.process_incoming_string(in_string=json_Input)

## This is where the user-friendly data is translated into the data that the servicer needs.
the_Service = input_translator(this_Transaction)

## This is where the servicer is called.
the_Response = Serve(the_Service)

## The following is one of the things the Main Servicer will do.
## That is, it will keep up with the names given each service.
##
## The zeroth service will not always be the one that is called.
## This is just an example.
## It's a service wrapper because it contains a name and a service.
servicewrapper = list(this_Transaction.inputs.entity.services)[0]
## The zeroth thing is a name and the first thing is a service.
service = servicewrapper[1]
service_name = list(service.keys())[0]
## The services and responses in the transaction are in dictionaries.
## So, we need put them in a dictionary.
the_wrapped_service = {service_name : the_Service.dict()}
the_wrapped_response = {service_name : the_Response.dict()}
## Note that this code does not add the response or the service to 
## the outgoing part of the transaction.

import json
the_output = json.dumps(the_wrapped_response, indent=2)

#print(f"the wrapped service is: {json.dumps(the_wrapped_service, indent=2)}")
#print(f"the wrapped response is: {the_output}")

expected_output = '''{
  "isAnybodyHome": {
    "typename": "Marco",
    "givenName": null,
    "myUuid": null,
    "outputs": {
      "message": "Polo"
    },
    "notices": null
  }
}'''

if the_output == expected_output:
    print("The test passed.")

# the wrapped service is: {
#   "isAnybodyHome": {
#     "typename": "Marco",
#     "givenName": null,
#     "myUuid": null,
#     "inputs": {
#       "entity": "CommonServicer"
#     },
#     "options": null
#   }
# }
# the wrapped response is: {
#   "isAnybodyHome": {
#     "typename": null,
#     "givenName": null,
#     "myUuid": null,
#     "outputs": {
#       "message": "Polo"
#     },
#     "notices": null
#   }
# }