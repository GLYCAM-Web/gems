#!/usr/bin/env python3
from pydantic import BaseModel, Field

from gemsModules.common.main_api_services import Service_Request, Service_Response

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)

# I'm writing this non-abstractly in delegator first.  After I get it working, I'll
#    move it to common and make it abstract.
### This particular service - 'error' - must live in common bc everything needs it

class error_Inputs(BaseModel) :
    entity : str  = Field(
        'Delegator',
        description="The entity finding the error.")
    
class error_Outputs(BaseModel) :
    message : str  = Field(
        None,
        description="A response to an error in a request.")

class error_Request(Service_Request) :
    typename : str  = Field(
        "Error",   
        alias='type'
    )
    inputs : error_Inputs = error_Inputs()

class error_Response(Service_Response) :
    typename : str  = Field(
        "Error",   
        alias='type'
    )
    outputs : error_Outputs = error_Outputs()
