#!/usr/bin/env python3
from gemsModules.batchcompute.json_string_manager import Batchcompute_Json_String_Manager
from gemsModules.batchcompute.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("batchcompute was called as an entity.  Processing.")
    batchcompute_manager = Batchcompute_Json_String_Manager()
    batchcompute_manager_error_response = batchcompute_manager.process(incoming_string = incomingString)
    if batchcompute_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return batchcompute_manager_error_response
    log.debug("The incoming string is valid")
    return batchcompute_manager.transaction.get_outgoing_string()
