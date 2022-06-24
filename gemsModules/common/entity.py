#!/usr/bin/env python3
from pydantic import BaseModel, Field
from gemsModules.common.notices import Notices
from gemsModules.common.services_responses import Services, Responses
from gemsModules.common.resources import Resources
from gemsModules.common.options import Options

from gemsModules.common import loggingConfig 
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

class Entity(BaseModel):
    """Holds information about the main object responsible for a service."""
    entityType : str = Field(
            ...,
            title='Type',
            alias='type'
            )
    requestID : str = Field(
            None,
            title = 'Request ID',
            description = 'User-specified ID that will be echoed in responses.'
            )
    services : Services = Services()
    responses : Responses = Responses()
    resources : Resources = Resources()
    notices : Notices = Notices()
    options : Options = Options()

def generateSchema():
    import json
    print(Entity.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()
