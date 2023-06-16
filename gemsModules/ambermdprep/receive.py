#!/usr/bin/env python3
from gemsModules.ambermdprep.json_string_manager import AmberMDPrep_Json_String_Manager
from gemsModules.ambermdprep.main_settings import WhoIAm


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("AmberMDPrep was called as an entity.  Processing.")
    manager = AmberMDPrep_Json_String_Manager()
    AmberMDPrep_manager_error_response = manager.process(incoming_string=incomingString)

    if AmberMDPrep_manager_error_response is not None:
        log.debug(
            "Error in AmberMDPrep Json String Manager:\tThe incoming string is not valid:\n%s\n%s",
            incomingString,
            AmberMDPrep_manager_error_response,
        )
        return AmberMDPrep_manager_error_response

    return manager.transaction.get_outgoing_string()
