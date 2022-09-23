#!/usr/bin/env python3

from docs.gemsModules.microcosm.common.main_api import Transaction
from docs.gemsModules.microcosm.common.marco_api import marco_Service as Service 

from docs.gemsModules.microcosm.common import loggingConfig
if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)


def input_translator (transaction : Transaction) -> Service:
    log.debug(f"transaction: {transaction}")
    service = Service()
    service.inputs.entity = transaction.inputs.entity.entityType
#    print(f"the services are:  {transaction.inputs.entity.services}")
    return service