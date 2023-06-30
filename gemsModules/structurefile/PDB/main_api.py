#!/usr/bin/env python3
from typing import Dict

from pydantic import Field, typing

from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.structurefile.PDB.main_api_project import PDB_Project
from gemsModules.structurefile.PDB.services.settings.known_available import (
    Available_Services,
)
from gemsModules.structurefile.PDB.main_settings import WhoIAm

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDB_Service_Request(main_api_services.Service_Request):
    typename: Available_Services = Field(
        "PDB",
        alias="type",
        title="Services offered by PDB Entity",
        description="The service requested of the PDB Servicer",
    )


class PDB_Service_Response(main_api_services.Service_Response):
    typename: Available_Services = Field(
        None,
        alias="type",
        title="Services offered by PDB Entity",
        description="The service response from PDB",
    )


class PDB_Service_Requests(main_api_services.Service_Requests):
    __root__: Dict[str, PDB_Service_Request] = None


class PDB_Service_Responses(main_api_services.Service_Responses):
    __root__: Dict[str, PDB_Service_Response] = None


class PDB_Entity(main_api_entity.Entity):
    entityType: typing.Literal[
        "PDB"
    ] = Field(  # This is the only required field in all of the API
        ..., title="Type", alias="type"
    )
    services: PDB_Service_Requests = PDB_Service_Requests()
    responses: PDB_Service_Responses = PDB_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to mmservice.mdaas
class PDB_API(main_api.Common_API):
    entity: PDB_Entity
    project: PDB_Project = PDB_Project()


class PDB_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return PDB_API
