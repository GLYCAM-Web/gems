#!/usr/bin/env python3
from pydantic import  Field, validator
from typing import Literal, Dict, List, Union, Annotated
from gemsModules.common import main_api
from gemsModules.common import main_api_entity
from gemsModules.common import main_api_services

from gemsModules.complex.GpBuilder.main_settings import WhoIAm
from gemsModules.complex.GpBuilder.main_api_project import GpBuilderProject
from gemsModules.complex.GpBuilder.services.settings.known_available import Available_Services

from gemsModules.complex.GpBuilder.services.ProjectManagement.api import ProjectManagement_Request, ProjectManagement_Response
from gemsModules.complex.GpBuilder.services.Build.api import BuildService_Request, BuildService_Response
from gemsModules.complex.GpBuilder.services.Evaluate.api import EvaluateService_Request, EvaluateService_Response
from gemsModules.complex.GpBuilder.main_api_common import GpBuilder_Service_Request, GpBuilder_Service_Response

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)



# Remove discriminator and add custom validator
GpRequests = Union[EvaluateService_Request, BuildService_Request, ProjectManagement_Request, GpBuilder_Service_Request]
GpResponses = Union[EvaluateService_Response, BuildService_Response, ProjectManagement_Response, GpBuilder_Service_Response]


class Gpbuilder_Service_Requests(main_api_services.Service_Requests):
    __root__: dict[str, GpRequests] = None
    
    @validator('__root__', pre=True, each_item=True)
    @classmethod
    def validate_service_request(cls, v):
        if not isinstance(v, dict):
            return v
        
        typename = v.get('typename') or v.get('type')
        
        # Only validate with the class that matches the typename
        log.debug(f"Validating service request with typename: {typename}")
        if typename == 'Evaluate':
            return EvaluateService_Request.parse_obj(v)
        elif typename == 'Build':
            return BuildService_Request.parse_obj(v)
        elif typename == 'ProjectManagement':
            return ProjectManagement_Request.parse_obj(v)
        elif typename == 'GpBuilder':
            return GpBuilder_Service_Request.parse_obj(v)
        else:
            raise ValueError(f"Unknown service typename: {typename}")


class GpBuilder_Service_Responses(main_api_services.Service_Responses):
    __root__: dict[str, GpResponses] = None
    
    @validator('__root__', pre=True, each_item=True)
    @classmethod
    def validate_service_response(cls, v):
        if not isinstance(v, dict):
            return v
        
        typename = v.get('typename') or v.get('type')
        
        # Only validate with the class that matches the typename
        if typename == 'Evaluate':
            return EvaluateService_Response.parse_obj(v)
        elif typename == 'Build':
            return BuildService_Response.parse_obj(v)
        elif typename == 'ProjectManagement':
            return ProjectManagement_Response.parse_obj(v)
        elif typename == 'GpBuilder':
            return GpBuilder_Service_Response.parse_obj(v)
        else:
            raise ValueError(f"Unknown service typename: {typename}")
        

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


