#!/usr/bin/env python3

from gemsModules.common.main_api import Transaction
from gemsModules.common.services.marco.api import marco_Service as Service 
from gemsModules.logging.logger import Set_Up_Logging

log = Set_Up_Logging(__name__)

#class marco_Transaction(Transaction) :
    #def get_API_type(self):
        #return "CommonServicer"

class input_translator () :

    def __init__ (self, transaction : Transaction) -> Service:
        log.debug(f"transaction: {transaction}")
        service = Service()
        service.inputs.entity = transaction.inputs.entity.entityType
        service.inputs.who_I_am = self.get_who_I_am()
        return service
