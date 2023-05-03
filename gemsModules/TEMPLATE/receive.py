#!/usr/bin/env python3
from gemsModules.TEMPLATE.receiver import Template_Receiver
from gemsModules.TEMPLATE.main_settings import WhoIAm
from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)


def receive(incomingString: str) -> str:
    log.info("Template was called as an entity.  Processing.")
    template_receiver = Template_Receiver()
    template_receiver_error_response = template_receiver.receive(incoming_string = incomingString)
    if template_receiver_error_response is not None:
        log.debug("The incoming string is not valid")
        return template_receiver_error_response
    log.debug("The incoming string is valid")
