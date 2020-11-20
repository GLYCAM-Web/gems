#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import traceback
import gemsModules
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.delegator import io as delegatorio
from gemsModules.sequence import settings as sequenceSettings

from gemsModules.common.loggingConfig import *
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##  @brief Default service is marco polo. Should this be something else?
#   @param Transaction thisTransaction
def doDefaultService(thisTransaction : delegatorio.Transaction):
    log.info("doDefaultService() was called.\n")
    # evaluate(thisTransaction : Transaction)
    # build3DStructure(thisTransaction : Transaction)
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='SequenceDefault'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'DefaultTest': {'payload':marco('Sequence')}})
    thisTransaction.build_outgoing_string()


##  @brief The main way Delegator interacts with this module. Request handling.
#   @param Transaction thisTransactrion
def receive(thisTransaction : delegatorio.Transaction):
    log.info("sequence.receive() was called:\n")
    import gemsModules.sequence
    ## First figure out the names of each of the requested services
    if not 'services' in thisTransaction.request_dict['entity'].keys():
        log.debug("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        return

    input_services = thisTransaction.request_dict['entity']['services']
    theServices=commonlogic.getTypesFromList(input_services)
    ## for each requested service:
    for currentService in theServices:
        log.debug("service, currentService: " + currentService)
        #####  the automated module loading doesn't work, and I can't figure out how to make it work,
              # that is:
              #  requestedModule='.'+settings.serviceModules[currentService]
              #  the_spec = importlib.util.find_spec('.sequence.entity.evaluate',gemsModules)
              # .... and many variants thereof
        #####  so, writing something ugly for now
        ## Only work on recognized services. Add an error and carry on checking other services if an unknown service is found.
        ##  TODO: Add a check for options like "On fail quit"
        ##  
        if currentService not in sequenceSettings.serviceModules.keys():
            if currentService not in common.settings.serviceModules.keys():
                log.error("The requested service is not recognized. Try: " + str(sequenceSettings.serviceModules.keys()))
                common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',currentService)
            else:
                pass
        ## TODO:  move all the service call parts to 'sequence/logic.py'
        ## if it is known, try to do it
        elif currentService == "Evaluate":
            log.debug("Evaluate service requested from sequence entity.")
            from gemsModules.sequence import evaluate
            try:
                evaluate.evaluateCondensedSequencePydantic(thisTransaction, currentService)
            except Exception as error:
                log.error("There was a problem evaluating the condensed sequence: " + str(error)) 
                log.error(traceback.format_exc())
                common.settings.appendCommonParserNotice( thisTransaction, 'InvalidInput', 'InvalidInputPayload')
        elif currentService == 'Build3DStructure':
            log.debug("Build3DStructure service requested from sequence entity.")
            try:
                ##first evaluate the requested structure. Only build if valid.
                from gemsModules.sequence import evaluate
                valid = evaluate.evaluateCondensedSequencePydantic(thisTransaction, "Evaluate")
            except Exception as error:
                log.error("There was a problem evaluating the condensed sequence: " + str(error)) 
                log.error(traceback.format_exc())
                common.settings.appendCommonParserNotice( thisTransaction, 'InvalidInput', 'InvalidInputPayload')
            else:
                if valid:
                    log.debug("Valid sequence.")
                    try:
                        from gemsModules.sequence import logic
                        logic.manageSequenceRequest(thisTransaction)
                    except Exception as error:
                        log.error("There was a problem with manageSequenceRequest(): " + str(error))
                        raise error
                else:
                    log.error("Invalid Sequence. Cannot build.")
                    common.settings.appendCommonParserNotice( thisTransaction,'InvalidInput',currentService)
        elif currentService == "Validate":
            log.debug("Validate service requested from sequence entity.")
            from gemsModules.sequence import evaluate
            try:
                evaluate.evaluateCondensedSequencePydantic(thisTransaction, True)
            except Exception as error:
                log.error("There was a problem validating the condensed sequence: " + str(error)) 
                common.settings.appendCommonParserNotice( thisTransaction, 'InvalidInput', 'InvalidInputPayload')
        else:
            log.error("got to the else, so something is wrong")
            common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity',currentService)

    ## prepares the transaction for return to the requestor, success or fail.     
    thisTransaction.build_outgoing_string()


def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

