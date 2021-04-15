#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import traceback
import gemsModules
import gemsModules.sequence
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.common import services as commonservices
from gemsModules.sequence import settings as sequenceSettings
from gemsModules.sequence import io as sequenceio

from gemsModules.common.loggingConfig import *
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##  @brief Default service is marco polo. Can change if needed later.
#   @param Transaction thisTransaction
#   @TODO: write this to use transaction_in and transaction_out
def doDefaultService(thisTransaction : sequenceio.Transaction):
    log.info("doDefaultService() was called.\n")
    if thisTransaction.response_dict is None:
        thisTransaction.response_dict={}
    thisTransaction.response_dict['entity']={}
    thisTransaction.response_dict['entity']['type']='SequenceDefault'
    thisTransaction.response_dict['responses']=[]
    thisTransaction.response_dict['responses'].append({'DefaultTest': {'payload':marco('Sequence')}})
    thisTransaction.build_outgoing_string()


##  @brief The main way Delegator interacts with this module. Request handling.
#   @param Transaction thisTransactrion
def receive(receivedTransaction : sequenceio.Transaction):
    log.info("sequence.receive() was called:\n")
    log.debug("The received transaction contains this incoming string: ")
    log.debug(receivedTransaction.incoming_string)
    log.debug("The received transaction contains this request dict: ")
    log.debug(receivedTransaction.request_dict)

    # ## To ensure that our Transacation is the Sequence variety, we
    # ## declare a new one and populate that.
    thisTransaction=sequenceio.Transaction(receivedTransaction.incoming_string)

    from pydantic import BaseModel, ValidationError
    try :
        thisTransaction.populate_transaction_in()
        thisTransaction.initialize_transaction_out_from_transaction_in()
    except ValidationError as e :
        log.error(e)
        thisTransaction.generateCommonParserNotice(noticeBrief='JsonParseEror')
        return

    # this next is used
    thisSequence=thisTransaction.transaction_in.entity
    # these are for logging/debugging
    log.debug("The entity type is : " + thisSequence.entityType)
    log.debug("The services are: ")
    log.debug(thisSequence.services)
    vals=thisSequence.services.values()
    for j in vals :
        if 'Build3DStructure' in j.typename :
            log.debug("Found a build 3d request.")
        elif 'Evaluate' in j.typename :
            log.debug("Found an evaluation request.")
        elif 'Validate' in j.typename :
            log.debug("Found a validation request.")
        else :
            log.debug("Found an unknown service: '" + str(j.typename))
    log.debug("The Seqence Entity's inputs looks like:")
    log.debug(thisSequence.inputs)
    log.debug("The Seqence Entity's inputs.Sequence looks like:")
    log.debug(thisSequence.inputs.sequence.payload)


    ## First figure out the names of each of the requested services
    if thisSequence.services is [] :
        log.debug("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        # TODO: write the following
#        thisTransaction.doDefaultService()
        return

    ## for each requested service:
    for currentService in thisSequence.services:
        log.debug("service, currentService: " + str(currentService))
        thisService=thisSequence.services[currentService]
        if 'Evaluate' in thisService.typename :
            log.debug("Evaluate service requested from sequence entity.")
            from gemsModules.sequence import evaluate
            try:
                thisTransaction.evaluateCondensedSequence()
                if thisTransaction.entity.inputs.evaluationOptions is not None :
                    if thisTransaction.entity.inputs.evaluationOptions.noBuild is False : 
                        ##Build the Default structure.  
                        from gemsModules.sequence import logic 
                        thisTransaction.manageSequenceRequest(defaultOnly=True)
            except Exception as error:
                log.error("There was a problem evaluating the condensed sequence: " + str(error)) 
                log.error(traceback.format_exc())
                thisTransaction.generateCommonParserNotice(noticeBrief = 'InvalidInputPayload')
        elif 'Build3DStructure' in thisService.typename:
            log.debug("Build3DStructure service requested from sequence entity.")
            try:
                ##first evaluate the requested structure. Only build if valid.
                from gemsModules.sequence import evaluate
                thisTransaction.evaluateCondensedSequence()
                valid = thisTransaction.transaction_out.entity.outputs.sequenceEvaluationOutput.sequenceIsValid
                thisTransaction.setIsEvaluationForBuild(True)
            except Exception as error:
                log.error("There was a problem evaluating the condensed sequence: " + str(error)) 
                log.error(traceback.format_exc())
                thisTransaction.generateCommonParserNotice(noticeBrief = 'InvalidInputPayload')
            else:
                if valid:
                    log.debug("Valid sequence.")
                    try:
                        from gemsModules.sequence import logic
                        thisTransaction.manageSequenceRequest()
                        
                    except Exception as error:
                        log.error("There was a problem with manageSequenceRequest(): " + str(error))
                        raise error
                else:
                    log.error("Invalid Sequence. Cannot build.")
                    print("the transaction is : ")
                    print(thisTransaction)
                    thisTransaction.generateCommonParserNotice(noticeBrief='InvalidInputPayload',additionalInfo={"hint":"Sequence is invalid"})
        elif "Validate" in thisService.typename:
            log.debug("Validate service requested from sequence entity.")
            from gemsModules.sequence import evaluate
            try:
                thisTransaction.evaluateCondensedSequence(validateOnly=True)
            except Exception as error:
                log.error("There was a problem validating the condensed sequence: " + str(error)) 
                thisTransaction.generateCommonParserNotice(noticeBrief = 'InvalidInputPayload')
        else:
            log.error("got to the else, so something is wrong")
            thisTransaction.generateCommonParserNotice(noticeBrief='ServiceNotKnownToEntity')

    ## prepares the transaction for return to the requestor, success or fail.     
    thisTransaction.build_outgoing_string()
    return thisTransaction


def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

