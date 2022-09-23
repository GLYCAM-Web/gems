#!/usr/bin/env python3

from textwrap import indent
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

class local_Transaction (Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
       return Common_API

this_Transaction = local_Transaction()
this_Transaction.process_incoming_string(in_string=json_Input)

the_Service = input_translator(this_Transaction)


the_Response = Serve(the_Service)

## The following is one of the things the Main Servicer will do.
## That is, it will keep up with the names given each service.
servicewrapper = list(this_Transaction.inputs.entity.services)[0]
service = servicewrapper[1]
service_name = list(service.keys())[0]
the_wrapped_service = {service_name : the_Service.dict()}
the_wrapped_response = {service_name : the_Response.dict()}

import json

the_output = json.dumps(the_wrapped_response, indent=2)

#print(f"the wrapped service is: {json.dumps(the_wrapped_service, indent=2)}")
#print(f"the wrapped response is: {the_output}")

expected_output = '''{
  "isAnybodyHome": {
    "typename": null,
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