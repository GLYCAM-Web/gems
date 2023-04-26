#!/usr/bin/env python3
## This is probably close to a realistic method for making this abstract.
## I don't have time to complete it. 

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, validator

from gemsModules.common.main_api_services import Service_Request, Service_Response

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


class marco_Inputs(ABC, BaseModel) :
    entity : str  = Field(
        None,
        description="The entity to which the Marco request is sent.")
    who_I_am : str = Field(
        None,
        description="The name of the entity receiving the Marco request.  Written by GEMS.")
    
    @validator('entity', pre=True, always=True)
    @abstractmethod
    def set_entity(cls, v):
        return 'CommonServicer'

    
class marco_Outputs(BaseModel) :
    message : str  = Field(
        None,
        description="The response to the Marco request.")

class marco_Request(ABC, Service_Request) :
    typename : str  = Field(
        "Marco",   
        alias='type'
    )
    # the following must be redefined in a child class
    inputs : marco_Inputs = marco_Inputs()

class marco_Response(Service_Response) :
    typename : str  = Field(
        "Marco",   
        alias='type'
    )
    outputs : marco_Outputs = marco_Outputs()
