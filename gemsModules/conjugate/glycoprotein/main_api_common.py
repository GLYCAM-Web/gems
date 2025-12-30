#!/usr/bin/env python3
from pydantic import  Field
from gemsModules.common import main_api_services

from gemsModules.conjugate.glycoprotein.services.settings.known_available import Available_Services


class GlycoProtein_Service_Request(main_api_services.Service_Request):
    typename : Available_Services = Field(
        None,
        alias='type',
        title='Services Offered by GlycoProtein',
        description='The service requested of the GlycoProtein'
    )


class GlycoProtein_Service_Response(main_api_services.Service_Response):
    typename : Available_Services = Field(
        None,
        alias='type',
        title='Services Offered by GlycoProtein',
        description='The service requested of GlycoProtein'
    )
