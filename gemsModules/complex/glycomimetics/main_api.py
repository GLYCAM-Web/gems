from typing import Literal
from pydantic import Field
from pydantic.typing import Literal as pyLiteral

from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.complex.glycomimetics.main_settings import WhoIAm
from gemsModules.complex.glycomimetics.main_api_project import GlycomimeticsProject

from .main_api_common import (
    Glycomimetics_Service_Request,
    Glycomimetics_Service_Response,
)
from .services.Build_Selected_Positions.api import (
    Build_Selected_Positions_Request,
    Build_Selected_Positions_Response,
)
from .services.Validate.api import Validate_Request, Validate_Response
from .services.Evaluate.api import Evaluate_Request, Evaluate_Response
from .services.Analyze.api import Analyze_Request, Analyze_Response
from .services.ProjectManagement.api import (
    ProjectManagement_Request,
    ProjectManagement_Response,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Glycomimetics_Service_Requests(main_api_services.Service_Requests):
    __root__: dict[
        str,
        Build_Selected_Positions_Request,
        Validate_Request,
        Evaluate_Request,
        Analyze_Request,
        ProjectManagement_Request,
        Glycomimetics_Service_Request,
    ] = None


class Glycomimetics_Service_Responses(main_api_services.Service_Responses):
    # __root__: dict[str, Build_Response, Validate_Response, Evaluate_Response, Analyze_Response, ProjectManagement_Response, Glycomimetics_Service_Response] = None
    __root__: dict[str, Glycomimetics_Service_Response] = None


class Glycomimetics_Entity(main_api_entity.Entity):
    entityType: Literal["Glycomimetics"] = (
        Field(  # This is the only required field in all of the API
            ..., title="Type", alias="type"
        )
    )
    services: Glycomimetics_Service_Requests = Glycomimetics_Service_Requests()
    responses: Glycomimetics_Service_Responses = Glycomimetics_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to mmservice.Glycomimetics
class Glycomimetics_API(main_api.Common_API):
    entity: Glycomimetics_Entity
    project: GlycomimeticsProject = GlycomimeticsProject()


class Glycomimetics_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return Glycomimetics_API
