#!/usr/bin/env python3
from gemsModules.common.main_api import Transaction
from gemsModules.common import loggingConfig 

if loggingConfig.loggers.get(__name__):
    pass
else:
    log = loggingConfig.createLogger(__name__)

def Serve(transaction : Transaction):
    log.info("The Status servicer was called.")
    transaction.entity.responses.add_response(
        typename = 'Status',
        outputs  = {'message': 'I AM ALIVE!!!!'},
        notices  = None
        )
    return transaction
