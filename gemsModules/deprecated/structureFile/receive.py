#!/usr/bin/env python3
import imp
import os, sys, importlib.util
import gemsModules.deprecated
import gemsModules.deprecated.structureFile.settings as structureFileSettings
import traceback
from gemsModules.deprecated.common.services import prettyPrint, getGemsHome, parseInput
from gemsModules.deprecated.common.logic import updateResponse
from gemsModules.deprecated.common import io as commonIO
from gemsModules.deprecated.project.projectUtil import *
from gemsModules.deprecated.common.loggingConfig import loggers, createLogger
from gemsModules.deprecated.structureFile.amber.evaluate import evaluatePdb
from gemsModules.deprecated.structureFile.amber.preprocess import preprocessPdbForAmber
from gemsModules.deprecated.structureFile.amber import io as amberIO

if loggers.get(__name__):
    pass
else:
    log = createLogger(__name__)

## Receives requests related to preprocessing files 
def receive(receivedTransaction : commonIO.Transaction):
    log.info("structureFile receive() was called.")
    try:
        pdbTransaction = __setup(receivedTransaction)
    except Exception as error:
        log.error("There was a problem setting up a pdbTransaction: " + str(error))
        receivedTransaction.generateCommonParserNotice(nodiceBrief="Failed to setup the pdbTransaction.")
        raise RuntimeError("Cannot instantiate a transaction.")
    try:
        if 'services' not in pdbTransaction.request_dict['entity'].keys():
            doDefaultService(pdbTransaction)
        else:
            services = pdbTransaction.request_dict['entity']['services']
            ## Keys at this level are allowed to be arbitrary, so dig for recognized types.
            for key in services.keys():
                requestedService = services[key]['type']

                if requestedService not in structureFileSettings.serviceModules.keys():
                    log.error("The requested service is not recognized.")
                    log.error("services: " + str(structureFileSettings.serviceModules.keys()))
                    pdbTransaction.generateCommonParserNotice(noticeBrief='Service not known to entity.')
                    raise AttributeError(requestedService)

                elif requestedService == "Evaluate":
                    try:
                        evaluatePdb(pdbTransaction)
                    except Exception as error:
                        log.error("There was a problem evaluating the pdb: " + str(error))
                        pdbTransaction.generateCommonParserNotice(noticeBrief='Failed to evaluate.')
                        raise AttributeError(requestedService)


                elif requestedService == "PreprocessPdbForAmber":
                    try:
                        preprocessPdbForAmber(pdbTransaction)
                    except Exception as error:
                        log.error("There was a problem evaluating the pdb: " + str(error))
                        pdbTransaction.generateCommonParserNotice(noticeBrief='Failed to preprocess.')
                        raise AttributeError(requestedService)
                else:
                    log.error("The requested service is not recognized.")
                    log.error("services: " + str(structureFileSettings.serviceModules.keys()))
                    pdbTransaction.generateCommonParserNotice(noticeBrief='Service not Known to entity.')
                    raise AttributeError(requestedService)

    except Exception as e:
        log.error("There was a problem identifying the requested service" + str(e))
        log.error(traceback.format_exc())
        pdbTransaction.generateCommonParserNotice(noticeBrief='Failed to provide a service.')
        return

    return pdbTransaction

## This method will throw errors if called from other files.
def __setup(receivedTransaction : commonIO.Transaction):
    log.debug("setting up a pdb preprocessor transaction.")
    ## This transaction pattern is strange. We take a generic transaction and instantiate that in 
    ##  the delegator, then use that here to create a new object that is a typed version
    ##  of the same class? 
    try:
        # ## Ensure that our Transacation is the Sequence variety
        pdbTransaction=amberIO.PdbTransaction(receivedTransaction.incoming_string)
        log.debug("request_dict: ")
        prettyPrint(pdbTransaction.request_dict)
    except Exception as e:
        log.error("There was a problem instantiating the PdbTransaction: " + str(e))
        log.error(traceback.format_exc())
        pdbTransaction.generateCommonParserNotice(noticeBrief='Failed to instantiate PdbTransaction')
        return

    try:    
        pdbTransaction.populate_transaction_in()
        # log.debug("transaction_in:")
        # log.debug(pdbTransaction.transaction_in.json(indent=2))
    except Exception as e:
        log.error("There was a problem populating the the PdbTransaction in: " + str(e))
        log.error(traceback.format_exc())
        pdbTransaction.generateCommonParserNotice(noticeBrief='Failed to populate transaction input')
        return

    try:
        pdbTransaction.initialize_transaction_out_from_transaction_in()
        # log.debug("pdbTransaction.transaction_out: " )
        # log.debug(pdbTransaction.transaction_out.json(indent=2))
    except Exception as error :
        log.error("There was a problem initializing the outgoing transaction : " + str(error))
        log.error(traceback.format_exc())
        raise error
    return pdbTransaction

## TODO: document me
#
def doDefaultService(receivedTransaction : commonIO.Transaction):
    log.info("doDefaultService() was called.")
    try:
        pdbTransaction = __setup(receivedTransaction)
    except Exception as error:
        log.error("There was a problem setting up a pdbTransaction: " + str(error))
        pdbTransaction.generateCommonParserNotice(nodiceBrief="Failed to setup the pdbTransaction.")
        raise RuntimeError("Cannot instantiate a transaction.")
    ##Preprocess PDB will be the default. Given a request to the StructureFile entity,
    ##  with no services or options defined, look for a pdb file and preprocess it for Amber.
    try:
        preprocessPdbForAmber(pdbTransaction)
        receivedTransaction.build_outgoing_string()
    except Exception as error:
        log.error("There was a problem doing the default service in the structureFile module.")
        raise error
    
    

## TODO: document me
#
def main():
    GemsPath = getGemsHome()
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            inputFile = sys.argv[1]
        else:
            log.error("No input file provided.")

    with open(inputFile, 'r') as file:
        jsonObjectString = file.read().replace('\n', '')

    receivedTransaction = commonIO.Transaction(jsonObjectString)

    try:
        parseInput(receivedTransaction)
    except Exception as error:
        log.error("Error parsing input.")
        log.error("Error type: " + str(type(error)))
        log.error(traceback.format_exc())
    receive(receivedTransaction)

    responseObjectString = receivedTransaction.outgoing_string
    return responseObjectString

if __name__ == "__main__":
    main()

