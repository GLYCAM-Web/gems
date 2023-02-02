#!/usr/bin/env python3
from pydantic import BaseModel, Field

from gemsModules.common.main_api_services import Service, Response
from gemsModules.logging.logger import Set_Up_Logging 

log = Set_Up_Logging(__name__)

class marco_Inputs(BaseModel) :
    entity : str  = Field(
        None,
        description="The entity to which the Marco request is sent.")
    who_I_am : str = Field(
        None,
        description="The name of the entity receiving the Marco request.  Written by GEMS.")
    
class marco_Outputs(BaseModel) :
    message : str  = Field(
        None,
        description="The response to the Marco request.")

class marco_Service(Service) :
    typename : str  = "Marco"
    inputs : marco_Inputs = marco_Inputs()

class marco_Response(Response) :
    typename : str  = "Marco"
    outputs : marco_Outputs = marco_Outputs()
