#!/usr/bin/env python3
from typing import Literal
from pydantic import BaseModel
from ..common import main_api_services

class ServiceB1_inputs (BaseModel):
    B1_int : int = 3
    B1_string : str = "B"

class ServiceB1_outputs (BaseModel):
    B1_bool : bool = False


class ServiceB1_Service (main_api_services.Service) :
    typename : Literal['ServiceB1']
    inputs : ServiceB1_inputs = None

class ServiceB1_Response (main_api_services.Response) :
    typename : Literal['ServiceB1']
    outputs : ServiceB1_outputs = None

