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
from gemsModules.mmservice.mdaas.services.settings.known_available import (
    Available_Services,
)


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


class MDaaS_Service_Request(main_api_services.Service_Request):
    typename: Available_Services = Field(
        "Marco",
        alias="type",
        title="Services Offered by MDaaS",
        description="The service requested of the Common Servicer",
    )


class MDaaS_Service_Response(main_api_services.Service_Response):
    typename: Available_Services = Field(
        None,
        alias="type",
        title="Services Offered by MDaaS",
        description="The service requested of MDaaS",
    )