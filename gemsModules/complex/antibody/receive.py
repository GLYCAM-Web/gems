#!/usr/bin/env python3
import os 

from gemsModules.networkconnections.grpc import (
    # Note: The name of this function has become a misnomer as it checks contexts regardless of submission method. # TODO: Rename
    is_GEMS_instance_for_SLURM_submission as is_correct_GEMS_instance_for_AAD2,
)
from gemsModules.networkconnections.seek_correct_host import execute as seek_correct_host


from gemsModules.complex.antibody.json_string_manager import (
    Antibody_Json_String_Manager,
)
from gemsModules.complex.antibody.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("Antibody was called as an entity.  Processing.")
    # Note: Hardcoded thoreau check; This is because AD2 can only work there for now.
    if not is_correct_GEMS_instance_for_AAD2(requested_ctx=WhoIAm, requested_instance="thoreau"):
        log.info("This is not the correct host to submit to.")
        
        # Patch the correct uploads paths
        GW_DOMAIN = os.getenv("GW_DOMAIN") or ""
        uploads_dir = ""
        if "actual" in GW_DOMAIN:
            uploads_dir = "/website/USERDATA/Actual/uploads"
        elif "dev" in GW_DOMAIN:
            uploads_dir = "/website/USERDATA/LiveDev/uploads"
        else:
            uploads_dir = "/website/USERDATA/LiveTest/uploads"
        
        log.debug(f"Original Incoming string: {incomingString}")
        incomingString = incomingString.replace("/website/uploads", uploads_dir)
        log.debug(f"The replaced uploads_dir: {uploads_dir}")
        log.debug(f"Modified Incoming string: {incomingString}")

        
        response = seek_correct_host(incomingString, WhoIAm, submission_fn_type="json")
        # replace the paths in the response from thoreau with the correct paths for the website. TODO: Fix these hacks. help me
        # These replacements correspond to instance config's filesystem paths as per thoreau and swarm paths.
        
        log.debug(f"Original Response: {response}")
        response = response.replace("/scratch2/thoreau-web/complex/ad/", "/website/userdata/complex/ad/")
        response = response.replace(uploads_dir, "/website/uploads")
        log.debug(f"Modified Response: {response}")
        
        return response
    else:
        log.info("This is the correct host to submit to.")
    
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
