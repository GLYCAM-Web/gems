#!/usr/bin/env python3
from gemsModules.mmservice.mdaas.json_string_manager import MDaaS_Json_String_Manager
from gemsModules.mmservice.mdaas.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("MDaaS was called as an entity.  Processing.")
    mdaas_manager = MDaaS_Json_String_Manager()
    mdaas_manager_error_response = mdaas_manager.process(incoming_string = incomingString)
    if mdaas_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return mdaas_manager_error_response
    log.debug("The incoming string is valid")
