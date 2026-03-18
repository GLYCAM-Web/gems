#!/usr/bin/env python3
from gemsModules.delegator.json_string_manager import Redirector_Json_String_Manager
from gemsModules.delegator.json_string_manager import Delegator_Json_String_Manager
from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.configuration.main_api import load_instance_config
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)


def process(incomingString: str) -> str:
    log.info("Delegator was called as an entity.  Processing.")
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

    # might be used, can be loaded as needed, but gets redundant
    this_config = load_instance_config() 
    local_host_name=str(this_config.get_localhost_hostName())

    string_manager = Redirector_Json_String_Manager()

    string_manager_error_response_string = string_manager.process(
        incoming_string=incomingString
    )

    if string_manager_error_response_string is not None:
        log.debug("The incoming string is not valid")
        log.debug("The incoming string (incomingString) is: ")
        log.debug(incomingString)
        log.debug("The error response string (receiver_error_response_string) is: ")
        log.debug(string_manager_error_response_string)
        return string_manager_error_response_string

    log.debug("The incoming string is valid")

    # Check to see if we need to set ourselves as the initial delegator
    tmp_dict = json.loads(incoming_string)
    if "initiation_timestamp" not in tmp_dict or not tmp_dict["initiation_timestamp"] :
        tmp_dict["initial_receiver"]=local_host_name
        tmp_dict["initiation_timestamp"]=str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        incoming_string = json.dumps(tmp_dict)

    requested_entity = string_manager.get_incoming_entity_type()

    if requested_entity == WhoIAm:
        log.debug("Delegating incoming string to self")
        tmp_dict = json.loads(incoming_string)
        tmp_dict["execution_host"]=local_host_name
        incoming_string = json.dumps(tmp_dict)
        return process(incomingString)
    else:
        log.debug("Delegating incoming string to entity: " + requested_entity)
        from gemsModules.delegator import redirector_settings

        entity_module = redirector_settings.Known_Entity_Reception_Modules[
            requested_entity
        ]
        return entity_module(incomingString)
