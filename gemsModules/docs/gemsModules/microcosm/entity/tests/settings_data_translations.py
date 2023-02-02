#!/usr/bin/env python3
from gemsModules.docs.microcosm.entity import settings_data_translations, main_api
from gemsModules.docs.microcosm.entity import serviceA_api

input_json='''{
"entity" : {
        "type" : "Module_Entity",
        "inputs" : {
                "string_A" : "hello, world!",
                "int_A" :  "12345"
            }
    }
}'''

this_Transaction = main_api.Module_Transaction()
this_Transaction.process_incoming_string(in_string=input_json)
print("the transaction inptus are ")
print(this_Transaction.inputs.dict())

this_Service = serviceA_api.ServiceA_Service()
print("the service is")
print(this_Service)


this_Service_response = settings_data_translations.generate_ServiceA_Service(this_Transaction)

print("the returned tuple is")
print(this_Service_response)
