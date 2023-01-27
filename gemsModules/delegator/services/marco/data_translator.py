#!/usr/bin/env python3

from gemsModules.delegator.main_api import Delegator_Transaction

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

class JSON_input_translator():

    def __init__ (self, transaction : Delegator_Transaction):
        log.debug(f"incoming transaction: {transaction}")


class Implied_services_filler():
    pass

class Request_input_translator():
    pass

class Response_output_translator():
    pass

class JSON_response_translator():
    pass


