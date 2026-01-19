#!/usr/bin/env python3
from gemsModules.structurefile.PDBFile.json_string_manager import (
    PDBFile_Json_String_Manager,
)
from gemsModules.structurefile.PDBFile.main_settings import WhoIAm


from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("PDB was called as an entity.  Processing.")
    manager = PDBFile_Json_String_Manager()
    error_response = manager.process(incoming_string=incomingString)

    if error_response is not None:
        log.debug(
            "Error in PDB Json String Manager:\n%s",
            error_response,
        )

    return manager.transaction.get_outgoing_string()
