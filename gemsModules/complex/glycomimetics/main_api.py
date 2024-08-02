from pydantic import Field
from pydantic.typing import Literal as pyLiteral

from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.complex.glycomimetics.main_settings import WhoIAm
from gemsModules.complex.glycomimetics.main_api_project import GlycomimeticsProject
from gemsModules.complex.glycomimetics.services.settings.known_available import (
    Available_Services,
)

from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class Glycomimetics_Service_Request(main_api_services.Service_Request):
    typename: Available_Services = Field(
        "Marco",
        alias="type",
        title="Services Offered by Glycomimetics",
        description="The service requested of the Common Servicer",
    )


class Glycomimetics_Service_Response(main_api_services.Service_Response):
    typename: Available_Services = Field(
        None,
        alias="type",
        title="Services Offered by Glycomimetics",
        description="The service requested of Glycomimetics",
    )


class Glycomimetics_Service_Requests(main_api_services.Service_Requests):
    __root__: dict[str, Glycomimetics_Service_Request] = None


class Glycomimetics_Service_Responses(main_api_services.Service_Responses):
    __root__: dict[str, Glycomimetics_Service_Response] = None


class Glycomimetics_Entity(main_api_entity.Entity):
    entityType: pyLiteral["Glycomimetics"] = (
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
