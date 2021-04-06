#!/usr/bin/env python3
import json, sys, os, re, importlib.util, shutil, uuid
import traceback
import gemsModules
import gemsModules.sequence
from gemsModules.common import io as commonio
from gemsModules.common import logic as commonlogic
from gemsModules.sequence import settings as sequenceSettings
from gemsModules.sequence import io as sequenceio

from gemsModules.common.loggingConfig import *
if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

##  @brief Default service is marco polo. Can change if needed later.
#   @param Transaction thisTransaction
def doDefaultService(thisTransaction : sequenceio.Transaction):
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
def receive(receivedTransaction : sequenceio.Transaction):
    log.info("sequence.receive() was called:\n")
    log.debug("The transaction contains this incoming string: ")
    log.debug(receivedTransaction.incoming_string)
    log.debug("The transaction contains this request dict: ")
    log.debug(receivedTransaction.request_dict)

    thisTransaction=sequenceio.Transaction(receivedTransaction.incoming_string)

    from pydantic import BaseModel, ValidationError
    try :
        thisTransaction.populate_transaction_in()
        #thisTransaction.transaction_in(**thisTransaction.request_dict)
    except ValidationError as e :
        log.error(e)
        appendCommonParserNotice(thisTransaction, 'JsonParseEror')
        return

    thisSequence=thisTransaction.transaction_in.entity
    print("The entity type is : " + thisSequence.entityType)
    print("The services are: ")
    print(thisSequence.services)
    for i in thisSequence.services :
        vals=i.values()
        print ("i.values() is :")
        print (vals)
        print ("the length is :")
        print (len(vals))
        theValue=list(i.items())[0][1]
        print("theValue.typename is : ")
        print(theValue.typename)
        for j in vals :
            print("j ia :")
            print(j)
            print("the service type is : ")
            print(j.typename)
            if 'Build3DStructure' in j.typename :
                print("Found a build 3d request.")
    print("The Seqence Entity's inputs looks like:")
    print(thisSequence.inputs)
    print("The Seqence Entity's inputs.Sequence looks like:")
    print(thisSequence.inputs[0].Sequence.payload)
    print("the length is :  ")
    print(len(thisSequence.inputs))
    for i in thisSequence.inputs :
        if i.Sequence is not None :
            print("Yay!")
        else :
            print ("Boo!")


    ## First figure out the names of each of the requested services
    if thisSequence.services is [] :
        log.debug("'services' was not present in the request. Do the default.")
        doDefaultService(thisTransaction)
        return

    ## for each requested service:
    for currentService in thisSequence.services:
        log.debug("service, currentService: " + str(currentService))
        if len(currentService.values()) is not 1 :
            log.error("There has been a logic error getting the service data.")
            common.settings.appendCommonParserNotice( thisTransaction,'GemsError' )
            return
        thisService=list(currentService.items())[0][1]
        if 'Evaluate' in thisService.typename :
            log.debug("Evaluate service requested from sequence entity.")
            from gemsModules.sequence import evaluate
            try:
                evaluate.evaluateCondensedSequencePydantic(thisTransaction, currentService)
                ##Build the Default structure.
                from gemsModules.sequence import logic
                logic.manageSequenceRequest(thisTransaction)
            except Exception as error:
                log.error("There was a problem evaluating the condensed sequence: " + str(error)) 
                log.error(traceback.format_exc())
                common.settings.appendCommonParserNotice( thisTransaction, 'InvalidInput', 'InvalidInputPayload')
        elif 'Build3DStructure' in thisService.typename:
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
                    common.settings.appendCommonParserNotice( thisTransaction,'InvalidInput')
        elif "Validate" in thisService.typename:
            log.debug("Validate service requested from sequence entity.")
            from gemsModules.sequence import evaluate
            try:
                evaluate.evaluateCondensedSequencePydantic(thisTransaction, True)
            except Exception as error:
                log.error("There was a problem validating the condensed sequence: " + str(error)) 
                common.settings.appendCommonParserNotice( thisTransaction, 'InvalidInputPayload')
        else:
            log.error("got to the else, so something is wrong")
            common.settings.appendCommonParserNotice( thisTransaction,'ServiceNotKnownToEntity')

    ## prepares the transaction for return to the requestor, success or fail.     
    thisTransaction.build_outgoing_string()


def main():
    log.info("main() was called.\n")

if __name__ == "__main__":
  main()

