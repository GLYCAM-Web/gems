#!/usr/bin/env python3
from pydantic import BaseModel, Field, validator
from gemsModules.docs.microcosm.common.main_api_notices import Notices
from gemsModules.docs.microcosm.common.main_api_services import Services, Responses
from gemsModules.docs.microcosm.common.main_api_resources import Resources
from gemsModules.docs.microcosm.common import main_settings

from gemsModules.docs.microcosm.common import loggingConfig 

if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

class Entity(BaseModel):
    """Holds information about the main object responsible for a service."""
    entityType : str = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )
    services : Services = Services()
    responses : Responses = Responses()
    resources : Resources = Resources()
    notices : Notices = Notices()

    @validator('entityType')
    def checkEntityType(cls, v):
        """This will be overridden by redirector in delegator."""
        if v != main_settings.WhoIAm:
            raise ValueError(f"The requested entity, {v}, is not {main_settings.WhoIAm}.")
        return v

def generateSchema():
    print(Entity.schema_json(indent=2))

if __name__ == "__main__":
    generateSchema()