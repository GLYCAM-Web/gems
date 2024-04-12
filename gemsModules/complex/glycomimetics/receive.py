#!/usr/bin/env python3
from gemsModules.complex.glycomimetics.json_string_manager import (
    Glycomimetics_Json_String_Manager,
)
from gemsModules.complex.glycomimetics.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("Glycomimetics was called as an entity.  Processing.")
    Glycomimetics_manager = Glycomimetics_Json_String_Manager()
    Glycomimetics_manager_error_response = Glycomimetics_manager.process(
        incoming_string=incomingString
    )

    if Glycomimetics_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return Glycomimetics_manager_error_response

    log.debug("The incoming string is valid")
    return Glycomimetics_manager.transaction.get_outgoing_string()
