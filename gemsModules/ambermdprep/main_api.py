#!/usr/bin/env python3
from typing import Dict

from pydantic import Field, typing

from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.ambermdprep.main_api_project import AmberMDPrepProject
from gemsModules.ambermdprep.services.settings.known_available import Available_Services

from gemsModules.ambermdprep.main_settings import WhoIAm

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class AmberMDPrep_Service_Request(main_api_services.Service_Request):
    typename: Available_Services = Field(
        "AmberMDPrep",
        alias="type",
        title="Services Offered by AmberMDPrep",
        description="The service requested of the AmberMDPrep Servicer",
    )


class AmberMDPrep_Service_Response(main_api_services.Service_Response):
    typename: Available_Services = Field(
        None,
        alias="type",
        title="Services Offered by AmberMDPrep",
        description="The service response from AmberMDPrep",
    )


class AmberMDPrep_Service_Requests(main_api_services.Service_Requests):
    __root__: Dict[str, AmberMDPrep_Service_Request] = None


class AmberMDPrep_Service_Responses(main_api_services.Service_Responses):
    __root__: Dict[str, AmberMDPrep_Service_Response] = None


class AmberMDPrep_Entity(main_api_entity.Entity):
    entityType: typing.Literal[
        "AmberMDPrep"
    ] = Field(  # This is the only required field in all of the API
        ..., title="Type", alias="type"
    )
    services: AmberMDPrep_Service_Requests = AmberMDPrep_Service_Requests()
    responses: AmberMDPrep_Service_Responses = AmberMDPrep_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to mmservice.mdaas
class AmberMDPrep_API(main_api.Common_API):
    entity: AmberMDPrep_Entity
    project: AmberMDPrepProject = AmberMDPrepProject()


class AmberMDPrep_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return AmberMDPrep_API
