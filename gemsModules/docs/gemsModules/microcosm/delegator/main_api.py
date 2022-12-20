#!/usr/bin/env python3
from pydantic import Json,validator
from ..common import main_api
from .redirector_settings import Known_Entities

from ..common import loggingConfig
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to the delegator
class Delegator_API(main_api.Common_API):
    pass

class Delegator_Transaction(main_api.Transaction):
    
    def get_API_type(self):  # This allows dependency injection in the children
        return Delegator_API

# The Redirector just redirects the transaction to the appropriate service module
class Redirector_Entity(main_api.Entity) :
    services  : Json = None
    responses : Json = None
    resources : Json = None
    notices   : Json = None

    @validator('entityType')
    def checkEntityType(cls, v):
        if v not in Known_Entities:
            raise ValueError(f"The requested entity, {v}, is not known.")
        return v

class Redirector_API(main_api.Common_API):
    entity  : Redirector_Entity       
    project : Json = None
    notices : Json = None

class Redirector_Transaction(Delegator_Transaction):
    
    def get_API_type(self):
        return Redirector_API

