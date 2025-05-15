#!/usr/bin/env python3
from gemsModules.complex.GpBuilder.json_string_manager import Gpbuilder_Json_String_Manager
from gemsModules.complex.GpBuilder.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("GpBuilder was called as an entity.  Processing.")
    GpBuilder_manager = Gpbuilder_Json_String_Manager()
    GpBuilder_manager_error_response = GpBuilder_manager.process(incoming_string = incomingString)
    
    if GpBuilder_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return GpBuilder_manager_error_response
    
    log.debug("The incoming string is valid")
    return GpBuilder_manager.transaction.get_outgoing_string()
