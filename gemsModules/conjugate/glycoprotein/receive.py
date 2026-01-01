#!/usr/bin/env python3
from gemsModules.conjugate.glycoprotein.json_string_manager import GlycoProtein_Json_String_Manager
from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("GlycoProtein was called as an entity.  Processing.")
    json_manager = GlycoProtein_Json_String_Manager()
    
    maybe_error_response = json_manager.process(incomingString)
    if maybe_error_response:
        log.debug("The incoming string is not valid")
        return maybe_error_response
    else:
        log.debug("The incoming string is valid")
        return json_manager.transaction.get_outgoing_string()
