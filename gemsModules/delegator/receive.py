#!/usr/bin/env python3
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def process(incomingString: str) -> str:
    log.info("Delegator was called as an entity.  Processing.")
    from gemsModules.delegator.json_string_manager import Delegator_Json_String_Manager
    delegator_string_manager = Delegator_Json_String_Manager()
    delegator_string_manager_error_response = delegator_string_manager.process(
        incoming_string=incomingString
    )
    if delegator_string_manager_error_response is not None:
        log.debug("The incoming string is not valid")
        return delegator_string_manager_error_response
    log.debug("The incoming string is valid")
    return delegator_string_manager.transaction.get_outgoing_string()


def receive(incomingString: str) -> str:
    log.info("Delegator's receive was called")

    # Get some basic info from the incoming json string and from the instance config
    import json
    tmp_dict = json.loads(incomingString)
    requested_entity = tmp_dict["entity"]["type"]
    log.debug("The requested entity is : " + requested_entity)
    from gemsModules.configuration.main_api import session_instance_config
    local_host_name = session_instance_config.get_localhost_hostName()
    log.debug("The tmp_dict is:")
    log.debug(tmp_dict)

    # See if we need to set ourselves as the initial delegator and respond as needed
    if "initiation_timestamp" not in tmp_dict or not tmp_dict["initiation_timestamp"] or tmp_dict["initiation_timestamp"]=="" :
        log.info("The initiation timestamp and receiving host will be set.")
        from datetime import datetime
        tmp_dict["initial_receiver"]=local_host_name
        tmp_dict["initiation_timestamp"]=str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

    # Figure out where the request needs to go, and send it there
    from gemsModules.delegator.main_settings import WhoIAm
    if requested_entity == WhoIAm:
        log.info("The requested entity is the delegator. Processing.")
        log.debug("Delegating incoming string to self")
        tmp_dict["execution_host"]=local_host_name
        incoming_string = json.dumps(tmp_dict)
        log.debug("The incoming string is now:")
        log.debug(incoming_string)
        return process(incoming_string)
    else:
        log.info("The requested entity is NOT delegator. Redirecting")
        log.debug("Delegating incoming string to entity: " + requested_entity)
        from gemsModules.delegator.redirector_settings import module_loader
        incoming_string = json.dumps(tmp_dict)
        entity_module = module_loader.get_module_attr(requested_entity)
        return entity_module(incoming_string)
