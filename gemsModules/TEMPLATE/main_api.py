#!/usr/bin/env python3
from pydantic import  Field
from typing import Literal, Dict
from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.TEMPLATE.main_settings import WhoIAm
from gemsModules.TEMPLATE.main_api_project import TemplateProject
from gemsModules.TEMPLATE.services.settings.known_available import Available_Services

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class Template_Service_Request(main_api_services.Service_Request):
    typename : Available_Services = Field(
        'Marco',
        alias='type',
        title='Services Offered by Template',
        description='The service requested of the Common Servicer'
    )

class Template_Service_Response(main_api_services.Service_Response):
    typename : Available_Services = Field(
        None,
        alias='type',
        title='Services Offered by Template',
        description='The service requested of Template'
    )

class Template_Service_Requests(main_api_services.Service_Requests):
    __root__ : Dict[str,Template_Service_Request] = None

class Template_Service_Responses(main_api_services.Service_Responses):
    __root__ : Dict[str,Template_Service_Response] = None

class Template_Entity(main_api_entity.Entity) :

    entityType : Literal['Template'] = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )
    services : Template_Service_Requests = Template_Service_Requests()  
    responses : Template_Service_Responses = Template_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to TEMPLATE
class Template_API(main_api.Common_API):
    entity : Template_Entity
    project : TemplateProject = TemplateProject()


class Template_Transaction(main_api.Transaction):
    
    def get_API_type(self):  # This allows dependency injection in the children
        return Template_API


