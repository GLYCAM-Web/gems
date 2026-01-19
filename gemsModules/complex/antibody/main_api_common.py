from pydantic import Field
from gemsModules.common import main_api_services

from gemsModules.complex.antibody.services.settings.known_available import (
    Available_Services,
)


class Antibody_Service_Request(main_api_services.Service_Request):
    typename: Available_Services = Field(
        "Marco",
        alias="type",
        title="Services Offered by Antibody",
        description="The service requested of the Common Servicer",
    )


class Antibody_Service_Response(main_api_services.Service_Response):
    typename: Available_Services = Field(
        None,
        alias="type",
        title="Services Offered by Antibody",
        description="The service requested of Antibody",
    )
