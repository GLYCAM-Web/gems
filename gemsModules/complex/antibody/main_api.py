from typing import Literal
from pydantic import Field
from pydantic.typing import Literal as pyLiteral

from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.complex.antibody.main_settings import WhoIAm
from gemsModules.complex.antibody.main_api_project import AntibodyProject

from .main_api_common import (
    Antibody_Service_Request,
    Antibody_Service_Response,
)

from .services.Analyze.api import Analyze_Request, Analyze_Response
from .services.Build.api import Build_Request, Build_Response
from .services.Evaluate.api import Evaluate_Request, Evaluate_Response
from .services.ProjectManagement.api import (
    ProjectManagement_Request,
    ProjectManagement_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Antibody_Service_Requests(main_api_services.Service_Requests):
    __root__: dict[
        str,
        Evaluate_Request,
        Build_Request,
        ProjectManagement_Request,
        Analyze_Request,
        Antibody_Service_Request,
    ] = None


class Antibody_Service_Responses(main_api_services.Service_Responses):
    # __root__: dict[str, Build_Response, Validate_Response, Evaluate_Response, Analyze_Response, ProjectManagement_Response, Antibody_Service_Response] = None
    __root__: dict[str, Antibody_Service_Response] = None


class Antibody_Entity(main_api_entity.Entity):
    entityType: Literal["AntibodyDocking"] = (
        Field(  # This is the only required field in all of the API
            ..., title="Type", alias="type"
        )
    )
    services: Antibody_Service_Requests = Antibody_Service_Requests()
    responses: Antibody_Service_Responses = Antibody_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to mmservice.Antibody
class Antibody_API(main_api.Common_API):
    entity: Antibody_Entity
    project: AntibodyProject = AntibodyProject()


class Antibody_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return Antibody_API
