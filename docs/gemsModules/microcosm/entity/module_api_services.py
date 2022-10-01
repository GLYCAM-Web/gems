#!/usr/bin/env python3
from typing import Union
from ..common import main_api_services as services_api
from . import main_settings as settings
from .serviceA_api import inputs as serviceA_inputs
from .serviceB1_api import inputs as serviceB1_inputs
from .serviceB2_api import inputs as serviceB2_inputs
from .serviceC_api import inputs as serviceC_inputs
from .serviceA_api import outputs as serviceA_outputs
from .serviceB1_api import outputs as serviceB1_outputs
from .serviceB2_api import outputs as serviceB2_outputs
from .serviceC_api import outputs as serviceC_outputs

All_The_Service_Inputs = Union [ 
        serviceA_inputs,
        serviceB1_inputs,
        serviceB2_inputs,
        serviceC_inputs 
        ]

All_The_Response_Outputs = Union [ 
        serviceA_outputs,
        serviceB1_outputs,
        serviceB2_outputs,
        serviceC_outputs 
        ]


class Module_Service(services_api.Service):
    typename : settings.All_Available_Services = None
    inputs : All_The_Service_Inputs = None

    class Config:
        smart_union = True

class Module_Response(services_api.Response):
    typename: settings.All_Available_Services = None
    outputs : All_The_Response_Outputs = None

    class Config:
        smart_union = True

def generate_schema() :
    print(Module_Service.schema_json(indent=2))
    print(Module_Response.schema_json(indent=2))
