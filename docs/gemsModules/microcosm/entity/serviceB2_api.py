#!/usr/bin/env python3
from typing import Literal
from pydantic import BaseModel
from ..common import main_api_services

class ServiceB2_inputs (BaseModel):
    B2_int : int = 8
    B2_string : str = "B2"

class ServiceB2_outputs (BaseModel):
    B2_bool : bool = True


class ServiceB2_Service (main_api_services.Service) :
    typename : Literal['ServiceB2']
    inputs : ServiceB2_inputs = None

class ServiceB2_Response (main_api_services.Response) :
    typename : Literal['ServiceB2']
    outputs : ServiceB2_outputs = None

