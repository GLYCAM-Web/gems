#!/usr/bin/env python3
from pydantic import  Field
from typing import Literal, Dict
from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.conjugate.glycoprotein.main_api_project import GlycoProteinProject

from gemsModules.conjugate.glycoprotein.main_api_common import GlycoProtein_Service_Request, GlycoProtein_Service_Response

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class GlycoProtein_Service_Requests(main_api_services.Service_Requests):
    __root__: Dict[str, GlycoProtein_Service_Request] = None


class GlycoProtein_Service_Responses(main_api_services.Service_Responses):
    __root__: Dict[str, GlycoProtein_Service_Response] = None
    

class GlycoProtein_Entity(main_api_entity.Entity) :
    entityType : Literal['GlycoProtein'] = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )
    services : GlycoProtein_Service_Requests = GlycoProtein_Service_Requests()  
    responses : GlycoProtein_Service_Responses = GlycoProtein_Service_Responses()


class GlycoProtein_API(main_api.Common_API):
    entity: GlycoProtein_Entity
    project: GlycoProteinProject = GlycoProteinProject()


class GlycoProtein_Transaction(main_api.Transaction):
    def get_API_type(self):  # This allows dependency injection in the children
        return GlycoProtein_API


