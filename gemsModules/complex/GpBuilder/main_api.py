#!/usr/bin/env python3
from pydantic import  Field
from typing import Literal, Dict
from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.complex.GpBuilder.main_api_project import GpBuilderProject

from gemsModules.complex.GpBuilder.main_api_common import GpBuilder_Service_Request, GpBuilder_Service_Response

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class Gpbuilder_Service_Requests(main_api_services.Service_Requests):
    __root__: Dict[str, GpBuilder_Service_Request] = None


class GpBuilder_Service_Responses(main_api_services.Service_Responses):
    __root__: Dict[str, GpBuilder_Service_Response] = None
    

class Gpbuilder_Entity(main_api_entity.Entity) :
    entityType : Literal['GpBuilder'] = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )
    services : Gpbuilder_Service_Requests = Gpbuilder_Service_Requests()  
    responses : GpBuilder_Service_Responses = GpBuilder_Service_Responses()


class GpBuilder_API(main_api.Common_API):
    entity: Gpbuilder_Entity
    project: GpBuilderProject = GpBuilderProject()


class Gpbuilder_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return GpBuilder_API


