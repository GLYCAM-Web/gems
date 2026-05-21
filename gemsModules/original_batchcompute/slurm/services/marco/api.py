#!/usr/bin/env python3
from pydantic import BaseModel, Field

from gemsModules.common.main_api_services import Service, Response
from gemsModules.common import loggingConfig 

if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


class build_submision_script_Inputs(BaseModel) :
    requesting_entity : str  = Field(
        None,
        description="The entity that initiated the request.")
    
class build_submission_script_Outputs(BaseModel) :
    message : str  = Field(
        None,
        description="The response to the Marco request.")

class build_submission_script_Service(Service) :
    typename : str  = "BuildSubmissionScript"
    inputs : marco_Inputs = marco_Inputs()

class build_submission_script_Response(Response) :
    outputs : marco_Outputs
