#!/usr/bin/env python3
from pydantic import  Field
from typing import Literal, Dict
from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.batchcompute.main_settings import WhoIAm
from gemsModules.batchcompute.main_api_project import Batchcompute_Project
from gemsModules.batchcompute.services.settings.known_available import Available_Services
from gemsModules.batchcompute.services.SubmitJob.api import SubmitJobService_Request, SubmitJobService_Response
from gemsModules.batchcompute.main_api_common import Batchcompute_Service_Request, batchcompute_Service_Response

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Batchcompute_Service_Requests(main_api_services.Service_Requests):
    __root__ : dict[str, SubmitJobService_Request, Batchcompute_Service_Request] = None


class batchcompute_Service_Responses(main_api_services.Service_Responses):
    __root__ : dict[str, SubmitJobService_Response, batchcompute_Service_Response] = None


class Batchcompute_Entity(main_api_entity.Entity) :

    #entityType : Literal['batchcompute'] =  not the module - the name of the entity is in upper camel case
    entityType : Literal['Batchcompute'] = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )
    services : Batchcompute_Service_Requests = Batchcompute_Service_Requests()  
    responses : batchcompute_Service_Responses = batchcompute_Service_Responses()


class batchcompute_API(main_api.Common_API):
    entity : Batchcompute_Entity
    project : Batchcompute_Project = Batchcompute_Project()


class Batchcompute_Transaction(main_api.Transaction):
    
    def get_API_type(self):  # This allows dependency injection in the children
        return batchcompute_API


