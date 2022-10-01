#!/usr/bin/env python3
from pydantic import BaseModel
from ..common import main_api_services

class inputs (BaseModel):
    A_int : int = 0
    A_string : str = ""

class outputs (BaseModel):
    A_bool : bool = False

class ServiceA_Service (main_api_services.Service) :
    inputs : inputs = None

class ServiceA_Response (main_api_services.Response) :
    outputs : outputs = None


