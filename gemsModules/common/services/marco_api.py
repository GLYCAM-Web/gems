#!/usr/bin/env python3
from pydantic import BaseModel, Field

from gemsModules.common.main_api_services import Service, Response
from gemsModules.common import loggingConfig 

if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


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
    outputs : marco_Outputs
