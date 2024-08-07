#!/usr/bin/env python3

from typing import Union
from pydantic import Field
from pydantic.typing import Literal, Dict, Any

from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services
from gemsModules.common.main_api_resources import Resources

from gemsModules.mmservice.mdaas.main_settings import WhoIAm
from gemsModules.mmservice.mdaas.main_api_project import MdProject
from gemsModules.mmservice.mdaas.main_api_common import MDaaS_Service_Request, MDaaS_Service_Response
from gemsModules.mmservice.mdaas.services.settings.known_available import (
    Available_Services,
)

from .services.Evaluate.api import Evaluate_Request, Evaluate_Response
from .services.ProjectManagement.api import ProjectManagement_Request, ProjectManagement_Response
from .services.run_md.run_md_api import run_md_Request, run_md_Response


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)



class MDaaS_Service_Requests(main_api_services.Service_Requests):
    __root__: dict[str, run_md_Request, Evaluate_Request, ProjectManagement_Request, MDaaS_Service_Request] = None


class MDaaS_Service_Responses(main_api_services.Service_Responses):
    __root__: dict[str, MDaaS_Service_Response] = None


class MDaaS_Entity(main_api_entity.Entity):
    entityType: Literal[
        "MDaaS"
    ] = Field(  # This is the only required field in all of the API
        ..., title="Type", alias="type"
    )
    services: MDaaS_Service_Requests = MDaaS_Service_Requests()
    responses: MDaaS_Service_Responses = MDaaS_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to mmservice.mdaas
class MDaaS_API(main_api.Common_API):
    entity: MDaaS_Entity
    project: MdProject = MdProject()


class MDaaS_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return MDaaS_API
