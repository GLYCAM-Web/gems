#!/usr/bin/env python3
from pydantic import  Field
from typing import Literal, Dict
from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.{{cookiecutter.gems_module}}.main_settings import WhoIAm
from gemsModules.{{cookiecutter.gems_module}}.main_api_project import {{cookiecutter.service_name}}_Project
from gemsModules.{{cookiecutter.gems_module}}.services.settings.known_available import Available_Services

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class {{cookiecutter.service_name}}_Service_Request(main_api_services.Service_Request):
    typename : Available_Services = Field(
        '{{cookiecutter.service_name}}',
        alias='type',
        title='Services Offered by {{cookiecutter.service_name}}',
        description='The service requested of the Common Servicer'
    )

class {{cookiecutter.service_name}}_Service_Response(main_api_services.Service_Response):
    typename : Available_Services = Field(
        None,
        alias='type',
        title='Services Offered by {{cookiecutter.service_name}}',
        description='The service requested of {{cookiecutter.service_name}}'
    )

class {{cookiecutter.service_name}}_Service_Requests(main_api_services.Service_Requests):
    __root__ : Dict[str,{{cookiecutter.service_name}}_Service_Request] = None

class {{cookiecutter.service_name}}_Service_Responses(main_api_services.Service_Responses):
    __root__ : Dict[str,{{cookiecutter.service_name}}_Service_Response] = None

class {{cookiecutter.service_name}}_Entity(main_api_entity.Entity) :

    entityType : Literal['{{cookiecutter.gems_module}}'] = Field(  # This is the only required field in all of the API
            ...,
            title='Type',
            alias='type'
            )
    services : {{cookiecutter.service_name}}_Service_Requests = {{cookiecutter.service_name}}_Service_Requests()  
    responses : {{cookiecutter.service_name}}_Service_Responses = {{cookiecutter.service_name}}_Service_Responses()


# The Delegator uses the main_api.Transaction class to define the transaction
# It should also define more services that are specific to {{cookiecutter.service_name}}
class {{cookiecutter.service_name}}_API(main_api.Common_API):
    entity : {{cookiecutter.service_name}}_Entity
    project : {{cookiecutter.service_name}}_Project = {{cookiecutter.service_name}}_Project()


class {{cookiecutter.service_name}}_Transaction(main_api.Transaction):
    
    def get_API_type(self):  # This allows dependency injection in the children
        return {{cookiecutter.service_name}}_API


