#!/usr/bin/env python3
import os 

from gemsModules.networkconnections.grpc import (
    # Note: The name of this function has become a misnomer as it checks contexts regardless of submission method. # TODO: Rename
    is_GEMS_instance_for_SLURM_submission as is_correct_GEMS_instance_for_AAD2,
)
from gemsModules.networkconnections.seek_correct_host import execute as seek_correct_host
from gemsModules.systemoperations.environment_ops import get_site_version

#from gemsModules.configuration.main_api import InstanceConfig, load_instance_config
from gemsModules.configuration.main_api import load_instance_config

from gemsModules.complex.antibody.json_string_manager import (
    Antibody_Json_String_Manager,
)
from gemsModules.complex.antibody.main_settings import WhoIAm, context_names
from gemsModules.logging.logger import Set_Up_Logging



log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("Antibody was called as an entity.  Processing.")
    # Note: Hardcoded thoreau check; This is because AD2 can only work there for now.
    #if not is_correct_GEMS_instance_for_AAD2(requested_ctx=WhoIAm, requested_instance="thoreau"):

    theIC=load_instance_config()
    if not theIC.localhost_supports_context(context_names=["AD", "AntibodyDocking"]) :
        log.info("This is not the correct host to submit to.")

        log.debug("Checking if this is the initial host.")
        this_config = load_instance_config()
        local_host_name=str(this_config.get_localhost_hostName())
        tmp_dict = json.loads(incoming_string)
        if "initiation_timestamp" not in tmp_dict or not tmp_dict["initiation_timestamp"] :
            log.error("The incoming string has no initiation_timestamp. I cannot determine my role.")
            raise ValueError ("Complex/Antibody: The incoming string has no initiation_timestamp. Cannot determine my role.")
        if tmp_dict["initial_receiver"] == local_host_name :
            log.debug("This is the initial host. Recording info as needed into the Project.")
### These should not happen until the correct host is found.
#        # Patch the correct uploads paths ### READ FROM IC - this happens later in Project
#        uploads_dir = ""
#        site_version = get_site_version()
#        if site_version == "swarmtest":
#            uploads_dir = "/website/USERDATA/swarmtest/uploads"
#        elif site_version == "test":
#            uploads_dir = "/website/USERDATA/LiveTest/uploads"
#        elif site_version == "dev":
#            uploads_dir = "/website/USERDATA/LiveDev/uploads"
#        elif site_version == "actual":
#            uploads_dir = "/website/USERDATA/Actual/uploads"
#        
#        log.debug(f"Original Incoming string: {incomingString}")
#        incomingString = incomingString.replace("/website/uploads", uploads_dir)
#        log.debug(f"The replaced uploads_dir: {uploads_dir}")
#        log.debug(f"Modified Incoming string: {incomingString}")


############# might need these, but...
#            uploads_dir = get_secure_inputs_path_by_service_ID("AD")
#            filesystem_path = get_filesystem_path_by_service_ID("AD")

            TODO - instantiating the project should pick all this up automatically

            probably do not need to instantiate it separately so that existing project info can be managed.
            
incoming_string = dump of the API object now including project

        else :
            log.debug("This is not the initial host. Making no changes to the request.")

        log.info("Seeking correct host.")
        response = seek_correct_host(incomingString, WhoIAm, submission_fn_type="json")
        # replace the paths in the response from thoreau with the correct paths for the website. TODO: Fix these hacks. help me
        # These replacements correspond to instance config's filesystem paths as per thoreau and swarm paths.
        
        log.debug(f"Original Response: {response}")


        ## Should not be needed. 
        ## The systems should ensure that the correct data are in findable places
        # Should be checking against the instance configs. Problem: Can't get both paths on each instance.
        #response = response.replace("/scratch2/thoreau-web/complex/ad/", "/website/userdata/complex/ad/")
        #response = response.replace(uploads_dir, "/website/uploads")
        #log.debug(f"Modified Response: {response}")
        
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
    # TODO/fixme: If this is a build request, it will use the autogenerated Build pUUID instead of the pUUID given to build.
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
