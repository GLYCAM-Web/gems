#!/usr/bin/env python3
from gemsModules.{{cookiecutter.gems_module}}.services.{{cookiecutter.service_name}}.api import {{cookiecutter.service_name}}Service_Request, {{cookiecutter.service_name}}Service_Response

from gemsModules.{{cookiecutter.gems_module}}.tasks import say_something_nice

from gemsModules.logging.logger import Set_Up_Logging 
log = Set_Up_Logging(__name__)


def Serve(service : {{cookiecutter.service_name}}Service_Request) -> {{cookiecutter.service_name}}Service_Response:

    message = say_something_nice.execute()
    response = {{cookiecutter.service_name}}Service_Response()
    response.outputs.message = message
    return response

    
