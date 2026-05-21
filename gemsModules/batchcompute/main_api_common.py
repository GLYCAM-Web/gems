#!/usr/bin/env python3
from pydantic import  Field
from gemsModules.common import main_api_services

from gemsModules.batchcompute.main_api_project import Batchcompute_Project
from gemsModules.batchcompute.services.settings.known_available import Available_Services

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Batchcompute_Service_Request(main_api_services.Service_Request):
    typename : Available_Services = Field(
        'SubmitJob',
        alias='type',
        title='Services Offered by batchcompute',
        description='The service requested of the batchcompute'
    )


class batchcompute_Service_Response(main_api_services.Service_Response):
    typename : Available_Services = Field(
        None,
        alias='type',
        title='Services Offered by batchcompute',
        description='The service requested of batchcompute'
    )