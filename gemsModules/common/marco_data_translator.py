#!/usr/bin/env python3
from abc import ABC, abstractmethod

from gemsModules.common.main_api import Transaction
from gemsModules.common.marco_api import marco_Service as Service 
from gemsModules.common import loggingConfig

if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


class input_translator (ABC) :

    @abstractmethod
    def get_who_I_am(self) -> str :
        return "CommonServicer"

    def __init__ (self, transaction : Transaction) -> Service:
        log.debug(f"transaction: {transaction}")
        service = Service()
        service.inputs.entity = transaction.inputs.entity.entityType
        service.inputs.who_I_am = self.get_who_I_am()
        return service
