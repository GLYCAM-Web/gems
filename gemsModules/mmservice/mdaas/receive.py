#!/usr/bin/env python3
from gemsModules.mmservice.mdaas.receiver import MDaaS_Receiver
from gemsModules.mmservice.mdaas.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("MDaaS was called as an entity.  Processing.")
    mdaas_receiver = MDaaS_Receiver()
    mdaas_receiver_error_response = mdaas_receiver.receive(incoming_string = incomingString)
    if mdaas_receiver_error_response is not None:
        log.debug("The incoming string is not valid")
        return mdaas_receiver_error_response
    log.debug("The incoming string is valid")
