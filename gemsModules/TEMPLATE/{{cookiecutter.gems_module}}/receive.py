#!/usr/bin/env python3
from gemsModules.{{cookiecutter.gems_module}}.json_string_manager import {{cookiecutter.service_name}}_Json_String_Manager
from gemsModules.{{cookiecutter.gems_module}}.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("{{cookiecutter.service_name}} was called as an entity.  Processing.")
    {{cookiecutter.service_name}}_manager = {{cookiecutter.service_name}}_Json_String_Manager()
    {{cookiecutter.service_name}}_manager_error_response = {{cookiecutter.service_name}}_manager.process(incoming_string = incomingString)
    if {{cookiecutter.service_name}}_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return {{cookiecutter.service_name}}_manager_error_response
    log.debug("The incoming string is valid")
