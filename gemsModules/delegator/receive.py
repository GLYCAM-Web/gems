#!/usr/bin/env python3
from gemsModules.delegator.receiver import Redirector_Receiver
from gemsModules.delegator.receiver import Delegator_Receiver
from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

def process(incomingString: str) -> str:
    log.info("Delegator was called as an entity.  Processing.")
    delegator_receiver = Delegator_Receiver()
    delegator_receiver_error_response = delegator_receiver.receive(incoming_string = incomingString)
    if delegator_receiver_error_response is not None:
        log.debug("The incoming string is not valid")
        return delegator_receiver_error_response
    log.debug("The incoming string is valid")

    ## Grab the incoming Entity

    ## Hand the entity off to the service manager

    ## Generate and return outgoing string


def receive(incomingString: str) -> str:
    log.info("Delegator's receive was called")

    receiver = Redirector_Receiver()

    receiver_error_response_string = receiver.receive(incoming_string = incomingString)

    if receiver_error_response_string is not None:
        log.debug("The incoming string is not valid")
        log.debug("The incoming string (incomingString) is: ")
        log.debug(incomingString)
        log.debug("The error response string (receiver_error_response_string) is: ")
        log.debug(receiver_error_response_string)
        return receiver_error_response_string

    log.debug("The incoming string is valid")
    requested_entity=receiver.get_incoming_entity_type()
########## 
## NOTE!!!
## this is temporary until Delegator's services work
#        log.debug("Delegating incoming string to entity: " + requested_entity)
#        from gemsModules.delegator import redirector_settings 
#        entity_module = redirector_settings.Known_Entity_Reception_Modules[requested_entity]
#        return entity_module(incomingString)
##
## This is how it should eventually work:
    if requested_entity == WhoIAm:
        log.debug("Delegating incoming string to self")
        return process(incomingString)
    else:
        log.debug("Delegating incoming string to entity: " + requested_entity)
        from gemsModules.delegator import redirector_settings 
        entity_module = redirector_settings.Known_Entity_Reception_Modules[requested_entity]
        return entity_module(incomingString)
