#!/usr/bin/env python3
from gemsModules.common import jsoninterface as commonIO  # can become a module-specific child
from gemsModules.common.loggingConfig import loggers, createLogger
import gemsModules

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)


## TODO: document me
#
def receive(receivedTransaction : commonIO.Transaction):
    log.info("receive was called.")
    try:
        ## Validate request against your module's classes with Pydantic.
        log.debug("validate")
        ## Check for an entity. Must match your gems module's.
        log.debug("entity check")
        ## Check for a service. If none, do default service. Else, delegate
        ##  to the appropriate module. Keep the logic here limited to that 
        ##  scope: farming out to the service.
        log.debug("service check")
        
    except Exception as error:
        ## Handle it.
        log.error("Failed to do something: " + str(error))
        raise error  

## TODO: document me
#
def doDefaultService(receivedTransaction : commonIO.Transaction):
    log.info("doDefaultService was called.")
    try:
        ##Do something.
        log.debug("Doing something.")
    except Exception as error:
        ## Handle it.
        log.error("Failed to do something: " + str(error))
        raise error        
