#!/usr/bin/env python3
from gemsModules.delegator.receiver import Redirector_Receiver
from gemsModules.delegator.receiver import Delegator_Receiver
from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

def process(incomingString: str) -> str:
    log.info("Delegator was called as an entity.  Processing.")
    receiver = Delegator_Receiver()
    receiver_string = receiver.receive(incoming_string = incomingString)
    if receiver_string is not None:
        log.debug("The incoming string is not valid")
        return receiver_string
    log.debug("The incoming string is valid")

    this_transaction= receiver.get_transaction()
    from gemsModules.delegator.inputs_translator import JSON_input_translator
    this_translator = JSON_input_translator(this_transaction.inputs)
    this_translator.translate()

#    from gemsModules.common.service_manager import Service_Manager
#    manager = Service_Manager(receiver.get_transaction())
#    transaction = manager.process()
#    return transaction.get_outgoing_string()


def receive(incomingString: str) -> str:
    log.info("Delegator's redirect was called")

    receiver = Redirector_Receiver()

    receiver_error_response_string = receiver.receive(incoming_string = incomingString)

    if receiver_error_response_string is not None:
        log.debug("The incoming string is not valid")
        return receiver_error_response_string

    log.debug("The incoming string is valid")
    requested_entity=receiver.get_incoming_entity_type()
########## 
## NOTE!!!
## this is temporary until Delegator's Marco and known Entities services work
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
