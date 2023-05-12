#!/usr/bin/env python3
from collections     import namedtuple
from  .main_api      import Module_Transaction
from  .serviceA_api  import ServiceA_Service, ServiceA_Response
from  .serviceB1_api import ServiceB1_Service, ServiceB1_Response
from  .serviceB2_api import ServiceB2_Service, ServiceB2_Response
from  .serviceC_api  import ServiceC_Service, ServiceC_Response

data_translation_response = namedtuple('data_translation_response', ['service', 'return_value', 'message'])

def generate_ServiceA_Service (transaction : Module_Transaction) -> data_translation_response :
    # Here, we require valid inputs or return none.  Other services might do otherwise.
    if transaction.inputs.entity.inputs.string_A == None : 
        error="could not find string_A"
        #print(error)
        return data_translation_response(service=None,return_value=1,message=error)
    if transaction.inputs.entity.inputs.int_A == None : 
        error="could not find int_A"
        return data_translation_response(service=None,return_value=1,message=error)
    service = ServiceA_Service(typename='ServiceA')
    service.inputs.A_int = transaction.inputs.entity.inputs.int_A
    service.inputs.A_string = transaction.inputs.entity.inputs.string_A
    return data_translation_response(service=service, return_value=0, message="")
