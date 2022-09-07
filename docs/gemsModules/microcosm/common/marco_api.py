#!/usr/bin/env python3
from pydantic import BaseModel, Field
from gemsModules.docs.microcosm.common.main_api_services import Service, Response

from gemsModules.docs.microcosm.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


class marco_Inputs(BaseModel) :
    entity : str  = Field(
        None,
        description="The entity to which the Marco request is sent.")
    
class marco_Outputs(BaseModel) :
    message : str  = Field(
        None,
        description="The response to the Marco request.")

class marco_Service(Service) :
    typename = 'Marco'
    inputs : marco_Inputs

class marco_Response(Response) :
    outputs : marco_Outputs
