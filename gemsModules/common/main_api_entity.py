#!/usr/bin/env python3
from abc import abstractmethod
from pydantic import BaseModel, Field, validator, Json

from gemsModules.common.main_api_notices import Notices
from gemsModules.common.main_api_services import Services, Responses
from gemsModules.common.main_api_resources import Resources
from gemsModules.common import settings_main

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

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

    @abstractmethod
    def getEntityType(self):
        return settings_main.WhoIAm

    @validator('entityType') # Override this as needed
    def checkEntityType(cls, v):
        I_am = cls.getEntityType()
        if v != I_am:
            raise ValueError(f"The requested entity, {v}, is not known to {I_am}.")
        return v

def generateSchema():
    print(Entity.schema_json(indent=2))
