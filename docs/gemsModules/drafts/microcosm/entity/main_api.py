#!/usr/bin/env python3
from typing import Dict
from typing_extensions import Annotated
from pydantic import Field
from ..common import main_api as common_api
from ..common import main_api_entity as entity_api
from ..common import main_api_services as services_api
from . import module_api
from . import settings_main as settings

Avail_Module_Service=Annotated[settings.Module_Available_Service_APIs, Field(discriminator='typename')]

Avail_Module_Response=Annotated[settings.Module_Available_Response_APIs, Field(discriminator='typename')]

class Module_Services(services_api.Services):
    __root__ : Dict[str,Avail_Module_Service ] = None


class Module_Responses(services_api.Responses):
    __root__ : Dict[str,Avail_Module_Response ] = None


class Module_Entity(entity_api.Entity):
    typename : str = settings.WhoIAm
    services  : Module_Services = Module_Services()
    responses : Module_Responses = Module_Responses()
    inputs    : module_api.Module_User_Friendliness_Inputs = None
    outputs   : module_api.Module_User_Friendliness_Outputs = None

class Module_API(common_api.Common_API):
    entity  : Module_Entity 

class Module_Transaction(common_api.Transaction):

    def get_API_type(self):
        return Module_API

    def generateSchema(self):
        print(self.get_API_type().schema_json(indent=2))

