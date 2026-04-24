#!/usr/bin/env python3
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

def process(incomingString: str) -> str:
    log.info("Delegator was called as an entity.  Processing.")

    #print("this is in delegator's process")

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

    #print("this is in delegator's receive")

    import json
    tmp_dict = json.loads(incomingString)
    requested_entity = tmp_dict["entity"]["type"]
    log.debug("The requested entity is : " + requested_entity)
    from gemsModules.configuration.main_api import session_instance_config
    local_host_name = session_instance_config.get_localhost_hostName()
    # Check to see if we need to set ourselves as the initial delegator
    # We definitely will need the local host name if so
    log.debug("The tmp_dict is:")
    log.debug(tmp_dict)
    if "initiation_timestamp" not in tmp_dict or not tmp_dict["initiation_timestamp"] or tmp_dict["initiation_timestamp"]=="" :
        log.info("Set initiation timestamp and receiving host is accessed.")
        from datetime import datetime
        tmp_dict["initial_receiver"]=local_host_name
        tmp_dict["initiation_timestamp"]=str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

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
        log.debug("Delegating incoming string to entity: " + requested_entity)
        from gemsModules.delegator import redirector_settings
        incoming_string = json.dumps(tmp_dict)
        entity_module = redirector_settings.get_receive_module(requested_entity)
        print(redirector_settings.get_known_entities())
        return entity_module(incoming_string)




### This should probably be in 'process' and maybe should just stay deleted
#    from gemsModules.delegator.json_string_manager import Redirector_Json_String_Manager
#    string_manager = Redirector_Json_String_Manager()
#
#    string_manager_error_response_string = string_manager.process(
#        incoming_string=incomingString
#    )
#
#    if string_manager_error_response_string is not None:
#        log.debug("The incoming string is not valid")
#        log.debug("The incoming string (incomingString) is: ")
#        log.debug(incomingString)
#        log.debug("The error response string (receiver_error_response_string) is: ")
#        log.debug(string_manager_error_response_string)
#        return string_manager_error_response_string
#
#    log.debug("The incoming string is valid")
