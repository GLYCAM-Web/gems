#!/usr/bin/env python3
from typing import Literal
from pydantic import BaseModel
from ..common import main_api_services

## These first two classes cannot simply be 'inputs' and 'outputs' This is 
## because of JSON, not Python.  In the JSON, it is necessary to have a 
## unique name for each service's inputs and outputs.  Since Pydantic
## uses the class name as the name for the definition in the JSON schema,
## these must be unique.  They probably need to be unique across entities.

class ServiceA_inputs (BaseModel):
    A_int : int = 0
    A_string : str = ""

class ServiceA_outputs (BaseModel):
    A_bool : bool = False

class ServiceA_Service (main_api_services.Service) :
    typename : Literal['ServiceA'] = "ServiceA"
    inputs : ServiceA_inputs = ServiceA_inputs()

class ServiceA_Response (main_api_services.Response) :
    typename : Literal['ServiceA']
    outputs : ServiceA_outputs = ServiceA_outputs()


