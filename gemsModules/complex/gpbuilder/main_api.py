#!/usr/bin/env python3

from typing import Union
from pydantic import Field
from pydantic.typing import Literal, Dict, Any

from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services
from gemsModules.common.main_api_resources import Resources

from gemsModules.complex.gpbuilder.main_settings import WhoIAm
from gemsModules.complex.gpbuilder.main_api_project import GpProject
from gemsModules.complex.gpbuilder.main_api_common import GpBuilder_Service_Request, GpBuilder_Service_Response
from gemsModules.complex.gpbuilder.services.settings.known_available import (
    Available_Services,
)
from .services.ProjectManagement.api import ProjectManagement_Request, ProjectManagement_Response

from .services.Validate.api import Validate_Request, Validate_Response
from .services.Evaluate.api import Evaluate_Request, Evaluate_Response
from .services.Build.api import Build_Request, Build_Response

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class GpBuilder_Service_Requests(main_api_services.Service_Requests):
    __root__: dict[str, GpBuilder_Service_Request] = None


class GpBuilder_Service_Responses(main_api_services.Service_Responses):
    __root__: dict[str, GpBuilder_Service_Response] = None


class GpBuilder_Entity(main_api_entity.Entity):
    entityType: Literal[
        "GpBuilder"
    ] = Field(  # This is the only required field in all of the API
        ..., title="Type", alias="type"
    )
    services: GpBuilder_Service_Requests = GpBuilder_Service_Requests()
    responses: GpBuilder_Service_Responses = GpBuilder_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to complex.gpbuilder
class GpBuilder_API(main_api.Common_API):
    entity: GpBuilder_Entity
    project: GpProject = GpProject()


class GpBuilder_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return GpBuilder_API
