#!/usr/bin/env python3
from pydantic import validator, Field, typing
from gemsModules.common import main_api, main_api_entity, main_api_services
from gemsModules.common.main_api_services import GenericServiceRequests

from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.delegator.services.settings.known_available import Available_Services
from gemsModules.delegator.redirector_settings import Known_Entities


from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Delegator_Entity(main_api_entity.Entity):
    entityType: WhoIAm = Field(  # This is the only required field in all of the API
        ..., title="Type", alias="type"
    )
    # Delegator overrides services so that it's own available services are used, which includes the common services too.
    services: GenericServiceRequests[Available_Services] = GenericServiceRequests()


# The Delegator uses the main_api.Transaction class to define the transaction
class Delegator_API(main_api.Common_API):
    entity: Delegator_Entity


class Delegator_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return Delegator_API


# The Redirector just redirects the transaction to the appropriate service module
class Redirector_Entity(main_api_entity.Entity):
    inputs: typing.Any = None
    services: typing.Any = None
    responses: typing.Any = None
    resources: typing.Any = None
    notices: typing.Any = None

    @validator("entityType")
    def checkEntityType(cls, v):
        if v not in Known_Entities.__members__.values():
            raise ValueError(
                f"From Delegator: The requested entity, {v}, is not known. Use entity 'Delegator' and service 'KnownEntities' to get a list of known entities"
            )
        return v


class Redirector_API(main_api.Common_API):
    entity: Redirector_Entity
    project: typing.Any = None
    notices: typing.Any = None


class Redirector_Transaction(Delegator_Transaction):
    def get_API_type(self):
        return Redirector_API
