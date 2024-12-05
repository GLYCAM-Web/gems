#!/usr/bin/env python3
from pydantic import  Field
from gemsModules.common import main_api_services

from gemsModules.GpBuilder.main_api_project import Gpbuilder_Project
from gemsModules.GpBuilder.services.settings.known_available import Available_Services

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Gpbuilder_Service_Request(main_api_services.Service_Request):
    typename : Available_Services = Field(
        'Build',
        alias='type',
        title='Services Offered by GpBuilder',
        description='The service requested of the GpBuilder'
    )


class GpBuilder_Service_Response(main_api_services.Service_Response):
    typename : Available_Services = Field(
        None,
        alias='type',
        title='Services Offered by GpBuilder',
        description='The service requested of GpBuilder'
    )