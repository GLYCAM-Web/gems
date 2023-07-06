#!/usr/bin/env python3
from typing import Dict

from pydantic import Field, typing

from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.structurefile.PDBFile.main_api_project import PDBFile_Project
from gemsModules.structurefile.PDBFile.services.settings.known_available import (
    Available_Services,
)
from gemsModules.structurefile.PDBFile.main_settings import WhoIAm

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class PDBFile_Service_Request(main_api_services.Service_Request):
    typename: Available_Services = Field(
        "PDBFile",
        alias="type",
        title="Services offered by PDB Entity",
        description="The service requested of the PDB Servicer",
    )


class PDBFile_Service_Response(main_api_services.Service_Response):
    typename: Available_Services = Field(
        None,
        alias="type",
        title="Services offered by PDB Entity",
        description="The service response from PDB",
    )


class PDBFile_Service_Requests(main_api_services.Service_Requests):
    __root__: Dict[str, PDBFile_Service_Request] = None


class PDBFile_Service_Responses(main_api_services.Service_Responses):
    __root__: Dict[str, PDBFile_Service_Response] = None


class PDBFile_Entity(main_api_entity.Entity):
    entityType: typing.Literal[
        "PDBFile"
    ] = Field(  # This is the only required field in all of the API
        ..., title="Type", alias="type"
    )
    services: PDBFile_Service_Requests = PDBFile_Service_Requests()
    responses: PDBFile_Service_Responses = PDBFile_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to mmservice.mdaas
class PDBFile_API(main_api.Common_API):
    entity: PDBFile_Entity
    project: PDBFile_Project = PDBFile_Project()


class PDBFile_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return PDBFile_API
