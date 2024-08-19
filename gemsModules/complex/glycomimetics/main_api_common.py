from pydantic import Field
from gemsModules.common import main_api_services

from gemsModules.complex.glycomimetics.services.settings.known_available import (
    Available_Services,
)

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
