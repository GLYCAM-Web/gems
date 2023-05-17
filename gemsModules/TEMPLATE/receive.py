#!/usr/bin/env python3
from gemsModules.TEMPLATE.json_string_manager import Template_Json_String_Manager
from gemsModules.TEMPLATE.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("Template was called as an entity.  Processing.")
    template_manager = Template_Json_String_Manager)
    template_manager_error_response = template_manager.process(incoming_string = incomingString)
    if template_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return template_manager_error_response
    log.debug("The incoming string is valid")
