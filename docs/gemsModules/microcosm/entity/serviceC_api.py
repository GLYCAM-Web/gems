#!/usr/bin/env python3
from typing import Literal
from pydantic import BaseModel
from ..common import main_api_services

class ServiceC_inputs (BaseModel):
    C_int : int = 42
    C_string : str = "EVERYTHING"

class ServiceC_outputs (BaseModel):
    C_string = "Uncertainty"


class ServiceC_Service (main_api_services.Service) :
    typename : Literal['ServiceC']
    inputs : ServiceC_inputs = None

class ServiceC_Response (main_api_services.Response) :
    typename : Literal['ServiceC']
    outputs : ServiceC_outputs = None

