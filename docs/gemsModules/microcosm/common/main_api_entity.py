#!/usr/bin/env python3
from pydantic import BaseModel, Field, validator, Json
from .main_api_notices import Notices
from .main_api_services import Services, Responses
from .main_api_resources import Resources
from . import settings_main

from . import loggingConfig 

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
    inputs : Json = Field(
            None,
            title='Inputs',
            description='User-friendly, top-level inputs to the services.'
    )
    outputs : Json = Field(
            None,
            title='Inputs',
            description='User-friendly, top-level outputs from the services.'
    )
    services : Services = Services()
    responses : Responses = Responses()
    resources : Resources = Resources()
    notices : Notices = Notices()

### This breaks because 'settings' can't be forced to change in children.... or can it?
#    @validator('entityType')
#    def checkEntityType(cls, v):
#        """This will be overridden by redirector in delegator."""
#        if v != settings_main.WhoIAm:
#            raise ValueError(f"The requested entity, {v}, is not {settings_main.WhoIAm}.")
#        return v

def generateSchema():
    print(Entity.schema_json(indent=2))
