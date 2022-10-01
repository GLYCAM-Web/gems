#!/usr/bin/env python3
from typing import Dict
from ..common import main_api
from ..common import main_api_entity as entity_api
from ..common import main_api_services as services_api
from . import module_api_services, module_api
from . import main_settings as settings

class Module_Service(services_api.Service):
    typename: settings.All_Available_Services

class Module_Response(services_api.Response):
    typename: settings.All_Available_Services

class Module_Services(services_api.Services):
    __root__ : Dict[str,module_api_services.Module_Service ] = None

class Module_Responses(services_api.Responses):
    __root__ : Dict[str,module_api_services.Module_Response ] = None

class Module_Entity(entity_api.Entity):
    services  : Module_Services = Module_Services()
    responses : Module_Responses = Module_Responses()
    inputs    : module_api.Module_User_Friendliness_Inputs = None
    outputs   : module_api.Module_User_Friendliness_Outputs = None

class Module_API(main_api.Common_API):
    entity  : Module_Entity 

class Module_Transaction(main_api.Transaction):

    def get_API_type(self):
        return Module_API
    ## If you want to use the schema from the parent, you can do this:
    ##    return super().get_API_type()
    ## To check that it does what you think, you can do this:
    ##    __super__ = super().get_API_type()
    ##    print("The api type is " + str(__super__))

    def generateSchema(self):
        print(self.get_API_type().schema_json(indent=2))

