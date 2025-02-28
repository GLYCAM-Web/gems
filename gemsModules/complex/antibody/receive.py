#!/usr/bin/env python3
import os 

from gemsModules.complex.antibody.json_string_manager import (
    Antibody_Json_String_Manager,
)
from gemsModules.complex.antibody.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("Antibody was called as an entity.  Processing.")
    Antibody_manager = Antibody_Json_String_Manager()
    Antibody_manager_error_response = Antibody_manager.process(
        incoming_string=incomingString
    )

    if Antibody_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return Antibody_manager_error_response

    log.debug("The incoming string is valid")
    
    # Write the response to a a file in the project directory
    output_path = Antibody_manager.transaction.outputs.project.project_dir
    if os.path.exists(output_path) is False:
        log.debug("The output path does not exist")
    else:
        response_json_path = output_path + "/response.json"
        with open(response_json_path, "w") as f:
            f.write(Antibody_manager.transaction.get_outgoing_string(prettyPrint=True))
            f.write("\n")
    
    # Return the response in a condensed format for the API
    return Antibody_manager.transaction.get_outgoing_string()
