#!/usr/bin/env python3
from gemsModules.common.receiver import Receiver
from gemsModules.delegator.main_settings import WhoIAm
from gemsModules.status.main_api import Status_Transaction

from gemsModules.logging.logger import Set_Up_Logging
log = Set_Up_Logging(__name__)

##
#@detail 
# write me
class Status_Receiver(Receiver):

    ##
    #@detail 
    # write me
    def get_local_entity_type(self) -> str:
        return WhoIAm
    
    ##
    #@detail 
    # write me
    def get_transaction_child_type(self):
        return Status_Transaction
        